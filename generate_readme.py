#!/usr/bin/env python3
"""Generate README.md for llm-crawler-benchmarks from report data.

Parses all benchmark reports and produces a data-driven README with
a leaderboard, methodology summary, and reproducibility instructions.
Keeps the README consistent across benchmark runs.

Usage:
    python generate_readme.py              # writes README.md
    python generate_readme.py --dry-run    # prints to stdout
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = SCRIPT_DIR / "reports"

sys.path.insert(0, str(SCRIPT_DIR / "self_improvement"))
from sync_markcrawl import (
    _get_col,
    _parse_table,
    parse_answer_quality,
    parse_costs,
    parse_quality,
    parse_retrieval,
    parse_speed,
)

BENCHMARK_VERSION = "2.0"


# ---------------------------------------------------------------------------
# Extra parsers (not in sync_markcrawl)
# ---------------------------------------------------------------------------

def _parse_content_signal(text: str) -> dict[str, int]:
    """Parse content signal % from QUALITY_COMPARISON.md summary."""
    result = {}
    for row in _parse_table(text, "Content signal"):
        tool = row.get("Tool", "").strip("*").strip()
        cs = _get_col(row, "Content signal").replace("%", "").strip()
        try:
            if cs and cs != "\u2014":
                result[tool] = int(cs)
        except ValueError:
            pass
    return result


def _parse_best_mrr(text: str) -> dict[str, dict]:
    """Parse best retrieval mode per tool from RETRIEVAL_COMPARISON.md."""
    result = {}
    for row in _parse_table(text, "Best mode"):
        tool = row.get("Tool", "").strip("*").strip()
        if not tool:
            continue
        mrr_str = row.get("MRR", "").strip()
        hit10_str = row.get("Hit@10", "").strip()
        try:
            mrr = float(mrr_str)
        except ValueError:
            continue
        m = re.match(r"(\d+)%", hit10_str)
        hit10 = int(m.group(1)) if m else None
        result[tool] = {"mrr": mrr, "hit10": hit10}
    return result


def _parse_pipeline(text: str) -> dict[str, dict]:
    """Parse pipeline timing summary from PIPELINE_TIMING.md."""
    result = {}
    for row in _parse_table(text, "Total (s)"):
        tool = row.get("Tool", "").strip("*").strip()
        if not tool:
            continue
        total_str = _get_col(row, "Total").strip("*").strip().replace(",", "")
        cost_str = _get_col(row, "Cost").strip("*").strip().replace("$", "").replace(",", "")
        try:
            result[tool] = {"total": float(total_str), "cost": float(cost_str)}
        except ValueError:
            pass
    return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_report(name: str) -> str:
    path = REPORTS_DIR / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _bold(text: str) -> str:
    return f"**{text}**"


def _bold_if_mc(text: str, tool: str) -> str:
    return _bold(text) if tool == "markcrawl" else text


def _winner(data: dict, higher_is_better: bool = True):
    """Return (tool, value) of the best entry."""
    if not data:
        return None, None
    fn = max if higher_is_better else min
    return fn(data.items(), key=lambda x: x[1])


def _runner_up(data: dict, higher_is_better: bool = True):
    """Return (tool, value) of the second-best entry."""
    if len(data) < 2:
        return None, None
    items = sorted(data.items(), key=lambda x: x[1], reverse=higher_is_better)
    return items[1]


# ---------------------------------------------------------------------------
# README generation
# ---------------------------------------------------------------------------

def generate_readme() -> str:
    # --- Load all report data ---
    quality_text = _read_report("QUALITY_COMPARISON.md")
    retrieval_text = _read_report("RETRIEVAL_COMPARISON.md")
    pipeline_text = _read_report("PIPELINE_TIMING.md")

    speed = parse_speed(_read_report("SPEED_COMPARISON.md"))
    quality = parse_quality(quality_text)
    content_signal = _parse_content_signal(quality_text)
    retrieval = parse_retrieval(retrieval_text)
    best_mrr = _parse_best_mrr(retrieval_text)
    answer = parse_answer_quality(_read_report("ANSWER_QUALITY.md"))
    costs = parse_costs(_read_report("COST_AT_SCALE.md"))
    pipeline = _parse_pipeline(pipeline_text)

    preamble_data = {
        t: v["preamble"]
        for t, v in quality.items()
        if v.get("preamble") is not None
    }
    cost_mid = {
        t: v["mid"]
        for t, v in costs.items()
        if v.get("mid") is not None
    }
    pipeline_time = {t: v["total"] for t, v in pipeline.items()}
    mrr_flat = {t: v["mrr"] for t, v in best_mrr.items() if v.get("mrr")}

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    num_sites = 8
    num_queries = 109  # from retrieval report header

    # --- Key Findings table ---
    rows = []

    # Speed
    sw, sv = _winner(speed, True)
    sr, srv = _runner_up(speed, True)
    rows.append(
        f"| [Speed](reports/SPEED_COMPARISON.md) | {_bold_if_mc(sw, sw)} "
        f"| {sv:.1f} pages/sec | {sr} ({srv:.1f} p/s) |"
    )

    # Extraction quality
    cw, cv = _winner(content_signal, True)
    cr, crv = _runner_up(content_signal, True)
    cw_preamble = preamble_data.get(cw)
    cr_preamble = preamble_data.get(cr)
    cs_metric = f"{cv}% content signal"
    if cw_preamble is not None:
        cs_metric += f", {cw_preamble} words preamble"
    cr_str = f"{cr} ({crv}%"
    if cr_preamble is not None:
        cr_str += f", {cr_preamble} words"
    cr_str += ")"
    rows.append(
        f"| [Extraction quality](reports/QUALITY_COMPARISON.md) | {_bold_if_mc(cw, cw)} "
        f"| {cs_metric} | {cr_str} |"
    )

    # Retrieval
    rw, rv = _winner(mrr_flat, True)
    rr, rrv = _runner_up(mrr_flat, True)
    rw_hit = best_mrr.get(rw, {}).get("hit10")
    rr_hit = best_mrr.get(rr, {}).get("hit10")
    ret_metric = f"{rw_hit}% Hit@10, {rv:.3f} MRR" if rw_hit else f"{rv:.3f} MRR"
    ret_ru = f"{rr} ({rr_hit}%, {rrv:.3f})" if rr_hit else f"{rr} ({rrv:.3f})"
    rows.append(
        f"| [Retrieval quality](reports/RETRIEVAL_COMPARISON.md) | {_bold_if_mc(rw, rw)} "
        f"| {ret_metric} | {ret_ru} |"
    )

    # Answer quality
    aw, av = _winner(answer, True)
    ar, arv = _runner_up(answer, True)
    rows.append(
        f"| [LLM answer quality](reports/ANSWER_QUALITY.md) | {_bold_if_mc(aw, aw)} "
        f"| {av:.2f}/5 overall score | {ar} ({arv:.2f}/5) |"
    )

    # Cost
    kw, kv = _winner(cost_mid, False)
    kr, krv = _runner_up(cost_mid, False)
    rows.append(
        f"| [Cost at scale](reports/COST_AT_SCALE.md) | {_bold_if_mc(kw, kw)} "
        f"| ${kv:,}/yr (100K pages, 1K q/day) | {kr} (${krv:,}/yr) |"
    )

    # Pipeline timing
    pw, pv = _winner(pipeline_time, False)
    pr, prv = _runner_up(pipeline_time, False)
    pw_cost = pipeline.get(pw, {}).get("cost")
    pr_cost = pipeline.get(pr, {}).get("cost")
    pipe_metric = f"{pv:.1f}s end-to-end"
    if pw_cost is not None:
        pipe_metric += f", ${pw_cost:.2f}"
    pipe_ru = f"{pr} ({prv:.1f}s"
    if pr_cost is not None:
        pipe_ru += f", ${pr_cost:.2f}"
    pipe_ru += ")"
    rows.append(
        f"| [Pipeline timing](reports/PIPELINE_TIMING.md) | {_bold_if_mc(pw, pw)} "
        f"| {pipe_metric} | {pipe_ru} |"
    )

    key_findings = "\n".join(rows)

    # --- Full leaderboard ---
    all_tools = sorted(
        {t for t in speed if t in answer},
        key=lambda t: speed.get(t, 0),
        reverse=True,
    )

    lb_rows = []
    for tool in all_tools:
        s = speed.get(tool)
        cs = content_signal.get(tool)
        mrr = mrr_flat.get(tool)
        aq = answer.get(tool)
        cost = cost_mid.get(tool)

        s_str = f"{s:.1f}" if s else "\u2014"
        cs_str = f"{cs}%" if cs is not None else "\u2014"
        mrr_str = f"{mrr:.3f}" if mrr else "\u2014"
        aq_str = f"{aq:.2f}" if aq else "\u2014"
        cost_str = f"${cost:,}" if cost else "\u2014"

        lb_rows.append(
            f"| {_bold_if_mc(tool, tool)} "
            f"| {_bold_if_mc(s_str, tool)} "
            f"| {_bold_if_mc(cs_str, tool)} "
            f"| {_bold_if_mc(mrr_str, tool)} "
            f"| {_bold_if_mc(aq_str, tool)} "
            f"| {_bold_if_mc(cost_str, tool)} |"
        )

    leaderboard = "\n".join(lb_rows)

    # --- Bottom line narrative ---
    aq_vals = sorted(answer.values())
    aq_min, aq_max = aq_vals[0], aq_vals[-1]
    aq_gap = (aq_max - aq_min) / aq_max * 100

    bottom_parts = []

    # Speed claim
    if sw == "markcrawl" and srv:
        pct = (sv - srv) / srv * 100
        first = (
            f"markcrawl v0.2.0 (async httpx) is the fastest crawler at "
            f"{sv:.1f} pages/sec -- {pct:.0f}% faster than the runner-up {sr}"
        )
    else:
        mc_spd = speed.get("markcrawl", 0)
        first = (
            f"{sw} is the fastest at {sv:.1f} pages/sec; "
            f"markcrawl is at {mc_spd:.1f}"
        )

    # Combine other markcrawl wins into one sentence
    also_wins = []
    if pw == "markcrawl" and pw_cost is not None:
        also_wins.append(f"pipeline timing (${pw_cost:.2f} end-to-end)")
    if cw == "markcrawl":
        also_wins.append(f"extraction quality ({cv}% content signal)")
    if also_wins:
        first += ". It also wins on " + " and ".join(also_wins)
    bottom_parts.append(first)

    # Answer quality
    bottom_parts.append(
        f"Answer quality is tight across all tools "
        f"({aq_min:.2f}-{aq_max:.2f}/5), with {aw} narrowly leading"
    )

    # Retrieval
    bottom_parts.append(
        "Retrieval quality barely differs between tools -- switching "
        "retrieval mode (e.g., to reranked) gains more than switching crawlers"
    )

    bottom_line = ". ".join(bottom_parts) + "."

    # --- Tool info (static, matches current README) ---
    tools_table = """| Tool | Type | JS rendering | Notes |
|------|------|-------------|-------|
| [markcrawl](https://github.com/AIMLPM/markcrawl) | Python | Optional | Markdown-first, lowest preamble |
| [scrapy](https://scrapy.org/)+md | Python | No | Fastest raw HTTP crawler |
| [crawl4ai](https://github.com/unclecode/crawl4ai) | Python | Built-in | AI-native, browser-based |
| crawl4ai-raw | Python | Built-in | crawl4ai with raw HTML output |
| [colly](https://github.com/gocolly/colly)+md | Go | No | Fast compiled crawler |
| [crawlee](https://github.com/apify/crawlee-python) | Python | Built-in | Apify's browser crawler |
| [playwright](https://playwright.dev/python/) | Python | Built-in | Microsoft's browser automation |"""

    # --- Sites table (static) ---
    sites_table = """| Site | Pages | Type |
|------|-------|------|
| [quotes.toscrape.com](http://quotes.toscrape.com) | 15 | Simple paginated HTML |
| [books.toscrape.com](http://books.toscrape.com) | 60 | E-commerce catalog |
| [fastapi.tiangolo.com](https://fastapi.tiangolo.com) | 153 | API docs (code blocks, tutorials) |
| [docs.python.org](https://docs.python.org/3/library/) | 500 | Standard library reference |
| [react.dev](https://react.dev/learn) | 500 | SPA, JS-rendered |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Python_(programming_language)) | 50 | Tables, infoboxes, citations |
| [docs.stripe.com](https://docs.stripe.com/payments) | 500 | Tabbed content, code samples |
| [github.blog](https://github.blog/engineering/) | 200 | Blog articles, images |"""

    num_tools = len(all_tools)

    return f"""# llm-crawler-benchmarks

### Which web crawler is best for LLM/RAG pipelines? We tested {num_tools} tools across {num_sites} sites to find out.

[![CI](https://github.com/AIMLPM/llm-crawler-benchmarks/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/AIMLPM/llm-crawler-benchmarks/actions/workflows/ci.yml)
![License](https://img.shields.io/github/license/AIMLPM/llm-crawler-benchmarks)

Head-to-head benchmark suite comparing web crawlers on speed, extraction
quality, retrieval quality, LLM answer quality, and cost at scale. Every
benchmark is reproducible from a single command.

## Why this exists

Most crawler benchmarks test one dimension (speed or extraction accuracy) in
isolation. But in an LLM/RAG pipeline, the crawler is stage 1 -- everything
downstream (chunking, embedding, retrieval, LLM generation) depends on what
the crawler produces. A tool that is fast but outputs noisy Markdown will
inflate your embedding costs and degrade retrieval quality.

This project measures the **full pipeline**: crawl, chunk, embed, retrieve,
and generate an LLM answer -- then scores each stage independently so you can
see where the differences actually matter.

## Key Findings

| Dimension | Winner | Key metric | Runner-up |
|-----------|--------|------------|-----------|
{key_findings}

## Leaderboard (Benchmark v{BENCHMARK_VERSION})

All {num_tools} tools, sorted by speed. {num_sites} sites, {num_queries} retrieval queries, scored on 5 dimensions.

| Tool | Speed (p/s) | Content Signal | MRR | Answer (/5) | Cost (100K/yr) |
|------|-------------|----------------|-----|-------------|----------------|
{leaderboard}

> **Column definitions:** **Speed** = pages/sec (median of 3 runs). **Content Signal** = (total words - preamble) / total words (higher = cleaner). **MRR** = Mean Reciprocal Rank, best retrieval mode per tool. **Answer** = LLM answer quality scored 1-5 by gpt-4o-mini. **Cost** = annual RAG pipeline cost at 100K pages, 1K queries/day.

**Bottom line:** {bottom_line}

## Tools Compared

{tools_table}

All tools output Markdown via the same html-to-markdown pipeline (except
crawl4ai-raw). See [METHODOLOGY.md](reports/METHODOLOGY.md) for tool
configurations and fairness decisions.

## Sites Tested

{sites_table}

## Reports

| Report | Question it answers |
|--------|---------------------|
| [Speed Comparison](reports/SPEED_COMPARISON.md) | Which crawler is fastest? |
| [Quality Comparison](reports/QUALITY_COMPARISON.md) | Which produces the cleanest Markdown? |
| [Retrieval Comparison](reports/RETRIEVAL_COMPARISON.md) | Does cleaner Markdown improve retrieval? |
| [Answer Quality](reports/ANSWER_QUALITY.md) | Does better retrieval improve LLM answers? |
| [Cost at Scale](reports/COST_AT_SCALE.md) | What does each crawler cost at 100K+ pages? |
| [Pipeline Timing](reports/PIPELINE_TIMING.md) | How long does the full RAG pipeline take? |
| [MarkCrawl Self-Benchmark](reports/MARKCRAWL_RESULTS.md) | MarkCrawl standalone performance |
| [Methodology](reports/METHODOLOGY.md) | How were these benchmarks run? |

## Transparency

This benchmark is maintained by the creators of
[markcrawl](https://github.com/AIMLPM/markcrawl), one of the tools tested.
We designed the [methodology](reports/METHODOLOGY.md) to be fair (identical
seed URLs, randomized execution order, published scripts), but readers should
be aware of this relationship. All code and data are published so results can
be independently verified. If you rerun and get different results,
[open an issue](https://github.com/AIMLPM/llm-crawler-benchmarks/issues).

## Limitations

- **Single machine, single location.** All benchmarks run on one machine in one
  geographic location. Network latency to each site varies by location, so
  absolute pages/sec numbers will differ on your hardware.
- **Live sites introduce variance.** These are real public websites, not frozen
  snapshots. Server load, CDN caching, and content changes cause run-to-run
  variance. We report medians across 3 iterations to reduce noise.
- **Markdown output only.** We evaluate Markdown extraction quality. Tools that
  excel at structured data extraction (JSON, tables) may rank differently on
  those tasks.
- **{num_tools} tools, not all crawlers.** We test the most common open-source
  crawlers used in RAG pipelines. Tools like Apify, ScrapingBee, and others
  are not included. See "Including a tool" below to add one.
- **LLM-judged quality.** Answer quality is scored by gpt-4o-mini, not human
  reviewers. LLM judges have known biases (verbosity preference, position
  effects). We mitigate with 4-dimension scoring but the scores are not
  ground truth.
- **No anti-bot, authentication, or JS-heavy SPA testing.** All test sites are
  publicly accessible and crawler-friendly. Results do not apply to sites with
  bot detection, rate limiting, or login walls.

## Including a tool

We welcome contributions. To add a crawler to the benchmark:

1. **Open an issue** describing the tool, its license, and what makes it
   relevant for LLM/RAG pipelines.
2. **Submit a PR** with a runner script in `runners/` that matches the
   interface of existing runners (accepts a URL list, outputs Markdown +
   JSONL index). See `runners/README.md` for the spec.
3. The tool must be **open-source** with a published package (pip, npm, go
   module, etc.).
4. We run all benchmarks on the same hardware with the same sites and queries.
   You don't need to provide benchmark results -- just the runner.

## Reproducing these results

```bash
# Install dependencies
pip install -e ".[dev]"

# Preflight check (verifies all tools are installed)
python preflight.py

# Run all benchmarks (~3-5 hours)
python benchmark_all_tools.py

# Run individual benchmarks
python benchmark_quality.py
python benchmark_retrieval.py
python benchmark_answer_quality.py
python benchmark_pipeline.py
python benchmark_markcrawl.py

# Regenerate this README from report data
python generate_readme.py
```

## Docker

```bash
docker build -t llm-crawler-benchmarks .
docker run --rm \\
  -e OPENAI_API_KEY \\
  -v $(pwd)/reports:/app/reports \\
  -v $(pwd)/runs:/app/runs \\
  llm-crawler-benchmarks
```

## Benchmark version

**v{BENCHMARK_VERSION}** -- {date}

When benchmark methodology changes (new sites, different scoring, updated
tool versions), we increment the version. Results from different versions
are not directly comparable. See [METHODOLOGY.md](reports/METHODOLOGY.md)
for the full test setup.

## Related Work

Other projects benchmark parts of the web scraping pipeline:

- **[Firecrawl scrape-evals](https://www.firecrawl.dev/blog/introducing-scrape-evals)** --
  1,000-URL extraction quality benchmark (precision/recall). Single-page quality
  only; no speed, retrieval, or LLM answer evaluation.
- **[WCXB](https://webcontentextraction.org/)** -- 2,008-page content extraction
  leaderboard with word-level F1. Covers traditional tools (trafilatura,
  readability) but not LLM-era crawlers.
- **[Spider.cloud benchmark](https://spider.cloud/blog/firecrawl-vs-crawl4ai-vs-spider-honest-benchmark)** --
  3-tool comparison (Firecrawl, Crawl4AI, Spider) on throughput, cost, and RAG
  retrieval accuracy.

This project differs by evaluating the **full RAG pipeline** -- from crawl through
chunk, embed, retrieve, and LLM answer -- across {num_tools} tools, {num_sites} sites, and 5
dimensions including downstream answer quality and cost at scale.

## Self-Improvement Framework

The `self_improvement/` directory contains a 9-spec review framework for
auditing benchmark quality. See [self_improvement/MASTER.md](self_improvement/MASTER.md).

## License

MIT
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate README.md from benchmark report data"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print to stdout without writing README.md",
    )
    args = parser.parse_args()

    readme = generate_readme()

    if args.dry_run:
        print(readme)
        return 0

    out = SCRIPT_DIR / "README.md"
    out.write_text(readme, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
