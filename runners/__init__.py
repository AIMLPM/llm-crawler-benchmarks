"""Tool runners package — each crawler has its own module.

Each module exposes:
  - check() -> bool     — is this tool installed/available?
  - run(...) -> int      — run the crawl, return pages saved

Import TOOLS for the registry used by the benchmark orchestrator,
or import individual runners to test a single tool.
"""
from runners import (
    colly_runner,
    crawl4ai_raw_runner,
    crawl4ai_runner,
    crawlee_runner,
    firecrawl_runner,
    markcrawl_runner,
    playwright_runner,
    scrapy_runner,
)

TOOLS = {
    "markcrawl": {"check": markcrawl_runner.check, "run": markcrawl_runner.run},
    "crawl4ai": {"check": crawl4ai_runner.check, "run": crawl4ai_runner.run},
    "crawl4ai-raw": {"check": crawl4ai_raw_runner.check, "run": crawl4ai_raw_runner.run},
    "scrapy+md": {"check": scrapy_runner.check, "run": scrapy_runner.run},
    "crawlee": {"check": crawlee_runner.check, "run": crawlee_runner.run},
    "colly+md": {"check": colly_runner.check, "run": colly_runner.run},
    "playwright": {"check": playwright_runner.check, "run": playwright_runner.run},
    "firecrawl": {"check": firecrawl_runner.check, "run": firecrawl_runner.run},
}

# Resource classification — browser tools use Chromium and are CPU/memory heavy.
BROWSER_TOOLS = {"crawl4ai", "crawl4ai-raw", "crawlee", "playwright"}
HTTP_TOOLS = {"markcrawl", "scrapy+md", "colly+md", "firecrawl"}
