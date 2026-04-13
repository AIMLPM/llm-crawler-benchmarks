# MarkCrawl Self-Benchmark (MarkCrawl only — no competitors)
<!-- style: v2, 2026-04-13 -->

> **Looking for the head-to-head comparison vs Crawl4AI and Scrapy?** See [SPEED_COMPARISON.md](SPEED_COMPARISON.md).

MarkCrawl achieves 17.60 pages/sec across 728 pages with 100% title extraction and citation completeness across all 4 test sites.

This report measures MarkCrawl's own performance and extraction quality.
No other tools are involved — this is a self-assessment of speed, content quality, and output completeness.

Generated: 2026-04-13 10:28:01 UTC

## What this measures

Each benchmark runs the **full MarkCrawl pipeline** end-to-end:

```
1. Discover URLs     — fetch robots.txt, parse sitemap or follow links
2. Fetch pages       — HTTP GET each URL (adaptive throttle, delay=0 base)
3. Clean HTML        — strip <nav>, <footer>, <script>, <style>, cookie banners
4. Convert to Markdown — transform cleaned HTML via markdownify
5. Write .md files   — one file per page with citation header
6. Write JSONL index — append url, title, crawled_at, citation, text per page
```

**Pages/second** includes all six steps — network fetch is typically the
bottleneck, not HTML parsing or Markdown conversion. Benchmarks run with
`delay=0` (adaptive throttle only). MarkCrawl automatically backs off
if the server is slow or returns 429 rate-limit responses.

Source: [`benchmark_markcrawl.py`](benchmark_markcrawl.py)

## Summary

- **Sites tested:** 4
- **Total pages crawled:** 728
- **Total time:** 41.4s
- **Overall pages/second:** 17.60

## Performance

### Medium (15-30 pages) — 668 pages in 37.1s (18.0 p/s), 22073 KB output

| Site | Description | Pages (a) | Time (b) | Pages/sec (a÷b) | Avg words [1] | Output KB [2] | Peak MB [3] |
|---|---|---|---|---|---|---|---|
| fastapi-docs | FastAPI framework docs (API docs with code examples, tutorials) | 153 | 11.4 | 13.40 | 2084 | 2952 | 0 |
| python-docs | Python standard library index + module pages | 500 | 22.1 | 22.63 | 3766 | 19103 | 0 |
| quotes-toscrape | Paginated quotes (tests link-following across 10+ pages) | 15 | 3.6 | 4.15 | 199 | 19 | 0 |

### Large (50-100 pages) — 60 pages in 4.2s (14.2 p/s), 155 KB output

| Site | Description | Pages (a) | Time (b) | Pages/sec (a÷b) | Avg words [1] | Output KB [2] | Peak MB [3] |
|---|---|---|---|---|---|---|---|
| books-toscrape | E-commerce catalog (50+ product pages, pagination, categories) | 60 | 4.2 | 14.19 | 339 | 155 | 0 |


## Extraction Quality

| Site | Junk detected | Title rate | Citation rate | JSONL complete |
|---|---|---|---|---|
| fastapi-docs | 2 | 100% | 100% | 100% |
| python-docs | 75 | 100% | 100% | 100% |
| quotes-toscrape | 0 | 100% | 100% | 100% |
| books-toscrape | 0 | 100% | 100% | 100% |

## Quality Scores

| Metric | Score | Target | Status |
|---|---|---|---|
| Title extraction rate | 100% | >90% | PASS |
| Citation completeness | 100% | 100% | PASS |
| JSONL field completeness | 100% | 100% | PASS |
| Junk in output | 77 matches | 0 | NEEDS WORK |
| Min pages crawled | all met | all sites | PASS |

> **Column definitions:** **Metric** = what is being tested. **Score** = actual measured value. **Target** = minimum acceptable threshold. **Status** = PASS if score meets target, NEEDS WORK if not.

## Junk Detection Details

### fastapi-docs
- cookie.?banner: 1 match(es)
- cookie.?consent: 1 match(es)

### python-docs
- ©\s*\d{4}.*all rights reserved: 3 match(es)
- all rights reserved: 3 match(es)
- ©\s*\d{4}.*all rights reserved: 4 match(es)
- all rights reserved: 5 match(es)
- ©\s*\d{4}.*all rights reserved: 4 match(es)
- all rights reserved: 5 match(es)
- ©\s*\d{4}.*all rights reserved: 4 match(es)
- all rights reserved: 5 match(es)
- all rights reserved: 1 match(es)
- ©\s*\d{4}.*all rights reserved: 3 match(es)


## What these metrics mean

### Performance table

- **Pages (a)**: Total pages crawled for the site.
- **Time (b)**: Wall-clock seconds for the full crawl (all 6 pipeline steps).
- **Pages/sec (a÷b)**: Crawl throughput. Affected by network, server response time, and `--delay`.
- **[1] Avg words**: Mean words per page (total words ÷ page count).
- **[2] Output KB**: Total Markdown output size across all pages.
- **[3] Peak MB**: Peak resident memory (RSS) during crawl.

### Extraction quality table

- **Junk detected**: Total count of navigation, footer, script, or cookie text found across all pages. Should be 0.
- **Title rate**: Percentage of pages where a `<title>` was successfully extracted.
- **Citation rate**: Percentage of JSONL rows with a complete citation string.
- **JSONL complete**: Percentage of JSONL rows with all required fields (url, title, path, crawled_at, citation, tool, text).

## Reproducing these results

```bash
pip install markcrawl
python benchmark_markcrawl.py
```
