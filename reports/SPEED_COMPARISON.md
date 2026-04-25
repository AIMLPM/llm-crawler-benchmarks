# Speed Comparison
<!-- style: v2, 2026-04-24 -->

markcrawl is the fastest crawler at 6.0 pages/sec overall, followed by scrapy+md (5.3 p/s).

Generated: 2026-04-24 23:53:04 UTC

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

### react-dev — React docs (SPA, JS-rendered, interactive examples)

Max pages: 500

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| markcrawl | 221 | 11.8 | ±0.3 | 18.7 | 1587 | 2770 | 79 |
| colly+md | 292 | 24.6 | ±0.3 | 11.9 | 5535 | 18880 | 243 |
| scrapy+md | 217 | 22.4 | ±10.7 | 10.9 | 1623 | 2885 | 171 |
| playwright | 221 | 49.1 | ±2.9 | 4.5 | 4330 | 11657 | 417 |
| crawlee | 217 | 79.2 | ±8.6 | 2.8 | 4442 | 11694 | 38 |
| crawl4ai | 500 | 221.8 | ±2.0 | 2.3 | 1870 | 10932 | 215 |
| crawl4ai-raw | 500 | 281.6 | ±58.8 | 1.8 | 1870 | 10933 | 248 |

### stripe-docs — Stripe API docs (tabbed content, code samples, sidebars)

Max pages: 500

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| scrapy+md | 497 | 56.2 | ±2.5 | 8.9 | 6995 | 42705 | 153 |
| markcrawl | 500 | 81.7 | ±2.2 | 6.1 | 766 | 2807 | 592 |
| colly+md | 498 | 140.5 | ±0.4 | 3.5 | 19248 | 273064 | 728 |
| crawlee | 501 | 485.6 | ±10.3 | 1.0 | 20621 | 271383 | 122 |
| playwright | 500 | 487.9 | ±14.7 | 1.0 | 20090 | 264240 | 764 |
| crawl4ai-raw | 500 | 645.8 | ±10.7 | 0.8 | 2052 | 9898 | 624 |
| crawl4ai | 500 | 741.4 | ±0.1 | 0.7 | 1524 | 7446 | 767 |

### huggingface-transformers — Hugging Face Transformers docs -- model cards, code examples, SPA

Max pages: 300

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| playwright | 60 | 22.8 | ±3.6 | 2.7 | 251 | 463 | 119 |
| crawl4ai-raw | 300 | 329.4 | ±9.4 | 0.9 | 870 | 2477 | 211 |
| crawl4ai | 300 | 359.3 | ±0.0 | 0.8 | 895 | 2487 | 191 |
| scrapy+md | 36 | 26.8 | ±33.5 | 0.7 | 354 | 281 | 238 |
| crawlee | 0 | 4.4 | ±0.3 | 0.0 | 0 | 0 | 28 |
| colly+md | 0 | 5.9 | ±0.1 | 0.0 | 0 | 0 | 270 |
| markcrawl | — | — | — | — | — | error: heartbeat stall: no new pages for 180s |

### kubernetes-docs — Kubernetes concepts + reference docs -- long-form, cross-linked

Max pages: 400

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| markcrawl | 400 | 22.9 | ±1.1 | 17.5 | 1735 | 5895 | 517 |
| scrapy+md | 314 | 44.6 | ±5.1 | 7.1 | 7832 | 10677 | 309 |
| playwright | 400 | 129.8 | ±0.1 | 3.1 | 5383 | 37973 | 362 |
| crawl4ai-raw | 400 | 220.5 | ±0.4 | 1.8 | 5354 | 45720 | 268 |
| crawl4ai | 400 | 245.6 | ±15.6 | 1.6 | 5383 | 45937 | 267 |
| crawlee | 401 | 425.2 | ±21.3 | 0.9 | 5443 | 39237 | 26 |
| colly+md | — | — | — | — | — | error: heartbeat stall: 0 pages after 120s |

### postgres-docs — PostgreSQL docs -- dense SQL reference, text-heavy

Max pages: 400

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| markcrawl | 400 | 16.8 | ±6.3 | 25.6 | 887 | 3560 | 113 |
| scrapy+md | 400 | 19.1 | ±6.4 | 22.1 | 1120 | 3503 | 225 |
| crawlee | 400 | 99.8 | ±7.6 | 4.0 | 974 | 3768 | 28 |
| playwright | 400 | 135.0 | ±63.7 | 3.3 | 969 | 3746 | 299 |
| crawl4ai-raw | 400 | 145.2 | ±4.4 | 2.8 | 962 | 5315 | 177 |
| crawl4ai | 400 | 162.5 | ±18.5 | 2.5 | 962 | 5315 | 183 |
| colly+md | — | — | — | — | — | error: heartbeat stall: 0 pages after 120s |

### mdn-css — MDN CSS reference -- property/selector pages, deeply linked

Max pages: 300

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| markcrawl | 300 | 11.3 | ±0.2 | 26.6 | 970 | 2293 | 105 |
| scrapy+md | 299 | 21.7 | ±1.0 | 13.8 | 616 | 6638 | 393 |
| playwright | 300 | 69.8 | ±8.2 | 4.3 | 4448 | 28691 | 670 |
| crawl4ai-raw | 300 | 159.9 | ±9.2 | 1.9 | 4208 | 36773 | 224 |
| crawl4ai | 300 | 211.9 | ±56.6 | 1.5 | 4208 | 36764 | 231 |
| crawlee | 300 | 396.6 | ±26.4 | 0.8 | 4162 | 28079 | 24 |
| colly+md | — | — | — | — | — | error: heartbeat stall: 0 pages after 120s |

### rust-book — The Rust Programming Language book -- chaptered tutorial

Max pages: 200

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| scrapy+md | 200 | 17.0 | ±2.2 | 11.9 | 3683 | 6760 | 73 |
| markcrawl | 200 | 18.0 | ±0.7 | 11.1 | 5440 | 10395 | 323 |
| playwright | 200 | 22.2 | ±1.2 | 9.0 | 4182 | 6939 | 516 |
| colly+md | 54 | 6.5 | ±0.1 | 8.4 | 11006 | 4564 | 670 |
| crawlee | 200 | 56.0 | ±0.9 | 3.6 | 4182 | 6939 | 73 |
| crawl4ai-raw | 200 | 62.4 | ±0.1 | 3.2 | 4062 | 8391 | 369 |
| crawl4ai | 200 | 69.6 | ±0.4 | 2.9 | 4062 | 8391 | 396 |

### newegg — Newegg electronics catalog -- product listings with pricing, clean /<slug>/p/<id> URL pattern

Max pages: 200

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| markcrawl | 200 | 38.4 | ±11.8 | 5.5 | 632 | 866 | 24 |
| playwright | 3 | 2.9 | ±0.2 | 1.0 | 1565 | 649 | 127 |
| crawl4ai | 200 | 217.7 | ±68.5 | 1.0 | 7244 | 24762 | 248 |
| crawl4ai-raw | 200 | 254.6 | ±1.1 | 0.8 | 9808 | 33981 | 273 |
| colly+md | 17 | 98.0 | ±0.0 | 0.2 | 3727 | 1397 | 433 |
| scrapy+md | 0 | 2.9 | ±0.0 | 0.0 | 0 | 0 | 25 |
| crawlee | 0 | 5.2 | ±0.7 | 0.0 | 0 | 0 | 32 |

### ikea — IKEA US furniture catalog -- product + category pages with pricing

Max pages: 200

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| scrapy+md | 186 | 43.2 | ±11.8 | 4.5 | 1546 | 4930 | 244 |
| markcrawl | 200 | 115.5 | ±0.0 | 1.7 | 1680 | 2818 | 179 |
| playwright | 200 | 192.5 | ±24.9 | 1.0 | 4853 | 27747 | 627 |
| crawlee | 201 | 205.1 | ±10.6 | 1.0 | 6400 | 34896 | 38 |
| crawl4ai-raw | 200 | 243.4 | ±19.5 | 0.8 | 2295 | 5700 | 173 |
| crawl4ai | 200 | 426.7 | ±0.0 | 0.5 | 2183 | 5247 | 189 |
| colly+md | — | — | — | — | — | error: heartbeat stall: 0 pages after 120s |

### smittenkitchen — Smitten Kitchen recipe blog -- WordPress long-form, recipe microdata

Max pages: 200

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| markcrawl | 200 | 28.0 | ±2.1 | 7.2 | 16272 | 19301 | 41 |
| playwright | 200 | 43.6 | ±0.4 | 4.6 | 3963 | 29453 | 254 |
| crawl4ai | 200 | 82.3 | ±1.2 | 2.4 | 1190 | 3494 | 197 |
| crawl4ai-raw | 200 | 83.6 | ±2.2 | 2.4 | 1184 | 3481 | 203 |
| scrapy+md | 190 | 189.6 | ±38.9 | 1.0 | 60493 | 92739 | 233 |
| crawlee | 104 | 81.7 | ±104.2 | 0.7 | 2145 | 15933 | 37 |
| colly+md | — | — | — | — | — | error: heartbeat stall: 0 pages after 120s |

### npr-news — NPR news section -- wire-style articles, deep linking, stable URLs

Max pages: 150

| Tool | Pages (a) | Time (b) | Std dev | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|---|
| crawl4ai-raw | 150 | 91.3 | ±4.3 | 1.6 | 2996 | 5290 | 427 |
| crawl4ai | 150 | 106.6 | ±0.2 | 1.4 | 2985 | 5280 | 218 |
| markcrawl | 150 | 116.8 | ±3.9 | 1.3 | 316 | 374 | 198 |
| crawlee | 150 | 179.8 | ±6.0 | 0.8 | 6629 | 24191 | 26 |
| scrapy+md | — | — | — | — | — | error: heartbeat stall: 0 pages after 120s |
| colly+md | — | — | — | — | — | error: heartbeat stall: 0 pages after 120s |
| playwright | — | — | — | — | — | error: wall-clock timeout after 360s |

> **Column definitions:** **Pages (a)** = pages discovered and fetched by this tool (varies per tool).
> **Time (b)** = wall-clock seconds to fetch and convert all pages (median of 3 iterations).
> **[1] Pages/sec** = median throughput across iterations.
> Approximately a÷b; small differences arise because each column is an independent median.
> **[2] Avg words** = mean words per page. **[3] Output KB** = total Markdown output size across all pages.
> **Std dev** = standard deviation of Time across iterations. **[4] Peak MB** = peak resident memory (RSS) during crawl.

## Overall summary

| Tool | Total pages (a) | Total time (b) | Avg pages/sec (a÷b) | Notes |
|---|---|---|---|---|
| markcrawl | 2771 | 461.2 | 6.0 | *(10/11 sites)* *(missing 579 pages)* |
| scrapy+md | 2338 | 443.5 | 5.3 | *(10/11 sites)* *(missing 1011 pages)* |
| colly+md | 862 | 275.4 | 3.1 | *(5/11 sites)* *(missing 2488 pages)* |
| playwright | 2484 | 1155.7 | 2.1 | *(10/11 sites)* *(missing 866 pages)* |
| crawl4ai-raw | 3350 | 2517.7 | 1.3 |  |
| crawlee | 2474 | 2018.7 | 1.2 | *(missing 875 pages)* |
| crawl4ai | 3350 | 2845.3 | 1.2 |  |

> **Column definitions:** **Total pages (a)** = sum of pages fetched across all sites.
> **Total time (b)** = sum of median wall-clock times across all sites. **Avg pages/sec (a÷b)** = overall throughput.

> **Note on variance:** These benchmarks fetch pages from live public websites.
> Network conditions, server load, and CDN caching can cause significant
> run-to-run variance. For the most reliable comparison,
> run multiple iterations and compare medians.

## What the results mean

HTTP-only tools (markcrawl, scrapy+md, colly+md) are consistently 2-7x faster than browser-based tools (crawl4ai, crawlee, playwright). The speed gap comes from skipping browser startup and JavaScript execution entirely.

markcrawl is fastest overall, but loses on stripe-docs (scrapy+md), huggingface-transformers (playwright), rust-book (scrapy+md), ikea (scrapy+md), npr-news (crawl4ai-raw). Site-specific results vary with server response times and content complexity.

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
