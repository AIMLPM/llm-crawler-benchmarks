# Changelog

All notable changes to llm-crawler-benchmarks are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Retry logic with exponential backoff for all OpenAI API calls in
  `benchmark_pipeline.py` (`_llm_with_retry`) and
  `benchmark_answer_quality.py` (`_embed_with_retry`)
- Checkpoint/resume for `benchmark_pipeline.py` — interrupted runs resume
  from last completed tool/site combo. Pass `--fresh` to force a clean run.
- Batch query embedding in `benchmark_pipeline.py` — queries are embedded
  once per site and reused across all 7 tools, reducing query embedding API
  calls by ~86%

### Changed
- `query_pipeline()` accepts pre-embedded `query_vectors` parameter to avoid
  redundant per-query embedding calls

## [0.1.0] - 2026-04-12

### Added
- End-to-end RAG pipeline benchmark (`benchmark_pipeline.py`) measuring
  scrape, chunk, embed, and query phases per tool per site
- API cost tracking with token counts (tiktoken for embeddings,
  `response.usage` for queries) and OpenAI pricing
- Per-page normalized cost/time table to account for tools fetching different
  page counts
- Parallel embedding batches via `ThreadPoolExecutor` (env-configurable
  `EMBED_PARALLEL_BATCHES`)
- Content-hash embedding cache leveraged for fast re-runs
- `PIPELINE_TIMING.md` report with summary, per-site breakdowns, and cost
  breakdown tables
- README with badges, key findings summary table, tools compared, sites
  tested, and bottom-line takeaway

### Changed
- `benchmark_retrieval.py` embedding now supports parallel batches via
  `EMBED_PARALLEL_BATCHES` env var
- Tool runners refactored into `runners/` package

## [0.0.3] - 2026-04-09

### Fixed
- crawl4ai hang: replaced `arun_many()` with sequential `arun()` to prevent
  deadlocks
- crawl4ai memory pressure: switched to streaming mode with capped
  concurrency
- crawl4ai per-page stall: added 30-second page timeout
- Dockerfile permissions: `chown /app` to bench user for caches and results
- Firecrawl self-hosted: per-URL scraping, connection retries, OOM tuning

### Added
- Graduated smoke test: 3-tier tool validation (5/30/100 pages) before full
  benchmark runs
- Heartbeat logging: 30-second periodic status during tool execution
- `make check` and `make review` targets for self-assessment
- `IMPROVE.md` one-command LLM prompt for self-improvement reviews
- Self-hosted Firecrawl setup script

## [0.0.2] - 2026-04-09

### Changed
- Renamed project from `llm-crawler-bench` to `llm-crawler-benchmarks`
- Moved colly crawler binary into `tools/` directory
- Neutralized language: benchmark suite is tool-agnostic, not
  markcrawl-centric

### Fixed
- Dockerfile: non-editable install, browser permissions, copy tools/

## [0.0.1] - 2026-04-08

### Added
- Initial benchmark suite comparing 7 web crawlers across 8 sites
- `benchmark_all_tools.py` — speed benchmark with median/stddev across
  iterations
- `benchmark_quality.py` — extraction quality (content signal, preamble,
  repeat rate)
- `benchmark_retrieval.py` — retrieval quality (Hit@K, MRR across 4 modes)
- `benchmark_answer_quality.py` — LLM answer quality scored by GPT-4o judge
- `benchmark_markcrawl.py` — markcrawl standalone performance benchmark
- Reports: SPEED_COMPARISON, QUALITY_COMPARISON, RETRIEVAL_COMPARISON,
  ANSWER_QUALITY, COST_AT_SCALE, MARKCRAWL_RESULTS, METHODOLOGY
- Style guide (v2) and `lint_reports.py` for report consistency
- Self-improvement framework (`self_improvement/`) with 9-spec review process
- Docker support with `Dockerfile` and `.dockerignore`
- `preflight.py` tool availability checker

[Unreleased]: https://github.com/AIMLPM/llm-crawler-benchmarks/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AIMLPM/llm-crawler-benchmarks/compare/v0.0.3...v0.1.0
[0.0.3]: https://github.com/AIMLPM/llm-crawler-benchmarks/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/AIMLPM/llm-crawler-benchmarks/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/AIMLPM/llm-crawler-benchmarks/releases/tag/v0.0.1
