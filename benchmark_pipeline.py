#!/usr/bin/env python3
"""End-to-end RAG pipeline timing benchmark.

Measures the full LLM pipeline per crawler tool:
  Phase 1: Scrape + Markdown (uses existing benchmark_all_tools.py run data)
  Phase 2: Chunk (markdown → RAG chunks)
  Phase 3: Embed (chunks → vectors via OpenAI)
  Phase 4: Query (retrieval + LLM answer generation)

Produces PIPELINE_TIMING.md with per-tool, per-phase timing breakdowns.

    python benchmark_pipeline.py                          # latest run
    python benchmark_pipeline.py --run run_20260412_073832
    python benchmark_pipeline.py --sites quotes-toscrape,fastapi-docs

Requires:
    pip install openai numpy rank_bm25
    export OPENAI_API_KEY=sk-...
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

BENCH_DIR = Path(__file__).parent

# Auto-relaunch inside .venv if needed
_VENV_PYTHON = BENCH_DIR / ".venv" / ("bin" if sys.platform != "win32" else "Scripts") / ("python3" if sys.platform != "win32" else "python.exe")
if sys.prefix == sys.base_prefix and _VENV_PYTHON.exists():
    os.execv(str(_VENV_PYTHON), [str(_VENV_PYTHON)] + sys.argv)

try:
    from dotenv import load_dotenv
    load_dotenv(BENCH_DIR / ".env")
except ImportError:
    pass

from benchmark_retrieval import (  # noqa: E402
    CHUNK_MAX_WORDS,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    TEST_QUERIES,
    TOOLS as RETRIEVAL_TOOLS,
    _get_openai_client,
    cosine_similarity,
    embed_texts,
    find_latest_run,
    load_pages,
)
from markcrawl.chunker import chunk_markdown  # noqa: E402

logger = logging.getLogger(__name__)

ANSWER_MODEL = os.environ.get("ANSWER_MODEL", "gpt-4o-mini")
TOP_K_FOR_ANSWER = 10


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class PhaseTimings:
    """Timing data for one tool on one site."""
    tool: str
    site: str
    scrape_seconds: float = 0.0
    pages_scraped: int = 0
    chunk_seconds: float = 0.0
    chunks_created: int = 0
    embed_seconds: float = 0.0
    query_seconds: float = 0.0
    queries_run: int = 0
    total_seconds: float = 0.0


@dataclass
class PipelineResult:
    """All timings across tools and sites."""
    timings: List[PhaseTimings] = field(default_factory=list)
    run_id: str = ""
    sites: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Phase 1: Load scrape timing from existing run metadata
# ---------------------------------------------------------------------------

def load_scrape_timings(run_dir: Path, tools: List[str], sites: List[str]) -> Dict[str, Dict[str, dict]]:
    """Load scrape timings from run_metadata.json."""
    meta_path = run_dir / "run_metadata.json"
    timings = {}
    if not meta_path.exists():
        return timings
    with open(meta_path) as f:
        meta = json.load(f)

    # New format: phases.benchmarking.results.{tool}.{site}
    bench_results = meta.get("phases", {}).get("benchmarking", {}).get("results", {})
    if bench_results:
        for tool, site_data in bench_results.items():
            if tool not in tools:
                continue
            for site, result in site_data.items():
                if site not in sites:
                    continue
                timings.setdefault(tool, {})[site] = {
                    "seconds": result.get("time_median_s", 0),
                    "pages": int(result.get("pages_median", 0)),
                }
        return timings

    # Fallback: flat results list
    for result in meta.get("results", []):
        tool = result.get("tool", "")
        site = result.get("site", "")
        if tool in tools and site in sites:
            timings.setdefault(tool, {})[site] = {
                "seconds": result.get("time_median", result.get("time_seconds", 0)),
                "pages": int(result.get("pages_median", result.get("pages", 0))),
            }
    return timings


# ---------------------------------------------------------------------------
# Phase 2: Chunk
# ---------------------------------------------------------------------------

def chunk_tool_site(pages: List[Dict], max_words: int = CHUNK_MAX_WORDS,
                    overlap: int = CHUNK_OVERLAP) -> tuple[List[dict], float]:
    """Chunk all pages for a tool/site. Returns (chunks, elapsed_seconds)."""
    start = time.time()
    chunks = []
    for page in pages:
        text = page.get("text", "")
        url = page.get("url", "")
        if not text.strip():
            continue
        page_chunks = chunk_markdown(text, max_words=max_words, overlap_words=overlap)
        for c in page_chunks:
            chunks.append({
                "text": c.text,
                "url": url,
                "index": c.index,
            })
    elapsed = time.time() - start
    return chunks, elapsed


# ---------------------------------------------------------------------------
# Phase 3: Embed
# ---------------------------------------------------------------------------

def embed_chunks(client, chunks: List[dict]) -> tuple[list, float]:
    """Embed all chunks. Returns (vectors, elapsed_seconds)."""
    texts = [c["text"] for c in chunks]
    if not texts:
        return [], 0.0
    start = time.time()
    vectors = embed_texts(client, texts)
    elapsed = time.time() - start
    return vectors, elapsed


# ---------------------------------------------------------------------------
# Phase 4: Query (retrieval + LLM answer)
# ---------------------------------------------------------------------------

def query_pipeline(client, chunks: List[dict], vectors: list,
                   queries: List[Dict], model: str = ANSWER_MODEL) -> tuple[int, float]:
    """Run retrieval + LLM answer for each query. Returns (queries_run, elapsed_seconds)."""
    import numpy as np

    if not chunks or not vectors or not queries:
        return 0, 0.0

    vec_matrix = np.array(vectors)
    start = time.time()
    queries_run = 0

    for q in queries:
        query_text = q["query"]
        # Embed query
        query_vec = embed_texts(client, [query_text])[0]

        # Retrieve top-K chunks
        scores = cosine_similarity(query_vec, vec_matrix)
        top_indices = list(np.argsort(scores)[-TOP_K_FOR_ANSWER:][::-1])
        context = "\n\n---\n\n".join(chunks[i]["text"] for i in top_indices)

        # Generate answer
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": f"Answer using ONLY this context:\n\n{context}\n\nQuestion: {query_text}\n\nAnswer:",
                }],
                max_tokens=300,
                temperature=0,
                timeout=30,
            )
            queries_run += 1
        except Exception as exc:
            logger.warning(f"Query failed: {exc}")
            queries_run += 1  # Count it even if it failed

    elapsed = time.time() - start
    return queries_run, elapsed


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(result: PipelineResult) -> str:
    """Generate PIPELINE_TIMING.md report."""
    lines = []
    lines.append("# End-to-End RAG Pipeline Timing Benchmark")
    lines.append("<!-- style: v2, 2026-04-12 -->")
    lines.append("")
    lines.append("Measures how long each crawler takes across the full RAG pipeline:")
    lines.append("scraping, chunking, embedding, and querying.")
    lines.append("")
    lines.append(f"**Run:** `{result.run_id}` | **Sites:** {', '.join(result.sites)} | "
                 f"**Embedding model:** {EMBEDDING_MODEL} | **Answer model:** {ANSWER_MODEL}")
    lines.append("")

    # --- Per-tool aggregate summary ---
    lines.append("## Summary: Total Pipeline Time by Tool")
    lines.append("")
    lines.append("| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | **Total (s)** | Pages | Chunks |")
    lines.append("|------|-----------|----------|----------|----------|--------------|-------|--------|")

    # Aggregate per tool
    tool_agg: Dict[str, dict] = {}
    for t in result.timings:
        agg = tool_agg.setdefault(t.tool, {
            "scrape": 0, "chunk": 0, "embed": 0, "query": 0,
            "total": 0, "pages": 0, "chunks": 0,
        })
        agg["scrape"] += t.scrape_seconds
        agg["chunk"] += t.chunk_seconds
        agg["embed"] += t.embed_seconds
        agg["query"] += t.query_seconds
        agg["total"] += t.total_seconds
        agg["pages"] += t.pages_scraped
        agg["chunks"] += t.chunks_created

    # Sort by total time ascending (fastest first)
    sorted_tools = sorted(tool_agg.items(), key=lambda x: x[1]["total"])

    for tool, agg in sorted_tools:
        bold = "**" if tool == "markcrawl" else ""
        lines.append(
            f"| {bold}{tool}{bold} | {agg['scrape']:.1f} | {agg['chunk']:.1f} | "
            f"{agg['embed']:.1f} | {agg['query']:.1f} | "
            f"**{agg['total']:.1f}** | {agg['pages']} | {agg['chunks']} |"
        )

    lines.append("")

    # --- Phase breakdown as % of total ---
    lines.append("## Phase Breakdown (% of Total Pipeline Time)")
    lines.append("")
    lines.append("| Tool | Scrape % | Chunk % | Embed % | Query % |")
    lines.append("|------|---------|--------|--------|--------|")
    for tool, agg in sorted_tools:
        total = agg["total"] or 1
        lines.append(
            f"| {tool} | {agg['scrape']/total*100:.1f}% | {agg['chunk']/total*100:.1f}% | "
            f"{agg['embed']/total*100:.1f}% | {agg['query']/total*100:.1f}% |"
        )
    lines.append("")

    # --- Per-site detail ---
    lines.append("## Per-Site Breakdown")
    lines.append("")
    for site in result.sites:
        site_timings = [t for t in result.timings if t.site == site]
        if not site_timings:
            continue
        lines.append(f"### {site}")
        lines.append("")
        lines.append("| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks |")
        lines.append("|------|-----------|----------|----------|----------|----------|-------|--------|")
        for t in sorted(site_timings, key=lambda x: x.total_seconds):
            bold = "**" if t.tool == "markcrawl" else ""
            lines.append(
                f"| {bold}{t.tool}{bold} | {t.scrape_seconds:.1f} | {t.chunk_seconds:.1f} | "
                f"{t.embed_seconds:.1f} | {t.query_seconds:.1f} | "
                f"{t.total_seconds:.1f} | {t.pages_scraped} | {t.chunks_created} |"
            )
        lines.append("")

    # --- Key findings ---
    lines.append("## Key Findings")
    lines.append("")
    if sorted_tools:
        fastest_tool = sorted_tools[0][0]
        slowest_tool = sorted_tools[-1][0]
        lines.append(f"- **Fastest end-to-end:** {fastest_tool} "
                     f"({sorted_tools[0][1]['total']:.1f}s total)")
        lines.append(f"- **Slowest end-to-end:** {slowest_tool} "
                     f"({sorted_tools[-1][1]['total']:.1f}s total)")

        # Which phase dominates?
        for tool, agg in sorted_tools[:3]:
            total = agg["total"] or 1
            phases = [
                ("scraping", agg["scrape"]),
                ("chunking", agg["chunk"]),
                ("embedding", agg["embed"]),
                ("querying", agg["query"]),
            ]
            dominant = max(phases, key=lambda x: x[1])
            lines.append(f"- **{tool}:** {dominant[0]} dominates at "
                         f"{dominant[1]/total*100:.0f}% of pipeline time")

    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("- **Scrape timing** comes from `benchmark_all_tools.py` run metadata")
    lines.append("- **Chunk timing** uses markcrawl's `chunk_markdown()` with "
                 f"{CHUNK_MAX_WORDS}-word chunks and {CHUNK_OVERLAP}-word overlap")
    lines.append(f"- **Embed timing** uses OpenAI `{EMBEDDING_MODEL}` (cached after first run)")
    lines.append(f"- **Query timing** includes embedding the query, cosine retrieval, "
                 f"and `{ANSWER_MODEL}` answer generation")
    lines.append("- See [METHODOLOGY.md](METHODOLOGY.md) for full test setup")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="End-to-end RAG pipeline timing benchmark")
    parser.add_argument("--run", help="Run directory name (e.g. run_20260412_073832)")
    parser.add_argument("--sites", help="Comma-separated site names to include")
    parser.add_argument("--tools", help="Comma-separated tool names to include")
    parser.add_argument("--output", default="reports/PIPELINE_TIMING.md")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Find run directory
    runs_base = BENCH_DIR / "runs"
    if args.run:
        run_dir = runs_base / args.run
        if not run_dir.is_dir():
            logger.error(f"Run directory not found: {run_dir}")
            sys.exit(1)
    else:
        run_dir = find_latest_run(runs_base)
    if not run_dir:
        logger.error("No benchmark run found. Run benchmark_all_tools.py first.")
        sys.exit(1)
    run_id = run_dir.name
    logger.info(f"Using run: {run_id}")

    # Determine sites and tools from available data
    available_tools = set()
    available_sites = set()
    for tool_dir in run_dir.iterdir():
        if tool_dir.is_dir() and not tool_dir.name.startswith("_"):
            tool_name = tool_dir.name
            for site_dir in tool_dir.iterdir():
                if site_dir.is_dir() and (site_dir / "pages.jsonl").exists():
                    available_tools.add(tool_name)
                    available_sites.add(site_dir.name)

    tools = args.tools.split(",") if args.tools else sorted(available_tools)
    sites = args.sites.split(",") if args.sites else sorted(available_sites)

    # Filter to tools/sites with test queries
    query_sites = set(TEST_QUERIES.keys())
    sites_with_queries = [s for s in sites if s in query_sites]
    sites_without_queries = [s for s in sites if s not in query_sites]

    logger.info(f"Tools: {', '.join(tools)}")
    logger.info(f"Sites with queries: {', '.join(sites_with_queries)}")
    if sites_without_queries:
        logger.info(f"Sites without queries (scrape/chunk/embed only): {', '.join(sites_without_queries)}")

    # Load scrape timings
    scrape_timings = load_scrape_timings(run_dir, tools, sites)

    # Get OpenAI client (optional - embed/query phases require it)
    api_key = os.environ.get("OPENAI_API_KEY")
    client = None
    if api_key:
        client = _get_openai_client()
    else:
        logger.warning("OPENAI_API_KEY not set — skipping embed and query phases.")
        logger.warning("Set it in .env or environment to enable full pipeline timing.")

    result = PipelineResult(run_id=run_id, sites=sites, tools=tools)
    pipeline_start = time.time()

    for site in sites:
        logger.info(f"\n--- {site} ---")
        queries = TEST_QUERIES.get(site, [])

        for tool in tools:
            # Load pages
            jsonl_path = run_dir / tool / site / "pages.jsonl"
            if not jsonl_path.exists():
                logger.info(f"  {tool}: no pages.jsonl for {site}, skipping")
                continue
            pages = load_pages(str(jsonl_path))
            if not pages:
                logger.info(f"  {tool}: no pages, skipping")
                continue

            timing = PhaseTimings(tool=tool, site=site)

            # Phase 1: Scrape timing (from metadata)
            scrape_data = scrape_timings.get(tool, {}).get(site, {})
            timing.scrape_seconds = scrape_data.get("seconds", 0)
            timing.pages_scraped = scrape_data.get("pages", len(pages))

            # Phase 2: Chunk
            logger.info(f"  {tool}: chunking {len(pages)} pages...")
            chunks, chunk_time = chunk_tool_site(pages)
            timing.chunk_seconds = chunk_time
            timing.chunks_created = len(chunks)

            # Phase 3: Embed (requires OpenAI API key)
            vectors = []
            if client:
                logger.info(f"  {tool}: embedding {len(chunks)} chunks...")
                vectors, embed_time = embed_chunks(client, chunks)
                timing.embed_seconds = embed_time

            # Phase 4: Query (only for sites with test queries, requires API key)
            if queries and client and vectors:
                logger.info(f"  {tool}: running {len(queries)} queries...")
                queries_run, query_time = query_pipeline(client, chunks, vectors, queries)
                timing.query_seconds = query_time
                timing.queries_run = queries_run

            timing.total_seconds = (timing.scrape_seconds + timing.chunk_seconds +
                                    timing.embed_seconds + timing.query_seconds)

            logger.info(f"  {tool}: total={timing.total_seconds:.1f}s "
                        f"(scrape={timing.scrape_seconds:.1f} chunk={timing.chunk_seconds:.1f} "
                        f"embed={timing.embed_seconds:.1f} query={timing.query_seconds:.1f})")

            result.timings.append(timing)

    pipeline_elapsed = time.time() - pipeline_start
    logger.info(f"\nPipeline benchmark completed in {pipeline_elapsed:.1f}s")

    # Generate report
    report = generate_report(result)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report)
    logger.info(f"Report saved to: {output_path}")

    # Also save raw timings as JSON
    json_path = run_dir / "pipeline_timings.json"
    raw_data = {
        "run_id": run_id,
        "tools": tools,
        "sites": sites,
        "pipeline_wall_time_s": pipeline_elapsed,
        "timings": [
            {
                "tool": t.tool,
                "site": t.site,
                "scrape_s": t.scrape_seconds,
                "pages": t.pages_scraped,
                "chunk_s": t.chunk_seconds,
                "chunks": t.chunks_created,
                "embed_s": t.embed_seconds,
                "query_s": t.query_seconds,
                "queries": t.queries_run,
                "total_s": t.total_seconds,
            }
            for t in result.timings
        ],
    }
    with open(json_path, "w") as f:
        json.dump(raw_data, f, indent=2)
    logger.info(f"Raw timings saved to: {json_path}")


if __name__ == "__main__":
    main()
