# llm-crawler-benchmarks

### Which web crawler is best for LLM/RAG pipelines? We tested 7 tools across 8 sites to find out.

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
| [Speed](reports/SPEED_COMPARISON.md) | markcrawl | 6.0 pages/sec | scrapy+md (5.3 p/s) |
| [Extraction quality](reports/QUALITY_COMPARISON.md) | markcrawl | 100% content signal, 0 words preamble | scrapy+md (99%, 88 words) |
| [Retrieval quality](reports/RETRIEVAL_COMPARISON.md) | crawlee | 95% Hit@10, 0.706 MRR | playwright (93%, 0.696) |
| [LLM answer quality](reports/ANSWER_QUALITY.md) | colly+md | 4.33/5 overall score | crawlee (4.24/5) |
| [Cost at scale](reports/COST_AT_SCALE.md) | markcrawl | $4,505/yr (100K pages, 1K q/day) | scrapy+md ($5,464/yr) |
| [Pipeline timing](reports/PIPELINE_TIMING.md) | markcrawl | 1191.0s end-to-end, $0.31 | scrapy+md (1465.4s, $3.92) |

## Leaderboard (Benchmark v2.0)

All 7 tools, sorted by speed. 8 sites, 109 retrieval queries, scored on 5 dimensions.

| Tool | Speed (p/s) | Content Signal | MRR | Answer (/5) | Cost (100K/yr) |
|------|-------------|----------------|-----|-------------|----------------|
| markcrawl | 6.0 | 100% | 0.594 | 3.97 | $4,505 |
| scrapy+md | 5.3 | 99% | 0.442 | 3.90 | $5,464 |
| colly+md | 3.1 | 67% | 0.617 | 4.33 | $7,213 |
| playwright | 2.1 | 69% | 0.696 | 3.88 | $7,320 |
| crawl4ai-raw | 1.3 | 83% | 0.633 | 4.19 | $6,961 |
| crawlee | 1.2 | 67% | 0.706 | 4.24 | $7,467 |
| crawl4ai | 1.2 | 82% | 0.658 | 4.16 | $6,960 |

> **Column definitions:** **Speed** = pages/sec (median of 3 runs). **Content Signal** = (total words - preamble) / total words (higher = cleaner). **MRR** = Mean Reciprocal Rank, best retrieval mode per tool. **Answer** = LLM answer quality scored 1-5 by gpt-4o-mini. **Cost** = annual RAG pipeline cost at 100K pages, 1K queries/day.

**Bottom line:** markcrawl v0.2.0 (async httpx) is the fastest crawler at 6.0 pages/sec -- 13% faster than the runner-up scrapy+md. It also wins on pipeline timing ($0.31 end-to-end) and extraction quality (100% content signal). Answer quality is tight across all tools (3.88-4.33/5), with colly+md narrowly leading. Retrieval quality barely differs between tools -- switching retrieval mode (e.g., to reranked) gains more than switching crawlers.

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
- **7 tools, not all crawlers.** We test the most common open-source
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
docker run --rm \
  -e OPENAI_API_KEY \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/runs:/app/runs \
  llm-crawler-benchmarks
```

## Benchmark version

**v2.0** -- 2026-04-25

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
chunk, embed, retrieve, and LLM answer -- across 7 tools, 8 sites, and 5
dimensions including downstream answer quality and cost at scale.

## Self-Improvement Framework

The `self_improvement/` directory contains a 9-spec review framework for
auditing benchmark quality. See [self_improvement/MASTER.md](self_improvement/MASTER.md).

## License

MIT
