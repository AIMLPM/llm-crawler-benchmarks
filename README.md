# llm-crawler-bench

Head-to-head benchmark suite for web crawlers used in LLM/RAG pipelines.

Compares 7 tools — [markcrawl](https://github.com/AIMLPM/markcrawl),
scrapy+md, crawl4ai, crawl4ai-raw, colly+md, crawlee, playwright — across
8 real-world sites on five dimensions:

- **Speed** — pages/second, total crawl time
- **Extraction quality** — content signal %, preamble, repeat rate
- **Retrieval quality** — Hit@K, MRR across 92 queries
- **LLM answer quality** — GPT-4o scoring on correctness, relevance, completeness, usefulness
- **Cost at scale** — embedding, storage, and query costs at 10K-1M pages

## Reports

| Report | Question |
|--------|----------|
| [Speed](reports/SPEED_COMPARISON.md) | Which crawler is fastest? |
| [Quality](reports/QUALITY_COMPARISON.md) | Which produces the cleanest Markdown? |
| [Retrieval](reports/RETRIEVAL_COMPARISON.md) | Does cleaner Markdown improve retrieval? |
| [Answer Quality](reports/ANSWER_QUALITY.md) | Does better retrieval improve LLM answers? |
| [Cost at Scale](reports/COST_AT_SCALE.md) | What does each crawler cost at 100K+ pages? |
| [MarkCrawl Self-Benchmark](reports/MARKCRAWL_RESULTS.md) | MarkCrawl standalone performance |
| [Methodology](reports/METHODOLOGY.md) | How were these benchmarks run? |

## Quick start

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
python benchmark_markcrawl.py
```

## Docker

```bash
docker build -t llm-crawler-bench .
docker run --rm \
  -e OPENAI_API_KEY \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/runs:/app/runs \
  llm-crawler-bench
```

## Self-improvement framework

The `self_improvement/` directory contains a 9-spec review framework for
auditing benchmark quality. See [self_improvement/MASTER.md](self_improvement/MASTER.md).

## License

MIT
