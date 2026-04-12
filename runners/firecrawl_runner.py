"""FireCrawl runner — SaaS API or self-hosted Docker.

Tested with: firecrawl-py (unpinned, v2 API)

Requires either:
  - FIRECRAWL_API_KEY env var (SaaS API — free tier available)
  - FIRECRAWL_API_URL env var (self-hosted via docker-compose)

Free tier has a 3 req/min rate limit — we retry with backoff.
Self-hosted: scrapes one URL at a time (batch_scrape crashes self-hosted).

Known issues (self-hosted):
  - react.dev fails with "Internal Server Error: Failed to scrape". Self-hosted
    only has the open-source playwright engine (quality=20). The SaaS API has
    the proprietary fire-engine with chrome-cdp and stealth proxies (quality=50),
    which would likely succeed. react.dev serves SSR HTML (markcrawl gets all
    pages with plain HTTP), so this is a container resource/config issue, not a
    JS rendering limitation per se.
  - stripe-docs stalls after ~4 pages due to Stripe rate-limiting/blocking the
    single self-hosted IP. The SaaS API uses distributed IPs and would largely
    avoid this. However, ~7 of ~500 Stripe pages exceed the V8 heap limit on
    any firecrawl configuration (SaaS included).
  - batch_scrape() crashes on self-hosted — we fall back to sequential
    single-URL scraping with 0.5s delay between pages.
"""
from __future__ import annotations

import json
import logging
import os
import re as _re
import time
from typing import List, Optional

logger = logging.getLogger(__name__)


def check() -> bool:
    """Check if FireCrawl is available and the API key is valid.

    Sets ``check.status`` with a human-readable detail string.
    """
    check.status = ""

    try:
        import firecrawl  # noqa: F401
    except ImportError:
        check.status = "firecrawl-py not installed"
        return False

    api_key = os.environ.get("FIRECRAWL_API_KEY")
    api_url = os.environ.get("FIRECRAWL_API_URL")

    if not (api_key or api_url):
        check.status = "FIRECRAWL_API_KEY not set"
        return False

    if api_url:
        check.status = f"self-hosted ({api_url})"
        return True

    fc_kwargs = {}
    if api_key:
        fc_kwargs["api_key"] = api_key
    if api_url:
        fc_kwargs["api_url"] = api_url

    try:
        app = firecrawl.FirecrawlApp(**fc_kwargs)
        usage = app.get_credit_usage()
    except Exception as exc:
        msg = str(exc)
        if "401" in msg or "Unauthorized" in msg:
            check.status = "invalid API key"
        else:
            check.status = f"API error: {msg[:100]}"
        return False

    try:
        remaining = getattr(usage, "remaining_credits", None)
        total = getattr(usage, "plan_credits", None)

        if remaining is None and isinstance(usage, dict):
            remaining = usage.get("remaining_credits", usage.get("remaining"))
            total = usage.get("plan_credits", usage.get("total"))

        if remaining is not None:
            check.status = f"{remaining:,}/{total or '?'} credits remaining"
            if remaining <= 0:
                check.status += " — NO CREDITS LEFT"
                return False
        else:
            check.status = "key valid (could not determine credits)"
    except (TypeError, KeyError, AttributeError):
        check.status = "key valid (could not parse credit info)"

    return True

check.status = ""


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, **kwargs) -> int:
    """Run FireCrawl and return pages saved."""
    from firecrawl import FirecrawlApp
    from firecrawl.v2.types import ScrapeOptions

    api_key = os.environ.get("FIRECRAWL_API_KEY")
    api_url = os.environ.get("FIRECRAWL_API_URL")

    fc_kwargs = {}
    if api_url:
        fc_kwargs["api_url"] = api_url
    elif api_key:
        fc_kwargs["api_key"] = api_key
    app = FirecrawlApp(**fc_kwargs)

    os.makedirs(out_dir, exist_ok=True)
    jsonl_path = os.path.join(out_dir, "pages.jsonl")

    max_retries = 5
    rate_limit_wait = 0.0
    is_self_hosted = bool(api_url)

    pages_saved = 0
    all_data: list = []
    urls_to_scrape = url_list[:max_pages] if url_list else None

    def _write_page(page) -> bool:
        """Write a single page's output. Returns True if saved."""
        nonlocal pages_saved
        markdown = getattr(page, "markdown", "") or ""
        meta = getattr(page, "metadata", None)
        page_url = getattr(meta, "source_url", "") or getattr(meta, "url", "") or ""
        title = getattr(meta, "title", "") or ""

        if not markdown or len(markdown.split()) < 5:
            return False

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
        return True

    def _scrape_single(page_url: str) -> object:
        """Scrape one URL with retry logic. Returns a Document or None."""
        for attempt in range(max_retries):
            try:
                return app.scrape(page_url, formats=["markdown"])
            except Exception as exc:
                msg = str(exc)
                is_rate_limit = "Rate Limit" in msg
                is_connection = any(s in msg for s in (
                    "Connection aborted", "RemoteDisconnected",
                    "ConnectionError", "ConnectionReset",
                ))
                if not is_rate_limit and not is_connection:
                    raise
                wait = (int(_re.search(r"retry after (\d+)s", msg).group(1)) + 2
                        if is_rate_limit and _re.search(r"retry after (\d+)s", msg)
                        else 10 * (attempt + 1))
                if attempt < max_retries - 1:
                    nonlocal rate_limit_wait
                    rate_limit_wait += wait
                    time.sleep(wait)
                else:
                    logger.warning(f"    [firecrawl] gave up on {page_url} after {max_retries} attempts")
                    return None
        return None

    if urls_to_scrape and is_self_hosted:
        # Self-hosted: scrape one URL at a time, write output immediately
        # so the heartbeat sees progress (avoids zero-output stall timeout).
        for i, page_url in enumerate(urls_to_scrape):
            doc = _scrape_single(page_url)
            if doc is not None:
                _write_page(doc)
            if (i + 1) % 50 == 0:
                logger.info(f"    [firecrawl] {i + 1}/{len(urls_to_scrape)} pages scraped")
            time.sleep(0.5)
    elif urls_to_scrape:
        # SaaS API: batch_scrape is reliable and faster
        for attempt in range(max_retries):
            try:
                result = app.batch_scrape(urls_to_scrape, formats=["markdown"])
                all_data.extend(getattr(result, "data", []) or [])
                break
            except Exception as exc:
                msg = str(exc)
                is_rate_limit = "Rate Limit" in msg
                is_connection = any(s in msg for s in (
                    "Connection aborted", "RemoteDisconnected",
                    "ConnectionError", "ConnectionReset",
                ))
                if not is_rate_limit and not is_connection:
                    raise
                wait = (int(_re.search(r"retry after (\d+)s", msg).group(1)) + 2
                        if is_rate_limit and _re.search(r"retry after (\d+)s", msg)
                        else 10 * (attempt + 1))
                if attempt < max_retries - 1:
                    logger.warning(f"    [firecrawl] retrying batch_scrape, waiting {wait}s (attempt {attempt + 1}/{max_retries})...")
                    rate_limit_wait += wait
                    time.sleep(wait)
                else:
                    raise
        # Write batch results
        for page in all_data:
            _write_page(page)
    else:
        # No URL list — let firecrawl crawl/discover on its own
        for attempt in range(max_retries):
            try:
                result = app.crawl(
                    url,
                    limit=max_pages,
                    scrape_options=ScrapeOptions(formats=["markdown"]),
                )
                all_data.extend(getattr(result, "data", []) or [])
                break
            except Exception as exc:
                msg = str(exc)
                is_rate_limit = "Rate Limit" in msg
                if not is_rate_limit:
                    raise
                match = _re.search(r"retry after (\d+)s", msg)
                wait = int(match.group(1)) + 2 if match else 15
                if attempt < max_retries - 1:
                    logger.warning(f"    [firecrawl] rate limited, waiting {wait}s (attempt {attempt + 1}/{max_retries})...")
                    rate_limit_wait += wait
                    time.sleep(wait)
                else:
                    raise
        # Write crawl results
        for page in all_data:
            _write_page(page)

    # Stash wait time where run_single can find it
    run._rate_limit_wait = rate_limit_wait

    return pages_saved
