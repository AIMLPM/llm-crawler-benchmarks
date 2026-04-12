"""MarkCrawl runner — requests + BeautifulSoup + markdownify.

Tested with: markcrawl >= 0.1.0
"""
from __future__ import annotations

import os
import json
from typing import List, Optional


def check() -> bool:
    try:
        from markcrawl.core import crawl  # noqa: F401
        return True
    except ImportError:
        return False


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, concurrency: int = 1, **kwargs) -> int:
    """Run MarkCrawl and return pages saved."""
    from markcrawl.core import crawl

    if url_list:
        from markcrawl.core import CrawlEngine

        os.makedirs(out_dir, exist_ok=True)
        engine = CrawlEngine(
            out_dir=out_dir, fmt="markdown", min_words=5, delay=0,
            timeout=15, concurrency=concurrency, include_subdomains=False,
            user_agent=None, render_js=False, proxy=None, show_progress=False,
        )
        jsonl_path = os.path.join(out_dir, "pages.jsonl")
        with open(jsonl_path, "w", encoding="utf-8") as jsonl_file:
            for page_url in url_list:
                resp = engine.fetch_page(page_url)
                page_data = engine.process_response(page_url, resp)
                if page_data:
                    engine.save_page(page_data, jsonl_file)
        engine.close()
        return engine.saved_count
    else:
        result = crawl(
            base_url=url,
            out_dir=out_dir,
            fmt="markdown",
            max_pages=max_pages,
            delay=0,
            timeout=15,
            show_progress=False,
            min_words=5,
        )
        return result.pages_saved
