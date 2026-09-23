#!/usr/bin/env python3
"""Retrieval quality benchmark — embed each tool's output, run queries, compare hit rates.

Measures what actually matters for RAG: does the right page surface when you
ask a question?  Uses the same chunking strategy and embedding model for all
tools so the only variable is extraction quality.

Supports four retrieval modes:
  - Embedding-only (cosine similarity)
  - BM25 keyword search
  - Hybrid (embedding + BM25 via Reciprocal Rank Fusion)
  - Reranked (hybrid results reranked by a cross-encoder)

    python benchmark_retrieval.py                        # latest run
    python benchmark_retrieval.py --run run_20260405_221158
    python benchmark_retrieval.py --output my_report.md
    python benchmark_retrieval.py --chunk-sizes 256,512,1024

Requires:
    pip install openai numpy rank_bm25 sentence-transformers
    export OPENAI_API_KEY=sk-...
"""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import json
import logging
import math
import os
import re
import sys
import time
import time as _time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

BENCH_DIR = Path(__file__).parent
REPO_ROOT = BENCH_DIR

# Load .env (OPENAI_API_KEY etc) — same pattern as benchmark_all_tools.py.
# Without this, direct invocation of this script (vs via run_benchmarks.sh)
# fails with "OPENAI_API_KEY environment variable not set".
try:
    from dotenv import load_dotenv  # noqa: E402
    load_dotenv(BENCH_DIR / ".env")
except ImportError:
    pass

from markcrawl.chunker import chunk_markdown  # noqa: E402

from tools.page_level_mrr import collapse_chunks_to_pages  # noqa: E402
from tools.page_level_mrr import hit_at_k as _page_hit_at_k  # noqa: E402
from tools.page_level_mrr import reciprocal_rank as _page_reciprocal_rank  # noqa: E402
from tools.three_metric import format_coverage as _format_coverage  # noqa: E402
from tools.three_metric import load_helpful_urls as _load_helpful_urls  # noqa: E402
from tools.three_metric import three_metrics as _three_metrics  # noqa: E402

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TOOLS = [
    "markcrawl", "crawl4ai", "crawl4ai-raw", "scrapy+md",
    "crawlee", "colly+md", "playwright", "firecrawl",
]

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSIONS = 1536
TOP_K = 50  # Retrieve top-50 candidates for reranking pipeline
REPORT_AT_K = [1, 3, 5, 10, 20]  # Report hit rates at each K value
CHUNK_MAX_WORDS = 400
CHUNK_OVERLAP = 50

# Chunk size sensitivity: test at multiple configurations
# Each entry is (max_words, overlap_words, label)
CHUNK_CONFIGS = [
    (200, 30, "~256tok"),
    (400, 50, "~512tok"),
    (800, 100, "~1024tok"),
]
DEFAULT_CHUNK_CONFIG = (400, 50, "~512tok")  # Used when not running sensitivity

# Cross-encoder reranking model
RERANK_MODEL = os.environ.get("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
RERANK_TOP_N = 20  # Rerank top-N from initial retrieval

# BM25 + Embedding fusion weight (for RRF)
RRF_K = 60  # Reciprocal Rank Fusion constant

# HyDE — Hypothetical Document Embedding
# Generate a hypothetical answer paragraph per query via LLM, embed that
# instead of (or in addition to) the raw query. Cached by (prompt, model,
# query) hash so runs are idempotent and cheap after the first.
HYDE_MODEL_DEFAULT = "gpt-4o-mini"
HYDE_CACHE_DIR = BENCH_DIR / "hyde_cache"
HYDE_PROMPT_TEMPLATE = (
    "Write a short paragraph (2–4 sentences) that would appear on a web page "
    "answering this question. Write it in the style of documentation, a "
    "reference page, or a technical blog post — as if excerpted from the "
    "source material itself. Do not add preamble, reasoning, caveats, or any "
    "meta-commentary. Output only the paragraph.\n\n"
    "Question: {query}\n\n"
    "Paragraph:"
)

# DS-7: Test queries are loaded from JSON at module import time. The v1.4
# LLM-generated, LLM-verified query set (queries/v14_queries.json, produced
# by tools/generate_queries.py per DS-6) takes priority; the archived v1.3
# hand-written set (queries/v13_queries.json) is the fallback so the
# benchmark still runs while v1.4 generation is in progress (Gates 3a/3b).
#
# Each query dict has: query text, url_match (substring identifying the
# correct source page), page_match (alternate match), category, description.
# Categories: api-function, code-example, conceptual, structured-data,
# factual-lookup, cross-page, navigation, js-rendered.
TEST_QUERY_SOURCES = [
    # v1.5: generated from the judged helpful-pages universe (unanchored).
    # Falls through to the older anchored corpora when it is absent, so a
    # partially-migrated checkout still runs.
    BENCH_DIR / "queries" / "v15_queries.json",
    BENCH_DIR / "queries" / "v14_queries.json",
    BENCH_DIR / "queries" / "v13_queries.json",
]


def _load_test_queries() -> Dict[str, List[Dict]]:
    """Load the canonical test query set, preferring v1.4 over v1.3."""
    for path in TEST_QUERY_SOURCES:
        if path.is_file():
            with open(path) as f:
                queries = json.load(f)
            logger.info(
                "Loaded %d queries across %d sites from %s",
                sum(len(v) for v in queries.values()),
                len(queries),
                path.name,
            )
            return queries
    raise FileNotFoundError(
        "No test query JSON found. Expected one of: "
        + ", ".join(str(p) for p in TEST_QUERY_SOURCES)
    )


TEST_QUERIES: Dict[str, List[Dict]] = _load_test_queries()


# Old inline TEST_QUERIES dict was extracted to queries/v13_queries.json by
# the DS-7 commit; see git log for the prior inline definition.

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class EmbeddedChunk:
    text: str
    url: str
    tool: str
    site: str
    chunk_index: int
    vector: List[float] = field(default_factory=list, repr=False)


@dataclass
class QueryResult:
    query: str
    description: str
    expected_url_match: str
    expected_page_match: str
    top_k_urls: List[str]
    top_k_scores: List[float]
    hit: bool
    hit_rank: Optional[int]  # 1-indexed rank where the hit was found, or None
    category: str = ""  # query category (api-function, code-example, etc.)


@dataclass
class RetrievalModeResult:
    """Results for a single retrieval mode (embedding, bm25, hybrid, reranked)."""
    mode: str  # "embedding", "bm25", "hybrid", "reranked"
    query_results: List[QueryResult]
    hits_at_k: Dict[int, int] = field(default_factory=dict)
    mrr: float = 0.0  # Mean Reciprocal Rank (chunk-level)
    # DS-1: page-level metrics — collapse chunks-per-URL using DS-2 normalized
    # URLs before computing MRR/Hit@K. Removes the chunk-density gaming signal
    # (a tool emitting 5 chunks per page no longer beats one emitting 1 chunk
    # when both rank the same canonical page first).
    page_mrr: float = 0.0
    page_hits_at_k: Dict[int, int] = field(default_factory=dict)


@dataclass
class ToolSiteRetrievalResult:
    tool: str
    site: str
    total_queries: int
    hits: int
    hit_rate: float
    total_chunks: int
    total_pages: int
    avg_chunk_words: float
    query_results: List[QueryResult]  # Primary mode results (embedding)
    embed_time: float
    search_time: float
    hits_at_k: Dict[int, int] = field(default_factory=dict)  # {k: hit_count}
    mrr: float = 0.0  # Mean Reciprocal Rank (chunk-level, embedding mode)
    mode_results: Dict[str, RetrievalModeResult] = field(default_factory=dict)
    chunk_config_label: str = ""  # e.g. "~512tok"
    page_mrr: float = 0.0  # DS-1: page-level MRR for embedding mode
    # DS-4 (spec SC-6): decomposition against the helpful-pages universe.
    # coverage_pct / retrieval_on_covered_mrr are None when not measurable
    # (no universe file for the site, or nothing covered) — None must not be
    # rendered as 0.0, which would read as a ranking failure.
    coverage_covered: int = 0
    coverage_total: int = 0
    coverage_pct: Optional[float] = None
    retrieval_on_covered_mrr: Optional[float] = None
    retrieval_on_covered_n: int = 0
    end_to_end_mrr: float = 0.0


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------

def _get_openai_client():
    try:
        from openai import OpenAI
    except ImportError:
        logger.error("openai package required. Install with: pip install openai")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    return OpenAI(api_key=api_key)


MAX_EMBED_TOKENS = 8100  # OpenAI limit is 8192; leave margin
EMBED_TIMEOUT = 30  # seconds per API call
EMBED_RETRIES = 3  # retry on timeout/network error (not retried for 400 errors)
EMBED_CACHE_DIR = BENCH_DIR / "embed_cache"

# Lazy-loaded tiktoken encoder
_tokenizer = None


def _get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        import tiktoken
        _tokenizer = tiktoken.encoding_for_model("text-embedding-3-small")
    return _tokenizer


def _truncate_to_tokens(text: str, max_tokens: int = MAX_EMBED_TOKENS) -> str:
    """Truncate text to stay under token limit using tiktoken for accuracy."""
    enc = _get_tokenizer()
    # disallowed_special=() prevents ValueError when the input contains literal
    # special-token strings like '<|endoftext|>' (which appear as content in model
    # documentation, e.g. crawled HF transformers pages). Encode them as normal
    # text — we are not generating, we are measuring length.
    tokens = enc.encode(text, disallowed_special=())
    if len(tokens) <= max_tokens:
        return text
    return enc.decode(tokens[:max_tokens])


def _embed_cache_key(texts: List[str], model: str) -> str:
    """Compute a stable hash for a batch of texts + model."""
    import hashlib
    h = hashlib.sha256()
    h.update(model.encode())
    for t in texts:
        h.update(t.encode())
    return h.hexdigest()


def _load_embed_cache(cache_key: str) -> Optional[List[List[float]]]:
    """Load cached embeddings if they exist."""
    cache_file = EMBED_CACHE_DIR / f"{cache_key}.json"
    if cache_file.is_file():
        with open(cache_file, "r") as f:
            return json.load(f)
    return None


EMBED_CACHE_MAX_GB = float(os.environ.get("EMBED_CACHE_MAX_GB", "20"))


def _evict_embed_cache() -> None:
    """Remove oldest cache files until total size is under EMBED_CACHE_MAX_GB."""
    if not EMBED_CACHE_DIR.is_dir():
        return
    max_bytes = EMBED_CACHE_MAX_GB * 1024 ** 3
    files = sorted(EMBED_CACHE_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)
    total = sum(f.stat().st_size for f in files)
    while total > max_bytes and files:
        oldest = files.pop(0)
        total -= oldest.stat().st_size
        oldest.unlink(missing_ok=True)


def _save_embed_cache(cache_key: str, vectors: List[List[float]]) -> None:
    """Save embeddings to disk cache with LRU eviction at EMBED_CACHE_MAX_GB."""
    EMBED_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = EMBED_CACHE_DIR / f"{cache_key}.json"
    with open(cache_file, "w") as f:
        json.dump(vectors, f)
    _evict_embed_cache()


def hyde_transform_queries(
    client,
    queries: List[str],
    model: str = HYDE_MODEL_DEFAULT,
    cache_dir: Path = HYDE_CACHE_DIR,
) -> List[str]:
    """Transform each query into a hypothetical answer paragraph via LLM.

    Caches per-(prompt, model, query) hash to disk, so the first run pays
    the LLM cost and subsequent runs are free. Uses the same OpenAI client
    object as embed_texts — assumes the caller has already configured it.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    out: List[str] = []
    new_calls = 0
    for q in queries:
        h = hashlib.sha256(f"{HYDE_PROMPT_TEMPLATE}|{model}|{q}".encode("utf-8")).hexdigest()[:20]
        cache_file = cache_dir / f"{h}.txt"
        if cache_file.exists():
            out.append(cache_file.read_text(encoding="utf-8"))
            continue
        # Miss: generate via LLM
        prompt = HYDE_PROMPT_TEMPLATE.format(query=q)
        for attempt in range(4):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                    temperature=0.0,  # deterministic for caching
                    timeout=30,
                )
                text = resp.choices[0].message.content.strip()
                cache_file.write_text(text, encoding="utf-8")
                out.append(text)
                new_calls += 1
                break
            except Exception as exc:
                if attempt == 3:
                    logger.warning("HyDE LLM call failed after 4 attempts for %r: %s — using raw query", q[:60], exc)
                    out.append(q)  # fall back to raw query
                    break
                _time.sleep(1.5 ** attempt)
    if new_calls:
        logger.info(f"    HyDE: {new_calls} new LLM calls, {len(queries)-new_calls} cache hits")
    else:
        logger.info(f"    HyDE: {len(queries)} cache hits (no LLM calls)")
    return out


# Lazy-loaded sentence-transformers models (keyed by model name)
_st_model_cache: Dict[str, object] = {}


def _embed_sentence_transformer(texts: List[str], model_name: str) -> List[List[float]]:
    """Embed via HuggingFace sentence-transformers. Used for any model name
    containing ``/`` (e.g. ``BAAI/bge-large-en-v1.5``).

    Model is loaded once per process and cached. Uses MPS on Apple Silicon
    when available; falls back to CPU otherwise.
    """
    global _st_model_cache
    if model_name not in _st_model_cache:
        import torch
        from sentence_transformers import SentenceTransformer
        device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"    Loading sentence-transformer {model_name!r} on {device}...")
        _st_model_cache[model_name] = SentenceTransformer(model_name, device=device)
    st_model = _st_model_cache[model_name]
    # SentenceTransformer.encode handles batching internally. Keep batch size modest for MPS memory.
    # Normalize embeddings so cosine similarity == dot product (matches OpenAI convention).
    vectors = st_model.encode(
        texts, batch_size=32, show_progress_bar=False, normalize_embeddings=True,
        convert_to_numpy=True,
    )
    return vectors.tolist()


def embed_texts(client, texts: List[str], model: str = EMBEDDING_MODEL) -> List[List[float]]:
    """Embed a batch of texts, dispatching by model name.

    Dispatch rule: model names containing ``/`` are treated as HuggingFace
    sentence-transformer identifiers (e.g. ``BAAI/bge-large-en-v1.5``);
    everything else is treated as an OpenAI embedding model.

    Features:
    - Disk cache keyed by (model, texts) — embeddings are cached by content
      hash, so re-runs are instant, and different models get different cache
      keys automatically.
    - Retry with timeout: survives wifi drops (retries 3x with 30s timeout)
    - Batching: sends 100 texts per API call for OpenAI; uses ST's internal
      batching for HuggingFace models.
    """
    # Check full-batch cache first (same mechanism for OpenAI and ST — model
    # is part of the cache key).
    cache_key = _embed_cache_key(texts, model)
    cached = _load_embed_cache(cache_key)
    if cached is not None:
        return cached

    # Dispatch to sentence-transformers for HF model identifiers.
    if "/" in model:
        vectors = _embed_sentence_transformer(texts, model)
        _save_embed_cache(cache_key, vectors)
        return vectors

    max_tokens_per_request = 250_000  # OpenAI limit is 300K; leave margin

    # Build batches respecting both text count and token budget
    tokenizer = _get_tokenizer()
    processed = [_truncate_to_tokens(t) if t.strip() else " " for t in texts]
    batches = []
    current_batch = []
    current_start = 0
    current_tokens = 0
    for i, text in enumerate(processed):
        text_tokens = len(tokenizer.encode(text, disallowed_special=()))
        if current_batch and (current_tokens + text_tokens > max_tokens_per_request or len(current_batch) >= 100):
            batches.append((current_start, current_batch))
            current_batch = []
            current_start = i
            current_tokens = 0
        current_batch.append(text)
        current_tokens += text_tokens
    if current_batch:
        batches.append((current_start, current_batch))

    max_retries = 6  # More retries to handle rate limits gracefully

    def _embed_batch(args):
        idx, batch = args
        for attempt in range(max_retries):
            try:
                response = client.embeddings.create(
                    input=batch, model=model, timeout=EMBED_TIMEOUT,
                )
                return idx, [d.embedding for d in response.data]
            except Exception as exc:
                exc_str = str(exc)
                is_client_error = "400" in exc_str or "BadRequest" in type(exc).__name__
                if is_client_error:
                    raise
                # Rate limits (429): wait longer, always retry
                is_rate_limit = "429" in exc_str or "RateLimit" in type(exc).__name__
                if is_rate_limit:
                    wait = min(2 ** attempt * 2, 60)
                    logger.warning(f"    Rate limited (attempt {attempt+1}/{max_retries}), waiting {wait}s...")
                    time.sleep(wait)
                elif attempt < max_retries - 1:
                    wait = 2 ** attempt * 2
                    logger.warning(f"    Embed API error (attempt {attempt+1}/{max_retries}): {exc}")
                    logger.warning(f"    Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise

    # Run batches with configurable parallelism (default: sequential)
    embed_workers = int(os.environ.get("EMBED_PARALLEL_BATCHES", "1"))
    results = {}
    if embed_workers > 1 and len(batches) > 1:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        with ThreadPoolExecutor(max_workers=min(embed_workers, len(batches))) as pool:
            futures = {pool.submit(_embed_batch, b): b for b in batches}
            for future in as_completed(futures):
                idx, vectors = future.result()
                results[idx] = vectors
    else:
        for batch_args in batches:
            idx, vectors = _embed_batch(batch_args)
            results[idx] = vectors

    # Reassemble in order
    all_vectors = []
    for idx, _ in batches:
        all_vectors.extend(results[idx])

    # Cache the result
    _save_embed_cache(cache_key, all_vectors)
    return all_vectors


# ---------------------------------------------------------------------------
# Cosine similarity (numpy-free fallback included)
# ---------------------------------------------------------------------------

def _cosine_similarity_np(a, b_matrix):
    """Compute cosine similarity between vector a and each row of b_matrix."""
    import numpy as np
    a = np.array(a)
    b = np.array(b_matrix)
    dot = b @ a
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b, axis=1)
    return dot / (norm_a * norm_b + 1e-10)


def _cosine_similarity_pure(a, b_matrix):
    """Pure-Python fallback for cosine similarity."""
    import math

    def _dot(x, y):
        return sum(xi * yi for xi, yi in zip(x, y))

    def _norm(x):
        return math.sqrt(sum(xi * xi for xi in x))

    norm_a = _norm(a)
    results = []
    for b in b_matrix:
        d = _dot(a, b)
        nb = _norm(b)
        results.append(d / (norm_a * nb + 1e-10))
    return results


try:
    import numpy  # noqa: F401
    cosine_similarity = _cosine_similarity_np
except ImportError:
    cosine_similarity = _cosine_similarity_pure


# ---------------------------------------------------------------------------
# BM25 search
# ---------------------------------------------------------------------------

def _build_bm25_index(chunk_texts: List[str]):
    """Build a BM25 index over tokenized chunk texts."""
    from rank_bm25 import BM25Okapi
    tokenized = [text.lower().split() for text in chunk_texts]
    return BM25Okapi(tokenized)


def _bm25_search(bm25_index, query: str, top_k: int) -> List[Tuple[int, float]]:
    """Return (index, score) pairs for top-k BM25 results."""
    tokenized_query = query.lower().split()
    scores = bm25_index.get_scores(tokenized_query)
    indexed = list(enumerate(scores))
    indexed.sort(key=lambda x: x[1], reverse=True)
    return indexed[:top_k]


# ---------------------------------------------------------------------------
# Reciprocal Rank Fusion (RRF)
# ---------------------------------------------------------------------------

def _reciprocal_rank_fusion(
    ranked_lists: List[List[Tuple[int, float]]],
    k: int = RRF_K,
    top_n: int = TOP_K,
) -> List[Tuple[int, float]]:
    """Merge multiple ranked lists using RRF. Each list is [(index, score), ...]."""
    rrf_scores: Dict[int, float] = {}
    for ranked in ranked_lists:
        for rank, (idx, _score) in enumerate(ranked, 1):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + 1.0 / (k + rank)
    # Sort by RRF score descending
    merged = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    return merged[:top_n]


# ---------------------------------------------------------------------------
# Maximal Marginal Relevance (MMR) diversification
# ---------------------------------------------------------------------------

def _mmr_rerank(
    candidates: List[Tuple[int, float]],
    vec_matrix,
    top_k: int,
    lambda_: float = 0.7,
) -> List[Tuple[int, float]]:
    """Greedy MMR re-rank. Picks diverse-yet-relevant top_k from candidates.

    score(c) = lambda_ * relevance(c) - (1-lambda_) * max_sim(c, selected)
    - lambda_ = 1.0: pure relevance (MMR disabled)
    - lambda_ = 0.0: pure diversity
    """
    if not candidates or lambda_ >= 0.999:
        return candidates[:top_k]

    # Normalize candidate relevance to [0, 1] by min-max so scale matches diversity
    scores_only = [s for _, s in candidates]
    s_min, s_max = min(scores_only), max(scores_only)
    denom = (s_max - s_min) or 1e-10
    rel_by_idx = {idx: (s - s_min) / denom for idx, s in candidates}

    remaining = [idx for idx, _ in candidates]
    selected: List[int] = []
    selected_scores: List[float] = []

    # Pre-extract candidate vectors for diversity computation
    cand_vecs = {idx: vec_matrix[idx] for idx in remaining}

    # Seed: highest-relevance candidate
    first = max(remaining, key=lambda i: rel_by_idx[i])
    selected.append(first)
    selected_scores.append(rel_by_idx[first])
    remaining.remove(first)

    while remaining and len(selected) < top_k:
        # For each remaining, find max similarity to any already-selected
        sel_matrix = [cand_vecs[s] for s in selected]
        best_idx = None
        best_mmr = -float("inf")
        for idx in remaining:
            sims = cosine_similarity(cand_vecs[idx], sel_matrix)
            max_sim = float(max(sims)) if len(sel_matrix) > 0 else 0.0
            mmr_score = lambda_ * rel_by_idx[idx] - (1.0 - lambda_) * max_sim
            if mmr_score > best_mmr:
                best_mmr = mmr_score
                best_idx = idx
        selected.append(best_idx)
        selected_scores.append(best_mmr)
        remaining.remove(best_idx)

    return list(zip(selected, selected_scores))


# ---------------------------------------------------------------------------
# Cross-encoder reranking
# ---------------------------------------------------------------------------

_reranker = None


def _get_reranker():
    """Lazy-load the cross-encoder reranking model."""
    global _reranker
    if _reranker is None:
        from sentence_transformers import CrossEncoder
        logger.info(f"  Loading reranker: {RERANK_MODEL}...")
        _reranker = CrossEncoder(RERANK_MODEL)
        logger.info("  Reranker loaded.")
    return _reranker


def _rerank(query: str, chunks: List[EmbeddedChunk], candidate_indices: List[int], top_n: int = RERANK_TOP_N) -> List[Tuple[int, float]]:
    """Rerank candidate chunks using cross-encoder. Returns [(chunk_index, score), ...]."""
    reranker = _get_reranker()
    pairs = [(query, chunks[i].text) for i in candidate_indices]
    scores = reranker.predict(pairs)
    scored = list(zip(candidate_indices, [float(s) for s in scores]))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]


# ---------------------------------------------------------------------------
# Hit checking and MRR
# ---------------------------------------------------------------------------

# DS-2: locale subdomain prefixes stripped before url_match evaluation.
# Explicit allowlist so legitimate-but-similar subdomains (docs.stripe.com,
# support.X.com) are not collapsed. ISO-639-1 + common BCP-47 region forms
# observed in the v1.3 site pool.
_LOCALE_SUBDOMAIN_PREFIXES = frozenset([
    "af", "ar", "az", "be", "bg", "bn", "bs", "ca", "cs", "da", "de", "el",
    "en", "eo", "es", "et", "eu", "fa", "fi", "fr", "ga", "gl", "he", "hi",
    "hr", "hu", "hy", "id", "is", "it", "ja", "ka", "kk", "km", "kn", "ko",
    "ky", "la", "lt", "lv", "mk", "ml", "mn", "mr", "ms", "mt", "my", "nb",
    "ne", "nl", "nn", "no", "pa", "pl", "ps", "pt", "ro", "ru", "sa", "si",
    "sk", "sl", "sq", "sr", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk",
    "ur", "uz", "vi", "zh",
    "zh-cn", "zh-tw", "zh-hk", "zh-hans", "zh-hant",
    "en-us", "en-gb", "en-ca", "en-au",
    "pt-br", "pt-pt",
    "es-mx", "es-ar", "es-es", "es-419",
    "fr-ca", "fr-fr",
    "de-de", "de-at", "de-ch",
])

# Query keys dropped before url_match evaluation. utm_* matched by prefix.
_STRIP_QUERY_KEYS = frozenset(["lang", "language", "locale", "random", "ref", "source"])
_STRIP_QUERY_KEY_PREFIXES = ("utm_",)


def _normalize_url_for_matching(url: str) -> str:
    """Normalize a URL before evaluating it against an expected_url_match
    substring (DS-2). Strips locale subdomain prefixes, drops UTM/lang/
    locale/random query params, drops the fragment, lowercases scheme +
    host + path.

    Eliminates the v1.3 false positive where `he.react.dev/learn/managing-state`
    matched url_match='state' for English queries. Malformed URLs fall
    back to the lowercased raw input — never drop a chunk on parse failure."""
    if not isinstance(url, str):
        return ""
    try:
        scheme, netloc, path, query, _frag = urlsplit(url.strip())
    except (ValueError, TypeError):
        return url.lower()

    netloc = netloc.lower()
    if "." in netloc:
        first, _, rest = netloc.partition(".")
        if first in _LOCALE_SUBDOMAIN_PREFIXES and rest:
            netloc = rest

    if query:
        kept = []
        for pair in query.split("&"):
            key = pair.partition("=")[0].lower()
            if key in _STRIP_QUERY_KEYS:
                continue
            if any(key.startswith(prefix) for prefix in _STRIP_QUERY_KEY_PREFIXES):
                continue
            kept.append(pair)
        query = "&".join(kept)

    return urlunsplit((scheme.lower(), netloc, path.lower(), query, ""))


def _check_hit(url_match: str, page_match: str, ranked_urls: List[str]) -> Tuple[bool, Optional[int]]:
    """Check if any URL in ranked list matches. Returns (hit, 1-indexed rank).

    URLs run through _normalize_url_for_matching before substring comparison
    so locale-prefixed and UTM-tagged variants of the same canonical URL no
    longer create false positives (DS-2)."""
    for rank, url in enumerate(ranked_urls, 1):
        normalized = _normalize_url_for_matching(url)
        if url_match and url_match.lower() in normalized:
            return True, rank
        if page_match and page_match.lower() in normalized:
            return True, rank
    return False, None


def _write_query_audit_csv(
    all_results: Dict[str, Dict[str, "ToolSiteRetrievalResult"]],
    output_path: Path,
    top_k: int = 5,
) -> int:
    """Write the per-(query × tool × rank) audit artifact (DS-3).

    One row per (query, tool, rank in [1..top_k]) with columns:
      query_id, query_text, site, tool, rank, url, cosine_score,
      is_hit, url_match_pattern, normalized_url

    Reviewers questioning a specific number can spot-check the CSV
    without re-running anything. Returns the row count written.

    Atomic write via .tmp + replace; idempotent across re-runs."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_suffix(".csv.tmp")
    rows_written = 0
    with open(tmp_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "query_id", "query_text", "site", "tool", "rank",
            "url", "cosine_score", "is_hit",
            "url_match_pattern", "normalized_url",
            "page_rank_after_collapse",
        ])
        for site, tool_map in all_results.items():
            for tool, r in tool_map.items():
                for q_idx, qr in enumerate(r.query_results):
                    pattern = qr.expected_url_match or ""
                    page_pattern = qr.expected_page_match or ""

                    # Pre-compute the page-rank assignment for each chunk:
                    # iterate top_k in order, assigning each unique normalized
                    # URL a 1-indexed page rank. Multiple chunks sharing the
                    # same normalized canonical (locale mirrors, fragment
                    # variants) share the same page_rank. Lets reviewers see
                    # the chunk → page collapse explicitly in the audit.
                    canonical_to_page_rank: Dict[str, int] = {}
                    for u in qr.top_k_urls:
                        canon = _normalize_url_for_matching(u)
                        if canon not in canonical_to_page_rank:
                            canonical_to_page_rank[canon] = len(canonical_to_page_rank) + 1

                    for rank in range(1, top_k + 1):
                        if rank > len(qr.top_k_urls):
                            break
                        url = qr.top_k_urls[rank - 1]
                        score = qr.top_k_scores[rank - 1] if rank - 1 < len(qr.top_k_scores) else ""
                        normalized = _normalize_url_for_matching(url)
                        is_hit = bool(
                            (pattern and pattern.lower() in normalized)
                            or (page_pattern and page_pattern.lower() in normalized)
                        )
                        page_rank = canonical_to_page_rank.get(normalized, "")
                        writer.writerow([
                            f"{site}:{q_idx}",
                            qr.query,
                            site,
                            tool,
                            rank,
                            url,
                            score,
                            "true" if is_hit else "false",
                            pattern,
                            normalized,
                            page_rank,
                        ])
                        rows_written += 1
    tmp_path.replace(output_path)
    return rows_written


def _compute_mrr(query_results: List[QueryResult]) -> float:
    """Compute Mean Reciprocal Rank from query results."""
    if not query_results:
        return 0.0
    rr_sum = 0.0
    for qr in query_results:
        if qr.hit_rank is not None:
            rr_sum += 1.0 / qr.hit_rank
    return rr_sum / len(query_results)


def _compute_hits_at_k(query_results: List[QueryResult]) -> Dict[int, int]:
    """Compute hit counts at each K threshold."""
    return {
        k: sum(1 for r in query_results if r.hit_rank is not None and r.hit_rank <= k)
        for k in REPORT_AT_K
    }


def _page_rr_per_query(query_results: List[QueryResult]) -> List[dict]:
    """Per-query page-level reciprocal rank, for the DS-4 decomposition.

    Mirrors _compute_page_level_mrr_and_hits exactly (same collapse, same
    matcher) but keeps the per-query value instead of averaging, so
    coverage-split metrics and the headline MRR can never disagree.
    """
    out: List[dict] = []
    for qr in query_results:
        url_match = (qr.expected_url_match or "").lower()
        page_match = (qr.expected_page_match or "").lower()

        def _matches(url: str, _um=url_match, _pm=page_match) -> bool:
            normalized = _normalize_url_for_matching(url)
            return bool((_um and _um in normalized) or (_pm and _pm in normalized))

        pages = collapse_chunks_to_pages(qr.top_k_urls, key_fn=_normalize_url_for_matching)
        out.append({
            "url_match": url_match,
            "page_match": page_match,
            "rr": _page_reciprocal_rank(pages, _matches),
        })
    return out


def _compute_page_level_mrr_and_hits(
    query_results: List[QueryResult],
) -> Tuple[float, Dict[int, int]]:
    """Page-level MRR and Hit@K (DS-1 + DS-2).

    Collapses chunks-per-URL to pages using DS-2 normalized URLs (so
    locale mirrors and fragment variants of the same canonical page
    collapse to a single rank slot), then computes MRR and Hit@K on
    the deduped page list. Removes the chunk-density gaming signal
    that affects chunk-level MRR.

    Bug-fix 2026-05-11: the previous version dedup'd by RAW URL, which
    meant `react.dev/X#a` and `react.dev/X#b` were treated as two
    distinct page entries — silently suppressing the page-level uplift
    for tools that emit multiple fragment-variant chunks per canonical
    page. Now passes `_normalize_url_for_matching` as the dedup key so
    those collapse to one entry per canonical page.
    """
    if not query_results:
        return 0.0, {k: 0 for k in REPORT_AT_K}

    rr_sum = 0.0
    hits_per_k = {k: 0 for k in REPORT_AT_K}

    for qr in query_results:
        url_match = (qr.expected_url_match or "").lower()
        page_match = (qr.expected_page_match or "").lower()

        def _matches(url: str, _um=url_match, _pm=page_match) -> bool:
            normalized = _normalize_url_for_matching(url)
            return bool(
                (_um and _um in normalized)
                or (_pm and _pm in normalized)
            )

        pages = collapse_chunks_to_pages(
            qr.top_k_urls, key_fn=_normalize_url_for_matching
        )
        rr_sum += _page_reciprocal_rank(pages, _matches)
        for k in REPORT_AT_K:
            if _page_hit_at_k(pages, k, _matches):
                hits_per_k[k] += 1

    return rr_sum / len(query_results), hits_per_k


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def load_pages(jsonl_path: str) -> List[Dict]:
    """Load pages from a JSONL file."""
    pages = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    pages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return pages


def _url_to_breadcrumb(url: str) -> str:
    """Convert a URL path to a readable breadcrumb. e.g. '/docs/tutorial/body/' -> 'docs > tutorial > body'"""
    import urllib.parse as up
    path = up.urlsplit(url).path.strip("/")
    if not path:
        return ""
    segments = [seg for seg in path.split("/") if seg]
    # Clean up common URL patterns
    segments = [seg.replace("-", " ").replace("_", " ") for seg in segments]
    return " > ".join(segments)


def _extract_heading(chunk_text: str) -> str:
    """Extract the first markdown heading from a chunk, if any."""
    for line in chunk_text.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            # Remove # prefix and any trailing anchors like [¶](#foo)
            heading = re.sub(r"^#{1,6}\s+", "", line)
            heading = re.sub(r"\[¶\].*$", "", heading).strip()
            return heading
    return ""


def _prepend_context(chunk_text: str, title: str, url: str, heading: str) -> str:
    """Prepend contextual metadata to a chunk for better embedding.

    Research shows this improves retrieval by 21-35% (NDCG) by helping
    the embedding model disambiguate chunks from different pages/sections.
    Metadata should be ~10% of chunk text.
    """
    parts = []
    if title:
        parts.append(f"Page: {title}")
    breadcrumb = _url_to_breadcrumb(url)
    if breadcrumb:
        parts.append(f"Path: {breadcrumb}")
    if heading and heading != title:
        parts.append(f"Section: {heading}")

    if not parts:
        return chunk_text

    context_line = " | ".join(parts)
    return f"{context_line}\n\n{chunk_text}"


def chunk_pages(
    pages: List[Dict],
    tool: str,
    site: str,
    max_words: int = CHUNK_MAX_WORDS,
    overlap_words: int = CHUNK_OVERLAP,
    add_context_headers: bool = False,
) -> List[EmbeddedChunk]:
    """Chunk all pages using markdown-aware chunking.

    If add_context_headers is True, prepend page title, URL breadcrumb, and
    section heading to each chunk before embedding.
    """
    chunks = []
    for page in pages:
        text = page.get("text", "")
        url = page.get("url", "")
        title = page.get("title", "")
        if not text.strip():
            continue
        page_chunks = chunk_markdown(text, max_words=max_words, overlap_words=overlap_words)
        for c in page_chunks:
            chunk_text = c.text
            if add_context_headers:
                heading = _extract_heading(chunk_text)
                chunk_text = _prepend_context(chunk_text, title, url, heading)
            chunks.append(EmbeddedChunk(
                text=chunk_text,
                url=url,
                tool=tool,
                site=site,
                chunk_index=c.index,
            ))
    return chunks


def _embedding_mode_top_indices(
    query_vec,
    chunks,
    vec_matrix,
    page_vec_by_url,
    dual_index: bool,
    page_weight: float,
) -> Tuple[List[int], List[float]]:
    """Return (top_indices, top_scores) for embedding mode (optionally dual-index).

    Extracted so the ensemble path can call it twice (primary + secondary) and
    fuse without duplicating the dual-index combination logic.
    """
    scores = cosine_similarity(query_vec, vec_matrix)
    if dual_index and page_vec_by_url:
        unique_urls = list(page_vec_by_url.keys())
        page_vecs = [page_vec_by_url[u] for u in unique_urls]
        page_scores_raw = cosine_similarity(query_vec, page_vecs)
        page_score_by_url = {u: float(page_scores_raw[i]) for i, u in enumerate(unique_urls)}
        combined = [
            page_weight * page_score_by_url.get(chunks[i].url, 0.0)
            + (1.0 - page_weight) * float(scores[i])
            for i in range(len(chunks))
        ]
        indexed = sorted(enumerate(combined), key=lambda x: x[1], reverse=True)
        top_indices = [i for i, _ in indexed[:TOP_K]]
        top_scores = [combined[i] for i in top_indices]
    else:
        if hasattr(scores, 'argsort'):
            import numpy as np
            top_indices = list(np.argsort(scores)[-TOP_K:][::-1])
        else:
            indexed = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
            top_indices = [i for i, _ in indexed[:TOP_K]]
        top_scores = [float(scores[i]) for i in top_indices]
    return top_indices, top_scores


def _run_single_mode(
    mode: str,
    query_text: str,
    query_vec: List[float],
    chunks: List[EmbeddedChunk],
    vec_matrix,
    bm25_index,
    url_match: str,
    page_match: str,
    page_vec_by_url: Optional[Dict[str, List[float]]] = None,
    dual_index: bool = False,
    page_weight: float = 0.3,
    mmr_lambda: float = 1.0,
    vec_matrix_ensemble: Optional[List[List[float]]] = None,
    query_vec_ensemble: Optional[List[float]] = None,
    page_vec_by_url_ensemble: Optional[Dict[str, List[float]]] = None,
) -> Tuple[List[str], List[float], bool, Optional[int]]:
    """Run a single retrieval mode and return (urls, scores, hit, hit_rank).

    If mmr_lambda < 1.0, apply MMR re-rank on the (embedding-mode) candidate set
    over chunk vectors for diversity.

    When vec_matrix_ensemble + query_vec_ensemble are provided, embedding-mode
    retrieval becomes RRF fusion of (primary ranking, secondary ranking). The
    secondary ranking uses the same dual-index configuration as the primary
    (primary page vectors with primary embedder, secondary page vectors with
    secondary embedder).
    """
    has_ensemble = vec_matrix_ensemble is not None and query_vec_ensemble is not None

    if mode == "embedding":
        top_indices, top_scores = _embedding_mode_top_indices(
            query_vec, chunks, vec_matrix, page_vec_by_url, dual_index, page_weight,
        )
        if has_ensemble:
            ens_indices, ens_scores = _embedding_mode_top_indices(
                query_vec_ensemble, chunks, vec_matrix_ensemble,
                page_vec_by_url_ensemble, dual_index, page_weight,
            )
            primary_ranked = [(i, s) for i, s in zip(top_indices, top_scores)]
            secondary_ranked = [(i, s) for i, s in zip(ens_indices, ens_scores)]
            fused = _reciprocal_rank_fusion([primary_ranked, secondary_ranked], top_n=TOP_K)
            top_indices = [i for i, _ in fused]
            top_scores = [s for _, s in fused]

        top_urls = [chunks[i].url for i in top_indices]

        if mmr_lambda < 0.999:
            candidates = list(zip(top_indices, top_scores))
            mmr_out = _mmr_rerank(candidates, vec_matrix, top_k=TOP_K, lambda_=mmr_lambda)
            top_indices = [i for i, _ in mmr_out]
            top_urls = [chunks[i].url for i in top_indices]
            top_scores = [s for _, s in mmr_out]

    elif mode == "bm25":
        bm25_results = _bm25_search(bm25_index, query_text, TOP_K)
        top_indices = [i for i, _ in bm25_results]
        top_urls = [chunks[i].url for i in top_indices]
        top_scores = [s for _, s in bm25_results]

    elif mode == "hybrid":
        # Embedding results
        emb_scores = cosine_similarity(query_vec, vec_matrix)
        if hasattr(emb_scores, 'argsort'):
            import numpy as np
            emb_top = list(np.argsort(emb_scores)[-TOP_K:][::-1])
        else:
            emb_indexed = sorted(enumerate(emb_scores), key=lambda x: x[1], reverse=True)
            emb_top = [i for i, _ in emb_indexed[:TOP_K]]
        emb_ranked = [(i, float(emb_scores[i])) for i in emb_top]

        # BM25 results
        bm25_ranked = _bm25_search(bm25_index, query_text, TOP_K)

        # Fuse with RRF
        fused = _reciprocal_rank_fusion([emb_ranked, bm25_ranked], top_n=TOP_K)
        top_indices = [i for i, _ in fused]
        top_urls = [chunks[i].url for i in top_indices]
        top_scores = [s for _, s in fused]

    elif mode == "reranked":
        # Get hybrid candidates first
        emb_scores = cosine_similarity(query_vec, vec_matrix)
        if hasattr(emb_scores, 'argsort'):
            import numpy as np
            emb_top = list(np.argsort(emb_scores)[-TOP_K:][::-1])
        else:
            emb_indexed = sorted(enumerate(emb_scores), key=lambda x: x[1], reverse=True)
            emb_top = [i for i, _ in emb_indexed[:TOP_K]]
        emb_ranked = [(i, float(emb_scores[i])) for i in emb_top]

        bm25_ranked = _bm25_search(bm25_index, query_text, TOP_K)
        fused = _reciprocal_rank_fusion([emb_ranked, bm25_ranked], top_n=TOP_K)
        candidate_indices = [i for i, _ in fused]

        # Rerank candidates with cross-encoder
        reranked = _rerank(query_text, chunks, candidate_indices, top_n=RERANK_TOP_N)
        top_indices = [i for i, _ in reranked]
        top_urls = [chunks[i].url for i in top_indices]
        top_scores = [s for _, s in reranked]
    else:
        raise ValueError(f"Unknown mode: {mode}")

    hit, hit_rank = _check_hit(url_match, page_match, top_urls)
    return top_urls, top_scores, hit, hit_rank


RETRIEVAL_MODES = ["embedding", "bm25", "hybrid", "reranked"]


def run_retrieval_test(
    client,
    chunks: List[EmbeddedChunk],
    queries: List[Dict],
    tool: str,
    site: str,
    chunk_config_label: str = "",
    query_vectors: Optional[List[List[float]]] = None,
    pages: Optional[List[Dict]] = None,
    dual_index: bool = False,
    page_weight: float = 0.3,
    mmr_lambda: float = 1.0,
    page_text_words: int = CHUNK_MAX_WORDS,
    query_prefix: str = "",
    ensemble_embedder: Optional[str] = None,
    ensemble_query_vectors: Optional[List[List[float]]] = None,
) -> ToolSiteRetrievalResult:
    """Embed chunks, run queries across all retrieval modes, compute hit rates + MRR.

    If query_vectors is provided, skip embedding queries (reuse from prior tool).
    If dual_index is True, also embed page-level text and combine scores:
        final = page_weight * page_score + (1 - page_weight) * chunk_score
    page_text_words controls how many body words are included in each page's
    embedding (W18). Default matches CHUNK_MAX_WORDS for backward compat.
    If ensemble_embedder is set, also embed chunks + queries with that model
    and RRF-fuse the resulting rankings into the "embedding" mode output.
    """
    # Embed all chunks
    chunk_texts = [c.text for c in chunks]
    logger.info(f"    Embedding {len(chunk_texts)} chunks for {tool}/{site}...")
    embed_start = time.time()
    vectors = embed_texts(client, chunk_texts)
    embed_time = time.time() - embed_start
    logger.info(f"    Embedded in {embed_time:.1f}s")

    for chunk, vec in zip(chunks, vectors):
        chunk.vector = vec

    vec_matrix = [c.vector for c in chunks]

    # Ensemble: embed chunks with the secondary embedder too (independent vectors)
    vec_matrix_ensemble: Optional[List[List[float]]] = None
    if ensemble_embedder:
        logger.info(f"    Ensemble: embedding {len(chunk_texts)} chunks with {ensemble_embedder}...")
        ens_start = time.time()
        vec_matrix_ensemble = embed_texts(client, chunk_texts, model=ensemble_embedder)
        logger.info(f"    Ensemble embedded in {time.time() - ens_start:.1f}s")

    # Dual-index: embed whole-page text (truncated) for unique URLs used by chunks
    page_vec_by_url: Optional[Dict[str, List[float]]] = None
    if dual_index and pages:
        chunk_urls = {c.url for c in chunks}
        page_text_by_url: Dict[str, str] = {}
        for p in pages:
            url = p.get("url", "")
            if url not in chunk_urls:
                continue
            title = p.get("title", "") or ""
            text = p.get("text", "") or ""
            # Truncate to page_text_words for embedding budget control (W18).
            words = text.split()
            if len(words) > page_text_words:
                text = " ".join(words[:page_text_words])
            composed = f"{title}\n\n{text}" if title else text
            if composed.strip():
                page_text_by_url[url] = composed
        if page_text_by_url:
            urls_ordered = list(page_text_by_url.keys())
            page_texts = [page_text_by_url[u] for u in urls_ordered]
            logger.info(f"    Embedding {len(page_texts)} pages for dual-index ({tool}/{site})...")
            page_vecs = embed_texts(client, page_texts)
            page_vec_by_url = {u: v for u, v in zip(urls_ordered, page_vecs)}

    # Ensemble dual-index: also embed pages with the secondary embedder
    page_vec_by_url_ensemble: Optional[Dict[str, List[float]]] = None
    if ensemble_embedder and dual_index and pages and page_vec_by_url:
        urls_ordered = list(page_vec_by_url.keys())
        page_texts_ens = [page_text_by_url[u] for u in urls_ordered]
        logger.info(f"    Ensemble: embedding {len(page_texts_ens)} pages with {ensemble_embedder}...")
        page_vecs_ens = embed_texts(client, page_texts_ens, model=ensemble_embedder)
        page_vec_by_url_ensemble = {u: v for u, v in zip(urls_ordered, page_vecs_ens)}

    # Build BM25 index
    bm25_index = _build_bm25_index(chunk_texts)

    # Embed queries if not provided (batch all at once)
    if query_vectors is None:
        query_texts = [query_prefix + q["query"] for q in queries]
        logger.info(f"    Embedding {len(query_texts)} queries...")
        query_vectors = embed_texts(client, query_texts)

    # Run queries across all modes
    search_start = time.time()
    mode_query_results: Dict[str, List[QueryResult]] = {m: [] for m in RETRIEVAL_MODES}

    for qi, q in enumerate(queries):
        query_vec = query_vectors[qi]
        query_vec_ensemble = ensemble_query_vectors[qi] if ensemble_query_vectors else None
        url_match = q.get("url_match", "")
        page_match = q.get("page_match", "")

        for mode in RETRIEVAL_MODES:
            top_urls, top_scores, hit, hit_rank = _run_single_mode(
                mode, q["query"], query_vec, chunks, vec_matrix, bm25_index,
                url_match, page_match,
                page_vec_by_url=page_vec_by_url,
                dual_index=dual_index,
                page_weight=page_weight,
                mmr_lambda=mmr_lambda,
                vec_matrix_ensemble=vec_matrix_ensemble,
                query_vec_ensemble=query_vec_ensemble,
                page_vec_by_url_ensemble=page_vec_by_url_ensemble,
            )
            mode_query_results[mode].append(QueryResult(
                query=q["query"],
                description=q["description"],
                expected_url_match=url_match,
                expected_page_match=page_match,
                top_k_urls=top_urls,
                top_k_scores=top_scores,
                hit=hit,
                hit_rank=hit_rank,
                category=q.get("category", ""),
            ))

    search_time = time.time() - search_start

    total_pages = len(set(c.url for c in chunks))
    avg_words = sum(len(c.text.split()) for c in chunks) / len(chunks) if chunks else 0

    # Build mode results
    mode_results: Dict[str, RetrievalModeResult] = {}
    for mode in RETRIEVAL_MODES:
        qrs = mode_query_results[mode]
        hits_at_k = _compute_hits_at_k(qrs)
        mrr = _compute_mrr(qrs)
        page_mrr, page_hits_at_k = _compute_page_level_mrr_and_hits(qrs)
        mode_results[mode] = RetrievalModeResult(
            mode=mode,
            query_results=qrs,
            hits_at_k=hits_at_k,
            mrr=mrr,
            page_mrr=page_mrr,
            page_hits_at_k=page_hits_at_k,
        )

    # DS-4: three-metric decomposition over the helpful-pages universe.
    # Indexed URLs come from the tool's own page list for this site.
    emb_for_triple = mode_results["embedding"]
    indexed_urls = list(page_text_by_url.keys()) if page_text_by_url else [
        c.get("url", "") for c in chunks
    ]
    triple = _three_metrics(
        _page_rr_per_query(emb_for_triple.query_results),
        indexed_urls,
        _load_helpful_urls(site),
        normalize=_normalize_url_for_matching,
    )
    logger.info(
        f"    DS-4 {tool}/{site}: coverage {_format_coverage(triple['coverage_covered'], triple['coverage_total'], triple['coverage_pct'])}"
        f" | on-covered MRR {triple['retrieval_on_covered_mrr']}"
        f" | end-to-end MRR {triple['end_to_end_mrr']:.4f}"
    )

    # Primary result uses embedding mode for backward compatibility
    emb = mode_results["embedding"]
    max_k = max(REPORT_AT_K)
    hits = emb.hits_at_k.get(max_k, 0)

    return ToolSiteRetrievalResult(
        tool=tool,
        site=site,
        total_queries=len(queries),
        hits=hits,
        hit_rate=hits / len(queries) if queries else 0,
        total_chunks=len(chunks),
        total_pages=total_pages,
        avg_chunk_words=avg_words,
        query_results=emb.query_results,
        embed_time=embed_time,
        search_time=search_time,
        hits_at_k=emb.hits_at_k,
        mrr=emb.mrr,
        mode_results=mode_results,
        chunk_config_label=chunk_config_label,
        page_mrr=emb.page_mrr,
        coverage_covered=triple["coverage_covered"],
        coverage_total=triple["coverage_total"],
        coverage_pct=triple["coverage_pct"],
        retrieval_on_covered_mrr=triple["retrieval_on_covered_mrr"],
        retrieval_on_covered_n=triple["retrieval_on_covered_n"],
        end_to_end_mrr=triple["end_to_end_mrr"],
    )


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def _compute_confidence_interval(hits: int, total: int) -> Tuple[float, float]:
    """Wilson score interval for binomial proportion (95% confidence)."""
    if total == 0:
        return (0.0, 0.0)
    z = 1.96  # 95% CI
    p_hat = hits / total
    denom = 1 + z * z / total
    center = (p_hat + z * z / (2 * total)) / denom
    spread = z * math.sqrt((p_hat * (1 - p_hat) + z * z / (4 * total)) / total) / denom
    return (max(0.0, center - spread), min(1.0, center + spread))


def _fmt_rate(hits: int, total: int, show_ci: bool = True) -> str:
    """Format hit rate with optional CI."""
    rate = hits / total if total else 0
    base = f"{rate:.0%} ({hits}/{total})"
    if show_ci:
        lo, hi = _compute_confidence_interval(hits, total)
        base += f" ±{(hi-lo)/2:.0%}"
    return base


def _aggregate_tool_mode(
    tool: str,
    mode: str,
    results: Dict[str, Dict[str, "ToolSiteRetrievalResult"]],
    sites: Optional[set] = None,
) -> Optional[tuple]:
    """Aggregate hit counts and MRR for a tool+mode over the given sites.

    Returns (total_queries, agg_hits_dict, mrr, page_mrr, agg_page_hits_dict)
    or None if no data. Page-level fields (DS-1) sit at indices 3 and 4.
    """
    total_queries = 0
    has_data = False
    agg_hits: Dict[int, int] = {k: 0 for k in REPORT_AT_K}
    agg_page_hits: Dict[int, int] = {k: 0 for k in REPORT_AT_K}
    rr_sum = 0.0
    page_rr_sum = 0.0

    for site, site_results in results.items():
        if sites is not None and site not in sites:
            continue
        r = site_results.get(tool)
        if r and mode in r.mode_results:
            has_data = True
            mr = r.mode_results[mode]
            total_queries += r.total_queries
            for k in REPORT_AT_K:
                agg_hits[k] += mr.hits_at_k.get(k, 0)
                agg_page_hits[k] += mr.page_hits_at_k.get(k, 0)
            rr_sum += mr.mrr * r.total_queries
            page_rr_sum += mr.page_mrr * r.total_queries

    if not has_data or total_queries == 0:
        return None
    return (
        total_queries,
        agg_hits,
        rr_sum / total_queries,
        page_rr_sum / total_queries,
        agg_page_hits,
    )


def generate_retrieval_report(
    results: Dict[str, Dict[str, ToolSiteRetrievalResult]],
    tool_names: List[str],
    chunk_sensitivity_results: Optional[Dict] = None,
    run_dir: Optional[Path] = None,
) -> str:
    """Generate the RETRIEVAL_COMPARISON.md report."""
    provenance = ""
    if run_dir is not None:
        try:
            from sites.pool import format_run_provenance_md
            provenance = format_run_provenance_md(run_dir)
        except Exception:
            provenance = ""
    total_queries_count = sum(
        len(TEST_QUERIES.get(site, []))
        for site in results.keys()
    )

    # Identify common sites where ALL tools have data, for fair comparison
    common_sites = set(results.keys())
    for site, site_results in results.items():
        for tool in tool_names:
            if tool not in site_results:
                common_sites.discard(site)
                break
    common_queries = sum(
        len(TEST_QUERIES.get(site, []))
        for site in common_sites
    )
    all_sites = set(results.keys())
    has_partial_tools = common_sites != all_sites

    lines = [
        "# Retrieval Quality Comparison",
        f"<!-- style: v2, {datetime.date.today().isoformat()} -->",
        "",
        "Crawler choice barely matters for retrieval — retrieval mode matters more.",
        "",
    ]
    if provenance:
        lines.extend([provenance, ""])
    lines.extend([
        "Does each tool's output produce embeddings that answer real questions?",
        "This benchmark chunks each tool's crawl output, embeds it with",
        f"`{EMBEDDING_MODEL}`, and measures retrieval across four modes:",
        "",
        "- **Embedding**: Cosine similarity on OpenAI embeddings",
        "- **BM25**: Keyword search (Okapi BM25)",
        "- **Hybrid**: Embedding + BM25 fused via Reciprocal Rank Fusion",
        f"- **Reranked**: Hybrid candidates reranked by `{RERANK_MODEL}`",
        "",
        f"**{total_queries_count} queries** across {len(results)} sites.",
        "Hit rate = correct source page in top-K results. Higher is better.",
    ])
    if has_partial_tools:
        missing_sites = all_sites - common_sites
        lines.append(
            f"Summary tables use the **{common_queries}-query common subset** "
            f"({len(common_sites)} sites) so all tools are compared on identical "
            f"queries. Sites excluded: {', '.join(sorted(missing_sites))} "
            f"(not all tools have data). Per-site tables show full results."
        )
    lines.append("")

    # ============================================================
    # Section 1a: Best mode per tool digest (7 rows)
    # ============================================================
    # Pre-compute all tool+mode aggregates for the digest and multi-mode table
    tool_mode_aggs: Dict[str, Dict[str, tuple]] = {}
    for tool in tool_names:
        tool_mode_aggs[tool] = {}
        for mode in RETRIEVAL_MODES:
            agg = _aggregate_tool_mode(tool, mode, results, common_sites)
            if agg is not None:
                tool_mode_aggs[tool][mode] = agg

    lines.extend(["## Quick summary: best retrieval mode per tool", ""])
    lines.append(
        "For each tool, the mode with the highest MRR. Most readers can stop here."
    )
    lines.append("")
    lines.append("| Tool | Best mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR | Page MRR |")
    lines.append("|---|---|---|---|---|---|---|---|")

    # Build digest rows, sorted by best MRR descending
    digest_rows = []
    for tool in tool_names:
        if not tool_mode_aggs[tool]:
            continue
        best_mode = max(tool_mode_aggs[tool], key=lambda m: tool_mode_aggs[tool][m][2])
        total_queries, agg_hits, mrr, page_mrr, _ = tool_mode_aggs[tool][best_mode]
        hit1 = _fmt_rate(agg_hits.get(1, 0), total_queries)
        hit3 = _fmt_rate(agg_hits.get(3, 0), total_queries)
        hit5 = _fmt_rate(agg_hits.get(5, 0), total_queries)
        hit10 = _fmt_rate(agg_hits.get(10, 0), total_queries)
        tname = tool
        digest_rows.append((mrr, f"| {tname} | {best_mode} | {hit1} | {hit3} | {hit5} | {hit10} | {mrr:.3f} | {page_mrr:.3f} |"))
    digest_rows.sort(key=lambda x: x[0], reverse=True)
    for _, row in digest_rows:
        lines.append(row)

    lines.extend([
        "",
        "> **Column definitions:** "
        "**Best mode** = retrieval strategy that maximizes MRR for this tool. "
        "**Hit@K** = % of queries where the correct source page appeared in the top K (chunk-level). "
        "**MRR** (chunk-level) = Mean Reciprocal Rank across all retrieved chunks. "
        "**Page MRR** (DS-1) = MRR after collapsing chunks-per-URL to unique pages — "
        "removes the chunk-density gaming signal where a tool emitting more chunks "
        "per page would otherwise rank ahead at the same content.",
        "",
        "> **Density sensitivity (DS-9):** Hit@1 is the LEAST chunk-density-sensitive "
        "(each chunk competes for one slot, so emitting more chunks doesn't help unless "
        "the first one is right). Hit@10 is the MOST sensitive (more chunks = more "
        "chances to land somewhere in the top 10). MRR sits between the two. Page MRR "
        "removes the density signal entirely — read it as the chunk-density-corrected "
        "MRR.",
        "",
    ])

    # ============================================================
    # Section 1b: Multi-mode summary (embedding vs hybrid vs reranked)
    # ============================================================
    lines.extend(["## Summary: retrieval modes compared", ""])
    if has_partial_tools:
        lines.append(
            f"_Computed over {common_queries} queries on {len(common_sites)} "
            f"common sites ({', '.join(sorted(common_sites))})._"
        )
        lines.append("")

    # Build header: Tool | Mode | Hit@K... | MRR | Page MRR
    k_headers = " | ".join(f"Hit@{k}" for k in REPORT_AT_K)
    lines.append(f"| Tool | Mode | {k_headers} | MRR | Page MRR |")
    lines.append("|---" + "|---" * len(REPORT_AT_K) + "|---|---|---|")

    # Sort within each mode group by MRR descending
    for mode in RETRIEVAL_MODES:
        mode_rows = []
        for tool in tool_names:
            agg = tool_mode_aggs[tool].get(mode)
            if agg is None:
                continue
            total_queries, agg_hits, mrr, page_mrr, _ = agg
            k_cols = [_fmt_rate(agg_hits[k], total_queries) for k in REPORT_AT_K]
            tname = tool
            mode_rows.append((mrr, f"| {tname} | {mode} | " + " | ".join(k_cols) + f" | {mrr:.3f} | {page_mrr:.3f} |"))
        mode_rows.sort(key=lambda x: x[0], reverse=True)
        for _, row in mode_rows:
            lines.append(row)

    lines.extend([
        "",
        "> **Column definitions:** "
        "**Hit@K** = percentage of queries where the correct source page appeared in the top K results (shown as % with raw counts). "
        "**MRR** (Mean Reciprocal Rank, chunk-level) = average of 1/rank for correct results across the chunk-ordered top-K (1.0 = always rank 1, 0.5 = always rank 2). "
        "**Page MRR** (DS-1, page-level) = MRR after collapsing multiple chunks per URL into a single rank — neutralises chunk-density inflation. Page MRR ≥ MRR by construction; the gap measures how much chunk-density was inflating the chunk-level number. "
        "**Mode** = retrieval strategy used (see definitions above).",
        "",
    ])

    # ============================================================
    # Section 2: Embedding-only summary (backward compatible)
    # ============================================================
    lines.extend(["## Summary: embedding-only (hit rate at multiple K values)", ""])
    if has_partial_tools:
        lines.append(
            f"_Computed over {common_queries} queries on {len(common_sites)} common sites._"
        )
        lines.append("")

    k_headers = " | ".join(f"Hit@{k}" for k in REPORT_AT_K)
    lines.append(f"| Tool | {k_headers} | MRR | Chunks | Avg words |")
    lines.append("|---" + "|---" * len(REPORT_AT_K) + "|---|---|---|")

    # Collect rows then sort by MRR descending
    emb_summary_rows = []
    for tool in tool_names:
        total_queries = 0
        total_chunks = 0
        total_chunk_words = 0
        has_data = False
        agg_hits: Dict[int, int] = {k: 0 for k in REPORT_AT_K}
        rr_sum = 0.0

        for site, site_results in results.items():
            if site not in common_sites:
                continue
            r = site_results.get(tool)
            if r:
                has_data = True
                total_queries += r.total_queries
                total_chunks += r.total_chunks
                total_chunk_words += r.avg_chunk_words * r.total_chunks
                for k in REPORT_AT_K:
                    agg_hits[k] += r.hits_at_k.get(k, 0)
                rr_sum += r.mrr * r.total_queries

        if not has_data:
            cols = " | ".join("—" for _ in REPORT_AT_K)
            emb_summary_rows.append((0.0, tool, f"| {tool} | {cols} | — | — | — |"))
            continue

        avg_words = total_chunk_words / total_chunks if total_chunks else 0
        mrr = rr_sum / total_queries if total_queries else 0
        k_cols = [_fmt_rate(agg_hits[k], total_queries) for k in REPORT_AT_K]
        tname = tool
        emb_summary_rows.append((mrr, tool, f"| {tname} | " + " | ".join(k_cols) +
            f" | {mrr:.3f} | {total_chunks} | {avg_words:.0f} |"))

    emb_summary_rows.sort(key=lambda x: x[0], reverse=True)
    for _, _, row in emb_summary_rows:
        lines.append(row)

    lines.extend([
        "",
        "> **Column definitions:** "
        "**Hit@K** = correct source page in top K results. "
        "**MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). "
        "**Chunks** = total chunks produced by this tool (across all pages in common sites). "
        "**Avg words** = mean words per chunk.",
        "",
    ])

    # ============================================================
    # "What this means" narrative interpretation
    # ============================================================
    lines.extend(["## What this means", ""])
    # Compute actual MRR range from the embedding summary rows.
    # Detect outliers: a tool is an outlier if it sits noticeably below the
    # cluster of the rest (gap to next-lowest >= 0.10, and >= 2x the spread of
    # the remaining tools). When an outlier exists, describe the cluster
    # separately rather than implying all tools are close.
    emb_mrrs_sorted = sorted(
        [(mrr, tool) for mrr, tool, _ in emb_summary_rows if mrr > 0],
        key=lambda x: x[0],
    )
    outlier = None
    cluster = emb_mrrs_sorted
    if len(emb_mrrs_sorted) >= 3:
        low_mrr, low_tool = emb_mrrs_sorted[0]
        rest = emb_mrrs_sorted[1:]
        rest_min = rest[0][0]
        rest_max = rest[-1][0]
        rest_spread = rest_max - rest_min
        gap = rest_min - low_mrr
        if gap >= 0.10 and (rest_spread == 0 or gap >= 2 * rest_spread):
            outlier = (low_tool, low_mrr)
            cluster = rest

    c_min = cluster[0][0] if cluster else 0.0
    c_max = cluster[-1][0] if cluster else 0.0
    c_spread = c_max - c_min
    cluster_count = len(cluster)
    total_count = len(emb_mrrs_sorted)
    if outlier:
        out_tool, out_mrr = outlier
        narrative = (
            f"{cluster_count} of the {total_count} tools cluster tightly "
            f"(MRR {c_min:.3f}-{c_max:.3f}, a {c_spread:.3f} spread on embedding "
            f"mode), while **{out_tool}** trails at MRR {out_mrr:.3f} -- a real "
            "outlier worth flagging rather than averaging away. "
            "Within the cluster, tools crawl similar pages from the same seed URLs "
            "and we apply identical chunking and embedding pipelines, so the "
            "extraction differences that matter for "
            "[content quality](QUALITY_COMPARISON.md) largely wash out at retrieval "
            f"time. {out_tool}'s gap likely reflects fewer or less complete pages "
            "discovered during crawling -- see the per-site coverage tables below."
        )
    elif cluster and c_spread < 0.10:
        narrative = (
            f"All tools perform within a narrow band (MRR {c_min:.3f}-{c_max:.3f} "
            "on embedding mode). "
            "This is expected: tools crawl similar pages from the same seed URLs, "
            "and we apply identical chunking and embedding pipelines. The "
            "extraction differences that matter for "
            "[content quality](QUALITY_COMPARISON.md) largely wash out at "
            "retrieval time."
        )
    elif cluster:
        narrative = (
            f"Tools span MRR {c_min:.3f}-{c_max:.3f} on embedding mode "
            f"(a {c_spread:.3f} spread). "
            "Tools crawl similar pages from the same seed URLs, and we apply "
            "identical chunking and embedding pipelines, but extraction "
            "differences -- see [content quality](QUALITY_COMPARISON.md) -- "
            "show up at retrieval time."
        )
    else:
        narrative = (
            "All tools perform with similar MRR on embedding mode. "
            "Tools crawl similar pages from the same seed URLs, and we apply "
            "identical chunking and embedding pipelines."
        )
    lines.extend([
        narrative,
        "",
        "**Retrieval mode matters more than crawler choice.** Embedding search beats "
        "BM25 by roughly 2x on MRR across all tools. Hybrid and reranked modes fall "
        "between the two. Choosing the right retrieval strategy will improve your RAG "
        "pipeline far more than switching crawlers.",
        "",
        "**The noise-vs-recall trade-off.** Noisier tools (crawlee, playwright) have "
        "slightly higher hit rates, but they produce 2x the chunks of leaner tools "
        "(markcrawl, scrapy+md). More chunks means higher embedding and storage costs "
        "with diminishing retrieval returns. See [COST_AT_SCALE.md](COST_AT_SCALE.md) "
        "for the dollar impact.",
        "",
        "**For most use cases, pick your crawler based on speed and cost, not retrieval "
        "quality.** The differences here are within confidence intervals. Where crawler "
        "choice _does_ matter is content quality and downstream answer quality "
        "-- see [ANSWER_QUALITY.md](ANSWER_QUALITY.md).",
        "",
    ])

    # ============================================================
    # Section 3: Per-category breakdown
    # ============================================================
    # Collect per-category results across all sites (embedding mode only)
    # category -> tool -> {hits_at_k, total, rr_sum}
    cat_stats: Dict[str, Dict[str, Dict]] = {}
    for site, site_results in results.items():
        if site not in common_sites:
            continue
        queries = TEST_QUERIES.get(site, [])
        for tool in tool_names:
            r = site_results.get(tool)
            if not r:
                continue
            emb = r.mode_results.get("embedding")
            if not emb:
                continue
            for qi, qr in enumerate(emb.query_results):
                cat = qr.category or (queries[qi].get("category", "") if qi < len(queries) else "")
                if not cat:
                    continue
                if cat not in cat_stats:
                    cat_stats[cat] = {}
                if tool not in cat_stats[cat]:
                    cat_stats[cat][tool] = {"hits10": 0, "total": 0, "rr_sum": 0.0}
                cs = cat_stats[cat][tool]
                cs["total"] += 1
                if qr.hit:
                    cs["hits10"] += 1
                if qr.hit_rank is not None:
                    cs["rr_sum"] += 1.0 / qr.hit_rank

    if cat_stats:
        lines.extend(["## Per-category breakdown (embedding mode)", ""])
        lines.append(
            "Query categories reveal where crawlers actually differ. "
            "Categories like `js-rendered` and `structured-data` stress-test "
            "browser rendering and table extraction, while `api-function` and "
            "`conceptual` queries test basic content retrieval."
        )
        lines.append("")

        # Sort categories alphabetically
        sorted_cats = sorted(cat_stats.keys())

        lines.append("| Category | Tool | Hit@10 | MRR | Queries |")
        lines.append("|---|---|---|---|---|")

        for cat in sorted_cats:
            tool_data = cat_stats[cat]
            # Sort tools by hit rate descending, then MRR descending as tiebreaker
            sorted_tools = sorted(
                tool_data.keys(),
                key=lambda t: (
                    tool_data[t]["hits10"] / tool_data[t]["total"] if tool_data[t]["total"] else 0,
                    tool_data[t]["rr_sum"] / tool_data[t]["total"] if tool_data[t]["total"] else 0,
                ),
                reverse=True,
            )
            for tool in sorted_tools:
                cs = tool_data[tool]
                rate = cs["hits10"] / cs["total"] if cs["total"] else 0
                mrr = cs["rr_sum"] / cs["total"] if cs["total"] else 0
                tname = tool
                lines.append(
                    f"| {cat} | {tname} | {rate:.0%} ({cs['hits10']}/{cs['total']}) "
                    f"| {mrr:.3f} | {cs['total']} |"
                )

        lines.extend(["", ""])

        # Add a condensed "best tool per category" digest
        lines.extend(["### Best tool per category", ""])
        lines.append("| Category | Best tool | Hit@10 | Spread |")
        lines.append("|---|---|---|---|")

        for cat in sorted_cats:
            tool_data = cat_stats[cat]
            best_tool = max(
                tool_data.keys(),
                key=lambda t: tool_data[t]["hits10"] / tool_data[t]["total"] if tool_data[t]["total"] else 0,
            )
            worst_tool = min(
                tool_data.keys(),
                key=lambda t: tool_data[t]["hits10"] / tool_data[t]["total"] if tool_data[t]["total"] else 0,
            )
            best_rate = tool_data[best_tool]["hits10"] / tool_data[best_tool]["total"] if tool_data[best_tool]["total"] else 0
            worst_rate = tool_data[worst_tool]["hits10"] / tool_data[worst_tool]["total"] if tool_data[worst_tool]["total"] else 0
            spread = best_rate - worst_rate
            tname = best_tool
            lines.append(
                f"| {cat} | {tname} | {best_rate:.0%} | {spread:.0%} |"
            )

        lines.append("")
        lines.append(
            "_Spread = difference between best and worst tool. "
            "High spread categories are where crawler choice matters most._"
        )
        lines.extend(["", ""])

    # ============================================================
    # Section 4: Chunk size sensitivity (if available)
    # ============================================================
    if chunk_sensitivity_results:
        lines.extend(["## Chunk size sensitivity analysis", ""])
        lines.append(
            "Does clean crawler output produce better retrieval *regardless* of chunk size? "
            "Each tool tested at three chunk configurations."
        )
        lines.append("")

        # Table: Tool | Config | Hit@5 | Hit@10 | Hit@20 | MRR
        lines.append("| Tool | Chunk size | Hit@5 | Hit@10 | Hit@20 | MRR |")
        lines.append("|---|---|---|---|---|---|")

        for tool in tool_names:
            for config_label, config_results in chunk_sensitivity_results.items():
                total_q = 0
                agg_5 = 0
                agg_10 = 0
                agg_20 = 0
                rr_sum = 0.0
                has = False
                for site_results in config_results.values():
                    r = site_results.get(tool)
                    if r:
                        has = True
                        emb = r.mode_results.get("embedding")
                        if emb:
                            total_q += r.total_queries
                            agg_5 += emb.hits_at_k.get(5, 0)
                            agg_10 += emb.hits_at_k.get(10, 0)
                            agg_20 += emb.hits_at_k.get(20, 0)
                            rr_sum += emb.mrr * r.total_queries
                if not has or total_q == 0:
                    continue
                mrr = rr_sum / total_q
                lines.append(
                    f"| {tool} | {config_label} "
                    f"| {_fmt_rate(agg_5, total_q, False)} "
                    f"| {_fmt_rate(agg_10, total_q, False)} "
                    f"| {_fmt_rate(agg_20, total_q, False)} "
                    f"| {mrr:.3f} |"
                )

        lines.extend(["", ""])

    # ============================================================
    # Section 5: Per-site breakdown
    # ============================================================
    for site, site_results in results.items():
        queries = TEST_QUERIES.get(site, [])
        if not queries:
            continue

        lines.extend([f"## {site}", ""])

        # Hit rate table with multi-K (embedding mode)
        k_headers = " | ".join(f"Hit@{k}" for k in REPORT_AT_K)
        lines.extend([
            f"| Tool | {k_headers} | MRR | Chunks | Pages |",
            "|---" + "|---" * len(REPORT_AT_K) + "|---|---|---|",
        ])

        # Collect per-site rows and sort by MRR descending
        site_tool_rows = []
        for tool in tool_names:
            r = site_results.get(tool)
            tname = tool
            if not r:
                cols = " | ".join("—" for _ in REPORT_AT_K)
                site_tool_rows.append((0.0, f"| {tname} | {cols} | — | — | — |"))
                continue
            k_cols = []
            for k in REPORT_AT_K:
                h = r.hits_at_k.get(k, 0)
                rate = h / r.total_queries if r.total_queries else 0
                k_cols.append(f"{rate:.0%} ({h}/{r.total_queries})")
            site_tool_rows.append((r.mrr, f"| {tname} | " + " | ".join(k_cols) +
                f" | {r.mrr:.3f} | {r.total_chunks} | {r.total_pages} |"))
        site_tool_rows.sort(key=lambda x: x[0], reverse=True)
        for _, row in site_tool_rows:
            lines.append(row)

        lines.extend([
            "",
            "> **Chunks** = total chunks from this tool for this site. "
            "**Pages** = pages crawled. "
            "Hit rates shown as % (hits/total queries).",
            "",
        ])

        # Per-query detail (show top-3 only for readability)
        detail_k = 3
        lines.append("<details>")
        lines.append(f"<summary>Query-by-query results for {site}</summary>")
        lines.append("")
        lines.append(
            "> **Hit** = rank position where correct page appeared "
            "(#1 = top result, 'miss' = not in top 20). "
            "**Score** = cosine similarity between query embedding and chunk embedding."
        )
        lines.append("")

        for qi, q in enumerate(queries):
            cat_label = f" [{q.get('category', '')}]" if q.get("category") else ""
            lines.extend([
                f"**Q{qi+1}: {q['query']}**{cat_label}",
                f"*(expects URL containing: `{q.get('url_match', '')}`)*",
                "",
                "| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |",
                "|---|---|---|---|---|---|---|---|",
            ])

            for tool in tool_names:
                r = site_results.get(tool)
                if not r or qi >= len(r.query_results):
                    lines.append(f"| {tool} | — | — | — | — | — | — | — |")
                    continue

                qr = r.query_results[qi]
                hit_marker = f"#{qr.hit_rank}" if qr.hit_rank is not None else "miss"
                row = f"| {tool} | {hit_marker} "
                for i in range(detail_k):
                    if i < len(qr.top_k_urls):
                        short_url = qr.top_k_urls[i].split("//")[-1][:50]
                        score = qr.top_k_scores[i]
                        row += f"| {short_url} | {score:.3f} "
                    else:
                        row += "| — | — "
                row += "|"
                lines.append(row)

            lines.extend(["", ""])

        lines.extend(["</details>", ""])

    # ============================================================
    # Methodology
    # ============================================================
    k_list = ", ".join(str(k) for k in REPORT_AT_K)
    config_list = ", ".join(f"{lbl}" for _, _, lbl in CHUNK_CONFIGS)
    lines.extend([
        "## Methodology",
        "",
        f"- **Queries:** {total_queries_count} across {len(results)} sites, categorized by type "
        "(api-function, code-example, conceptual, structured-data, factual-lookup, cross-page, navigation, js-rendered)",
        f"- **Embedding model:** `{EMBEDDING_MODEL}` ({EMBEDDING_DIMENSIONS} dimensions)",
        f"- **Chunking:** Markdown-aware, {CHUNK_MAX_WORDS} word max, {CHUNK_OVERLAP} word overlap",
        f"- **Retrieval modes:** Embedding (cosine), BM25 (Okapi), Hybrid (RRF k={RRF_K}), Reranked (`{RERANK_MODEL}`)",
        f"- **Retrieval:** Hit rate reported at K = {k_list}, plus MRR",
        f"- **Reranking:** Top-{TOP_K} candidates from hybrid search, reranked to top-{RERANK_TOP_N}",
        f"- **Chunk sensitivity:** Tested at {config_list}",
        "- **Confidence intervals:** Wilson score interval (95%)",
        "- **Same chunking and embedding** for all tools — only extraction quality varies",
        "- **No fine-tuning or tool-specific optimization** — identical pipeline for all",
        "",
        "See [METHODOLOGY.md](METHODOLOGY.md) for full test setup, tool configurations,",
        "and fairness decisions.",
        "",
        "## See also",
        "",
        "- [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) — content quality differences "
        "that wash out at retrieval time but affect downstream answers",
        "- [ANSWER_QUALITY.md](ANSWER_QUALITY.md) — where the LLM's final answers diverge "
        "despite similar retrieval",
        "- [COST_AT_SCALE.md](COST_AT_SCALE.md) — the dollar impact of chunk count "
        "differences (2x chunks = 2x embedding cost)",
        "- [METHODOLOGY.md](METHODOLOGY.md) — full test setup, tool configurations, "
        "and fairness decisions",
        "",
    ])

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Find latest run
# ---------------------------------------------------------------------------

def find_latest_run(runs_dir: Path) -> Optional[Path]:
    """Find the most recent benchmark run directory."""
    if not runs_dir.is_dir():
        return None
    runs = sorted(runs_dir.glob("run_*"), reverse=True)
    return runs[0] if runs else None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

CHECKPOINT_DIR = BENCH_DIR / "retrieval_checkpoints"


def _embedder_slug(model_name: Optional[str] = None) -> str:
    """Filesystem-safe slug for an embedder model name.

    text-embedding-3-small               -> text-embedding-3-small
    mixedbread-ai/mxbai-embed-large-v1   -> mixedbread-ai_mxbai-embed-large-v1
    """
    name = model_name if model_name is not None else EMBEDDING_MODEL
    return name.replace("/", "_")


def _site_queries_hash(site: str) -> str:
    """8-char SHA-256 prefix of canonicalized TEST_QUERIES[site]. Per-site
    rather than whole-dict so that tweaking one site's queries (e.g.,
    re-firing DS-6 for huggingface-transformers only) invalidates JUST
    that site's cache instead of all 11.

    Returns an empty-set hash if the site has no entry, which still
    differs from any populated set — so adding a new site cleanly busts
    its cache too."""
    site_queries = TEST_QUERIES.get(site, [])
    canonical = json.dumps(site_queries, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()[:8]


def _checkpoint_key(run_name: str, tool: str, site: str, config_label: str) -> str:
    """Cache-aware key. Includes the embedder slug (DS-13b) AND a
    per-site queries hash so that any change to either invalidates the
    per-(tool, site) cache. The per-site hash matters for v1.4+ cycles
    where DS-6 can be re-fired site-by-site (e.g., HF scope-filter fix
    2026-05-11) — whole-dict hashing would invalidate every site on
    any per-site tweak."""
    embedder = _embedder_slug()
    queries = _site_queries_hash(site)
    safe = f"{run_name}__{embedder}__{queries}__{tool}__{site}__{config_label}".replace("/", "_")
    return safe


def _save_checkpoint(run_name: str, tool: str, site: str, config_label: str, result: ToolSiteRetrievalResult) -> None:
    """Save a completed tool/site result to disk."""
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    key = _checkpoint_key(run_name, tool, site, config_label)
    data = {
        "tool": result.tool,
        "site": result.site,
        "total_queries": result.total_queries,
        "hits": result.hits,
        "hit_rate": result.hit_rate,
        "total_chunks": result.total_chunks,
        "total_pages": result.total_pages,
        "avg_chunk_words": result.avg_chunk_words,
        "embed_time": result.embed_time,
        "search_time": result.search_time,
        "hits_at_k": result.hits_at_k,
        "mrr": result.mrr,
        "page_mrr": result.page_mrr,
        "chunk_config_label": result.chunk_config_label,
        "mode_results": {},
        "query_results": [],  # primary (embedding) mode
    }
    # Save each mode's results
    for mode, mr in result.mode_results.items():
        mode_data = {
            "mode": mr.mode,
            "hits_at_k": mr.hits_at_k,
            "mrr": mr.mrr,
            "page_mrr": mr.page_mrr,
            "page_hits_at_k": mr.page_hits_at_k,
            "query_results": [],
        }
        for qr in mr.query_results:
            mode_data["query_results"].append({
                "query": qr.query,
                "description": qr.description,
                "expected_url_match": qr.expected_url_match,
                "expected_page_match": qr.expected_page_match,
                "top_k_urls": qr.top_k_urls[:20],  # save top-20 only to limit size
                "top_k_scores": qr.top_k_scores[:20],
                "hit": qr.hit,
                "hit_rank": qr.hit_rank,
                "category": qr.category,
            })
        data["mode_results"][mode] = mode_data

    # Primary query results
    for qr in result.query_results:
        data["query_results"].append({
            "query": qr.query,
            "description": qr.description,
            "expected_url_match": qr.expected_url_match,
            "expected_page_match": qr.expected_page_match,
            "top_k_urls": qr.top_k_urls[:20],
            "top_k_scores": qr.top_k_scores[:20],
            "hit": qr.hit,
            "hit_rank": qr.hit_rank,
            "category": qr.category,
        })

    path = CHECKPOINT_DIR / f"{key}.json"
    tmp_path = path.with_suffix(".json.tmp")
    with open(tmp_path, "w") as f:
        json.dump(data, f)
    tmp_path.replace(path)


def _load_checkpoint(run_name: str, tool: str, site: str, config_label: str) -> Optional[ToolSiteRetrievalResult]:
    """Load a checkpoint if it exists."""
    key = _checkpoint_key(run_name, tool, site, config_label)
    path = CHECKPOINT_DIR / f"{key}.json"
    if not path.is_file():
        return None

    with open(path, "r") as f:
        data = json.load(f)

    def _load_qrs(qr_list):
        return [
            QueryResult(
                query=q["query"],
                description=q["description"],
                expected_url_match=q["expected_url_match"],
                expected_page_match=q["expected_page_match"],
                top_k_urls=q["top_k_urls"],
                top_k_scores=q["top_k_scores"],
                hit=q["hit"],
                hit_rank=q["hit_rank"],
                category=q.get("category", ""),
            )
            for q in qr_list
        ]

    mode_results = {}
    for mode, md in data.get("mode_results", {}).items():
        mode_qrs = _load_qrs(md["query_results"])
        # Recompute page-level metrics from query_results on load rather
        # than trusting checkpoint values — this makes the system
        # self-healing for page-level methodology fixes (e.g., the
        # 2026-05-11 collapse-key bug fix). Cheap because it's just URL
        # matching, no cosine math.
        page_mrr, page_hits_at_k = _compute_page_level_mrr_and_hits(mode_qrs)
        mode_results[mode] = RetrievalModeResult(
            mode=md["mode"],
            query_results=mode_qrs,
            hits_at_k={int(k): v for k, v in md["hits_at_k"].items()},
            mrr=md["mrr"],
            page_mrr=page_mrr,
            page_hits_at_k=page_hits_at_k,
        )

    # Top-level page_mrr mirrors embedding mode (matches construction
    # path at the main run site). Warn loudly if embedding mode is
    # missing — silent zero would let a malformed checkpoint sneak a
    # 0.0 page-MRR into the rendered report (reviewer Q3).
    if "embedding" in mode_results:
        top_level_page_mrr = mode_results["embedding"].page_mrr
    else:
        logger.warning(
            "Checkpoint for %s/%s missing 'embedding' mode_results — "
            "top-level page_mrr will be reported as 0.0. Re-run without "
            "--report-only to regenerate this checkpoint.",
            data["tool"], data["site"],
        )
        top_level_page_mrr = 0.0

    return ToolSiteRetrievalResult(
        tool=data["tool"],
        site=data["site"],
        total_queries=data["total_queries"],
        hits=data["hits"],
        hit_rate=data["hit_rate"],
        total_chunks=data["total_chunks"],
        total_pages=data["total_pages"],
        avg_chunk_words=data["avg_chunk_words"],
        query_results=_load_qrs(data["query_results"]),
        embed_time=data["embed_time"],
        search_time=data["search_time"],
        hits_at_k={int(k): v for k, v in data["hits_at_k"].items()},
        mrr=data["mrr"],
        mode_results=mode_results,
        chunk_config_label=data.get("chunk_config_label", ""),
        page_mrr=top_level_page_mrr,
    )


def _run_benchmark_for_config(
    client,
    run_dir: Path,
    sites: List[str],
    available_tools: List[str],
    max_words: int,
    overlap_words: int,
    config_label: str,
    verbose: bool = True,
    add_context_headers: bool = False,
    dual_index: bool = False,
    page_weight: float = 0.3,
    mmr_lambda: float = 1.0,
    page_text_words: int = CHUNK_MAX_WORDS,
    query_prefix: str = "",
    hyde: bool = False,
    hyde_model: str = HYDE_MODEL_DEFAULT,
    hyde_cache_dir: Path = HYDE_CACHE_DIR,
    ensemble_embedder: Optional[str] = None,
) -> Dict[str, Dict[str, ToolSiteRetrievalResult]]:
    """Run the full retrieval benchmark for a single chunk configuration.

    Supports resuming: completed tool/site results are checkpointed to disk
    and reloaded on restart, so wifi drops only lose the in-progress item.
    """
    run_name = run_dir.name
    all_results: Dict[str, Dict[str, ToolSiteRetrievalResult]] = {}

    for site in sites:
        queries = TEST_QUERIES.get(site)
        if not queries:
            if verbose:
                logger.info(f"\n  Skipping {site}: no test queries defined")
            continue

        if verbose:
            logger.info(f"\n{'='*60}")
            logger.info(f"Site: {site} ({len(queries)} queries) [{config_label}]")
            logger.info(f"{'='*60}")

        site_results: Dict[str, ToolSiteRetrievalResult] = {}

        # Pre-embed queries once per site (reused across all tools)
        query_vectors: Optional[List[List[float]]] = None
        needs_embedding = any(
            _load_checkpoint(run_name, t, site, config_label) is None
            and (run_dir / t / site / "pages.jsonl").is_file()
            for t in available_tools
        )
        if needs_embedding:
            raw_query_texts = [q["query"] for q in queries]
            if hyde:
                if verbose:
                    logger.info(f"\n  HyDE: transforming {len(raw_query_texts)} queries for {site} via {hyde_model}...")
                query_texts = hyde_transform_queries(
                    client, raw_query_texts, model=hyde_model, cache_dir=hyde_cache_dir,
                )
            else:
                query_texts = [query_prefix + q for q in raw_query_texts]
            if verbose:
                logger.info(f"\n  Embedding {len(query_texts)} queries for {site} (shared across tools)...")
            query_vectors = embed_texts(client, query_texts)
            # Ensemble: also embed queries with secondary embedder
            if ensemble_embedder:
                if verbose:
                    logger.info(f"  Ensemble: embedding queries for {site} with {ensemble_embedder}...")
                ensemble_query_vectors = embed_texts(client, query_texts, model=ensemble_embedder)
            else:
                ensemble_query_vectors = None
        else:
            ensemble_query_vectors = None

        for tool in available_tools:
            # Check for checkpoint first
            cached_result = _load_checkpoint(run_name, tool, site, config_label)
            if cached_result is not None:
                site_results[tool] = cached_result
                if verbose:
                    emb = cached_result.mode_results.get("embedding")
                    h10 = emb.hits_at_k.get(10, 0) if emb else 0
                    logger.info(f"\n  {tool}: RESUMED from checkpoint -- Hit@10: {h10}/{cached_result.total_queries}")
                continue

            jsonl_path = run_dir / tool / site / "pages.jsonl"
            if not jsonl_path.is_file() or jsonl_path.stat().st_size == 0:
                if verbose:
                    logger.info(f"  {tool}: no data, skipping")
                continue

            if verbose:
                logger.info(f"\n  {tool}:")
            pages = load_pages(str(jsonl_path))
            if verbose:
                logger.info(f"    {len(pages)} pages loaded")

            chunks = chunk_pages(pages, tool, site, max_words=max_words, overlap_words=overlap_words, add_context_headers=add_context_headers)
            if verbose:
                logger.info(f"    {len(chunks)} chunks created")

            if not chunks:
                if verbose:
                    logger.warning("    no chunks created, skipping")
                continue

            result = run_retrieval_test(
                client, chunks, queries, tool, site, config_label, query_vectors,
                pages=pages, dual_index=dual_index, page_weight=page_weight,
                mmr_lambda=mmr_lambda, page_text_words=page_text_words,
                query_prefix=query_prefix,
                ensemble_embedder=ensemble_embedder,
                ensemble_query_vectors=ensemble_query_vectors,
            )
            site_results[tool] = result

            # Checkpoint immediately after each tool/site completes
            _save_checkpoint(run_name, tool, site, config_label, result)

            if verbose:
                emb = result.mode_results.get("embedding")
                reranked = result.mode_results.get("reranked")
                if emb:
                    h10 = emb.hits_at_k.get(10, 0)
                    logger.info(f"    Embedding  Hit@10: {h10}/{result.total_queries} ({h10/result.total_queries:.0%})  MRR: {emb.mrr:.3f}")
                if reranked:
                    h10 = reranked.hits_at_k.get(10, 0)
                    logger.info(f"    Reranked   Hit@10: {h10}/{result.total_queries} ({h10/result.total_queries:.0%})  MRR: {reranked.mrr:.3f}")

        all_results[site] = site_results

    return all_results


def main():
    parser = argparse.ArgumentParser(description="Retrieval quality benchmark — embed and compare")
    parser.add_argument("--run", default=None, help="Specific run directory name (e.g. run_20260405_221158)")
    parser.add_argument("--output", default=str(BENCH_DIR / "reports" / "RETRIEVAL_COMPARISON.md"),
                        help="Output path for the retrieval report")
    parser.add_argument("--sites", default=None, help="Comma-separated sites to test")
    parser.add_argument("--tools", default=None, help="Comma-separated tools to test")
    parser.add_argument("--chunk-sensitivity", action="store_true",
                        help="Run chunk size sensitivity analysis at multiple configurations")
    parser.add_argument("--no-rerank", action="store_true",
                        help="Skip cross-encoder reranking (faster but less complete)")
    parser.add_argument("--context-headers", action="store_true",
                        help="Prepend page title, section heading, and URL path to each chunk")
    parser.add_argument("--dual-index", action="store_true",
                        help="Combine page-level + chunk-level embedding scores (W7B multi-granularity)")
    parser.add_argument("--page-weight", type=float, default=0.3,
                        help="Weight alpha for page score in dual-index: final = alpha*page + (1-alpha)*chunk (default 0.3)")
    parser.add_argument("--mmr-lambda", type=float, default=1.0,
                        help="MMR lambda for diversity re-rank (W14). 1.0=off (pure relevance), <1.0 trades relevance for diversity")
    parser.add_argument("--page-text-words", type=int, default=CHUNK_MAX_WORDS,
                        help="Words of page body text to include in page vector (dual-index only). Default matches CHUNK_MAX_WORDS (400).")
    parser.add_argument("--query-prefix", type=str, default="",
                        help="String to prepend to every query text before embedding (W19 instruction-style prefix). Default empty.")
    parser.add_argument("--hyde", action="store_true",
                        help="HyDE: use LLM-generated hypothetical answers as the text to embed, instead of raw queries. Generic retrieval-side technique.")
    parser.add_argument("--hyde-model", type=str, default=HYDE_MODEL_DEFAULT,
                        help=f"LLM model for HyDE answer generation (default: {HYDE_MODEL_DEFAULT}).")
    parser.add_argument("--hyde-cache-dir", type=str, default=str(HYDE_CACHE_DIR),
                        help=f"Directory for cached HyDE outputs (default: {HYDE_CACHE_DIR}).")
    parser.add_argument("--ensemble-embedder", type=str, default=None,
                        help="Secondary embedder for RRF ensemble with the primary (EMBEDDING_MODEL). "
                             "Accepts an OpenAI model name or a HuggingFace sentence-transformers id "
                             "(e.g. 'BAAI/bge-large-en-v1.5'). When set, embedding-mode retrieval "
                             "becomes RRF fusion of primary + secondary rankings.")
    parser.add_argument("--fresh", action="store_true",
                        help="Clear checkpoints and embedding cache — start from scratch")
    parser.add_argument("--report-only", action="store_true",
                        help="Regenerate report from checkpoints only — no API calls")
    parser.add_argument("--allow-stale-markcrawl", action="store_true",
                        help="Proceed even if the installed markcrawl is older than PyPI's latest "
                             "(deliberate old-version runs only).")
    args = parser.parse_args()

    # Every tool's output is chunked with markcrawl's chunker, so a stale
    # install skews all tools' scores, not just markcrawl's.
    if not args.report_only:
        from tools.markcrawl_freshness import enforce as _enforce_markcrawl_fresh
        _enforce_markcrawl_fresh(args.allow_stale_markcrawl)

    # If --no-rerank, remove reranked from modes
    global RETRIEVAL_MODES
    if args.no_rerank:
        RETRIEVAL_MODES = [m for m in RETRIEVAL_MODES if m != "reranked"]

    # Clear caches if --fresh
    if args.fresh:
        import shutil
        if CHECKPOINT_DIR.is_dir():
            shutil.rmtree(CHECKPOINT_DIR)
            logger.info("Cleared retrieval checkpoints.")
        if EMBED_CACHE_DIR.is_dir():
            shutil.rmtree(EMBED_CACHE_DIR)
            logger.info("Cleared embedding cache.")

    runs_dir = BENCH_DIR / "runs"

    if args.run:
        run_dir = runs_dir / args.run
    else:
        run_dir = find_latest_run(runs_dir)

    if not run_dir or not run_dir.is_dir():
        logger.error(f"No benchmark run found at {run_dir}")
        sys.exit(1)

    # DS-13a defense-in-depth: assert embedding-model invariant + write
    # per-phase models_manifest.json BEFORE any API spend. PUBLISH-BOTH
    # allows EMBEDDING_MODEL to be either the OpenAI default or the
    # mxbai secondary; anything else is methodology drift and the
    # assertion fires here, before query embeddings get billed.
    from models_manifest import assert_embedding_model, write_models_manifest
    assert_embedding_model(EMBEDDING_MODEL)
    manifest_path = write_models_manifest(
        run_dir,
        "retrieval",
        embedding_model=EMBEDDING_MODEL,
    )
    logger.info(f"Wrote models manifest section to {manifest_path}")

    logger.info(f"Using benchmark run: {run_dir.name}")

    # Determine sites and tools to test.
    # Precedence: --sites CLI flag > run manifest sampled_sites > all TEST_QUERIES.
    if args.sites:
        sites = args.sites.split(",")
    else:
        try:
            from sites.pool import read_manifest
            m = read_manifest(run_dir)
        except Exception:
            m = None
        if m and m.get("sampled_sites"):
            sites = [entry["name"] for entry in m["sampled_sites"]]
            logger.info(f"Using sampled sites from manifest ({len(sites)} sites)")
        else:
            sites = list(TEST_QUERIES.keys())
    tools = args.tools.split(",") if args.tools else TOOLS

    # Only test sites that have queries defined
    sites = [s for s in sites if s in TEST_QUERIES]

    # Check which tools have data
    available_tools = []
    for tool in tools:
        has_any_data = False
        for site in sites:
            jsonl = run_dir / tool / site / "pages.jsonl"
            if jsonl.is_file() and jsonl.stat().st_size > 0:
                has_any_data = True
                break
        if has_any_data:
            available_tools.append(tool)
        else:
            logger.info(f"  Skipping {tool}: no data in this run")

    if not available_tools:
        logger.error("No tools have data for the selected sites")
        sys.exit(1)

    logger.info(f"Tools with data: {', '.join(available_tools)}")
    logger.info(f"Sites: {', '.join(sites)}")
    logger.info(f"Retrieval modes: {', '.join(RETRIEVAL_MODES)}")

    # --report-only: load all results from checkpoints, skip API calls
    if args.report_only:
        run_name = run_dir.name
        max_words, overlap_words, config_label = DEFAULT_CHUNK_CONFIG
        all_results: Dict[str, Dict[str, ToolSiteRetrievalResult]] = {}
        missing = []
        for site in sites:
            if site not in TEST_QUERIES:
                continue
            site_results: Dict[str, ToolSiteRetrievalResult] = {}
            for tool in available_tools:
                # Skip tools that have no pages data for this site (file
                # missing OR empty — empty pages.jsonl is the v1.3 cycle's
                # "tool couldn't crawl this site" sentinel and matches the
                # behaviour of the main run path).
                tool_pages = run_dir / tool / site / "pages.jsonl"
                if not tool_pages.exists() or tool_pages.stat().st_size == 0:
                    logger.debug("Skipping %s/%s — no pages data", tool, site)
                    continue
                cached = _load_checkpoint(run_name, tool, site, config_label)
                if cached is not None:
                    site_results[tool] = cached
                else:
                    missing.append(f"{tool}/{site}")
            all_results[site] = site_results

        if missing:
            logger.error("Missing checkpoints for --report-only: %s", ", ".join(missing))
            logger.error("Run without --report-only first to generate checkpoints.")
            sys.exit(1)

        logger.info(f"Loaded all results from checkpoints ({sum(len(v) for v in all_results.values())} tool/site combos)")
        chunk_sensitivity_results = None
    else:
        # Initialize OpenAI client
        client = _get_openai_client()

        # Verify API works with a tiny test
        logger.info("Verifying OpenAI API key...")
        try:
            embed_texts(client, ["test"])
            logger.info("  OK")
        except Exception as exc:
            logger.error(f"  FAILED: {exc}")
            sys.exit(1)

        # Run primary benchmark (default chunk config)
        max_words, overlap_words, config_label = DEFAULT_CHUNK_CONFIG
        all_results = _run_benchmark_for_config(
            client, run_dir, sites, available_tools,
            max_words, overlap_words, config_label,
            add_context_headers=args.context_headers,
            dual_index=args.dual_index,
            page_weight=args.page_weight,
            mmr_lambda=args.mmr_lambda,
            page_text_words=args.page_text_words,
            query_prefix=args.query_prefix,
            hyde=args.hyde,
            hyde_model=args.hyde_model,
            hyde_cache_dir=Path(args.hyde_cache_dir),
            ensemble_embedder=args.ensemble_embedder,
        )

        # Run chunk sensitivity analysis if requested
        chunk_sensitivity_results: Optional[Dict[str, Dict[str, Dict[str, ToolSiteRetrievalResult]]]] = None
        if args.chunk_sensitivity:
            chunk_sensitivity_results = {}
            for mw, ow, label in CHUNK_CONFIGS:
                if (mw, ow, label) == DEFAULT_CHUNK_CONFIG:
                    # Reuse primary results
                    chunk_sensitivity_results[label] = all_results
                else:
                    logger.info(f"\n\n{'#'*60}")
                    logger.info(f"# Chunk sensitivity: {label} (max_words={mw}, overlap={ow})")
                    logger.info(f"{'#'*60}")
                    chunk_sensitivity_results[label] = _run_benchmark_for_config(
                        client, run_dir, sites, available_tools,
                        mw, ow, label, verbose=True,
                        add_context_headers=args.context_headers,
                    )

    # Generate report
    report = generate_retrieval_report(all_results, available_tools, chunk_sensitivity_results, run_dir=run_dir)
    output_path = args.output
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    logger.info(f"\nRetrieval report written to: {output_path}")

    # Post-generation validation
    from lint_reports import lint_file
    lint_warnings = lint_file(Path(output_path))
    if lint_warnings:
        logger.warning("Post-generation lint found %d issue(s):", len(lint_warnings))
        for w in lint_warnings:
            logger.warning("  - %s", w)

    # DS-3: emit per-query audit CSV alongside the markdown report.
    # Embedder-aware filename so PUBLISH-BOTH primary + secondary runs don't
    # overwrite each other (caught 2026-05-11 when the DS-13a LOCAL fire's
    # audit CSV stomped the primary's audit data).
    audit_basename = (
        "QUERY_AUDIT.csv"
        if EMBEDDING_MODEL == "text-embedding-3-small"
        else "QUERY_AUDIT_LOCAL.csv"
    )
    audit_path = Path(output_path).parent / audit_basename
    try:
        rows = _write_query_audit_csv(all_results, audit_path)
        logger.info("Query audit written to %s (%d rows)", audit_path, rows)
    except Exception as e:
        logger.warning("Query audit CSV write failed (non-fatal): %s", e)

    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("SUMMARY (all retrieval modes)")
    logger.info("=" * 60)
    for mode in RETRIEVAL_MODES:
        logger.info(f"\n  --- {mode.upper()} ---")
        k_header = " | ".join(f"Hit@{k:>2}" for k in REPORT_AT_K)
        logger.info(f"  {'Tool':>15}  {k_header}  |  MRR")
        for tool in available_tools:
            total_queries = 0
            agg_hits: Dict[int, int] = {k: 0 for k in REPORT_AT_K}
            rr_sum = 0.0

            for site_results in all_results.values():
                r = site_results.get(tool)
                if r and mode in r.mode_results:
                    mr = r.mode_results[mode]
                    total_queries += r.total_queries
                    for k in REPORT_AT_K:
                        agg_hits[k] += mr.hits_at_k.get(k, 0)
                    rr_sum += mr.mrr * r.total_queries

            if not total_queries:
                continue
            mrr = rr_sum / total_queries
            k_vals = []
            for k in REPORT_AT_K:
                h = agg_hits[k]
                k_vals.append(f"{h}/{total_queries} ({h/total_queries:.0%})")
            logger.info(f"  {tool:>15}  {'  '.join(k_vals)}  |  {mrr:.3f}")

    # Regenerate README from updated report data
    try:
        import subprocess as _sp
        _sp.run([sys.executable, "generate_readme.py"], check=True)
        logger.info("README.md regenerated from report data.")
    except Exception as e:
        logger.warning(f"Could not regenerate README.md: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
