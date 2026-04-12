"""Colly + markdownify runner — Go fetch (Colly) + Python markdownify.

Tested with: colly_crawler Go binary (built from tools/colly_crawler/)

Colly handles HTTP fetching at Go speed. Python markdownify converts the
downloaded HTML to Markdown.

Known issues:
  - The Go binary originally had no retry logic for HTTP 429 and zero delay
    between requests, causing most pages to be dropped on rate-limiting sites
    (github.blog: 19/200, stripe-docs: 194/500). Fixed by adding 100ms delay
    and retry-on-429 with backoff (max 3 retries). Colly itself supports retry
    natively — this was a gap in our binary, not a colly limitation.
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def _colly_bin_works(path: str) -> bool:
    """Return True if the colly binary at *path* can execute on this platform."""
    try:
        subprocess.run(
            [path, "-h"], capture_output=True, timeout=5, check=False,
        )
        return True
    except (OSError, subprocess.TimeoutExpired):
        return False


def _find_colly_bin() -> Optional[str]:
    """Find a colly binary that is executable on the current platform."""
    candidates = [
        "/usr/local/bin/colly_crawler",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools", "colly_crawler", "colly_crawler"),
    ]
    for path in candidates:
        if os.path.isfile(path) and _colly_bin_works(path):
            return path
    return None


def check() -> bool:
    return _find_colly_bin() is not None


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, **kwargs) -> int:
    """Run Colly (Go) for fetching + Python markdownify for conversion."""
    os.makedirs(out_dir, exist_ok=True)

    colly_bin = _find_colly_bin()
    if not colly_bin:
        return 0
    html_dir = os.path.join(out_dir, "_html")
    os.makedirs(html_dir, exist_ok=True)

    cmd = [colly_bin, "-url", url, "-out", html_dir, "-max", str(max_pages)]

    effective_urls = url_list[:max_pages] if url_list else [url]
    url_map: Dict[str, str] = {}
    for u in effective_urls:
        safe = u.replace("://", "_").replace("/", "_")[:80]
        url_map[safe] = u

    url_map_path = os.path.join(out_dir, "_url_map.json")
    with open(url_map_path, "w", encoding="utf-8") as f:
        json.dump(url_map, f)

    if url_list:
        urls_file = os.path.join(out_dir, "_urls.txt")
        with open(urls_file, "w") as f:
            f.write("\n".join(url_list))
        cmd.extend(["-urls", urls_file])

    colly_result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, check=False)
    if colly_result.stderr:
        logger.warning(f"[colly] stderr: {colly_result.stderr[:2000]}")

    from markdownify import markdownify as md

    pages_saved = 0
    jsonl_path = os.path.join(out_dir, "pages.jsonl")

    for html_file in sorted(Path(html_dir).glob("*.html")):
        html_content = html_file.read_text(encoding="utf-8", errors="ignore")
        markdown = md(html_content, heading_style="ATX", strip=["img", "script", "style", "nav", "footer"])

        if len(markdown.split()) < 5:
            continue

        md_path = os.path.join(out_dir, html_file.stem + ".md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        stem = html_file.stem
        if stem in url_map:
            page_url = url_map[stem]
        elif stem.startswith("https_"):
            page_url = "https://" + stem[6:].replace("_", "/")
        elif stem.startswith("http_"):
            page_url = "http://" + stem[5:].replace("_", "/")
        else:
            page_url = stem.replace("_", "/")

        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "url": page_url,
                "title": "",
                "text": markdown,
            }, ensure_ascii=False) + "\n")

        pages_saved += 1

    return pages_saved
