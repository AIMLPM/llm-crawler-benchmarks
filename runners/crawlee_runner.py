"""Crawlee runner — Playwright-based Python crawling framework.

Tested with: crawlee[playwright] (unpinned)

Each call runs in a subprocess to get a fresh event loop, avoiding the
asyncio.Lock/event-loop mismatch that occurs when crawlee is invoked
multiple times in the same process (Python 3.13 regression in crawlee's
storage client).

Known issues:
  - Intermittent 0-page results on Vercel-hosted sites (react.dev) due to bot
    detection — same root cause as crawl4ai/patchright. Playwright-framework
    tools are affected more than raw Playwright.
  - Subprocess timeout must scale with max_pages. Previously hardcoded at 300s,
    which killed the process before large crawls (500 pages) could finish.
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

_CRAWLEE_WORKER = Path(__file__).parent.parent / "crawlee_worker.py"


def check() -> bool:
    try:
        import crawlee  # noqa: F401
        return True
    except ImportError:
        return False


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, **kwargs) -> int:
    """Run Crawlee (Python) with Playwright in a subprocess."""
    os.makedirs(out_dir, exist_ok=True)
    cmd = [sys.executable, str(_CRAWLEE_WORKER), url, out_dir, str(max_pages)]
    if url_list:
        cmd.extend(url_list[:max_pages])
    timeout = 60 + 2 * max_pages
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        if result.stderr:
            logger.warning(f"[crawlee stderr] {result.stderr[:500]}")
        last_line = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else "0"
        return int(last_line)
    except subprocess.TimeoutExpired:
        logger.warning(f"[crawlee] timed out after {timeout}s")
        return 0
    except ValueError:
        return 0
