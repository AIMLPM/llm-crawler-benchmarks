"""Raw Playwright runner — browser fetch + markdownify, no framework overhead.

Tested with: playwright (unpinned)

This is the raw Playwright baseline: direct browser control, no crawling
framework. Blocks images/CSS/fonts to measure pure HTML→Markdown speed.
"""
from __future__ import annotations

import json
import logging
import os
from typing import List, Optional

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
    urls_to_fetch = url_list if url_list else [url]
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
        for page_url in urls_to_fetch[:max_pages]:
            try:
                page.goto(page_url, timeout=15000, wait_until="domcontentloaded")
                html = page.content()
                title = page.title()
            except (PlaywrightError, OSError) as exc:
                logger.debug("playwright: skipping %s: %s", page_url, exc)
                continue

            markdown = md(html, heading_style="ATX", strip=["img", "script", "style", "nav", "footer"])
            if len(markdown.split()) < 5:
                continue

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

        context.close()
        browser.close()

    return pages_saved
