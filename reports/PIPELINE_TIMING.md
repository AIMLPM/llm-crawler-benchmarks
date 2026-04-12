# End-to-End RAG Pipeline Timing Benchmark
<!-- style: v2, 2026-04-12 -->

Measures how long each crawler takes across the full RAG pipeline:
scraping, chunking, embedding, and querying.

**Run:** `run_20260412_075832` | **Sites:** books-toscrape, fastapi-docs, python-docs, quotes-toscrape | **Embedding model:** text-embedding-3-small | **Answer model:** gpt-4o-mini

## Summary: Total Pipeline Time by Tool

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | **Total (s)** | Pages | Chunks |
|------|-----------|----------|----------|----------|--------------|-------|--------|
| scrapy+md | 73.3 | 0.8 | 119.4 | 158.3 | **351.8** | 556 | 14104 |
| colly+md | 62.7 | 1.6 | 129.6 | 189.2 | **383.1** | 728 | 17037 |
| **markcrawl** | 113.1 | 2.4 | 146.5 | 143.7 | **405.7** | 728 | 12901 |
| crawlee | 201.5 | 1.2 | 131.5 | 143.9 | **478.1** | 728 | 17108 |
| playwright | 168.5 | 0.9 | 129.0 | 187.1 | **485.5** | 728 | 17109 |
| crawl4ai | 162.8 | 1.0 | 185.9 | 149.7 | **499.3** | 728 | 17908 |
| crawl4ai-raw | 342.3 | 1.2 | 133.5 | 130.1 | **607.1** | 728 | 17908 |

## Phase Breakdown (% of Total Pipeline Time)

| Tool | Scrape % | Chunk % | Embed % | Query % |
|------|---------|--------|--------|--------|
| scrapy+md | 20.8% | 0.2% | 33.9% | 45.0% |
| colly+md | 16.4% | 0.4% | 33.8% | 49.4% |
| markcrawl | 27.9% | 0.6% | 36.1% | 35.4% |
| crawlee | 42.2% | 0.3% | 27.5% | 30.1% |
| playwright | 34.7% | 0.2% | 26.6% | 38.5% |
| crawl4ai | 32.6% | 0.2% | 37.2% | 30.0% |
| crawl4ai-raw | 56.4% | 0.2% | 22.0% | 21.4% |

## Per-Site Breakdown

### books-toscrape

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks |
|------|-----------|----------|----------|----------|----------|-------|--------|
| **markcrawl** | 9.5 | 0.0 | 1.4 | 41.9 | 52.8 | 60 | 112 |
| crawl4ai | 11.8 | 0.0 | 4.8 | 36.2 | 52.9 | 60 | 628 |
| crawlee | 15.9 | 0.0 | 1.5 | 42.5 | 59.8 | 60 | 134 |
| crawl4ai-raw | 26.8 | 0.0 | 5.1 | 32.4 | 64.2 | 60 | 628 |
| colly+md | 5.9 | 0.0 | 4.0 | 63.4 | 73.3 | 60 | 134 |
| scrapy+md | 4.6 | 0.1 | 16.9 | 60.1 | 81.8 | 60 | 130 |
| playwright | 23.5 | 0.0 | 1.3 | 81.5 | 106.4 | 60 | 134 |

### fastapi-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks |
|------|-----------|----------|----------|----------|----------|-------|--------|
| scrapy+md | 17.2 | 0.1 | 29.7 | 49.9 | 97.0 | 153 | 3739 |
| colly+md | 18.9 | 1.0 | 30.3 | 54.0 | 104.2 | 153 | 3869 |
| crawl4ai | 60.0 | 0.3 | 28.9 | 47.7 | 136.9 | 153 | 4147 |
| playwright | 60.0 | 0.3 | 29.0 | 56.0 | 145.2 | 153 | 3857 |
| **markcrawl** | 30.0 | 0.3 | 72.8 | 47.5 | 150.5 | 153 | 3288 |
| crawl4ai-raw | 119.8 | 0.2 | 27.7 | 49.6 | 197.2 | 153 | 4147 |
| crawlee | 125.7 | 0.2 | 30.2 | 52.5 | 208.5 | 153 | 3856 |

### python-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks |
|------|-----------|----------|----------|----------|----------|-------|--------|
| scrapy+md | 46.9 | 0.5 | 72.3 | 28.1 | 147.7 | 328 | 10210 |
| colly+md | 34.5 | 0.6 | 94.7 | 47.6 | 177.5 | 500 | 13006 |
| **markcrawl** | 69.5 | 2.2 | 71.8 | 35.1 | 178.6 | 500 | 9477 |
| crawlee | 52.8 | 1.0 | 99.3 | 30.2 | 183.4 | 500 | 13090 |
| playwright | 79.5 | 0.6 | 98.5 | 29.7 | 208.4 | 500 | 13090 |
| crawl4ai | 86.5 | 0.6 | 151.7 | 30.3 | 269.0 | 500 | 13110 |
| crawl4ai-raw | 186.7 | 1.0 | 100.6 | 25.1 | 313.4 | 500 | 13110 |

### quotes-toscrape

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks |
|------|-----------|----------|----------|----------|----------|-------|--------|
| **markcrawl** | 4.0 | 0.0 | 0.5 | 19.3 | 23.8 | 15 | 24 |
| scrapy+md | 4.6 | 0.0 | 0.4 | 20.2 | 25.3 | 15 | 25 |
| playwright | 5.4 | 0.0 | 0.2 | 19.9 | 25.5 | 15 | 28 |
| crawlee | 7.1 | 0.0 | 0.5 | 18.7 | 26.3 | 15 | 28 |
| colly+md | 3.3 | 0.0 | 0.6 | 24.2 | 28.2 | 15 | 28 |
| crawl4ai-raw | 9.1 | 0.0 | 0.2 | 23.0 | 32.3 | 15 | 23 |
| crawl4ai | 4.5 | 0.0 | 0.5 | 35.5 | 40.4 | 15 | 23 |

## Key Findings

- **Fastest end-to-end:** scrapy+md (351.8s total)
- **Slowest end-to-end:** crawl4ai-raw (607.1s total)
- **scrapy+md:** querying dominates at 45% of pipeline time
- **colly+md:** querying dominates at 49% of pipeline time
- **markcrawl:** embedding dominates at 36% of pipeline time

## Methodology

- **Scrape timing** comes from `benchmark_all_tools.py` run metadata
- **Chunk timing** uses markcrawl's `chunk_markdown()` with 400-word chunks and 50-word overlap
- **Embed timing** uses OpenAI `text-embedding-3-small` (cached after first run)
- **Query timing** includes embedding the query, cosine retrieval, and `gpt-4o-mini` answer generation
- See [METHODOLOGY.md](METHODOLOGY.md) for full test setup
