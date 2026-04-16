# Speed Comparison
<!-- style: v2, 2026-04-15 -->

**markcrawl** is the fastest crawler at 12.1 pages/sec overall, followed by scrapy+md (9.5 p/s).

Generated: 2026-04-16 03:00:38 UTC

## Methodology

**Per-tool discovery:** Each tool starts from the same seed URL and discovers
its own pages through link-following. This tests real-world crawl behavior —
discovery quality, link extraction, and content extraction are all measured.
Page counts may vary between tools depending on each tool's link-following strategy.

Settings:
- **Seed URL:** Same for all tools per site
- **Max pages:** Same limit for all tools per site
- **Delay:** 0 (no politeness throttle)
- **Concurrency:** 5
- **Iterations:** 3 per tool per site (reporting median + std dev)
- **Warm-up:** 1 throwaway run per site before timing
- **Output:** Markdown files + JSONL index

See [METHODOLOGY.md](METHODOLOGY.md) for full methodology.

## Tools tested

| Tool | Type | Available | Notes |
|---|---|---|---|
| markcrawl | HTTP | Yes | requests + BeautifulSoup + markdownify — [AIMLPM/markcrawl](https://github.com/AIMLPM/markcrawl) |
| crawl4ai | Browser | Yes | Playwright + arun_many() batch concurrency — [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) |
| crawl4ai-raw | Browser | Yes | Playwright + sequential arun(), default config (out-of-box baseline) |
| scrapy+md | HTTP | Yes | Scrapy async + markdownify — [scrapy/scrapy](https://github.com/scrapy/scrapy) |
| crawlee | Browser | Yes | Playwright + markdownify — [apify/crawlee-python](https://github.com/apify/crawlee-python) |
| colly+md | HTTP | Yes | Go fetch (Colly) + Python markdownify — [gocolly/colly](https://github.com/gocolly/colly) |
| playwright | Browser | Yes | Raw Playwright baseline + markdownify (no framework) |
| firecrawl | Browser (self-hosted) | Not installed | Self-hosted Docker — [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) |

## Context for the numbers

**Pages/sec** measures raw crawl throughput — how fast a tool fetches and converts HTML to Markdown. Tools using Playwright (browser rendering) are inherently slower than HTTP-only tools (requests/Scrapy/Colly) because they must launch a browser and wait for JavaScript execution. **Avg words** and **Output KB** reflect output volume, not quality — see [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for whether more words means better content.

## Results by site

### quotes-toscrape — Paginated quotes (simple HTML, link-following)

Max pages: 15

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| scrapy+md | 15 | 3.5 | ±0.1 | 4.2 | 209 | 30 | 200 |
| **markcrawl** | 15 | 3.9 | ±0.2 | 3.9 | 280 | 27 | 125 |
| playwright | 15 | 4.4 | ±0.2 | 3.4 | 229 | 29 | 109 |
| crawlee | 15 | 6.6 | ±0.1 | 2.3 | 215 | 27 | 200 |
| colly+md | 15 | 6.7 | ±3.1 | 2.2 | 215 | 27 | 304 |
| crawl4ai-raw | 15 | 7.3 | ±0.0 | 2.1 | 226 | 38 | 199 |
| crawl4ai | 15 | 7.7 | ±0.3 | 1.9 | 226 | 38 | 181 |

### books-toscrape — E-commerce catalog (60 pages, pagination)

Max pages: 60

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| scrapy+md | 60 | 4.8 | ±0.2 | 12.5 | 473 | 216 | 110 |
| **markcrawl** | 60 | 5.1 | ±0.2 | 11.7 | 389 | 186 | 324 |
| playwright | 60 | 18.7 | ±2.2 | 3.2 | 384 | 270 | 320 |
| crawlee | 60 | 19.2 | ±0.7 | 3.1 | 384 | 270 | 296 |
| crawl4ai-raw | 60 | 21.8 | ±0.3 | 2.8 | 504 | 534 | 176 |
| crawl4ai | 60 | 24.3 | ±0.1 | 2.5 | 504 | 534 | 313 |
| colly+md | 60 | 30.0 | ±0.3 | 2.0 | 384 | 270 | 176 |

### fastapi-docs — API documentation (code blocks, headings, tutorials)

Max pages: 500

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| **markcrawl** | 500 | 35.7 | ±1.0 | 14.0 | 1967 | 10073 | 258 |
| scrapy+md | 496 | 46.6 | ±0.9 | 10.6 | 2799 | 15277 | 269 |
| colly+md | 500 | 94.5 | ±0.7 | 5.3 | 3218 | 19029 | 317 |
| playwright | 500 | 200.5 | ±16.7 | 2.5 | 3253 | 22529 | 911 |
| crawl4ai-raw | 500 | 334.6 | ±8.8 | 1.5 | 3630 | 22665 | 314 |
| crawl4ai | 500 | 341.2 | ±18.9 | 1.5 | 3625 | 22650 | 353 |
| crawlee | 502 | 367.7 | ±11.5 | 1.4 | 3241 | 22546 | 45 |

### python-docs — Python standard library docs

Max pages: 500

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| **markcrawl** | 500 | 37.3 | ±4.5 | 13.4 | 3713 | 18525 | 302 |
| scrapy+md | 500 | 59.6 | ±9.2 | 8.2 | 3983 | 21017 | 105 |
| colly+md | 500 | 130.0 | ±0.0 | 3.8 | 5453 | 24839 | 912 |
| playwright | 500 | 130.0 | ±11.6 | 3.8 | 3064 | 15460 | 338 |
| crawlee | 500 | 130.3 | ±1.5 | 3.8 | 3064 | 15463 | 42 |
| crawl4ai | 500 | 192.0 | ±15.6 | 2.6 | 3058 | 18362 | 267 |
| crawl4ai-raw | 500 | 228.1 | ±29.4 | 2.2 | 3058 | 18362 | 277 |

### react-dev — React docs (SPA, JS-rendered, interactive examples)

Max pages: 500

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| **markcrawl** | 221 | 11.0 | ±0.1 | 20.1 | 1587 | 2769 | 191 |
| scrapy+md | 217 | 15.4 | ±1.9 | 14.1 | 1623 | 2885 | 213 |
| colly+md | 292 | 24.1 | ±2.9 | 12.1 | 5535 | 18880 | 311 |
| playwright | 221 | 44.1 | ±2.7 | 5.0 | 4330 | 11657 | 652 |
| crawlee | 217 | 72.4 | ±2.1 | 3.0 | 4432 | 11667 | 31 |
| crawl4ai | 500 | 221.4 | ±7.2 | 2.3 | 1866 | 10911 | 304 |
| crawl4ai-raw | 500 | 224.7 | ±12.1 | 2.2 | 1866 | 10911 | 520 |

### wikipedia-python — Wikipedia (tables, infoboxes, citations, deep linking)

Max pages: 50

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| **markcrawl** | 50 | 6.9 | ±0.5 | 7.3 | 3491 | 1771 | 242 |
| scrapy+md | 50 | 8.5 | ±2.8 | 5.9 | 3764 | 2425 | 279 |
| playwright | 50 | 34.2 | ±27.3 | 1.5 | 6645 | 4534 | 506 |
| crawl4ai | 50 | 43.0 | ±3.6 | 1.2 | 6644 | 4708 | 233 |
| crawl4ai-raw | 50 | 44.4 | ±7.1 | 1.1 | 6641 | 4704 | 311 |
| crawlee | 50 | 47.8 | ±9.8 | 1.0 | 12020 | 13469 | 176 |
| colly+md | — | — | — | — | — | error: heartbeat stall: 0 pages after 120s |

### stripe-docs — Stripe API docs (tabbed content, code samples, sidebars)

Max pages: 500

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| scrapy+md | 498 | 49.7 | ±3.9 | 10.0 | 3741 | 20967 | 269 |
| **markcrawl** | 500 | 63.2 | ±3.3 | 7.9 | 767 | 2808 | 206 |
| colly+md | 498 | 127.2 | ±1.7 | 3.9 | 21170 | 294038 | 600 |
| playwright | 500 | 449.2 | ±12.4 | 1.1 | 20274 | 266655 | 724 |
| crawlee | 500 | 468.4 | ±2.8 | 1.1 | 20292 | 264386 | 133 |
| crawl4ai-raw | 500 | 628.0 | ±201.2 | 0.8 | 2038 | 9857 | 684 |
| crawl4ai | 500 | 708.0 | ±9.4 | 0.7 | 1514 | 7418 | 648 |

### blog-engineering — GitHub Engineering Blog (articles, images, technical content)

Max pages: 200

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| **markcrawl** | 200 | 6.0 | ±23.4 | 33.5 | 703 | 1139 | 145 |
| scrapy+md | 195 | 25.0 | ±3.7 | 7.7 | 1051 | 1709 | 211 |
| playwright | 200 | 40.7 | ±14.2 | 4.9 | 3375 | 13779 | 651 |
| crawlee | 200 | 59.6 | ±11.9 | 3.4 | 3369 | 13724 | 105 |
| crawl4ai | 200 | 65.1 | ±0.6 | 3.1 | 2148 | 4864 | 270 |
| crawl4ai-raw | 200 | 65.9 | ±0.7 | 3.0 | 2148 | 4864 | 269 |
| colly+md | 200 | 74.0 | ±9.6 | 2.7 | 3674 | 12873 | 262 |

> **Column definitions:** **Pages (a)** = pages discovered and fetched by this tool (varies per tool).
> **Time (b)** = wall-clock seconds to fetch and convert all pages (median of 3 iterations).
> **[1] Pages/sec** = median throughput across iterations.
> Approximately a÷b; small differences arise because each column is an independent median.
> **[2] Avg words** = mean words per page. **[3] Output KB** = total Markdown output size across all pages.
> **Std dev** = standard deviation of Time across iterations. **[4] Peak MB** = peak resident memory (RSS) during crawl.

## Overall summary

| Tool | Total pages (a) | Total time (b) | Avg pages/sec (a÷b) | Notes |
|---|---|---|---|---|
| **markcrawl** | 2046 | 169.0 | 12.1 | *(missing 279 pages)* |
| scrapy+md | 2031 | 213.1 | 9.5 | *(missing 294 pages)* |
| colly+md | 2065 | 486.6 | 4.2 | *(7/8 sites)* *(missing 260 pages)* |
| playwright | 2046 | 921.8 | 2.2 | *(missing 279 pages)* |
| crawlee | 2044 | 1172.0 | 1.7 | *(missing 281 pages)* |
| crawl4ai-raw | 2325 | 1554.6 | 1.5 |  |
| crawl4ai | 2325 | 1602.7 | 1.5 |  |

> **Column definitions:** **Total pages (a)** = sum of pages fetched across all sites.
> **Total time (b)** = sum of median wall-clock times across all sites. **Avg pages/sec (a÷b)** = overall throughput.

> **Note on variance:** These benchmarks fetch pages from live public websites.
> Network conditions, server load, and CDN caching can cause significant
> run-to-run variance. For the most reliable comparison,
> run multiple iterations and compare medians.

## What the results mean

HTTP-only tools (markcrawl, scrapy+md, colly+md) are consistently 2-7x faster than browser-based tools (crawl4ai, crawlee, playwright). The speed gap comes from skipping browser startup and JavaScript execution entirely.

markcrawl is fastest overall, but loses on quotes-toscrape (scrapy+md), books-toscrape (scrapy+md), stripe-docs (scrapy+md). Site-specific results vary with server response times and content complexity.

Higher word counts from browser-based tools (crawlee, playwright) do not indicate better extraction quality — they often reflect extra navigation chrome and repeated boilerplate. See [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for content signal analysis.

Some tools miss pages on certain sites: scrapy+md and colly+md fetch fewer pages than expected on some sites, which inflates their per-page speed but means incomplete coverage. Check the per-site tables for exact page counts.

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
