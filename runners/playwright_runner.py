"""Raw Playwright runner — browser fetch + markdownify, no framework overhead.

Tested with: playwright (unpinned)

This is the raw Playwright baseline: direct browser control, no crawling
framework. Blocks images/CSS/fonts to measure pure HTML→Markdown speed.

Supports two modes:
  - Discovery (url_list=None): BFS link crawl from seed URL, same-domain only.
  - Batch (url_list provided): fetch exactly those URLs, no link following.
"""
from __future__ import annotations

import json
import logging
import os
from collections import deque
from typing import List, Optional
from urllib.parse import urlparse, urljoin

logger = logging.getLogger(__name__)


def check() -> bool:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        return True
    except ImportError:
        return False


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, **kwargs) -> int:
    """Raw Playwright baseline — browser fetch + markdownify, no framework overhead."""
    from playwright.sync_api import sync_playwright, Error as PlaywrightError

    os.makedirs(out_dir, exist_ok=True)
    pages_saved = 0
    jsonl_path = os.path.join(out_dir, "pages.jsonl")

    from markdownify import markdownify as md

    with sync_playwright() as p:
        launch_args = [
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-dev-shm-usage",
            "--no-first-run",
        ]
        if os.getuid() == 0 or os.path.exists("/.dockerenv"):
            launch_args.extend(["--no-sandbox", "--disable-setuid-sandbox"])
        browser = p.chromium.launch(headless=True, args=launch_args)

        context = browser.new_context()
        context.route("**/*.{png,jpg,jpeg,gif,webp,svg,ico}", lambda route: route.abort())
        context.route("**/*.{css,less,scss}", lambda route: route.abort())
        context.route("**/*.{woff,woff2,ttf,otf,eot}", lambda route: route.abort())
        page = context.new_page()

        if url_list:
            # Batch mode: fetch exactly the provided URLs
            urls_to_fetch = url_list[:max_pages]
        else:
            # Discovery mode: BFS crawl from seed URL
            urls_to_fetch = None

        def _save_page(page_url, html, title):
            nonlocal pages_saved
            markdown = md(html, heading_style="ATX", strip=["img", "script", "style", "nav", "footer"])
            if len(markdown.split()) < 5:
                return
            safe_name = page_url.replace("://", "_").replace("/", "_")[:80]
            md_path = os.path.join(out_dir, f"{safe_name}.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown)
            with open(jsonl_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "url": page_url,
                    "title": title,
                    "text": markdown,
                }, ensure_ascii=False) + "\n")
            pages_saved += 1

        if urls_to_fetch is not None:
            # Batch mode
            for page_url in urls_to_fetch:
                try:
                    page.goto(page_url, timeout=15000, wait_until="domcontentloaded")
                    _save_page(page_url, page.content(), page.title())
                except (PlaywrightError, OSError) as exc:
                    logger.debug("playwright: skipping %s: %s", page_url, exc)
        else:
            # Discovery mode: BFS link crawl
            base_domain = urlparse(url).netloc
            visited = set()
            queue = deque([url])

            while queue and pages_saved < max_pages:
                current_url = queue.popleft()
                if current_url in visited:
                    continue
                visited.add(current_url)

                try:
                    page.goto(current_url, timeout=15000, wait_until="domcontentloaded")
                    html = page.content()
                    title = page.title()
                except (PlaywrightError, OSError) as exc:
                    logger.debug("playwright: skipping %s: %s", current_url, exc)
                    continue

                _save_page(current_url, html, title)

                # Extract links and enqueue same-domain ones
                try:
                    hrefs = page.eval_on_selector_all(
                        "a[href]",
                        "(elements) => elements.map(e => e.href)",
                    )
                    for href in hrefs:
                        abs_url = urljoin(current_url, href).split("#")[0]
                        if urlparse(abs_url).netloc == base_domain and abs_url not in visited:
                            queue.append(abs_url)
                except PlaywrightError:
                    pass

        context.close()
        browser.close()

    return pages_saved
