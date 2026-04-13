# End-to-End RAG Pipeline Timing Benchmark
<!-- style: v2, 2026-04-12 -->

Measures how long each crawler takes across the full RAG pipeline:
scraping, chunking, embedding, and querying.

**Run:** `run_20260412_195003` | **Sites:** blog-engineering, books-toscrape, fastapi-docs, python-docs, quotes-toscrape, react-dev, stripe-docs, wikipedia-python | **Embedding model:** text-embedding-3-small | **Answer model:** gpt-4o-mini

## Summary: Total Pipeline Time by Tool

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | **Total (s)** | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|--------------|-------|--------|------|
| **markcrawl** | 103.9 | 1.2 | 5.1 | 366.4 | **476.5** | 1456 | 22132 | $0.222 |
| scrapy+md | 138.8 | 1.1 | 6.1 | 369.3 | **515.3** | 1284 | 23854 | $0.237 |
| colly+md | 209.3 | 3.8 | 10.7 | 368.4 | **592.3** | 1376 | 42934 | $1.22 |
| playwright | 692.8 | 3.6 | 12.8 | 289.5 | **998.7** | 1448 | 46439 | $1.33 |
| crawl4ai | 716.4 | 1.1 | 8.4 | 373.5 | **1099.5** | 1456 | 32735 | $0.366 |
| crawlee | 806.2 | 4.4 | 13.0 | 342.5 | **1166.1** | 1456 | 47560 | $1.41 |
| crawl4ai-raw | 1027.5 | 1.8 | 8.1 | 332.6 | **1370.0** | 1456 | 32735 | $0.366 |

> **Column definitions:** **Scrape/Chunk/Embed/Query (s)** = wall-clock seconds for each pipeline phase (summed across all sites). **Total (s)** = sum of all phases. **Pages** = total pages fetched. **Chunks** = total text chunks produced. **Cost** = total API cost (embedding + LLM query).

*(Cost uses OpenAI `text-embedding-3-small` at $0.02/1M tokens, `gpt-4o-mini` at $0.15/$0.6 per 1M input/output tokens)*

## Per-Page Pipeline Cost (normalized)

Since scrapy+md fetched fewer pages (due to timeouts), this table normalizes
time and cost per page for a fairer comparison.

| Tool | Pages | Total (s) | s/page | Cost/page | Chunks/page |
|------|-------|----------|--------|-----------|-------------|
| **markcrawl** | 1456 | 476.5 | 0.33 | $0.0002 | 15.2 |
| scrapy+md | 1284 | 515.3 | 0.40 | $0.0002 | 18.6 |
| colly+md | 1376 | 592.3 | 0.43 | $0.0009 | 31.2 |
| playwright | 1448 | 998.7 | 0.69 | $0.0009 | 32.1 |
| crawl4ai | 1456 | 1099.5 | 0.76 | $0.0003 | 22.5 |
| crawlee | 1456 | 1166.1 | 0.80 | $0.0010 | 32.7 |
| crawl4ai-raw | 1456 | 1370.0 | 0.94 | $0.0003 | 22.5 |

> **Column definitions:** **s/page** = Total (s) ÷ Pages. **Cost/page** = total API cost ÷ Pages. **Chunks/page** = Chunks ÷ Pages. All values are per-page averages.

## Phase Breakdown (% of Total Pipeline Time)

| Tool | Scrape % | Chunk % | Embed % | Query % |
|------|---------|--------|--------|--------|
| markcrawl | 21.8% | 0.2% | 1.1% | 76.9% |
| scrapy+md | 26.9% | 0.2% | 1.2% | 71.7% |
| colly+md | 35.3% | 0.6% | 1.8% | 62.2% |
| playwright | 69.4% | 0.4% | 1.3% | 29.0% |
| crawl4ai | 65.2% | 0.1% | 0.8% | 34.0% |
| crawlee | 69.1% | 0.4% | 1.1% | 29.4% |
| crawl4ai-raw | 75.0% | 0.1% | 0.6% | 24.3% |

> Each percentage = phase time ÷ total pipeline time. Shows which phase dominates.

## API Cost Breakdown

*(Pricing: `text-embedding-3-small` at $0.02/1M tokens, `gpt-4o-mini` input at $0.15/1M, output at $0.6/1M)*

| Tool | Embed tokens | Embed cost | Query in tokens | Query out tokens | Query cost | **Total cost** |
|------|-------------|-----------|----------------|-----------------|-----------|---------------|
| **markcrawl** | 8,004,177 | $0.160 | 356,550 | 14,636 | $0.062 | **$0.222** |
| scrapy+md | 8,231,949 | $0.165 | 418,797 | 15,091 | $0.072 | **$0.237** |
| colly+md | 57,384,047 | $1.15 | 444,930 | 14,746 | $0.076 | **$1.22** |
| playwright | 62,853,049 | $1.26 | 441,118 | 14,591 | $0.075 | **$1.33** |
| crawl4ai | 14,113,383 | $0.282 | 502,137 | 13,658 | $0.084 | **$0.366** |
| crawlee | 66,893,569 | $1.34 | 441,799 | 14,750 | $0.075 | **$1.41** |
| crawl4ai-raw | 14,109,525 | $0.282 | 502,761 | 13,769 | $0.084 | **$0.366** |

> **Embed tokens** = tokens sent to the embedding API (all chunks). **Query in/out tokens** = tokens sent to and received from the answer LLM. **Total cost** = Embed cost + Query cost.

## Per-Site Breakdown

Per-site tables use the same columns as the summary table above. See [summary legend](#summary-total-pipeline-time-by-tool) for column definitions.

### blog-engineering

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| scrapy+md | 6.7 | 0.0 | 0.3 | 24.6 | 31.6 | 200 | 1636 | $0.0085 |
| **markcrawl** | 11.7 | 0.0 | 0.5 | 21.1 | 33.4 | 200 | 1791 | $0.0084 |
| colly+md | 28.9 | 0.2 | 0.6 | 29.1 | 58.8 | 123 | 3286 | $0.048 |
| playwright | 40.2 | 0.3 | 1.4 | 20.3 | 62.3 | 200 | 5969 | $0.097 |
| crawl4ai | 58.9 | 0.1 | 1.5 | 26.5 | 87.0 | 200 | 5315 | $0.030 |
| crawlee | 73.4 | 0.4 | 1.4 | 23.7 | 98.8 | 200 | 5963 | $0.096 |
| crawl4ai-raw | 87.0 | 0.1 | 1.2 | 21.1 | 109.4 | 200 | 5315 | $0.030 |

### books-toscrape

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| crawl4ai | 11.4 | 0.0 | 0.1 | 45.3 | 56.9 | 60 | 628 | $0.021 |
| **markcrawl** | 4.2 | 0.0 | 0.0 | 64.1 | 68.4 | 60 | 139 | $0.014 |
| crawl4ai-raw | 27.7 | 0.0 | 0.1 | 44.1 | 71.9 | 60 | 628 | $0.021 |
| crawlee | 16.6 | 0.0 | 0.0 | 59.8 | 76.4 | 60 | 134 | $0.018 |
| playwright | 35.1 | 0.0 | 0.0 | 42.7 | 77.8 | 60 | 134 | $0.018 |
| scrapy+md | 4.9 | 0.0 | 0.0 | 79.1 | 84.0 | 60 | 130 | $0.018 |
| colly+md | 6.5 | 0.0 | 0.0 | 81.5 | 88.0 | 60 | 134 | $0.018 |

### fastapi-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| **markcrawl** | 11.4 | 0.1 | 0.7 | 66.0 | 78.1 | 153 | 3413 | $0.022 |
| scrapy+md | 29.6 | 0.1 | 0.8 | 59.0 | 89.4 | 153 | 3741 | $0.031 |
| colly+md | 27.1 | 0.2 | 0.8 | 64.1 | 92.2 | 153 | 3871 | $0.036 |
| playwright | 86.3 | 0.3 | 0.9 | 60.5 | 147.9 | 153 | 3857 | $0.042 |
| crawl4ai | 90.4 | 0.2 | 1.1 | 69.0 | 160.7 | 153 | 4143 | $0.044 |
| crawlee | 128.1 | 0.2 | 0.9 | 65.6 | 194.8 | 153 | 3856 | $0.042 |
| crawl4ai-raw | 139.8 | 0.1 | 1.0 | 60.3 | 201.2 | 153 | 4144 | $0.044 |

### python-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| **markcrawl** | 22.1 | 0.9 | 2.4 | 53.3 | 78.7 | 500 | 9479 | $0.115 |
| colly+md | 43.5 | 0.6 | 3.2 | 39.7 | 87.0 | 500 | 13221 | $0.122 |
| scrapy+md | 37.6 | 0.7 | 3.3 | 50.7 | 92.3 | 328 | 10421 | $0.094 |
| crawlee | 74.4 | 1.1 | 3.9 | 39.2 | 118.6 | 500 | 13304 | $0.125 |
| playwright | 121.1 | 0.7 | 4.1 | 37.3 | 163.1 | 500 | 13304 | $0.125 |
| crawl4ai | 131.0 | 0.6 | 3.0 | 35.4 | 169.9 | 500 | 13248 | $0.161 |
| crawl4ai-raw | 187.6 | 1.3 | 3.7 | 39.2 | 231.8 | 500 | 13248 | $0.161 |

### quotes-toscrape

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| **markcrawl** | 3.6 | 0.0 | 0.0 | 21.3 | 24.9 | 15 | 18 | $0.0058 |
| playwright | 5.1 | 0.0 | 0.0 | 21.5 | 26.6 | 15 | 28 | $0.010 |
| crawlee | 6.8 | 0.0 | 0.0 | 26.2 | 33.0 | 15 | 28 | $0.010 |
| colly+md | 4.0 | 0.0 | 0.0 | 29.8 | 33.8 | 15 | 28 | $0.010 |
| scrapy+md | 4.7 | 0.0 | 0.0 | 35.9 | 40.6 | 15 | 25 | $0.011 |
| crawl4ai-raw | 9.6 | 0.0 | 0.0 | 39.0 | 48.5 | 15 | 23 | $0.014 |
| crawl4ai | 5.0 | 0.0 | 0.0 | 56.6 | 61.5 | 15 | 23 | $0.014 |

### react-dev

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| **markcrawl** | 8.4 | 0.1 | 0.7 | 54.4 | 63.6 | 221 | 3496 | $0.019 |
| scrapy+md | 22.9 | 0.1 | 0.8 | 46.8 | 70.7 | 221 | 3557 | $0.020 |
| colly+md | 32.3 | 0.6 | 1.6 | 48.4 | 82.9 | 221 | 6355 | $0.075 |
| playwright | 59.7 | 0.2 | 1.5 | 45.6 | 107.0 | 221 | 6355 | $0.075 |
| crawlee | 76.8 | 0.3 | 1.5 | 46.5 | 125.0 | 221 | 6444 | $0.077 |
| crawl4ai | 109.7 | 0.1 | 1.6 | 41.8 | 153.2 | 221 | 4756 | $0.035 |
| crawl4ai-raw | 123.1 | 0.1 | 1.1 | 48.5 | 172.9 | 221 | 4756 | $0.035 |

### stripe-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| scrapy+md | 24.2 | 0.1 | 0.7 | 38.1 | 63.0 | 257 | 3035 | $0.020 |
| **markcrawl** | 35.7 | 0.1 | 0.5 | 35.6 | 71.9 | 257 | 2772 | $0.014 |
| colly+md | 58.0 | 2.0 | 4.1 | 34.0 | 98.2 | 254 | 14661 | $0.875 |
| crawl4ai | 268.5 | 0.1 | 0.7 | 39.3 | 308.5 | 257 | 3379 | $0.023 |
| playwright | 333.2 | 2.0 | 4.7 | 37.1 | 377.1 | 257 | 15680 | $0.930 |
| crawl4ai-raw | 423.1 | 0.1 | 0.8 | 39.0 | 462.9 | 257 | 3378 | $0.023 |
| crawlee | 413.2 | 2.3 | 4.8 | 43.4 | 463.6 | 257 | 15683 | $0.931 |

### wikipedia-python

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| playwright | 12.2 | 0.1 | 0.2 | 24.5 | 37.0 | 42 | 1112 | $0.034 |
| scrapy+md | 8.2 | 0.1 | 0.2 | 35.2 | 43.7 | 50 | 1309 | $0.034 |
| colly+md | 9.0 | 0.2 | 0.3 | 41.9 | 51.3 | 50 | 1378 | $0.037 |
| crawlee | 17.0 | 0.2 | 0.5 | 38.1 | 55.7 | 50 | 2148 | $0.113 |
| **markcrawl** | 6.7 | 0.0 | 0.2 | 50.5 | 57.5 | 50 | 1024 | $0.023 |
| crawl4ai-raw | 29.5 | 0.1 | 0.3 | 41.5 | 71.4 | 50 | 1243 | $0.038 |
| crawl4ai | 41.7 | 0.1 | 0.3 | 59.7 | 101.7 | 50 | 1243 | $0.038 |

## Key Findings

- **Fastest end-to-end:** markcrawl (476.5s total)
- **Slowest end-to-end:** crawl4ai-raw (1370.0s total)
- **markcrawl:** querying dominates at 77% of pipeline time
- **scrapy+md:** querying dominates at 72% of pipeline time
- **colly+md:** querying dominates at 62% of pipeline time
- **Cheapest API cost:** markcrawl ($0.222)
- **Most expensive API cost:** crawlee ($1.41)

## Methodology

- **Scrape timing** comes from `benchmark_all_tools.py` run metadata
- **Chunk timing** uses markcrawl's `chunk_markdown()` with 400-word chunks and 50-word overlap
- **Embed timing** uses OpenAI `text-embedding-3-small` (cached after first run)
- **Query timing** includes embedding the query, cosine retrieval, and `gpt-4o-mini` answer generation
- **Cost tracking** counts actual tokens from API responses (embed tokens estimated via tiktoken, query tokens from response.usage)
- **Embedding cache** — chunks are cached by content hash; re-runs with unchanged pages.jsonl skip API calls entirely
- See [METHODOLOGY.md](METHODOLOGY.md) for full test setup
