# MarkCrawl Head-to-Head Comparison

Generated: 2026-04-12 07:58:32 UTC

## Methodology

**Two-phase approach** for a fair comparison:

1. **URL Discovery** — MarkCrawl crawls each site once to build a URL list
2. **Benchmarking** — All tools fetch the **identical URLs** (no discovery, pure fetch+convert speed)

Settings:
- **Delay:** 0 (no politeness throttle)
- **Concurrency:** 5
- **Iterations:** 3 per tool per site (reporting median + std dev)
- **Warm-up:** 1 throwaway run per site before timing
- **Output:** Markdown files + JSONL index
- **URL list:** Identical for all tools (discovered in Phase 1)

See [METHODOLOGY.md](METHODOLOGY.md) for full methodology.

## Tools tested

| Tool | Available | Notes |
|---|---|---|
| markcrawl | Yes | requests + BeautifulSoup + markdownify — [AIMLPM/markcrawl](https://github.com/AIMLPM/markcrawl) |
| crawl4ai | Yes | Playwright + arun_many() batch concurrency — [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) |
| crawl4ai-raw | Yes | Playwright + sequential arun(), default config (out-of-box baseline) |
| scrapy+md | Yes | Scrapy async + markdownify — [scrapy/scrapy](https://github.com/scrapy/scrapy) |
| crawlee | Yes | Playwright + markdownify — [apify/crawlee-python](https://github.com/apify/crawlee-python) |
| colly+md | Yes | Go fetch (Colly) + Python markdownify — [gocolly/colly](https://github.com/gocolly/colly) |
| playwright | Yes | Raw Playwright baseline + markdownify (no framework) |
| firecrawl | Not installed | Self-hosted Docker — [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) |

## Results by site

### quotes-toscrape — Paginated quotes (simple HTML, link-following)

Max pages: 15

| Tool | Pages | Time (s) | Std dev | Pages/sec | Avg words | Output KB | Peak MB |
|---|---|---|---|---|---|---|---|
| markcrawl | 15 | 4.0 | ±0.0 | 3.7 | 259 | 33 | 202 |
| crawl4ai | 15 | 4.5 | ±0.0 | 3.4 | 242 | 42 | 111 |
| crawl4ai-raw | 15 | 9.1 | ±0.0 | 1.7 | 242 | 42 | 161 |
| scrapy+md | 15 | 4.6 | ±0.0 | 3.3 | 242 | 31 | 130 |
| crawlee | 15 | 7.1 | ±0.0 | 2.1 | 245 | 31 | 115 |
| colly+md | 15 | 3.3 | ±0.0 | 4.5 | 245 | 31 | 149 |
| playwright | 15 | 5.4 | ±0.0 | 2.8 | 245 | 31 | 203 |

### books-toscrape — E-commerce catalog (60 pages, pagination)

Max pages: 60

| Tool | Pages | Time (s) | Std dev | Pages/sec | Avg words | Output KB | Peak MB |
|---|---|---|---|---|---|---|---|
| markcrawl | 60 | 9.5 | ±0.0 | 6.3 | 320 | 160 | 203 |
| crawl4ai | 60 | 11.8 | ±0.0 | 5.1 | 493 | 482 | 94 |
| crawl4ai-raw | 60 | 26.8 | ±0.0 | 2.2 | 493 | 482 | 315 |
| scrapy+md | 60 | 4.6 | ±0.0 | 13.0 | 387 | 251 | 216 |
| crawlee | 60 | 15.9 | ±0.0 | 3.8 | 395 | 254 | 153 |
| colly+md | 60 | 5.9 | ±0.0 | 10.1 | 395 | 254 | 153 |
| playwright | 60 | 23.5 | ±0.0 | 2.6 | 395 | 254 | 226 |

### fastapi-docs — API documentation (code blocks, headings, tutorials)

Max pages: 500

| Tool | Pages | Time (s) | Std dev | Pages/sec | Avg words | Output KB | Peak MB |
|---|---|---|---|---|---|---|---|
| markcrawl | 153 | 30.0 | ±0.0 | 5.1 | 2100 | 2991 | 280 |
| crawl4ai | 153 | 60.0 | ±0.0 | 2.5 | 3519 | 6537 | 277 |
| crawl4ai-raw | 153 | 119.8 | ±0.0 | 1.3 | 3519 | 6537 | 326 |
| scrapy+md | 153 | 17.2 | ±0.0 | 8.9 | 2851 | 4677 | 203 |
| crawlee | 153 | 125.7 | ±0.0 | 1.2 | 3153 | 6512 | 281 |
| colly+md | 153 | 18.9 | ±0.0 | 8.1 | 3175 | 5437 | 284 |
| playwright | 153 | 60.0 | ±0.0 | 2.5 | 3159 | 6520 | 356 |

### python-docs — Python standard library docs

Max pages: 500

| Tool | Pages | Time (s) | Std dev | Pages/sec | Avg words | Output KB | Peak MB |
|---|---|---|---|---|---|---|---|
| markcrawl | 500 | 69.5 | ±0.0 | 7.2 | 3838 | 19569 | 324 |
| crawl4ai | 500 | 86.5 | ±0.0 | 5.8 | 4180 | 26207 | 751 |
| crawl4ai-raw | 500 | 186.7 | ±0.0 | 2.7 | 4180 | 26207 | 789 |
| scrapy+md | 328 | 46.9 | ±0.0 | 7.0 | 4796 | 15751 | 272 |
| crawlee | 500 | 52.8 | ±0.0 | 9.5 | 4140 | 21108 | 280 |
| colly+md | 500 | 34.5 | ±0.0 | 14.5 | 4070 | 20718 | 315 |
| playwright | 500 | 79.5 | ±0.0 | 6.3 | 4140 | 21108 | 341 |

### react-dev — React docs (SPA, JS-rendered, interactive examples)

Max pages: 500

| Tool | Pages | Time (s) | Std dev | Pages/sec | Avg words | Output KB | Peak MB |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | — | — | — | — | — | — | — |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | — | — | — | — | — | — | — |

### wikipedia-python — Wikipedia (tables, infoboxes, citations, deep linking)

Max pages: 50

| Tool | Pages | Time (s) | Std dev | Pages/sec | Avg words | Output KB | Peak MB |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | — | — | — | — | — | — | — |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | — | — | — | — | — | — | — |

### stripe-docs — Stripe API docs (tabbed content, code samples, sidebars)

Max pages: 500

| Tool | Pages | Time (s) | Std dev | Pages/sec | Avg words | Output KB | Peak MB |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | — | — | — | — | — | — | — |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | — | — | — | — | — | — | — |

### blog-engineering — GitHub Engineering Blog (articles, images, technical content)

Max pages: 200

| Tool | Pages | Time (s) | Std dev | Pages/sec | Avg words | Output KB | Peak MB |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | — | — | — | — | — | — | — |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — |
| playwright | — | — | — | — | — | — | — |

## Overall summary

| Tool | Total pages | Total time (s) | Avg pages/sec | Notes |
|---|---|---|---|---|
| markcrawl | 728 | 113.1 | 6.4 | *(4/8 sites)*
| crawl4ai | 728 | 162.8 | 4.5 | *(4/8 sites)*
| crawl4ai-raw | 728 | 342.3 | 2.1 | *(4/8 sites)*
| scrapy+md | 556 | 73.3 | 7.6 | *(4/8 sites)*
| crawlee | 728 | 201.5 | 3.6 | *(4/8 sites)*
| colly+md | 728 | 62.7 | 11.6 | *(4/8 sites)*
| playwright | 728 | 168.5 | 4.3 | *(4/8 sites)*

> **Note on variance:** These benchmarks fetch pages from live public websites.
> Network conditions, server load, and CDN caching can cause significant
> run-to-run variance (std dev shown per site). For the most reliable comparison,
> run multiple iterations and compare medians.

## Reproducing these results

```bash
# Install all tools
pip install markcrawl crawl4ai scrapy markdownify
playwright install chromium  # for crawl4ai

# Run comparison
python benchmark_all_tools.py
```

For FireCrawl, also run:
```bash
docker run -p 3002:3002 firecrawl/firecrawl:latest
export FIRECRAWL_API_URL=http://localhost:3002
python benchmark_all_tools.py
```
