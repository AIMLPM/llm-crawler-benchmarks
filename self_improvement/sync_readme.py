#!/usr/bin/env python3
"""Sync benchmark numbers from reports into markcrawl's README.

Reads report files from this repo, extracts headline numbers, and patches
the <details> "How it compares" section in markcrawl's README.md.

Usage:
    python self_improvement/sync_readme.py \
        --markcrawl-readme /path/to/markcrawl/README.md \
        --reports-dir reports/

    python self_improvement/sync_readme.py --dry-run  # preview without writing
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_REPORTS = REPO_ROOT / "reports"


def parse_speed_rankings(text: str) -> list[tuple[str, float]]:
    """Extract tool speed rankings from SPEED_COMPARISON.md summary table."""
    rankings = []
    in_table = False
    for line in text.split("\n"):
        if "|" in line and "pages/sec" in line.lower():
            in_table = True
            continue
        if in_table and line.startswith("|"):
            if "---" in line:
                continue
            cols = [c.strip().strip("*") for c in line.split("|")[1:-1]]
            if len(cols) >= 3:
                tool = cols[0].strip("*").strip()
                try:
                    speed = float(re.sub(r"[^\d.]", "", cols[2]))
                    rankings.append((tool, speed))
                except (ValueError, IndexError):
                    pass
        elif in_table and not line.startswith("|"):
            break
    return rankings


def parse_answer_quality(text: str) -> list[tuple[str, float]]:
    """Extract tool answer quality scores from ANSWER_QUALITY.md summary table."""
    scores = []
    in_table = False
    for line in text.split("\n"):
        if "|" in line and "overall" in line.lower() and "tool" in line.lower():
            in_table = True
            continue
        if in_table and line.startswith("|"):
            if "---" in line:
                continue
            cols = [c.strip().strip("*") for c in line.split("|")[1:-1]]
            if len(cols) >= 2:
                tool = cols[0].strip("*").strip()
                try:
                    score = float(cols[-1].strip().strip("*"))
                    scores.append((tool, score))
                except (ValueError, IndexError):
                    pass
        elif in_table and not line.startswith("|"):
            break
    return scores


def parse_cost_chunks_per_page(text: str) -> dict[str, float]:
    """Extract chunks/page from COST_AT_SCALE.md source data table."""
    result = {}
    in_table = False
    for line in text.split("\n"):
        if "|" in line and "chunks/page" in line.lower():
            in_table = True
            continue
        if in_table and line.startswith("|"):
            if "---" in line:
                continue
            cols = [c.strip().strip("*") for c in line.split("|")[1:-1]]
            if len(cols) >= 3:
                tool = cols[0].strip("*").strip()
                try:
                    cpp = float(cols[2]) if len(cols) > 2 else float(cols[1])
                    result[tool] = cpp
                except (ValueError, IndexError):
                    pass
        elif in_table and not line.startswith("|"):
            break
    return result


def parse_annual_costs(text: str) -> dict[str, float]:
    """Extract annual costs from COST_AT_SCALE.md scenario B table."""
    result = {}
    in_table = False
    for line in text.split("\n"):
        if "|" in line and "annual" in line.lower() and "tool" in line.lower():
            in_table = True
            continue
        if in_table and line.startswith("|"):
            if "---" in line:
                continue
            cols = [c.strip().strip("*") for c in line.split("|")[1:-1]]
            if len(cols) >= 2:
                tool = cols[0].strip("*").strip()
                cost_str = cols[-1].strip().strip("*").replace("$", "").replace(",", "")
                try:
                    result[tool] = float(cost_str)
                except ValueError:
                    pass
        elif in_table and not line.startswith("|"):
            break
    return result


def generate_details_section(
    speed_rankings: list[tuple[str, float]],
    answer_quality: list[tuple[str, float]],
    chunks_per_page: dict[str, float],
    annual_costs: dict[str, float],
) -> str:
    """Generate the <details> section for markcrawl's README."""
    base = "https://github.com/AIMLPM/llm-crawler-bench/blob/main/reports"

    # Speed narrative
    if speed_rankings:
        fastest = speed_rankings[0]
        mc_rank = next(
            (i + 1 for i, (t, _) in enumerate(speed_rankings) if t == "markcrawl"),
            None,
        )
        mc_speed = next(
            (s for t, s in speed_rankings if t == "markcrawl"),
            None,
        )
        ordinals = {1: "fastest", 2: "second", 3: "third", 4: "fourth",
                    5: "fifth", 6: "sixth", 7: "seventh"}
        if mc_rank == 1:
            speed_line = f"markcrawl is fastest ({mc_speed} pages/sec)"
        else:
            speed_line = (
                f"{fastest[0]} is fastest ({fastest[1]} pages/sec), "
                f"markcrawl {ordinals.get(mc_rank, 'ranks ' + str(mc_rank))} ({mc_speed})"
            )
    else:
        speed_line = "Speed data not available"

    # Build quality/cost table
    table_lines = [
        "| Tool | Answer quality | Chunks/page | Annual cost (50K pages) |",
        "|------|---------------|-------------|------------------------|",
    ]
    # Use answer quality order for table
    for tool, score in answer_quality:
        cpp = chunks_per_page.get(tool, 0)
        cost = annual_costs.get(tool, 0)
        bold = "**" if tool == "markcrawl" else ""
        cost_str = f"${cost:,.0f}" if cost >= 10 else f"${cost:.2f}"
        table_lines.append(
            f"| {bold}{tool}{bold} | {bold}{score:.2f}{bold} | "
            f"{bold}{cpp:.1f}{bold} | {bold}{cost_str}{bold} |"
        )

    table = "\n".join(table_lines)

    return f"""<details>
<summary>How it compares to other crawlers</summary>

We benchmarked 7 crawlers across 8 real-world sites. {speed_line}.
HTTP-only tools (scrapy+md, colly+md) are inherently faster; markcrawl
and crawl4ai use headless browsers to handle JS-rendered content.

{table}

See detailed reports:
[Speed]({base}/SPEED_COMPARISON.md) |
[Quality]({base}/QUALITY_COMPARISON.md) |
[Retrieval]({base}/RETRIEVAL_COMPARISON.md) |
[Answer Quality]({base}/ANSWER_QUALITY.md) |
[Cost]({base}/COST_AT_SCALE.md) |
[Methodology]({base}/METHODOLOGY.md)

</details>"""


def patch_readme(readme_text: str, new_details: str) -> str:
    """Replace the <details>...</details> section in the README."""
    pattern = r"<details>\s*\n\s*<summary>How it compares.*?</details>"
    match = re.search(pattern, readme_text, re.DOTALL)
    if not match:
        raise ValueError("Could not find <details> 'How it compares' section in README")
    return readme_text[:match.start()] + new_details + readme_text[match.end():]


def main():
    parser = argparse.ArgumentParser(description="Sync benchmark numbers to markcrawl README")
    parser.add_argument("--markcrawl-readme", type=Path,
                        help="Path to markcrawl's README.md")
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS,
                        help="Path to reports directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the generated section without writing")
    args = parser.parse_args()

    reports = args.reports_dir

    # Parse all report data
    speed_text = (reports / "SPEED_COMPARISON.md").read_text(encoding="utf-8")
    aq_text = (reports / "ANSWER_QUALITY.md").read_text(encoding="utf-8")
    cost_text = (reports / "COST_AT_SCALE.md").read_text(encoding="utf-8")

    speed_rankings = parse_speed_rankings(speed_text)
    answer_quality = parse_answer_quality(aq_text)
    chunks_per_page = parse_cost_chunks_per_page(cost_text)
    annual_costs = parse_annual_costs(cost_text)

    details = generate_details_section(speed_rankings, answer_quality,
                                       chunks_per_page, annual_costs)

    if args.dry_run:
        print(details)
        return 0

    if not args.markcrawl_readme:
        parser.error("--markcrawl-readme is required unless using --dry-run")

    readme = args.markcrawl_readme.read_text(encoding="utf-8")
    patched = patch_readme(readme, details)
    args.markcrawl_readme.write_text(patched, encoding="utf-8")
    print(f"Patched {args.markcrawl_readme}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
