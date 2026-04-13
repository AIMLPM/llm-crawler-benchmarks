# Speed Comparison
<!-- style: v2, 2026-04-13 -->

**markcrawl** is the fastest crawler at 14.0 pages/sec overall, followed by scrapy+md (9.3 p/s).

Generated: 2026-04-13 10:30:28 UTC

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

| Tool | Pages (a) | Time (b) | Pages/sec [3] | Avg words [1] | Output KB [2] |
|---|---|---|---|---|---|
| **markcrawl** | 15 | 3.6 | 4.2 | 199 | 19 |
| crawl4ai | 15 | 5.0 | 3.0 | 242 | 42 |
| crawl4ai-raw | 15 | 9.6 | 1.6 | 242 | 42 |
| scrapy+md | 15 | 4.7 | 3.2 | 242 | 31 |
| crawlee | 15 | 6.8 | 2.2 | 245 | 31 |
| colly+md | 15 | 4.0 | 3.8 | 245 | 31 |
| playwright | 15 | 5.1 | 3.0 | 245 | 31 |

### books-toscrape — E-commerce catalog (60 pages, pagination)

Max pages: 60

| Tool | Pages (a) | Time (b) | Pages/sec [3] | Avg words [1] | Output KB [2] |
|---|---|---|---|---|---|
| **markcrawl** | 60 | 4.2 | 14.3 | 339 | 155 |
| crawl4ai | 60 | 11.4 | 5.3 | 493 | 482 |
| crawl4ai-raw | 60 | 27.7 | 2.2 | 493 | 482 |
| scrapy+md | 60 | 4.9 | 12.3 | 387 | 251 |
| crawlee | 60 | 16.6 | 3.6 | 395 | 254 |
| colly+md | 60 | 6.5 | 9.2 | 395 | 254 |
| playwright | 60 | 35.1 | 1.8 | 395 | 254 |

### fastapi-docs — API documentation (code blocks, headings, tutorials)

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [3] | Avg words [1] | Output KB [2] |
|---|---|---|---|---|---|
| **markcrawl** | 153 | 11.4 | 13.4 | 2084 | 2952 |
| crawl4ai | 153 | 90.4 | 1.7 | 3519 | 6537 |
| crawl4ai-raw | 153 | 139.8 | 1.1 | 3521 | 6538 |
| scrapy+md | 153 | 29.6 | 5.2 | 2851 | 4677 |
| crawlee | 153 | 128.1 | 1.2 | 3154 | 6513 |
| colly+md | 153 | 27.1 | 5.6 | 3175 | 5437 |
| playwright | 153 | 86.3 | 1.8 | 3160 | 6521 |

### python-docs — Python standard library docs

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [3] | Avg words [1] | Output KB [2] |
|---|---|---|---|---|---|
| **markcrawl** | 500 | 22.1 | 22.7 | 3766 | 19103 |
| crawl4ai | 500 | 131.0 | 3.9 | 4180 | 26207 |
| crawl4ai-raw | 500 | 187.6 | 2.7 | 4180 | 26207 |
| scrapy+md | 328 | 37.6 | 8.7 | 4796 | 15751 |
| crawlee | 500 | 74.4 | 6.7 | 4140 | 21108 |
| colly+md | 500 | 43.5 | 11.5 | 4070 | 20718 |
| playwright | 500 | 121.1 | 4.4 | 4140 | 21108 |

### react-dev — React docs (SPA, JS-rendered, interactive examples)

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [3] | Avg words [1] | Output KB [2] |
|---|---|---|---|---|---|
| **markcrawl** | 221 | 8.4 | 26.3 | 1559 | 2711 |
| crawl4ai | 221 | 109.7 | 2.0 | 2277 | 5678 |
| crawl4ai-raw | 221 | 123.1 | 1.8 | 2279 | 5685 |
| scrapy+md | 221 | 22.9 | 9.6 | 1601 | 2914 |
| crawlee | 221 | 76.8 | 2.9 | 4370 | 11751 |
| colly+md | 221 | 32.3 | 6.9 | 4292 | 11570 |
| playwright | 221 | 59.7 | 3.7 | 4292 | 11570 |

### wikipedia-python — Wikipedia (tables, infoboxes, citations, deep linking)

Max pages: 50

| Tool | Pages (a) | Time (b) | Pages/sec [3] | Avg words [1] | Output KB [2] |
|---|---|---|---|---|---|
| **markcrawl** | 50 | 6.7 | 7.5 | 3417 | 1848 |
| crawl4ai | 50 | 41.7 | 1.2 | 5106 | 3664 |
| crawl4ai-raw | 50 | 29.5 | 1.7 | 5106 | 3664 |
| scrapy+md | 50 | 8.2 | 6.3 | 4925 | 3052 |
| crawlee | 50 | 17.0 | 3.0 | 10493 | 13532 |
| colly+md | 50 | 9.0 | 5.6 | 5446 | 3635 |
| playwright | 42 | 12.2 | 3.5 | 5249 | 3079 |

### stripe-docs — Stripe API docs (tabbed content, code samples, sidebars)

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [3] | Avg words [1] | Output KB [2] |
|---|---|---|---|---|---|
| **markcrawl** | 257 | 35.7 | 7.2 | 1165 | 2100 |
| crawl4ai | 257 | 268.5 | 1.0 | 1372 | 3605 |
| crawl4ai-raw | 257 | 423.1 | 0.6 | 1369 | 3598 |
| scrapy+md | 257 | 24.2 | 10.6 | 1360 | 2908 |
| crawlee | 257 | 413.2 | 0.6 | 18095 | 122070 |
| colly+md | 254 | 58.0 | 4.4 | 16950 | 114124 |
| playwright | 257 | 333.2 | 0.8 | 18073 | 122018 |

### blog-engineering — GitHub Engineering Blog (articles, images, technical content)

Max pages: 200

| Tool | Pages (a) | Time (b) | Pages/sec [3] | Avg words [1] | Output KB [2] |
|---|---|---|---|---|---|
| **markcrawl** | 200 | 11.7 | 17.5 | 667 | 1064 |
| crawl4ai | 200 | 58.9 | 3.4 | 2301 | 5266 |
| crawl4ai-raw | 200 | 87.0 | 2.3 | 2301 | 5266 |
| scrapy+md | 200 | 6.7 | 30.1 | 659 | 1075 |
| crawlee | 200 | 73.4 | 2.7 | 3576 | 14420 |
| colly+md | 124 | 28.9 | 4.4 | 3048 | 7229 |
| playwright | 200 | 40.2 | 5.0 | 3584 | 14500 |

> **Column definitions:** **Pages (a)** = total pages fetched from the site (identical URL list for all tools).
> **Time (b)** = wall-clock seconds to fetch and convert all pages (median of 3 iterations).
> **[3] Pages/sec** = median throughput across 3 iterations. Approximately a÷b; small differences arise because each column is an independent median.
> **[1] Avg words** = mean words per page. **[2] Output KB** = total Markdown output size across all pages.

## Overall summary

| Tool | Total pages (a) | Total time (b) | Avg pages/sec (a÷b) | Notes |
|---|---|---|---|---|
| **markcrawl** | 1456 | 103.9 | 14.0 | |
| crawl4ai | 1456 | 716.4 | 2.0 | |
| crawl4ai-raw | 1456 | 1027.5 | 1.4 | |
| scrapy+md | 1284 | 138.8 | 9.3 | |
| crawlee | 1456 | 806.2 | 1.8 | |
| colly+md | 1376 | 209.3 | 6.6 | |
| playwright | 1448 | 692.8 | 2.1 | |

> **Column definitions:** **Total pages (a)** = sum of pages fetched across all sites.
> **Total time (b)** = sum of median wall-clock times across all sites. **Avg pages/sec (a÷b)** = overall throughput.

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

## See also

- [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) — higher word counts don't mean higher quality
- [COST_AT_SCALE.md](COST_AT_SCALE.md) — what these speed differences cost at 100K+ pages
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup and fairness decisions
