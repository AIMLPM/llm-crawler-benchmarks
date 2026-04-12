# llm-crawler-benchmarks

### Which web crawler is best for LLM/RAG pipelines? We tested 7 tools across 8 sites to find out.

[![CI](https://github.com/AIMLPM/llm-crawler-benchmarks/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/AIMLPM/llm-crawler-benchmarks/actions/workflows/ci.yml)
![License](https://img.shields.io/github/license/AIMLPM/llm-crawler-benchmarks)

Head-to-head benchmark suite comparing web crawlers on speed, extraction
quality, retrieval quality, LLM answer quality, and cost at scale. Every
benchmark is reproducible from a single command.

## Key Findings

| Dimension | Winner | Key metric | Runner-up |
|-----------|--------|------------|-----------|
| [Speed](reports/SPEED_COMPARISON.md) | scrapy+md | 9.1 pages/sec | colly+md (5.8 p/s) |
| [Extraction quality](reports/QUALITY_COMPARISON.md) | **markcrawl** | 100% content signal, 4 words preamble | scrapy+md (97%, 23 words) |
| [Retrieval quality](reports/RETRIEVAL_COMPARISON.md) | crawlee | 85% Hit@5, 0.787 MRR | playwright (85%, 0.787) |
| [LLM answer quality](reports/ANSWER_QUALITY.md) | **markcrawl** | 3.91/5 overall score | scrapy+md (3.86/5) |
| [Cost at scale](reports/COST_AT_SCALE.md) | **markcrawl** | $4,505/yr (100K pages, 1K q/day) | scrapy+md ($5,464/yr) |
| [Pipeline timing](reports/PIPELINE_TIMING.md) | colly+md | 259.6s end-to-end | scrapy+md (268.0s) |

**Bottom line:** No single tool wins everything. scrapy+md and colly+md are
fastest, but markcrawl produces the cleanest output, the best LLM answers,
and the lowest cost at scale (21-66% savings on RAG infrastructure). Retrieval
quality barely differs between tools — switching retrieval mode (e.g., to
reranked) gains 15-20 points, while switching crawlers gains ~5.

## Tools Compared

| Tool | Type | JS rendering | Notes |
|------|------|-------------|-------|
| [markcrawl](https://github.com/AIMLPM/markcrawl) | Python | Optional | Markdown-first, lowest preamble |
| [scrapy](https://scrapy.org/)+md | Python | No | Fastest raw HTTP crawler |
| [crawl4ai](https://github.com/unclecode/crawl4ai) | Python | Built-in | AI-native, browser-based |
| crawl4ai-raw | Python | Built-in | crawl4ai with raw HTML output |
| [colly](https://github.com/gocolly/colly)+md | Go | No | Fast compiled crawler |
| [crawlee](https://github.com/apify/crawlee-python) | Python | Built-in | Apify's browser crawler |
| [playwright](https://playwright.dev/python/) | Python | Built-in | Microsoft's browser automation |

All tools output Markdown via the same html-to-markdown pipeline (except
crawl4ai-raw). See [METHODOLOGY.md](reports/METHODOLOGY.md) for tool
configurations and fairness decisions.

## Sites Tested

| Site | Pages | Type |
|------|-------|------|
| [quotes.toscrape.com](http://quotes.toscrape.com) | 15 | Simple paginated HTML |
| [books.toscrape.com](http://books.toscrape.com) | 60 | E-commerce catalog |
| [fastapi.tiangolo.com](https://fastapi.tiangolo.com) | 153 | API docs (code blocks, tutorials) |
| [docs.python.org](https://docs.python.org/3/library/) | 500 | Standard library reference |
| [react.dev](https://react.dev/learn) | 500 | SPA, JS-rendered |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Python_(programming_language)) | 50 | Tables, infoboxes, citations |
| [docs.stripe.com](https://docs.stripe.com/payments) | 500 | Tabbed content, code samples |
| [github.blog](https://github.blog/engineering/) | 200 | Blog articles, images |

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

## Quick Start

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
```

## Docker

```bash
docker build -t llm-crawler-benchmarks .
docker run --rm \
  -e OPENAI_API_KEY \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/runs:/app/runs \
  llm-crawler-benchmarks
```

## Related Work

Other projects benchmark parts of the web scraping pipeline:

- **[Firecrawl scrape-evals](https://www.firecrawl.dev/blog/introducing-scrape-evals)** —
  1,000-URL extraction quality benchmark (precision/recall). Single-page quality
  only; no speed, retrieval, or LLM answer evaluation.
- **[WCXB](https://webcontentextraction.org/)** — 2,008-page content extraction
  leaderboard with word-level F1. Covers traditional tools (trafilatura,
  readability) but not LLM-era crawlers.
- **[Spider.cloud benchmark](https://spider.cloud/blog/firecrawl-vs-crawl4ai-vs-spider-honest-benchmark)** —
  3-tool comparison (Firecrawl, Crawl4AI, Spider) on throughput, cost, and RAG
  retrieval accuracy.

This project differs by evaluating the **full RAG pipeline** — from crawl through
chunk, embed, retrieve, and LLM answer — across 7 tools, 8 sites, and 5
dimensions including downstream answer quality and cost at scale.

## Self-Improvement Framework

The `self_improvement/` directory contains a 9-spec review framework for
auditing benchmark quality. See [self_improvement/MASTER.md](self_improvement/MASTER.md).

## License

MIT
