"""Crawl4AI raw runner — sequential arun(), default config (out-of-box baseline).

Tested with: crawl4ai == 0.8.6

This is the simplest possible crawl4ai usage: one page at a time with
arun(), no batching, no custom concurrency. Compare against crawl4ai_runner
which uses arun_many() for batch parallelism.

Supports two modes:
  - Discovery (url_list=None): BFS link crawl from seed URL using internal links.
  - Batch (url_list provided): fetch exactly those URLs sequentially.

Known issues:
  - Same patchright/Vercel bot detection issue as crawl4ai_runner — see that
    file for details. Sequential arun() is less likely to trigger it than
    arun_many() but still affected.
"""
from __future__ import annotations

import json
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)


def check() -> bool:
    try:
        import crawl4ai  # noqa: F401
        return True
    except ImportError:
        return False


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, **kwargs) -> int:
    """Run Crawl4AI with minimal/out-of-box settings — sequential arun(), default config."""
    import asyncio

    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

    os.makedirs(out_dir, exist_ok=True)
    pages_saved = 0
    jsonl_path = os.path.join(out_dir, "pages.jsonl")

    async def _crawl():
        nonlocal pages_saved
        in_container = os.getuid() == 0 or os.path.exists("/.dockerenv")
        extra = ["--no-sandbox", "--disable-setuid-sandbox"] if in_container else None
        browser_config = BrowserConfig(headless=True, extra_args=extra)
        run_config = CrawlerRunConfig()

        def _write_output(page_url, result):
            nonlocal pages_saved
            safe_name = page_url.replace("://", "_").replace("/", "_")[:80]
            md_path = os.path.join(out_dir, f"{safe_name}.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(result.markdown)
            with open(jsonl_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "url": page_url,
                    "title": result.metadata.get("title", "") if result.metadata else "",
                    "text": result.markdown,
                }, ensure_ascii=False) + "\n")
            pages_saved += 1

        async with AsyncWebCrawler(config=browser_config) as crawler:
            if url_list:
                # Batch mode: fetch exactly the provided URLs
                for page_url in url_list[:max_pages]:
                    try:
                        result = await crawler.arun(url=page_url, config=run_config)
                        if not result.success or not result.markdown:
                            continue
                        _write_output(page_url, result)
                    except (OSError, ValueError, KeyError, AttributeError) as exc:
                        logger.debug("crawl4ai-raw: skipping %s: %s", page_url, exc)
                        continue
            else:
                # Discovery mode: BFS crawl from seed URL
                base_domain = url.split("//")[-1].split("/")[0]
                visited = set()
                to_visit = [url]

                while to_visit and pages_saved < max_pages:
                    current_url = to_visit.pop(0)
                    if current_url in visited:
                        continue
                    visited.add(current_url)

                    try:
                        result = await crawler.arun(url=current_url, config=run_config)
                        if not result.success or not result.markdown:
                            continue
                        _write_output(current_url, result)
                        # Extract internal links for BFS
                        if hasattr(result, "links") and result.links:
                            for link_info in result.links.get("internal", []):
                                link = link_info.get("href", "") if isinstance(link_info, dict) else str(link_info)
                                if link and link not in visited and base_domain in link:
                                    to_visit.append(link)
                    except (OSError, ValueError, KeyError, AttributeError) as exc:
                        logger.debug("crawl4ai-raw: skipping %s: %s", current_url, exc)
                        continue

    asyncio.run(_crawl())
    return pages_saved
