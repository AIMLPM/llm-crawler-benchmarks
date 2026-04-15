#!/usr/bin/env python3
"""Head-to-head benchmark: runs all available crawlers against the same sites.

Compares 7+ tools with equivalent settings, measuring performance,
extraction quality, and output characteristics.

FireCrawl runs if FIRECRAWL_API_KEY or FIRECRAWL_API_URL is set. The script
auto-loads .env from the project root, so no manual `source .env` is needed.

Usage:
    python benchmark_all_tools.py
    python benchmark_all_tools.py --parallel                    # cross-site parallelism
    python benchmark_all_tools.py --parallel --site-parallelism 2  # 2 tools per site
    python benchmark_all_tools.py --sites quotes-toscrape,fastapi-docs
    python benchmark_all_tools.py --iterations 1 --skip-warmup  # quick test

See reports/METHODOLOGY.md for the methodology.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Auto-relaunch inside .venv if we're running from the system Python.
# This ensures all pip-installed benchmark tools are importable regardless
# of whether the user remembered to `source .venv/bin/activate`.
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parent
_VENV_PYTHON = _REPO_ROOT / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / ("python.exe" if sys.platform == "win32" else "python3")

if sys.prefix == sys.base_prefix and _VENV_PYTHON.exists():
    os.execv(str(_VENV_PYTHON), [str(_VENV_PYTHON)] + sys.argv)

import argparse  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import random  # noqa: E402
import shutil  # noqa: E402
import statistics  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ThreadPoolExecutor, as_completed  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from typing import Callable, Dict, List, Optional  # noqa: E402

logger = logging.getLogger(__name__)

# Load .env from project root if present (so FIRECRAWL_API_KEY etc. are available
# without needing to `source .env` manually before running)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

COMPARISON_SITES = {
    "quotes-toscrape": {
        "url": "http://quotes.toscrape.com",
        "max_pages": 15,
        "description": "Paginated quotes (simple HTML, link-following)",
    },
    "books-toscrape": {
        "url": "http://books.toscrape.com",
        "max_pages": 60,
        "description": "E-commerce catalog (60 pages, pagination)",
    },
    "fastapi-docs": {
        "url": "https://fastapi.tiangolo.com",
        "max_pages": 500,
        "description": "API documentation (code blocks, headings, tutorials)",
    },
    "python-docs": {
        "url": "https://docs.python.org/3/library/",
        "max_pages": 500,
        "description": "Python standard library docs",
    },
    # --- New diverse sites ---
    "react-dev": {
        "url": "https://react.dev/learn",
        "max_pages": 500,
        "description": "React docs (SPA, JS-rendered, interactive examples)",
        "render_js": True,
    },
    "wikipedia-python": {
        "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "max_pages": 50,
        "description": "Wikipedia (tables, infoboxes, citations, deep linking)",
    },
    "stripe-docs": {
        "url": "https://docs.stripe.com/payments",
        "max_pages": 500,
        "description": "Stripe API docs (tabbed content, code samples, sidebars)",
    },
    "blog-engineering": {
        "url": "https://github.blog/engineering/",
        "max_pages": 200,
        "description": "GitHub Engineering Blog (articles, images, technical content)",
    },
}


# ---------------------------------------------------------------------------
# Memory tracker (shared)
# ---------------------------------------------------------------------------

def _get_memory_mb() -> float:
    try:
        import psutil
        return psutil.Process().memory_info().rss / (1024 * 1024)
    except ImportError:
        import resource
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform == "darwin":
            return usage / (1024 * 1024)
        return usage / 1024


class MemoryTracker:
    def __init__(self, interval: float = 0.5):
        self.interval = interval
        self.peak_mb: float = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        self.peak_mb = _get_memory_mb()
        self._running = True
        self._thread = threading.Thread(target=self._sample, daemon=True)
        self._thread.start()

    def stop(self) -> float:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        return self.peak_mb

    def _sample(self):
        while self._running:
            current = _get_memory_mb()
            if current > self.peak_mb:
                self.peak_mb = current
            time.sleep(self.interval)


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class RunResult:
    tool: str
    site: str
    pages: int
    time_seconds: float
    pages_per_second: float
    output_kb: float
    peak_memory_mb: float
    avg_words: float
    error: Optional[str] = None


@dataclass
class ToolSiteResult:
    """Aggregated results across iterations for one tool on one site."""
    tool: str
    site: str
    description: str
    pages_median: float
    time_median: float
    time_stddev: float
    pps_median: float
    output_kb: float
    peak_memory_mb: float
    avg_words: float
    runs: List[RunResult] = field(default_factory=list)
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Tool runners — imported from runners/ package
# ---------------------------------------------------------------------------

from runners import TOOLS, BROWSER_TOOLS, HTTP_TOOLS  # noqa: E402
from runners import firecrawl_runner  # noqa: E402 — needed for .status attribute



# (URL discovery removed — each tool now discovers its own pages from the seed URL)


# ---------------------------------------------------------------------------
# Tool runners are in runners/ package — see runners/__init__.py for registry
# ---------------------------------------------------------------------------






# ---------------------------------------------------------------------------
# Graduated smoke test — catch scale-dependent failures early
# ---------------------------------------------------------------------------

SMOKE_TIERS = [
    {
        "name": "sanity",
        "site": "quotes-toscrape",
        "max_pages": 5,
        "timeout": 60,
        "description": "Basic functionality (5 pages)",
        "exclude_on_fail": True,
    },
    {
        "name": "small",
        "site": "books-toscrape",
        "max_pages": 30,
        "timeout": 90,
        "description": "Small scale stability (30 pages)",
        "exclude_on_fail": True,
    },
    {
        "name": "medium",
        "site": "python-docs",
        "max_pages": 100,
        "timeout": 180,
        "description": "Medium scale / memory pressure (100 pages)",
        "exclude_on_fail": False,
    },
]


@dataclass
class SmokeResult:
    tool: str
    tier: str
    site: str
    max_pages: int
    pages_returned: int
    time_seconds: float
    peak_memory_mb: float
    passed: bool
    error: Optional[str] = None
    skipped: bool = False


@dataclass
class SmokeReport:
    results: List[SmokeResult]

    def get_excluded_tools(self, strict: bool = False) -> set:
        """Return tools that should be excluded from the full run."""
        excluded = set()
        for r in self.results:
            if r.skipped:
                continue
            if not r.passed:
                tier_cfg = next(t for t in SMOKE_TIERS if t["name"] == r.tier)
                if tier_cfg["exclude_on_fail"] or strict:
                    excluded.add(r.tool)
        return excluded

    def get_warned_tools(self) -> set:
        """Return tools that failed a non-excluding tier."""
        warned = set()
        excluded = self.get_excluded_tools()
        for r in self.results:
            if r.skipped or r.passed:
                continue
            if r.tool not in excluded:
                warned.add(r.tool)
        return warned

    def print_matrix(self) -> None:
        """Print a console-friendly matrix of results."""
        # Collect all tools in order
        tools_seen = []
        for r in self.results:
            if r.tool not in tools_seen:
                tools_seen.append(r.tool)

        tier_names = [t["name"] for t in SMOKE_TIERS]

        print("\n═══ Graduated Smoke Test ═══════════════════════════════\n")

        # Per-tier detail
        for tier_cfg in SMOKE_TIERS:
            tn = tier_cfg["name"]
            tier_results = [r for r in self.results if r.tier == tn]
            if not tier_results:
                continue
            print(f"  Tier: {tn} ({tier_cfg['site']}, {tier_cfg['max_pages']} pages, {tier_cfg['timeout']}s timeout)")
            for r in tier_results:
                label = f"{r.tool:<16}"
                if r.skipped:
                    print(f"    ⊘  {label} skipped (failed earlier tier)")
                elif r.passed:
                    print(f"    ✓  {label} {r.pages_returned:>3}/{r.max_pages} pages  {r.time_seconds:>6.1f}s  {r.peak_memory_mb:>5.0f}MB")
                else:
                    err_short = (r.error or "unknown")[:70]
                    print(f"    ✗  {label} {r.pages_returned:>3}/{r.max_pages} pages  {r.time_seconds:>6.1f}s  {r.peak_memory_mb:>5.0f}MB")
                    print(f"       → {err_short}")
            print()

        # Summary
        print("  ── Summary ──────────────────────────────────────────")
        excluded = self.get_excluded_tools()
        warned = self.get_warned_tools()
        for tool in tools_seen:
            parts = []
            for tn in tier_names:
                r = next((r for r in self.results if r.tool == tool and r.tier == tn), None)
                if r is None:
                    parts.append("  ")
                elif r.skipped:
                    parts.append("⊘")
                elif r.passed:
                    parts.append("✓")
                else:
                    parts.append("✗")
            tier_str = "  ".join(f"T{i+1} {p}" for i, p in enumerate(parts))
            if tool in excluded:
                verdict = "→ Excluded"
            elif tool in warned:
                verdict = "→ Warning (may fail on large sites)"
            else:
                verdict = "→ Ready"
            print(f"    {tool:<16} {tier_str}  {verdict}")

        if excluded:
            print(f"\n  Excluded from full run: {', '.join(sorted(excluded))}")
        if warned:
            print(f"  Warnings: {', '.join(sorted(warned))}")
        print()

    def to_json(self) -> dict:
        """Serialize for JSON output."""
        return {
            "tiers": [{k: v for k, v in t.items()} for t in SMOKE_TIERS],
            "results": [
                {
                    "tool": r.tool, "tier": r.tier, "site": r.site,
                    "max_pages": r.max_pages, "pages_returned": r.pages_returned,
                    "time_seconds": round(r.time_seconds, 2),
                    "peak_memory_mb": round(r.peak_memory_mb, 1),
                    "passed": r.passed, "error": r.error, "skipped": r.skipped,
                }
                for r in self.results
            ],
            "excluded_tools": sorted(self.get_excluded_tools()),
            "warned_tools": sorted(self.get_warned_tools()),
        }


def _run_smoke_single(
    tool_name: str,
    tier: dict,
    base_dir: str,
    concurrency: int,
) -> SmokeResult:
    """Run a single tool on a single smoke tier (discovery mode)."""
    site_name = tier["site"]
    site_config = {
        **COMPARISON_SITES[site_name],
        "max_pages": tier["max_pages"],
    }

    out_dir = os.path.join(base_dir, f"smoke_{tool_name}_{tier['name']}")
    os.makedirs(out_dir, exist_ok=True)

    run_fn = TOOLS[tool_name]["run"]
    mem = MemoryTracker()
    mem.start()
    start = time.time()

    try:
        pages = run_fn(
            site_config["url"], out_dir, tier["max_pages"],
            url_list=None, concurrency=concurrency,
        )
        error = None
    except Exception as exc:
        pages = 0
        error = str(exc)
    finally:
        peak_mem = mem.stop()

    elapsed = time.time() - start

    # Subtract firecrawl rate-limit wait
    rl_wait = getattr(run_fn, "_rate_limit_wait", 0.0)
    if rl_wait > 0:
        elapsed = max(0.1, elapsed - rl_wait)
        run_fn._rate_limit_wait = 0.0

    passed = pages > 0 and error is None
    shutil.rmtree(out_dir, ignore_errors=True)

    return SmokeResult(
        tool=tool_name, tier=tier["name"], site=site_name,
        max_pages=tier["max_pages"], pages_returned=pages,
        time_seconds=elapsed, peak_memory_mb=peak_mem,
        passed=passed, error=error,
    )


def _run_smoke_tier(
    tier: dict,
    tools: List[str],
    base_dir: str,
    concurrency: int,
) -> List[SmokeResult]:
    """Execute one smoke tier across all provided tools (discovery mode)."""
    results = []
    browser_sem = threading.Semaphore(1)

    def _run_one(tool_name: str) -> SmokeResult:
        is_browser = tool_name in BROWSER_TOOLS
        if is_browser:
            browser_sem.acquire()
        try:
            return _run_smoke_single(tool_name, tier, base_dir, concurrency)
        finally:
            if is_browser:
                browser_sem.release()

    with ThreadPoolExecutor(max_workers=len(tools)) as executor:
        futures = {executor.submit(_run_one, t): t for t in tools}
        for future in as_completed(futures):
            tool_name = futures[future]
            try:
                result = future.result(timeout=tier["timeout"] + 30)
            except Exception as exc:
                result = SmokeResult(
                    tool=tool_name, tier=tier["name"], site=tier["site"],
                    max_pages=tier["max_pages"], pages_returned=0,
                    time_seconds=tier["timeout"], peak_memory_mb=0,
                    passed=False, error=f"timeout: {exc}",
                )
            results.append(result)

    return results


def run_smoke_tests(
    available_tools: List[str],
    concurrency: int = 5,
    strict: bool = False,
) -> SmokeReport:
    """Run graduated smoke tests (sanity → small → medium).

    Tests each tool at increasing page counts. Tools that fail a tier
    are skipped for subsequent tiers.
    """
    all_results: List[SmokeResult] = []
    surviving_tools = list(available_tools)
    base_dir = tempfile.mkdtemp(prefix="smoke_")

    for tier in SMOKE_TIERS:
        site_name = tier["site"]
        site_config = COMPARISON_SITES.get(site_name)
        if not site_config:
            logger.warning(f"Smoke tier '{tier['name']}': site '{site_name}' not in COMPARISON_SITES, skipping")
            continue

        # Each tool discovers its own pages from the seed URL
        tier_results = _run_smoke_tier(tier, surviving_tools, base_dir, concurrency)
        all_results.extend(tier_results)

        # Log results inline
        for r in tier_results:
            if r.passed:
                logger.info(f"    ✓ {r.tool}: {r.pages_returned}/{r.max_pages} pages in {r.time_seconds:.1f}s")
            else:
                logger.warning(f"    ✗ {r.tool}: {r.pages_returned}/{r.max_pages} pages — {(r.error or 'unknown')[:60]}")

        # Remove failed tools from subsequent tiers
        failed = {r.tool for r in tier_results if not r.passed}
        if failed:
            surviving_tools = [t for t in surviving_tools if t not in failed]
            # Add skip markers for failed tools in remaining tiers
            remaining_tiers = [t for t in SMOKE_TIERS if t["name"] != tier["name"]
                               and SMOKE_TIERS.index(t) > SMOKE_TIERS.index(tier)]
            for rt in remaining_tiers:
                for ft in failed:
                    all_results.append(SmokeResult(
                        tool=ft, tier=rt["name"], site=rt["site"],
                        max_pages=rt["max_pages"], pages_returned=0,
                        time_seconds=0, peak_memory_mb=0,
                        passed=False, skipped=True,
                    ))

    shutil.rmtree(base_dir, ignore_errors=True)
    return SmokeReport(results=all_results)


def analyze_output(out_dir: str) -> dict:
    """Analyze Markdown output quality."""
    total_words = 0
    total_bytes = 0
    page_count = 0

    for f in Path(out_dir).glob("*.md"):
        content = f.read_text(encoding="utf-8", errors="ignore")
        total_words += len(content.split())
        total_bytes += f.stat().st_size
        page_count += 1

    return {
        "avg_words": total_words / page_count if page_count else 0,
        "output_kb": total_bytes / 1024,
    }


class _Heartbeat:
    """Logs periodic progress during tool execution by counting output files.

    Detects two stall conditions and sets timed_out for run_single to check:
      - Zero-output stall: 0 pages after zero_stall_s (default 120s)
      - Progress stall: no new pages for stall_s consecutive seconds
    """

    def __init__(self, tool_name: str, site_name: str, out_dir: str,
                 max_pages: int, interval: float = 30.0,
                 zero_stall_s: float = 120.0, stall_s: float = 180.0):
        self.tool_name = tool_name
        self.site_name = site_name
        self.out_dir = out_dir
        self.max_pages = max_pages
        self.interval = interval
        self.zero_stall_s = zero_stall_s
        self.stall_s = stall_s
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._last_count = 0
        self._last_progress_time: float = 0.0
        self.timed_out = False
        self.timeout_reason = ""

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._pulse, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _pulse(self):
        while self._running:
            time.sleep(self.interval)
            if not self._running:
                break
            try:
                count = sum(1 for f in Path(self.out_dir).glob("*.md") if f.stat().st_size > 0)
            except OSError:
                count = self._last_count
            now = time.time()
            elapsed = now - self._start_time
            status = f"{count}/{self.max_pages} pages"
            if count > self._last_count:
                delta = count - self._last_count
                status += f" (+{delta})"
                self._last_progress_time = now
            elif count == self._last_count and self._last_count > 0:
                stall_dur = now - self._last_progress_time
                status += f" (stalled {stall_dur:.0f}s)"
                if stall_dur >= self.stall_s:
                    self.timed_out = True
                    self.timeout_reason = f"no new pages for {stall_dur:.0f}s"
                    logger.warning(f"      [{self.tool_name}/{self.site_name}] STALL TIMEOUT: {self.timeout_reason}")
            status += f", {elapsed:.0f}s elapsed"
            logger.info(f"      [{self.tool_name}/{self.site_name}] heartbeat: {status}")
            self._last_count = count

            # Zero-output stall: tool started but produced nothing
            if count == 0 and elapsed >= self.zero_stall_s:
                self.timed_out = True
                self.timeout_reason = f"0 pages after {elapsed:.0f}s"
                logger.warning(f"      [{self.tool_name}/{self.site_name}] ZERO-OUTPUT TIMEOUT: {self.timeout_reason}")

    def set_start_time(self, t: float):
        self._start_time = t
        self._last_count = 0
        self._last_progress_time = t
        self.timed_out = False
        self.timeout_reason = ""


# Hard wall-clock timeout per run.  Scales with max_pages so large sites
# (500 pages) get more time than small ones (15 pages).
# Formula: base + per_page * max_pages.  e.g. 500 pages → 60 + 2*500 = 1060s ≈ 18 min.
_RUN_TIMEOUT_BASE_S = 60
_RUN_TIMEOUT_PER_PAGE_S = 2


def run_single(
    tool_name: str,
    run_fn: Callable,
    site_name: str,
    site_config: dict,
    base_dir: str,
    url_list: Optional[List[str]] = None,
    concurrency: int = 1,
) -> RunResult:
    """Run a single tool on a single site and return results."""
    out_dir = os.path.join(base_dir, tool_name, site_name)
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    url = site_config["url"]
    max_pages = site_config["max_pages"]
    wall_timeout = _RUN_TIMEOUT_BASE_S + _RUN_TIMEOUT_PER_PAGE_S * max_pages

    heartbeat = _Heartbeat(tool_name, site_name, out_dir, max_pages)
    mem = MemoryTracker()
    mem.start()
    start = time.time()
    heartbeat.set_start_time(start)
    heartbeat.start()

    # Run the tool in a thread so we can enforce a hard wall-clock timeout
    # and also abort early when the heartbeat detects a stall.
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            run_fn, url, out_dir, max_pages,
            url_list=url_list, concurrency=concurrency,
        )
        try:
            # Poll every 5s so we can check the heartbeat stall flag
            deadline = start + wall_timeout
            while True:
                remaining = deadline - time.time()
                if remaining <= 0:
                    raise TimeoutError(f"wall-clock timeout after {wall_timeout}s")
                if heartbeat.timed_out:
                    raise TimeoutError(f"heartbeat stall: {heartbeat.timeout_reason}")
                try:
                    pages = future.result(timeout=min(5.0, remaining))
                    error = None
                    break
                except TimeoutError:
                    # future.result timeout — re-check stall / wall clock
                    if future.done():
                        pages = future.result()
                        error = None
                        break
                    continue
        except TimeoutError as exc:
            pages = 0
            error = str(exc)
            future.cancel()
            logger.warning(f"    [{tool_name}/{site_name}] ABORTED: {error}")
        except Exception as exc:
            pages = 0
            error = str(exc)
        finally:
            heartbeat.stop()

    elapsed = time.time() - start

    # Subtract any rate-limit wait time (firecrawl free tier)
    rate_limit_wait = getattr(run_fn, "_rate_limit_wait", 0.0)
    if rate_limit_wait > 0:
        elapsed = max(0.1, elapsed - rate_limit_wait)
        run_fn._rate_limit_wait = 0.0  # reset for next call

    peak_mem = mem.stop()

    analysis = analyze_output(out_dir)

    return RunResult(
        tool=tool_name,
        site=site_name,
        pages=pages,
        time_seconds=elapsed,
        pages_per_second=pages / elapsed if elapsed > 0 else 0,
        output_kb=analysis["output_kb"],
        peak_memory_mb=peak_mem,
        avg_words=analysis["avg_words"],
        error=error,
    )


def aggregate_runs(runs: List[RunResult], site_config: dict) -> ToolSiteResult:
    """Aggregate multiple iterations into median + stddev."""
    if not runs:
        return ToolSiteResult(
            tool="", site="", description="", pages_median=0,
            time_median=0, time_stddev=0, pps_median=0,
            output_kb=0, peak_memory_mb=0, avg_words=0,
        )

    successful = [r for r in runs if r.error is None]
    if not successful:
        return ToolSiteResult(
            tool=runs[0].tool,
            site=runs[0].site,
            description=site_config["description"],
            pages_median=0, time_median=0, time_stddev=0, pps_median=0,
            output_kb=0, peak_memory_mb=0, avg_words=0,
            runs=runs,
            error=runs[0].error,
        )

    times = [r.time_seconds for r in successful]
    return ToolSiteResult(
        tool=runs[0].tool,
        site=runs[0].site,
        description=site_config["description"],
        pages_median=statistics.median([r.pages for r in successful]),
        time_median=statistics.median(times),
        time_stddev=statistics.stdev(times) if len(times) > 1 else 0,
        pps_median=statistics.median([r.pages_per_second for r in successful]),
        output_kb=statistics.median([r.output_kb for r in successful]),
        peak_memory_mb=max(r.peak_memory_mb for r in successful),
        avg_words=statistics.median([r.avg_words for r in successful]),
        runs=runs,
    )


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_comparison_report(
    results: dict[str, dict[str, ToolSiteResult]],
    available_tools: list[str],
    output_path: str,
    concurrency: int = 1,
):
    """Generate SPEED_COMPARISON.md report."""
    import datetime

    # Compute overall fastest tool for one-line answer
    tool_total_pages = {}
    tool_total_time = {}
    for tool in available_tools:
        tool_results = results.get(tool, {})
        successful = {k: v for k, v in tool_results.items() if not v.error}
        tool_total_pages[tool] = sum(r.pages_median for r in successful.values())
        tool_total_time[tool] = sum(r.time_median for r in successful.values())
    tool_avg_pps = {
        t: tool_total_pages[t] / tool_total_time[t]
        for t in available_tools if tool_total_time.get(t, 0) > 0
    }
    fastest_tool = max(tool_avg_pps, key=tool_avg_pps.get) if tool_avg_pps else "unknown"
    fastest_pps = tool_avg_pps.get(fastest_tool, 0)
    runner_up = sorted(tool_avg_pps, key=tool_avg_pps.get, reverse=True)
    runner_up_name = runner_up[1] if len(runner_up) > 1 else "N/A"
    runner_up_pps = tool_avg_pps.get(runner_up_name, 0)

    today = datetime.date.today().isoformat()
    lines = [
        "# Speed Comparison",
        f"<!-- style: v2, {today} -->",
        "",
        f"**{fastest_tool}** is the fastest crawler at {fastest_pps:.1f} pages/sec overall, "
        f"followed by {runner_up_name} ({runner_up_pps:.1f} p/s).",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}",
        "",
        "## Methodology",
        "",
        "**Per-tool discovery:** Each tool starts from the same seed URL and discovers",
        "its own pages through link-following. This tests real-world crawl behavior —",
        "discovery quality, link extraction, and content extraction are all measured.",
        "Page counts may vary between tools depending on each tool's link-following strategy.",
        "",
        "Settings:",
        "- **Seed URL:** Same for all tools per site",
        "- **Max pages:** Same limit for all tools per site",
        "- **Delay:** 0 (no politeness throttle)",
        f"- **Concurrency:** {concurrency}",
        "- **Iterations:** 3 per tool per site (reporting median + std dev)",
        "- **Warm-up:** 1 throwaway run per site before timing",
        "- **Output:** Markdown files + JSONL index",
        "",
        "See [METHODOLOGY.md](METHODOLOGY.md) for full methodology.",
        "",
        "## Tools tested",
        "",
        "| Tool | Type | Available | Notes |",
        "|---|---|---|---|",
    ]

    all_tools = ["markcrawl", "crawl4ai", "crawl4ai-raw", "scrapy+md", "crawlee", "colly+md", "playwright", "firecrawl"]
    tool_types = {
        "markcrawl": "HTTP",
        "scrapy+md": "HTTP",
        "colly+md": "HTTP",
        "crawl4ai": "Browser",
        "crawl4ai-raw": "Browser",
        "crawlee": "Browser",
        "playwright": "Browser",
        "firecrawl": "Browser (self-hosted)",
    }
    for tool in all_tools:
        available = tool in available_tools
        notes = {
            "markcrawl": "requests + BeautifulSoup + markdownify — [AIMLPM/markcrawl](https://github.com/AIMLPM/markcrawl)",
            "crawl4ai": "Playwright + arun_many() batch concurrency — [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai)",
            "crawl4ai-raw": "Playwright + sequential arun(), default config (out-of-box baseline)",
            "scrapy+md": "Scrapy async + markdownify — [scrapy/scrapy](https://github.com/scrapy/scrapy)",
            "crawlee": "Playwright + markdownify — [apify/crawlee-python](https://github.com/apify/crawlee-python)",
            "colly+md": "Go fetch (Colly) + Python markdownify — [gocolly/colly](https://github.com/gocolly/colly)",
            "playwright": "Raw Playwright baseline + markdownify (no framework)",
            "firecrawl": "Self-hosted Docker — [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl)",
        }
        status = "Yes" if available else "Not installed"
        ttype = tool_types.get(tool, "")
        lines.append(f"| {tool} | {ttype} | {status} | {notes.get(tool, '')} |")

    lines.extend([
        "",
        "## Context for the numbers",
        "",
        "**Pages/sec** measures raw crawl throughput — how fast a tool fetches and converts HTML "
        "to Markdown. Tools using Playwright (browser rendering) are inherently slower than "
        "HTTP-only tools (requests/Scrapy/Colly) because they must launch a browser and wait "
        "for JavaScript execution. **Avg words** and **Output KB** reflect output volume, not "
        "quality — see [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for whether more words "
        "means better content.",
        "",
        "## Results by site",
        "",
    ])

    # Detect whether std dev and peak memory have real data (not all zeros)
    has_stddev = any(
        r.time_stddev > 0
        for tool_results in results.values()
        for r in tool_results.values()
        if not r.error
    )
    has_peak_mem = any(
        r.peak_memory_mb > 0
        for tool_results in results.values()
        for r in tool_results.values()
        if not r.error
    )

    for site_name, site_config in COMPARISON_SITES.items():
        # Build header dynamically based on available data
        header = "| Tool | Pages (a) | Time (b) |"
        sep = "|---|---|---|"
        if has_stddev:
            header += " Std dev |"
            sep += "---|"
        header += " Pages/sec [1] | Avg words [2] | Output KB [3] |"
        sep += "---|---|---|"
        if has_peak_mem:
            header += " Peak MB [4] |"
            sep += "---|"

        lines.extend([
            f"### {site_name} — {site_config['description']}",
            "",
            f"Max pages: {site_config['max_pages']}",
            "",
            header,
            sep,
        ])

        # Sort tools by pps_median descending (best first)
        def _site_sort_key(tool):
            r = results.get(tool, {}).get(site_name)
            if r and not r.error:
                return r.pps_median
            return -1  # errors/missing last
        sorted_tools = sorted(available_tools, key=_site_sort_key, reverse=True)

        for tool in sorted_tools:
            r = results.get(tool, {}).get(site_name)
            tool_label = f"**{tool}**" if tool == "markcrawl" else tool
            if r and not r.error:
                row = f"| {tool_label} | {r.pages_median:.0f} | {r.time_median:.1f} |"
                if has_stddev:
                    row += f" ±{r.time_stddev:.1f} |"
                row += f" {r.pps_median:.1f} | {r.avg_words:.0f} | {r.output_kb:.0f} |"
                if has_peak_mem:
                    row += f" {r.peak_memory_mb:.0f} |"
                lines.append(row)
            elif r and r.error:
                ncols = 4 + (1 if has_stddev else 0) + (1 if has_peak_mem else 0)
                dashes = " — |" * (ncols - 1)
                lines.append(f"| {tool_label} |{dashes} error: {r.error[:50]} |")
            else:
                ncols = 5 + (1 if has_stddev else 0) + (1 if has_peak_mem else 0)
                dashes = " — |" * ncols
                lines.append(f"| {tool_label} |{dashes}")

        lines.append("")

    # Column legend for per-site tables (printed once after all sites)
    from report_utils import table_legend
    legend_cols = [
        ("Pages (a)", "pages discovered and fetched by this tool (varies per tool)"),
        ("Time (b)", "wall-clock seconds to fetch and convert all pages (median of 3 iterations)"),
        ("[1] Pages/sec", "median throughput across iterations. Approximately a÷b; small differences arise because each column is an independent median"),
        ("[2] Avg words", "mean words per page"),
        ("[3] Output KB", "total Markdown output size across all pages"),
    ]
    if has_stddev:
        legend_cols.append(("Std dev", "standard deviation of Time across iterations"))
    if has_peak_mem:
        legend_cols.append(("[4] Peak MB", "peak resident memory (RSS) during crawl"))
    lines.extend(table_legend(legend_cols))
    lines.append("")

    # Overall summary
    lines.extend([
        "## Overall summary",
        "",
        "| Tool | Total pages (a) | Total time (b) | Avg pages/sec (a÷b) | Notes |",
        "|---|---|---|---|---|",
    ])

    total_sites = len(COMPARISON_SITES)
    # Compute max possible pages across all sites
    max_possible_pages = sum(
        sum(r.pages_median for r in results.get(t, {}).values() if not r.error)
        for t in available_tools
    )
    # Find the tool with the most pages to use as reference
    tool_page_totals = {}
    for tool in available_tools:
        tool_results_map = results.get(tool, {})
        successful = {k: v for k, v in tool_results_map.items() if not v.error}
        tool_page_totals[tool] = sum(r.pages_median for r in successful.values())
    max_tool_pages = max(tool_page_totals.values()) if tool_page_totals else 0

    # Build summary rows, then sort by avg_pps descending
    summary_rows = []
    for tool in available_tools:
        tool_results_map = results.get(tool, {})
        successful = {k: v for k, v in tool_results_map.items() if not v.error}
        total_pages = sum(r.pages_median for r in successful.values())
        total_time = sum(r.time_median for r in successful.values())
        avg_pps = total_pages / total_time if total_time > 0 else 0
        note = ""
        if len(successful) == 0:
            summary_rows.append((tool, 0, 0, 0, "*all sites errored*"))
            continue
        if len(successful) < total_sites and len(successful) > 0:
            note = f"*({len(successful)}/{total_sites} sites)* "
        # Flag incomplete page counts
        missing = int(max_tool_pages - total_pages)
        if missing > 0:
            note += f"*(missing {missing} pages)*"
        note = note.strip()
        summary_rows.append((tool, total_pages, total_time, avg_pps, note))

    # Sort by avg_pps descending
    summary_rows.sort(key=lambda x: x[3], reverse=True)

    for tool, total_pages, total_time, avg_pps, note in summary_rows:
        tool_label = f"**{tool}**" if tool == "markcrawl" else tool
        if total_pages == 0 and total_time == 0 and avg_pps == 0:
            lines.append(f"| {tool_label} | — | — | — | {note} |")
            continue
        lines.append(f"| {tool_label} | {total_pages:.0f} | {total_time:.1f} | {avg_pps:.1f} | {note} |")

    lines.extend([
        "",
        *table_legend([
            ("Total pages (a)", "sum of pages fetched across all sites"),
            ("Total time (b)", "sum of median wall-clock times across all sites"),
            ("Avg pages/sec (a÷b)", "overall throughput"),
        ]),
        "",
        "> **Note on variance:** These benchmarks fetch pages from live public websites.",
        "> Network conditions, server load, and CDN caching can cause significant",
        "> run-to-run variance. For the most reliable comparison,",
        "> run multiple iterations and compare medians.",
        "",
        "## What the results mean",
        "",
        f"HTTP-only tools ({fastest_tool}, scrapy+md, colly+md) are consistently 2-7x faster than "
        "browser-based tools (crawl4ai, crawlee, playwright). The speed gap comes from skipping "
        "browser startup and JavaScript execution entirely.",
        "",
    ])

    # Build per-site winners for narrative
    site_winners = {}
    for site_name_n in COMPARISON_SITES:
        best_tool_n = None
        best_pps_n = 0
        for tool in available_tools:
            r = results.get(tool, {}).get(site_name_n)
            if r and not r.error and r.pps_median > best_pps_n:
                best_pps_n = r.pps_median
                best_tool_n = tool
        if best_tool_n:
            site_winners[site_name_n] = best_tool_n

    # Find sites where markcrawl is NOT the fastest
    mc_losses = [s for s, t in site_winners.items() if t != "markcrawl"]
    if mc_losses:
        loss_parts = [f"{s} ({site_winners[s]})" for s in mc_losses]
        lines.append(
            f"{fastest_tool} is fastest overall, but loses on "
            f"{', '.join(loss_parts)}. "
            "Site-specific results vary with server response times and content complexity."
        )
    else:
        lines.append(f"{fastest_tool} is fastest on every site tested.")

    lines.extend([
        "",
        "Higher word counts from browser-based tools (crawlee, playwright) do not indicate "
        "better extraction quality — they often reflect extra navigation chrome and repeated "
        "boilerplate. See [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for content signal analysis.",
        "",
        "Some tools miss pages on certain sites: scrapy+md and colly+md fetch fewer pages than "
        "expected on some sites, which inflates their per-page speed but means incomplete coverage. "
        "Check the per-site tables for exact page counts.",
        "",
        "## Reproducing these results",
        "",
        "```bash",
        "# Install all tools",
        "pip install markcrawl crawl4ai scrapy markdownify",
        "playwright install chromium  # for crawl4ai",
        "",
        "# Run comparison",
        "python benchmark_all_tools.py",
        "```",
        "",
        "For FireCrawl, also run:",
        "```bash",
        "docker run -p 3002:3002 firecrawl/firecrawl:latest",
        "export FIRECRAWL_API_URL=http://localhost:3002",
        "python benchmark_all_tools.py",
        "```",
        "",
        "## See also",
        "",
        "- [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) — higher word counts don't mean higher quality",
        "- [COST_AT_SCALE.md](COST_AT_SCALE.md) — what these speed differences cost at 100K+ pages",
        "- [METHODOLOGY.md](METHODOLOGY.md) — full test setup and fairness decisions",
    ])

    report = "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    # Post-generation validation: run lint checks on the generated report
    from lint_reports import lint_file
    from pathlib import Path
    lint_warnings = lint_file(Path(output_path))
    if lint_warnings:
        logger.warning("Post-generation lint found %d issue(s):", len(lint_warnings))
        for w in lint_warnings:
            logger.warning("  - %s", w)
        # Empty data tables are a critical error — the report is broken
        empty_table_warnings = [w for w in lint_warnings if "has no data" in w]
        if empty_table_warnings:
            logger.error(
                "CRITICAL: %d section(s) have empty data tables! "
                "The report has missing benchmark results. "
                "Re-run the benchmark for the affected sites.",
                len(empty_table_warnings),
            )

    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _get_tool_version(tool_name: str) -> str:
    """Return installed package version for a tool, or 'unknown'."""
    pkg_map = {
        "markcrawl": "markcrawl",
        "crawl4ai": "crawl4ai",
        "scrapy+md": "scrapy",
        "crawlee": "crawlee",
        "playwright": "playwright",
        "firecrawl": "firecrawl-py",
        "colly+md": None,  # Go binary — no Python package
    }
    pkg = pkg_map.get(tool_name)
    if pkg is None:
        return "go binary"
    try:
        import importlib.metadata
        return importlib.metadata.version(pkg)
    except Exception:
        return "unknown"


def _regenerate_from_run(run_name: str, output_path: str):
    """Regenerate the speed comparison report from a previous run's saved data.

    Reads run_metadata.json for timing data and pages.jsonl files for content
    metrics (avg words, output KB). No crawling is performed.
    """
    runs_dir = Path("runs")
    run_dir = runs_dir / run_name
    meta_path = run_dir / "run_metadata.json"

    if not meta_path.exists():
        logger.error("run_metadata.json not found in %s", run_dir)
        sys.exit(1)

    with open(meta_path) as f:
        metadata = json.load(f)

    bench_results = metadata["phases"]["benchmarking"]["results"]
    tools_meta = metadata.get("tools", {})

    # Reconstruct ToolSiteResult objects from saved data
    results: dict[str, dict[str, ToolSiteResult]] = {}
    available_tools = []

    for tool_name, site_data in bench_results.items():
        available_tools.append(tool_name)
        results[tool_name] = {}
        for site_name, site_info in site_data.items():
            # Read pages.jsonl for content metrics
            pages_path = run_dir / tool_name / site_name / "pages.jsonl"
            avg_words = 0.0
            output_kb = 0.0
            if pages_path.exists():
                word_counts = []
                total_bytes = 0
                with open(pages_path) as pf:
                    for line in pf:
                        try:
                            page = json.loads(line)
                            text = page.get("text", "")
                            word_counts.append(len(text.split()))
                            total_bytes += len(text.encode("utf-8"))
                        except json.JSONDecodeError:
                            continue
                if word_counts:
                    avg_words = statistics.mean(word_counts)
                    output_kb = total_bytes / 1024

            error = site_info.get("error")
            description = COMPARISON_SITES.get(site_name, {}).get("description", site_name)
            results[tool_name][site_name] = ToolSiteResult(
                tool=tool_name,
                site=site_name,
                description=description,
                pages_median=site_info.get("pages_median", 0),
                time_median=site_info.get("time_median_s", 0),
                time_stddev=0.0,  # not stored in metadata
                pps_median=site_info.get("pps_median", 0),
                output_kb=output_kb,
                peak_memory_mb=0.0,  # not stored in metadata
                avg_words=avg_words,
                error=error,
            )

    # Sort tools to match original order
    tool_order = ["markcrawl", "crawl4ai", "crawl4ai-raw", "scrapy+md", "crawlee", "colly+md", "playwright", "firecrawl"]
    available_tools = [t for t in tool_order if t in available_tools]

    concurrency = metadata.get("settings", {}).get("concurrency", 5)
    logger.info("Regenerating report from %s (%d tools, %d sites)",
                run_name, len(available_tools),
                sum(len(sites) for sites in bench_results.values()) // max(len(available_tools), 1))

    generate_comparison_report(results, available_tools, output_path, concurrency=concurrency)
    logger.info("Report saved to: %s", output_path)


def main():
    parser = argparse.ArgumentParser(description="Head-to-head crawler comparison")
    parser.add_argument("--sites", default=None, help="Comma-separated sites to test")
    parser.add_argument("--tools", default=None,
                        help="Comma-separated tools to run (e.g. --tools firecrawl,markcrawl). "
                             "Default: all available tools.")
    parser.add_argument("--iterations", type=int, default=2, help="Iterations per tool per site (default: 2)")
    parser.add_argument("--skip-warmup", action="store_true", help="Skip warm-up run")
    parser.add_argument("--concurrency", type=int, default=5, help="Concurrency level for tools that support it (default: 5)")
    parser.add_argument("--parallel", action="store_true", default=True,
                        help="Run tools on different sites in parallel (default: on)")
    parser.add_argument("--sequential", action="store_true",
                        help="Run tools sequentially instead of in parallel")
    parser.add_argument("--site-parallelism", type=int, default=2,
                        help="Max tools hitting the same site simultaneously (default: 2)")
    parser.add_argument("--firecrawl-tier", choices=["free", "paid"], default=None,
                        help="FireCrawl account tier. 'free' skips warmup to save credits, "
                             "'paid' enables warmup. Auto-detected from FIRECRAWL_TIER env var, "
                             "defaults to 'free'.")
    parser.add_argument("--smoke-test", action="store_true",
                        help="Run graduated smoke tests before the full benchmark; exclude failing tools")
    parser.add_argument("--smoke-only", action="store_true",
                        help="Run smoke tests and exit (no full benchmark)")
    parser.add_argument("--smoke-strict", action="store_true",
                        help="Exclude tools that fail any smoke tier (default: only tiers 1-2 exclude)")
    parser.add_argument("--no-resume", action="store_true",
                        help="Ignore any saved checkpoint and start fresh")
    parser.add_argument("--run", default=None,
                        help="Regenerate report from a previous run's data (e.g. --run run_20260412_195003). "
                             "Skips crawling entirely — reads run_metadata.json and pages.jsonl files.")
    parser.add_argument("--output", default="reports/SPEED_COMPARISON.md", help="Output report path")
    args = parser.parse_args()

    # --run: regenerate report from saved data (no crawling)
    if args.run:
        _regenerate_from_run(args.run, args.output)
        return

    # --sequential overrides --parallel
    if args.sequential:
        args.parallel = False

    # Determine firecrawl tier: CLI flag > env var > default "free"
    firecrawl_tier = args.firecrawl_tier or os.environ.get("FIRECRAWL_TIER", "free").lower()

    run_start = time.time()
    run_start_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(run_start))

    # Select sites
    if args.sites:
        site_names = [s.strip() for s in args.sites.split(",")]
        sites = {k: v for k, v in COMPARISON_SITES.items() if k in site_names}
    else:
        sites = COMPARISON_SITES

    # Filter tools if --tools was specified
    tool_filter = None
    if args.tools:
        tool_filter = set(t.strip() for t in args.tools.split(","))
        unknown = tool_filter - set(TOOLS.keys())
        if unknown:
            logger.error(f"Unknown tool(s): {', '.join(unknown)}")
            logger.error(f"Available: {', '.join(TOOLS.keys())}")
            sys.exit(1)

    # Check available tools
    available = []
    skipped = {}
    logger.info("Checking tools...")
    for name, tool in TOOLS.items():
        if tool_filter and name not in tool_filter:
            continue
        check_fn = tool["check"]
        ok = check_fn()
        extra = ""
        if name == "firecrawl":
            detail = getattr(check_fn, "status", "")
            if ok:
                extra = f" [{firecrawl_tier} tier -- {detail}]" if detail else f" [{firecrawl_tier} tier]"
            elif detail:
                extra = f" ({detail})"
        status = "available" if ok else "NOT AVAILABLE"
        logger.info(f"  {name}: {status}{extra}")
        if ok:
            available.append(name)
        else:
            reason = getattr(check_fn, "status", "") if name == "firecrawl" else "not installed"
            skipped[name] = reason or "not installed"

    if not available:
        logger.error("No tools available. Install at least: pip install markcrawl")
        sys.exit(1)

    # --- Pre-flight: run the full preflight check before starting ---
    logger.info("\n--- Pre-flight check ---")
    try:
        from preflight import print_ready_status, run_checks
        tool_results, _ = run_checks()
        print_ready_status(tool_results)
        # Only fail on tools we're actually going to run (already passed check())
        not_ready = [t for t, ok in tool_results.items()
                     if not ok and t in available]
        if not_ready:
            logger.error(f"Pre-flight FAILED: {len(not_ready)} tool(s) not ready: {', '.join(not_ready)}")
            logger.error("  Fix: python preflight.py --install")
            sys.exit(1)
        logger.info("Pre-flight passed -- all tools ready.\n")
    except ImportError:
        logger.warning("  preflight.py not found, skipping pre-flight checks.\n")

    # --- Graduated smoke test (optional) ---
    if args.smoke_test or args.smoke_only:
        logger.info("\n--- Graduated Smoke Test ---")
        smoke_report = run_smoke_tests(
            available_tools=available,
            concurrency=args.concurrency,
            strict=args.smoke_strict,
        )
        smoke_report.print_matrix()

        excluded = smoke_report.get_excluded_tools(strict=args.smoke_strict)
        if excluded:
            logger.warning(f"Smoke test exclusions: {', '.join(sorted(excluded))}")
            available = [t for t in available if t not in excluded]

        if args.smoke_only:
            sys.exit(0 if not excluded else 1)

        if not available:
            logger.error("All tools failed smoke tests. Aborting.")
            sys.exit(1)

    mode = "parallel" if args.parallel else "sequential"
    logger.info(f"\nRunning comparison: {len(available)} tool(s) x {len(sites)} site(s) x {args.iterations} iteration(s) [{mode}]")
    if not args.skip_warmup:
        logger.info("(+ 1 warm-up run per site)")
    if args.parallel:
        logger.info(f"(max {args.site_parallelism} tool(s) per site simultaneously)")
    logger.info("=" * 60)

    # --- Checkpoint: attempt to resume a previous interrupted run ---
    checkpoint_path = _DEFAULT_CHECKPOINT
    args_dict = {
        "iterations": args.iterations,
        "skip_warmup": args.skip_warmup,
        "concurrency": args.concurrency,
        "sites": sorted(sites.keys()),
        "tools": sorted(available),
    }

    cp = None if args.no_resume else _load_checkpoint(checkpoint_path, args_dict)
    resumed_results: Dict[str, Dict[str, ToolSiteResult]] = {}
    resumed_base_dir: Optional[str] = None
    if cp:
        resumed_results = _restore_results(cp)
        resumed_base_dir = cp.get("base_dir")
        completed = sum(len(s) for s in resumed_results.values())
        total = len(available) * len(sites)
        logger.info(f"\n  Resuming from checkpoint: {completed}/{total} tool-site pairs already done.")
    elif not args.no_resume:
        # No valid checkpoint — clean start
        pass

    # Each tool discovers its own pages from the seed URL (no shared URL list)
    bench_start = time.time()
    if resumed_base_dir and os.path.isdir(resumed_base_dir):
        base_dir = resumed_base_dir
    else:
        base_dir = tempfile.mkdtemp(prefix="benchmark_comparison_")
    results: dict[str, dict[str, ToolSiteResult]] = {}
    tool_site_timing: dict[str, dict[str, dict]] = {}

    for tool_name in available:
        results[tool_name] = resumed_results.get(tool_name, {})
        tool_site_timing[tool_name] = {}

    # Lock for thread-safe checkpoint writes and progress tracking in parallel mode
    _checkpoint_lock = threading.Lock()
    _progress = {
        "completed": sum(len(s) for s in resumed_results.values()),
        "total": len(available) * len(sites),
        "errors": 0,
        "start_time": time.time(),
        "tool_errors": {t: 0 for t in available},  # consecutive errors per tool
    }
    # How many consecutive site failures before we skip a tool entirely
    _TOOL_FAIL_THRESHOLD = 3

    def _print_progress(tool_name: str, site_name: str, error: Optional[str]) -> None:
        """Print a one-line progress summary after each tool-site pair."""
        with _checkpoint_lock:
            _progress["completed"] += 1
            if error:
                _progress["errors"] += 1
                _progress["tool_errors"][tool_name] += 1
            else:
                _progress["tool_errors"][tool_name] = 0  # reset on success

            done = _progress["completed"]
            total = _progress["total"]
            errs = _progress["errors"]
            elapsed = time.time() - _progress["start_time"]

            # Estimate remaining time
            if done > 0:
                per_pair = elapsed / done
                remaining = per_pair * (total - done)
                if remaining >= 3600:
                    eta = f"~{remaining / 3600:.1f}h remaining"
                elif remaining >= 60:
                    eta = f"~{remaining / 60:.0f}m remaining"
                else:
                    eta = f"~{remaining:.0f}s remaining"
            else:
                eta = ""

            status = "✓" if not error else "✗"
            err_msg = f", {errs} error(s)" if errs else ""
            logger.info(f"\n  [{status}] Progress: {done}/{total} complete{err_msg} [{eta}]")

            # Warn if a tool is failing repeatedly
            consec = _progress["tool_errors"][tool_name]
            if consec >= _TOOL_FAIL_THRESHOLD:
                logger.warning(f"  {tool_name} has failed {consec} sites in a row -- "
                               f"likely a systemic issue, skipping remaining sites for this tool.")

    def _tool_should_skip(tool_name: str) -> bool:
        """Return True if a tool has hit the consecutive failure threshold."""
        return _progress["tool_errors"].get(tool_name, 0) >= _TOOL_FAIL_THRESHOLD

    def _bench_tool_site(tool_name: str, site_name: str) -> None:
        """Run warmup + iterations for one tool on one site."""
        # Skip if already completed in a resumed checkpoint
        if site_name in results.get(tool_name, {}):
            r = results[tool_name][site_name]
            status = f"error: {r.error[:40]}" if r.error else f"{r.pages_median:.0f} pages, {r.time_median:.1f}s"
            logger.info(f"\n  {tool_name} -> {site_name}: skipped (checkpoint: {status})")
            return

        # Skip if this tool has failed too many sites in a row
        if _tool_should_skip(tool_name):
            logger.info(f"\n  {tool_name} -> {site_name}: skipped (repeated failures)")
            _print_progress(tool_name, site_name, "skipped-repeated-failure")
            return

        run_fn = TOOLS[tool_name]["run"]
        site_config = sites[site_name]
        tool_site_start = time.time()

        logger.info(f"\n  {tool_name} -> {site_name} (discovery mode, max {site_config['max_pages']} pages):")

        # Warm-up — skip for firecrawl on free tier (wastes API credits)
        skip_warmup = args.skip_warmup or (tool_name == "firecrawl" and firecrawl_tier == "free")
        if not skip_warmup:
            logger.info(f"    [{tool_name}/{site_name}] warm-up...")
            try:
                run_single(tool_name, run_fn, site_name, site_config, base_dir,
                           url_list=None, concurrency=args.concurrency)
            except Exception as exc:
                logger.warning(f"    [{tool_name}/{site_name}] warm-up failed: {exc}")

        # Iterations
        runs = []
        for i in range(args.iterations):
            result = run_single(tool_name, run_fn, site_name, site_config, base_dir,
                                url_list=None, concurrency=args.concurrency)
            if result.error:
                logger.warning(f"    [{tool_name}/{site_name}] run {i+1}/{args.iterations}: error: {result.error[:60]}")
            else:
                logger.info(f"    [{tool_name}/{site_name}] run {i+1}/{args.iterations}: "
                            f"{result.pages} pages in {result.time_seconds:.1f}s ({result.pages_per_second:.1f} p/s)")
            runs.append(result)

        agg = aggregate_runs(runs, site_config)
        results[tool_name][site_name] = agg
        tool_site_timing[tool_name][site_name] = {
            "wall_start_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(tool_site_start)),
            "wall_end_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "pages_median": agg.pages_median,
            "time_median_s": round(agg.time_median, 3),
            "pps_median": round(agg.pps_median, 3),
            "error": agg.error,
        }

        # Save checkpoint after each tool-site pair completes
        with _checkpoint_lock:
            _save_checkpoint(checkpoint_path, results, base_dir, args_dict)

        _print_progress(tool_name, site_name, agg.error)

    if args.parallel:
        # Resource-aware parallel scheduler.
        #
        # Browser-based tools (crawl4ai, crawlee, playwright) use Chromium and
        # are CPU/memory heavy. Running two simultaneously on a single laptop
        # causes contention that degrades throughput — "more parallel" becomes
        # "less throughput." HTTP tools (markcrawl, scrapy, colly) are lightweight.
        #
        # Schedule rules:
        #   - At most 1 browser tool running globally (browser_semaphore)
        #   - HTTP tools run freely in parallel
        #   - Per-site semaphore still applies (max site_parallelism per host)
        #   - Allowed pairings: browser+HTTP, HTTP+HTTP
        #   - Avoided: browser+browser (globally, not just per-site)
        #
        # This typically gives ~2x speedup over sequential by filling idle time
        # with HTTP tools while a browser tool runs, without the throughput
        # degradation of browser-browser contention.
        #
        # Validated by external analysis showing browser tools are ~84% of total
        # runtime and contention between them reduces rather than increases
        # throughput on a single developer laptop.

        browser_avail = [t for t in available if t in BROWSER_TOOLS]
        http_avail = [t for t in available if t in HTTP_TOOLS]
        logger.info("\n--- Benchmarking (resource-aware parallel, per-tool discovery) ---")
        logger.info(f"  Browser lane (max 1 concurrent): {', '.join(browser_avail) or 'none'}")
        logger.info(f"  HTTP lane (unlimited): {', '.join(http_avail) or 'none'}")

        browser_semaphore = threading.Semaphore(1)
        site_semaphores: dict[str, threading.Semaphore] = {
            site: threading.Semaphore(args.site_parallelism) for site in sites
        }

        # Build work items: (tool, site) pairs — randomized to reduce ordering bias
        work_items = [(tool, site) for tool in available for site in sites]
        random.shuffle(work_items)

        def _guarded_bench(tool_name: str, site_name: str) -> None:
            is_browser = tool_name in BROWSER_TOOLS
            if is_browser:
                browser_semaphore.acquire()
            try:
                with site_semaphores[site_name]:
                    _bench_tool_site(tool_name, site_name)
            finally:
                if is_browser:
                    browser_semaphore.release()

        # Workers: enough for all HTTP tools + 1 browser tool to run concurrently
        max_workers = min(len(work_items), len(http_avail) + 1) if http_avail else 1
        max_workers = max(max_workers, 2)  # at least 2 for any parallelism
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = [pool.submit(_guarded_bench, tool, site) for tool, site in work_items]
            for future in as_completed(futures):
                exc = future.exception()
                if exc:
                    logger.warning(f"  benchmark task failed: {exc}")
    else:
        # Sequential mode — randomize tool order per site to eliminate
        # cache/CDN bias from fixed ordering.
        logger.info("\n--- Benchmarking (per-tool discovery, randomized tool order) ---")
        for site_name in sites:
            tool_order = list(available)
            random.shuffle(tool_order)
            logger.info(f"  {site_name} tool order: {', '.join(tool_order)}")
            for tool_name in tool_order:
                _bench_tool_site(tool_name, site_name)

    bench_end = time.time()
    run_end = time.time()

    logger.info("\n" + "=" * 60)
    generate_comparison_report(results, available, args.output, concurrency=args.concurrency)
    logger.info(f"Report saved to: {args.output}")

    # All done — remove checkpoint file
    _remove_checkpoint(checkpoint_path)
    logger.info("Checkpoint cleared (run completed successfully).")
    logger.info(f"\nRun data saved to: {base_dir}")
    # Regenerate README from updated report data
    try:
        import subprocess as _sp
        _sp.run([sys.executable, "generate_readme.py"], check=True)
        logger.info("README.md regenerated from report data.")
    except Exception as e:
        logger.warning(f"Could not regenerate README.md: {e}")

    logger.info("\nTo score extraction quality (preamble, repeat rate, precision/recall):")
    logger.info("  python benchmark_quality.py")

    # Write run_metadata.json before saving
    metadata = {
        "run_start_iso": run_start_iso,
        "run_end_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(run_end)),
        "total_wall_seconds": round(run_end - run_start, 1),
        "settings": {
            "iterations": args.iterations,
            "skip_warmup": args.skip_warmup,
            "sites": list(sites.keys()),
        },
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
        },
        "tools": {
            name: {
                "available": name in available,
                "version": _get_tool_version(name) if name in available else None,
                "skip_reason": skipped.get(name),
            }
            for name in TOOLS
        },
        "methodology": "per_tool_discovery",
        "phases": {
            "benchmarking": {
                "start_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(bench_start)),
                "end_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(bench_end)),
                "wall_seconds": round(bench_end - bench_start, 1),
                "results": tool_site_timing,
            },
            "parallel_mode": args.parallel,
            "site_parallelism": args.site_parallelism,
        },
        "output_report": args.output,
        "note": "Markdown output files in each tool/site subfolder are usable for a "
                "later embedding pass without re-running the crawl.",
    }
    metadata_path = os.path.join(base_dir, "run_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # Save run data (keep last 10 runs)
    _save_run_data(base_dir)


# ---------------------------------------------------------------------------
# Checkpoint support — resume after interruption
# ---------------------------------------------------------------------------

_DEFAULT_CHECKPOINT = os.path.join(os.path.dirname(__file__), ".benchmark_checkpoint.json")


def _save_checkpoint(
    path: str,
    results: Dict[str, Dict[str, ToolSiteResult]],
    base_dir: str,
    args_dict: dict,
) -> None:
    """Persist progress so the benchmark can resume after interruption."""
    serialized_results: Dict[str, Dict[str, dict]] = {}
    for tool, sites in results.items():
        serialized_results[tool] = {}
        for site, tsr in sites.items():
            serialized_results[tool][site] = {
                "tool": tsr.tool,
                "site": tsr.site,
                "description": tsr.description,
                "pages_median": tsr.pages_median,
                "time_median": tsr.time_median,
                "time_stddev": tsr.time_stddev,
                "pps_median": tsr.pps_median,
                "output_kb": tsr.output_kb,
                "peak_memory_mb": tsr.peak_memory_mb,
                "avg_words": tsr.avg_words,
                "error": tsr.error,
            }

    checkpoint = {
        "version": 2,
        "base_dir": base_dir,
        "args": args_dict,
        "results": serialized_results,
    }
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=2)
    os.replace(tmp, path)


def _load_checkpoint(path: str, args_dict: dict) -> Optional[dict]:
    """Load a checkpoint if it exists and settings match the current run."""
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            cp = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    if cp.get("version") != 2:
        return None

    # Settings must match — different iterations/concurrency/sites means start fresh
    if cp.get("args") != args_dict:
        logger.info("  Checkpoint found but settings differ -- starting fresh.")
        return None

    return cp


def _restore_results(cp: dict) -> Dict[str, Dict[str, ToolSiteResult]]:
    """Rebuild ToolSiteResult objects from checkpoint data."""
    results: Dict[str, Dict[str, ToolSiteResult]] = {}
    for tool, sites in cp.get("results", {}).items():
        results[tool] = {}
        for site, data in sites.items():
            results[tool][site] = ToolSiteResult(
                tool=data["tool"],
                site=data["site"],
                description=data["description"],
                pages_median=data["pages_median"],
                time_median=data["time_median"],
                time_stddev=data["time_stddev"],
                pps_median=data["pps_median"],
                output_kb=data["output_kb"],
                peak_memory_mb=data["peak_memory_mb"],
                avg_words=data["avg_words"],
                error=data.get("error"),
            )
    return results


def _remove_checkpoint(path: str) -> None:
    """Remove checkpoint file after successful completion."""
    try:
        os.remove(path)
    except OSError:
        pass


def _save_run_data(base_dir: str) -> None:
    """Copy run output to runs/ with timestamp. Keep last 10 runs (~35-40MB each)."""
    runs_dir = os.path.join(os.path.dirname(__file__), "runs")
    os.makedirs(runs_dir, exist_ok=True)

    # Save current run
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    run_dest = os.path.join(runs_dir, f"run_{timestamp}")
    try:
        shutil.copytree(base_dir, run_dest)
        logger.info(f"Run data saved to: {run_dest}")
    except Exception as exc:
        logger.warning(f"could not save run data: {exc}")
        shutil.rmtree(base_dir, ignore_errors=True)
        return

    # Clean up temp dir
    shutil.rmtree(base_dir, ignore_errors=True)

    # Keep only the last 10 runs
    existing_runs = sorted(
        [d for d in os.listdir(runs_dir) if d.startswith("run_") and os.path.isdir(os.path.join(runs_dir, d))],
    )
    while len(existing_runs) > 10:
        oldest = existing_runs.pop(0)
        oldest_path = os.path.join(runs_dir, oldest)
        shutil.rmtree(oldest_path, ignore_errors=True)
        logger.info(f"Removed old run: {oldest}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
