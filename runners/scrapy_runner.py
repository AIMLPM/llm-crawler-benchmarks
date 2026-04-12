"""Scrapy + markdownify runner — async HTTP crawling with Scrapy framework.

Tested with: scrapy (unpinned), markdownify (unpinned)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import List, Optional


def check() -> bool:
    try:
        import markdownify  # noqa: F401
        import scrapy  # noqa: F401
        return True
    except ImportError:
        return False


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, concurrency: int = 1, **kwargs) -> int:
    """Run Scrapy with markdownify pipeline via subprocess."""
    os.makedirs(out_dir, exist_ok=True)

    if url_list:
        url_list_json = json.dumps(url_list)
        spider_code = f'''
import json
import os
import scrapy
from markdownify import markdownify as md
from scrapy.crawler import CrawlerProcess

class BenchSpider(scrapy.Spider):
    name = "bench"
    start_urls = {url_list_json}
    custom_settings = {{
        "LOG_LEVEL": "ERROR",
        "ROBOTSTXT_OBEY": True,
        "CONCURRENT_REQUESTS": {concurrency},
        "DOWNLOAD_DELAY": 0,
    }}

    def parse(self, response):
        body = response.css("main").get() or response.css("body").get() or response.text
        markdown = md(body, heading_style="ATX", strip=["img", "script", "style", "nav", "footer"])
        title = response.css("title::text").get() or ""
        if len(markdown.split()) < 5:
            return
        safe_name = response.url.replace("://", "_").replace("/", "_")[:80]
        md_path = os.path.join("{out_dir}", f"{{safe_name}}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        jsonl_path = os.path.join("{out_dir}", "pages.jsonl")
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({{
                "url": response.url,
                "title": title.strip(),
                "text": markdown,
            }}, ensure_ascii=False) + "\\n")

process = CrawlerProcess()
process.crawl(BenchSpider)
process.start()
'''
    else:
        spider_code = f'''
import json
import os
import scrapy
from markdownify import markdownify as md
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse

class BenchSpider(scrapy.Spider):
    name = "bench"
    start_urls = ["{url}"]
    custom_settings = {{
        "LOG_LEVEL": "ERROR",
        "ROBOTSTXT_OBEY": True,
        "CONCURRENT_REQUESTS": {concurrency},
        "DOWNLOAD_DELAY": 0,
        "CLOSESPIDER_PAGECOUNT": {max_pages},
    }}
    pages_saved = 0

    def parse(self, response):
        if self.pages_saved >= {max_pages}:
            return
        body = response.css("main").get() or response.css("body").get() or response.text
        markdown = md(body, heading_style="ATX", strip=["img", "script", "style", "nav", "footer"])
        title = response.css("title::text").get() or ""
        if len(markdown.split()) < 5:
            return
        safe_name = response.url.replace("://", "_").replace("/", "_")[:80]
        md_path = os.path.join("{out_dir}", f"{{safe_name}}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        jsonl_path = os.path.join("{out_dir}", "pages.jsonl")
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({{
                "url": response.url,
                "title": title.strip(),
                "text": markdown,
            }}, ensure_ascii=False) + "\\n")
        self.pages_saved += 1
        base_domain = urlparse("{url}").netloc
        for href in response.css("a::attr(href)").getall():
            full_url = response.urljoin(href)
            if urlparse(full_url).netloc == base_domain:
                yield scrapy.Request(full_url, callback=self.parse)

process = CrawlerProcess()
process.crawl(BenchSpider)
process.start()
'''

    spider_file = os.path.join(out_dir, "_spider.py")
    with open(spider_file, "w") as f:
        f.write(spider_code)

    subprocess.run(
        [sys.executable, spider_file],
        capture_output=True,
        timeout=300,
        check=False,
    )

    jsonl_path = os.path.join(out_dir, "pages.jsonl")
    if os.path.isfile(jsonl_path):
        with open(jsonl_path) as f:
            return sum(1 for line in f if line.strip())
    return 0
