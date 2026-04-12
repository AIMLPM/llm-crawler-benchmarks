"""Crawl4AI runner — Playwright + arun_many() with streaming.

Tested with: crawl4ai == 0.8.6

Key configuration:
  - MemoryAdaptiveDispatcher(max_session_permit=5) caps concurrent Chromium tabs.
    Default is 10-20 which causes renderer OOM on heavy pages in Docker.
  - stream=True yields results incrementally so single-page crashes don't
    block the entire batch.
  - Chromium flags reduce per-tab memory: --disable-dev-shm-usage,
    --js-flags=--max-old-space-size=256.

Known issues:
  - MemoryAdaptiveDispatcher's memory_threshold_percent has no effect in Docker
    (GitHub issue #1608). We bypass it by hard-capping max_session_permit.
  - arun_many() without streaming blocks until ALL URLs finish — one crash = 0 output.
  - [ANTIBOT] labels in crawl4ai logs are misleading — they label ALL retry-loop
    errors, including Chromium crashes that have nothing to do with bot detection.
  - Patchright (crawl4ai's Playwright fork) is intermittently blocked by Vercel
    bot detection (HTTP 403). react.dev is affected — runs flip between 221/221
    and 0/221 depending on Vercel's mood. Stock Playwright is blocked less often,
    possibly due to a different browser fingerprint. arun_many()'s concurrent tabs
    may also increase the risk of triggering rate limits.
"""
from __future__ import annotations

import json
import logging
import os
import time
from typing import List, Optional

logger = logging.getLogger(__name__)


def check() -> bool:
    try:
        import crawl4ai  # noqa: F401
        return True
    except ImportError:
        return False


def _categorize_error(result) -> str:
    """Classify a crawl4ai failure into a diagnostic category."""
    err = getattr(result, "error_message", "") or ""
    err_lower = err.lower()
    if "target crashed" in err_lower or "target closed" in err_lower:
        return "renderer_crash"
    if "timeout" in err_lower or "navigation" in err_lower:
        return "timeout"
    if not getattr(result, "markdown", None):
        return "empty_content"
    if "net::" in err_lower:
        return "network_error"
    return "other"


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, **kwargs) -> int:
    """Run Crawl4AI and return pages saved."""
    import asyncio

    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

    os.makedirs(out_dir, exist_ok=True)
    pages_saved = 0
    jsonl_path = os.path.join(out_dir, "pages.jsonl")
    telemetry_path = os.path.join(out_dir, "_telemetry.jsonl")
    crawl_start = time.time()

    # Telemetry accumulators
    telemetry_errors: dict[str, int] = {}
    telemetry_page_times: list[float] = []
    telemetry_page_sizes: list[int] = []
    telemetry_peak_rss_mb: float = 0.0

    urls_to_fetch = url_list if url_list else None

    def _sample_memory() -> float:
        """Return current process RSS in MB (includes child processes)."""
        try:
            import psutil
            proc = psutil.Process()
            rss = proc.memory_info().rss
            for child in proc.children(recursive=True):
                try:
                    rss += child.memory_info().rss
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return rss / (1024 * 1024)
        except ImportError:
            return 0.0

    def _log_telemetry(entry: dict):
        """Append a telemetry entry to the JSONL log."""
        nonlocal telemetry_peak_rss_mb
        mem_mb = _sample_memory()
        if mem_mb > telemetry_peak_rss_mb:
            telemetry_peak_rss_mb = mem_mb
        entry["rss_mb"] = round(mem_mb, 1)
        entry["elapsed_s"] = round(time.time() - crawl_start, 2)
        entry["pages_saved"] = pages_saved
        with open(telemetry_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    async def _crawl():
        nonlocal pages_saved
        in_container = os.getuid() == 0 or os.path.exists("/.dockerenv")
        extra_args = []
        if in_container:
            extra_args += ["--no-sandbox", "--disable-setuid-sandbox"]
        extra_args += [
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--js-flags=--max-old-space-size=256",
        ]
        browser_config = BrowserConfig(headless=True, extra_args=extra_args)
        run_config = CrawlerRunConfig(
            page_timeout=30000,
        )

        _log_telemetry({"event": "crawl_start", "max_pages": max_pages,
                        "url_count": len(urls_to_fetch) if urls_to_fetch else 0,
                        "mode": "batch" if urls_to_fetch else "discovery"})

        async with AsyncWebCrawler(config=browser_config) as crawler:
            if urls_to_fetch:
                from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher
                stream_config = CrawlerRunConfig(
                    page_timeout=30000,
                    stream=True,
                )
                dispatcher = MemoryAdaptiveDispatcher(
                    max_session_permit=5,
                )
                page_seq = 0
                async for result in await crawler.arun_many(
                    urls=urls_to_fetch[:max_pages],
                    config=stream_config,
                    dispatcher=dispatcher,
                ):
                    page_start = time.time()
                    page_seq += 1
                    try:
                        if not result.success or not result.markdown:
                            cat = _categorize_error(result)
                            telemetry_errors[cat] = telemetry_errors.get(cat, 0) + 1
                            _log_telemetry({
                                "event": "page_fail", "seq": page_seq,
                                "url": getattr(result, "url", "?"),
                                "category": cat,
                                "error": (getattr(result, "error_message", "") or "")[:200],
                            })
                            continue
                        md_size = len(result.markdown.encode("utf-8"))
                        telemetry_page_sizes.append(md_size)
                        _write_output(out_dir, jsonl_path, result.url, result)
                        pages_saved += 1
                        page_dur = time.time() - page_start
                        telemetry_page_times.append(page_dur)
                        _log_telemetry({
                            "event": "page_ok", "seq": page_seq,
                            "url": result.url,
                            "md_bytes": md_size,
                            "page_s": round(page_dur, 3),
                        })
                    except Exception as exc:
                        telemetry_errors["exception"] = telemetry_errors.get("exception", 0) + 1
                        _log_telemetry({
                            "event": "page_exception", "seq": page_seq,
                            "url": getattr(result, "url", "?"),
                            "error": str(exc)[:200],
                        })
                        continue
            else:
                visited = set()
                to_visit = [url]
                while to_visit and pages_saved < max_pages:
                    current_url = to_visit.pop(0)
                    if current_url in visited:
                        continue
                    visited.add(current_url)
                    page_start = time.time()
                    try:
                        result = await crawler.arun(url=current_url, config=run_config)
                        if not result.success or not result.markdown:
                            cat = _categorize_error(result)
                            telemetry_errors[cat] = telemetry_errors.get(cat, 0) + 1
                            _log_telemetry({
                                "event": "page_fail", "url": current_url,
                                "category": cat,
                                "error": (getattr(result, "error_message", "") or "")[:200],
                            })
                            continue
                        md_size = len(result.markdown.encode("utf-8"))
                        telemetry_page_sizes.append(md_size)
                        _write_output(out_dir, jsonl_path, current_url, result)
                        pages_saved += 1
                        page_dur = time.time() - page_start
                        telemetry_page_times.append(page_dur)
                        _log_telemetry({
                            "event": "page_ok", "url": current_url,
                            "md_bytes": md_size, "page_s": round(page_dur, 3),
                        })
                        if hasattr(result, "links") and result.links:
                            base_domain = url.split("//")[-1].split("/")[0]
                            for link_info in result.links.get("internal", []):
                                link = link_info.get("href", "") if isinstance(link_info, dict) else str(link_info)
                                if link and link not in visited and base_domain in link:
                                    to_visit.append(link)
                    except (OSError, ValueError, KeyError, AttributeError) as exc:
                        telemetry_errors["exception"] = telemetry_errors.get("exception", 0) + 1
                        _log_telemetry({
                            "event": "page_exception", "url": current_url,
                            "error": str(exc)[:200],
                        })
                        continue

        # Write telemetry summary
        summary = {
            "event": "crawl_end",
            "pages_saved": pages_saved,
            "pages_failed": sum(telemetry_errors.values()),
            "error_categories": telemetry_errors,
            "total_s": round(time.time() - crawl_start, 2),
            "peak_rss_mb": round(telemetry_peak_rss_mb, 1),
        }
        if telemetry_page_times:
            summary["avg_page_s"] = round(sum(telemetry_page_times) / len(telemetry_page_times), 3)
            summary["max_page_s"] = round(max(telemetry_page_times), 3)
        if telemetry_page_sizes:
            summary["avg_md_bytes"] = int(sum(telemetry_page_sizes) / len(telemetry_page_sizes))
            summary["max_md_bytes"] = max(telemetry_page_sizes)
        _log_telemetry(summary)

        summary_path = os.path.join(out_dir, "_telemetry_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    def _write_output(out_dir, jsonl_path, page_url, result):
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

    asyncio.run(_crawl())
    return pages_saved
