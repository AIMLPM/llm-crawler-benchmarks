# End-to-End RAG Pipeline Timing Benchmark
<!-- style: v2, 2026-04-12 -->

markcrawl completes the full RAG pipeline (scrape + chunk + embed + query) in 1191.0s — 2.4x faster than the median tool. For HTTP-only crawlers, the LLM query phase dominates at 16-27% of total time, not scraping.

**Run:** `run_20260424_235304` | **Sites:** huggingface-transformers, ikea, kubernetes-docs, mdn-css, newegg, npr-news, postgres-docs, react-dev, rust-book, smittenkitchen, stripe-docs | **Embedding model:** text-embedding-3-small | **Answer model:** gpt-4o-mini

## What these phases mean

Each tool is measured across four pipeline phases:

- **Scrape** = fetch HTML and convert to Markdown (dominated by network I/O). HTTP-only tools (markcrawl, scrapy+md, colly+md) scrape 2-7x faster than browser-based tools (crawl4ai, crawlee, playwright) because they skip JavaScript rendering overhead.
- **Chunk** = split Markdown into overlapping text chunks (CPU-only, fast)
- **Embed** = send chunks to OpenAI embedding API (scales with chunk count)
- **Query** = embed question + retrieve top chunks + send to LLM for answer (scales with query count)

## Summary: Total Pipeline Time by Tool

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | **Total (s)** | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|--------------|-------|--------|------|
| markcrawl | 461.2 | 2.1 | 397.9 | 329.9 | **1191.0** | 2771 | 52809 | $0.311 |
| scrapy+md | 413.8 | 7.7 | 800.3 | 243.5 | **1465.4** | 2300 | 93042 | $3.92 |
| colly+md | 269.5 | 6.7 | 1075.6 | 270.6 | **1622.4** | 861 | 59746 | $2.46 |
| playwright | 1155.7 | 7.6 | 1273.4 | 477.2 | **2913.9** | 2484 | 87126 | $3.09 |
| crawl4ai-raw | 2517.7 | 2.7 | 531.8 | 328.3 | **3380.5** | 3350 | 69739 | $0.898 |
| crawl4ai | 2845.3 | 2.7 | 558.5 | 365.7 | **3772.2** | 3350 | 67393 | $0.884 |
| crawlee | 2009.0 | 8.5 | 1431.0 | 379.8 | **3828.3** | 2473 | 95701 | $3.74 |

> **Column definitions:** **Scrape/Chunk/Embed/Query (s)** = wall-clock seconds for each pipeline phase (summed across all sites). **Total (s)** = sum of all phases. **Pages** = total pages fetched. **Chunks** = total text chunks produced. **Cost** = total API cost (embedding + LLM query).

*(Cost uses OpenAI `text-embedding-3-small` at $0.02/1M tokens, `gpt-4o-mini` at $0.15/$0.6 per 1M input/output tokens)*

## Per-Page Pipeline Cost (normalized)

Since scrapy+md fetched fewer pages (due to timeouts), this table normalizes
time and cost per page for a fairer comparison.

| Tool | Pages | Total (s) | s/page | Cost/page | Chunks/page |
|------|-------|----------|--------|-----------|-------------|
| markcrawl | 2771 | 1191.0 | 0.43 | $0.0001 | 19.1 |
| scrapy+md | 2300 | 1465.4 | 0.64 | $0.0017 | 40.5 |
| colly+md | 861 | 1622.4 | 1.88 | $0.0029 | 69.4 |
| playwright | 2484 | 2913.9 | 1.17 | $0.0012 | 35.1 |
| crawl4ai-raw | 3350 | 3380.5 | 1.01 | $0.0003 | 20.8 |
| crawl4ai | 3350 | 3772.2 | 1.13 | $0.0003 | 20.1 |
| crawlee | 2473 | 3828.3 | 1.55 | $0.0015 | 38.7 |

> **Column definitions:** **s/page** = Total (s) ÷ Pages. **Cost/page** = total API cost ÷ Pages. **Chunks/page** = Chunks ÷ Pages. All values are per-page averages.

## Phase Breakdown (% of Total Pipeline Time)

| Tool | Scrape % | Chunk % | Embed % | Query % |
|------|---------|--------|--------|--------|
| markcrawl | 38.7% | 0.2% | 33.4% | 27.7% |
| scrapy+md | 28.2% | 0.5% | 54.6% | 16.6% |
| colly+md | 16.6% | 0.4% | 66.3% | 16.7% |
| playwright | 39.7% | 0.3% | 43.7% | 16.4% |
| crawl4ai-raw | 74.5% | 0.1% | 15.7% | 9.7% |
| crawl4ai | 75.4% | 0.1% | 14.8% | 9.7% |
| crawlee | 52.5% | 0.2% | 37.4% | 9.9% |

> Each percentage = phase time ÷ total pipeline time. Shows which phase dominates.

## API Cost Breakdown

*(Pricing: `text-embedding-3-small` at $0.02/1M tokens, `gpt-4o-mini` input at $0.15/1M, output at $0.6/1M)*

| Tool | Embed tokens | Embed cost | Query in tokens | Query out tokens | Query cost | **Total cost** |
|------|-------------|-----------|----------------|-----------------|-----------|---------------|
| markcrawl | 13,169,925 | $0.263 | 258,113 | 14,116 | $0.047 | **$0.311** |
| scrapy+md | 193,845,341 | $3.88 | 229,691 | 11,749 | $0.042 | **$3.92** |
| colly+md | 119,397,381 | $2.39 | 410,753 | 10,316 | $0.068 | **$2.46** |
| playwright | 147,263,434 | $2.95 | 895,111 | 14,005 | $0.143 | **$3.09** |
| crawl4ai-raw | 40,396,793 | $0.808 | 543,739 | 14,942 | $0.091 | **$0.898** |
| crawl4ai | 39,605,503 | $0.792 | 553,050 | 14,908 | $0.092 | **$0.884** |
| crawlee | 182,575,944 | $3.65 | 511,251 | 13,050 | $0.085 | **$3.74** |

> **Embed tokens** = tokens sent to the embedding API (all chunks). **Query in/out tokens** = tokens sent to and received from the answer LLM. **Total cost** = Embed cost + Query cost.

## What the results mean

For fast HTTP-only crawlers, scraping is NOT the bottleneck — LLM queries dominate at 70-77% of total pipeline time. The scrape phase only matters for browser-based tools where JavaScript rendering adds 3-7x overhead.

The biggest cost lever is chunk count: markcrawl produces 52,809 chunks vs scrapy+md's 93,042, leading to 14.7x lower embedding costs ($0.263 vs $3.88). At scale, the per-query cost difference is small; the savings compound from embedding fewer chunks.

See [COST_AT_SCALE.md](COST_AT_SCALE.md) for projections of these per-run costs to production workloads.

## Per-Site Breakdown

### huggingface-transformers

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| markcrawl | 0.0 | 0.0 | 3.3 | 13.6 | 17.0 | 0 | 495 | $0.0040 |
| playwright | 22.8 | 0.0 | 1.6 | 106.8 | 131.2 | 60 | 107 | $0.079 |
| crawl4ai-raw | 329.4 | 0.1 | 16.4 | 39.1 | 384.9 | 300 | 2128 | $0.034 |
| crawl4ai | 359.3 | 0.1 | 26.6 | 56.1 | 442.1 | 300 | 2955 | $0.044 |

### ikea

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| scrapy+md | 43.2 | 0.1 | 29.8 | 8.3 | 81.5 | 186 | 4118 | $0.019 |
| markcrawl | 115.5 | 0.1 | 38.5 | 13.1 | 167.3 | 200 | 4699 | $0.021 |
| playwright | 192.5 | 0.4 | 76.8 | 9.6 | 279.2 | 200 | 7732 | $0.295 |
| crawl4ai-raw | 243.4 | 0.1 | 49.6 | 16.0 | 309.1 | 200 | 5873 | $0.071 |
| crawlee | 205.1 | 0.5 | 96.2 | 9.7 | 311.6 | 201 | 9432 | $0.544 |
| crawl4ai | 426.7 | 0.1 | 43.2 | 23.1 | 493.1 | 200 | 5289 | $0.058 |

### kubernetes-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| markcrawl | 22.9 | 0.1 | 54.1 | 20.3 | 97.6 | 400 | 7400 | $0.032 |
| colly+md | 0.0 | 0.7 | 83.0 | 26.6 | 110.3 | 0 | 11169 | $0.122 |
| scrapy+md | 44.5 | 0.6 | 163.6 | 32.9 | 241.5 | 313 | 14566 | $3.23 |
| playwright | 129.8 | 0.6 | 96.7 | 25.0 | 252.1 | 400 | 11181 | $0.123 |
| crawl4ai-raw | 220.5 | 0.6 | 84.6 | 26.0 | 331.7 | 400 | 10748 | $0.153 |
| crawl4ai | 245.6 | 0.5 | 87.4 | 24.8 | 358.4 | 400 | 10862 | $0.154 |
| crawlee | 425.2 | 0.9 | 129.2 | 24.8 | 580.1 | 401 | 11181 | $0.318 |

### mdn-css

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| markcrawl | 11.3 | 0.2 | 13.3 | 27.5 | 52.2 | 300 | 1962 | $0.017 |
| scrapy+md | 21.7 | 0.1 | 24.8 | 17.2 | 63.7 | 299 | 2733 | $0.053 |
| playwright | 69.8 | 0.5 | 52.0 | 25.1 | 147.4 | 300 | 7064 | $0.075 |
| crawl4ai-raw | 159.9 | 0.4 | 49.1 | 19.2 | 228.6 | 300 | 6553 | $0.060 |
| crawl4ai | 211.9 | 0.4 | 48.3 | 19.6 | 280.1 | 300 | 6539 | $0.060 |
| crawlee | 396.6 | 0.6 | 62.5 | 23.9 | 483.5 | 300 | 6967 | $0.070 |

### newegg

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| playwright | 2.9 | 0.0 | 1.0 | 3.4 | 7.3 | 3 | 18 | $0.0075 |
| markcrawl | 38.4 | 0.0 | 4.1 | 10.3 | 52.8 | 200 | 482 | $0.0078 |
| colly+md | 98.0 | 0.0 | 3.8 | 37.7 | 139.5 | 17 | 402 | $0.035 |
| crawl4ai | 217.7 | 0.7 | 59.1 | 21.2 | 298.6 | 200 | 7012 | $0.148 |
| crawl4ai-raw | 254.6 | 0.6 | 57.9 | 17.7 | 330.8 | 200 | 7007 | $0.148 |

### npr-news

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| playwright | 0.0 | 0.1 | 45.9 | 23.5 | 69.5 | 0 | 5630 | $0.047 |
| markcrawl | 116.8 | 0.0 | 2.3 | 9.9 | 129.1 | 150 | 212 | $0.0048 |
| crawl4ai-raw | 91.3 | 0.1 | 51.4 | 15.1 | 158.0 | 150 | 6457 | $0.027 |
| crawl4ai | 106.6 | 0.1 | 50.9 | 13.3 | 170.9 | 150 | 6533 | $0.028 |
| crawlee | 179.8 | 0.4 | 81.3 | 11.2 | 272.8 | 150 | 8931 | $0.187 |

### postgres-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| colly+md | 0.0 | 0.1 | 17.7 | 25.4 | 43.2 | 0 | 1724 | $0.017 |
| markcrawl | 16.8 | 0.1 | 25.6 | 17.1 | 59.6 | 400 | 3668 | $0.030 |
| scrapy+md | 19.1 | 0.1 | 18.0 | 24.0 | 61.3 | 399 | 2314 | $0.020 |
| crawlee | 99.8 | 0.1 | 13.4 | 23.8 | 137.1 | 400 | 1715 | $0.017 |
| playwright | 135.0 | 0.1 | 15.0 | 24.0 | 174.1 | 400 | 1708 | $0.017 |
| crawl4ai-raw | 145.2 | 0.1 | 16.4 | 28.7 | 190.5 | 400 | 1680 | $0.053 |
| crawl4ai | 162.5 | 0.1 | 18.2 | 40.4 | 221.2 | 400 | 1680 | $0.053 |

### react-dev

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| scrapy+md | 22.4 | 0.1 | 24.5 | 63.1 | 110.1 | 217 | 3517 | $0.018 |
| markcrawl | 11.8 | 0.1 | 23.3 | 98.7 | 133.9 | 221 | 3382 | $0.018 |
| colly+md | 24.6 | 0.5 | 85.0 | 110.2 | 220.3 | 292 | 9347 | $0.233 |
| playwright | 49.1 | 0.3 | 59.6 | 169.5 | 278.5 | 221 | 6400 | $0.168 |
| crawlee | 79.2 | 0.5 | 67.2 | 183.1 | 330.0 | 217 | 6439 | $0.228 |
| crawl4ai | 221.8 | 0.2 | 90.9 | 63.8 | 376.8 | 500 | 9400 | $0.167 |
| crawl4ai-raw | 281.6 | 0.3 | 98.1 | 75.4 | 455.4 | 500 | 9400 | $0.167 |

### rust-book

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| colly+md | 6.5 | 0.2 | 41.8 | 22.4 | 70.8 | 54 | 5542 | $0.036 |
| crawl4ai-raw | 62.4 | 0.2 | 1.0 | 20.5 | 84.1 | 200 | 6056 | $0.082 |
| playwright | 22.2 | 0.7 | 47.0 | 19.1 | 89.0 | 200 | 6306 | $0.045 |
| crawlee | 56.0 | 0.2 | 47.5 | 21.5 | 125.2 | 200 | 6306 | $0.045 |
| scrapy+md | 17.0 | 0.4 | 99.3 | 19.7 | 136.4 | 200 | 12332 | $0.044 |
| crawl4ai | 69.6 | 0.2 | 49.8 | 30.8 | 150.4 | 200 | 6056 | $0.082 |
| markcrawl | 18.0 | 0.3 | 121.4 | 23.2 | 162.9 | 200 | 15649 | $0.056 |

### smittenkitchen

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| playwright | 43.6 | 0.5 | 50.4 | 8.1 | 102.7 | 200 | 5276 | $0.241 |
| crawl4ai-raw | 83.6 | 0.1 | 28.5 | 8.9 | 121.1 | 200 | 3893 | $0.029 |
| crawl4ai | 82.3 | 0.1 | 33.6 | 8.6 | 124.6 | 200 | 3893 | $0.029 |
| markcrawl | 28.0 | 1.0 | 89.9 | 21.4 | 140.3 | 200 | 11370 | $0.102 |
| crawlee | 81.7 | 0.5 | 68.3 | 6.7 | 157.2 | 103 | 6496 | $0.260 |
| scrapy+md | 189.6 | 5.6 | 337.7 | 19.7 | 552.6 | 189 | 40444 | $0.358 |

### stripe-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| markcrawl | 81.7 | 0.1 | 22.0 | 74.7 | 178.5 | 500 | 3490 | $0.019 |
| scrapy+md | 56.2 | 0.8 | 102.6 | 58.7 | 218.2 | 497 | 13018 | $0.173 |
| crawl4ai-raw | 645.8 | 0.2 | 78.7 | 61.7 | 786.4 | 500 | 9944 | $0.073 |
| crawl4ai | 741.4 | 0.2 | 50.5 | 64.1 | 856.1 | 500 | 7174 | $0.061 |
| colly+md | 140.5 | 5.2 | 844.3 | 48.3 | 1038.3 | 498 | 31562 | $2.01 |
| playwright | 487.9 | 4.4 | 827.5 | 63.1 | 1382.8 | 500 | 35704 | $1.99 |
| crawlee | 485.6 | 4.6 | 865.5 | 75.1 | 1430.8 | 501 | 38234 | $2.07 |

## Key Findings

- **Fastest end-to-end:** markcrawl (1191.0s total)
- **Slowest end-to-end:** crawlee (3828.3s total)
- **markcrawl:** scraping dominates at 39% of pipeline time
- **scrapy+md:** embedding dominates at 55% of pipeline time
- **colly+md:** embedding dominates at 66% of pipeline time
- **Cheapest API cost:** markcrawl ($0.311)
- **Most expensive API cost:** scrapy+md ($3.92)

## Methodology

- **Scrape timing** comes from `benchmark_all_tools.py` run metadata
- **Chunk timing** uses markcrawl's `chunk_markdown()` with 400-word chunks and 50-word overlap
- **Embed timing** uses OpenAI `text-embedding-3-small` (cached after first run)
- **Query timing** includes embedding the query, cosine retrieval, and `gpt-4o-mini` answer generation
- **Cost tracking** counts actual tokens from API responses (embed tokens estimated via tiktoken, query tokens from response.usage)
- **Embedding cache** — chunks are cached by content hash; re-runs with unchanged pages.jsonl skip API calls entirely
- See [METHODOLOGY.md](METHODOLOGY.md) for full test setup

## See also

- [SPEED_COMPARISON.md](SPEED_COMPARISON.md) — raw crawl speed without pipeline overhead
- [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) — why chunk counts vary between tools
- [COST_AT_SCALE.md](COST_AT_SCALE.md) — what these per-run costs look like at scale
- [ANSWER_QUALITY.md](ANSWER_QUALITY.md) — whether answer quality differs despite similar pipeline costs
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup
