# Runner Interface

Each crawler tool has a runner module in this directory. To add a new tool,
create a Python file that exposes two functions:

## Required functions

### `check() -> bool`

Returns `True` if the tool is installed and available. The benchmark
orchestrator calls this to skip unavailable tools gracefully.

```python
def check() -> bool:
    try:
        import your_tool  # noqa: F401
        return True
    except ImportError:
        return False
```

### `run(url, out_dir, max_pages, url_list=None, concurrency=1, **kwargs) -> int`

Run the crawl and return the number of pages saved.

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | `str` | The seed URL for discovery mode |
| `out_dir` | `str` | Directory to write output files |
| `max_pages` | `int` | Maximum pages to fetch |
| `url_list` | `list[str] \| None` | Explicit list of URLs to fetch (no discovery). `None` = discovery mode (default in benchmarks) |
| `concurrency` | `int` | Number of concurrent fetches |

**Discovery mode (`url_list=None`)** is the default in benchmarks. Each runner
must support BFS link crawling from the seed URL, staying on the same domain,
up to `max_pages`. The `url_list` parameter is retained for testing and batch
scenarios.

## Output format

The runner must write two things to `out_dir`:

1. **Markdown files** -- one `.md` file per page (any naming scheme).
2. **`pages.jsonl`** -- one JSON object per line with at least:
   ```json
   {"url": "https://example.com/page", "title": "Page Title", "content": "# Markdown content..."}
   ```

## Registration

After creating your runner, add it to `runners/__init__.py`:

```python
from runners import your_tool_runner

TOOLS = {
    ...
    "your-tool": {"check": your_tool_runner.check, "run": your_tool_runner.run},
}
```

If your tool uses a browser (Playwright/Chromium), also add it to `BROWSER_TOOLS`.

## Existing runners

| Runner | Tool | Type |
|--------|------|------|
| `markcrawl_runner.py` | markcrawl | HTTP (async httpx) |
| `scrapy_runner.py` | scrapy+md | HTTP (Scrapy) |
| `crawl4ai_runner.py` | crawl4ai | Browser (Playwright) |
| `crawl4ai_raw_runner.py` | crawl4ai-raw | Browser (Playwright) |
| `colly_runner.py` | colly+md | HTTP (Go binary) |
| `crawlee_runner.py` | crawlee | Browser (Playwright) |
| `playwright_runner.py` | playwright | Browser (Playwright) |
| `firecrawl_runner.py` | firecrawl | Browser (self-hosted) |
