#!/usr/bin/env python3
"""Cross-report data consistency checker.

Validates that key numbers (answer quality scores, chunks/page) are
consistent across COST_AT_SCALE.md and ANSWER_QUALITY.md.

Run before committing any report changes:

    python self_improvement/check_cross_report_consistency.py

Exit code 0 = all checks pass. Non-zero = mismatches found.

Implements the automation recommended after the Spec 05 audit found that
report data inconsistencies were the only CRITICAL finding — and Spec 05
was entirely manual at that time.

Note: README consistency checks (X1-X3, X5, X6) were removed when this
script moved to the standalone llm-crawler-bench repo.  The README lives
in the markcrawl repo and is validated by sync_readme.py instead.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

failures = []
passes = []


def check(check_id: str, description: str, passed: bool, detail: str = ""):
    if passed:
        passes.append(f"  PASS  {check_id}: {description}")
    else:
        msg = f"  FAIL  {check_id}: {description}"
        if detail:
            msg += f" -- {detail}"
        failures.append(msg)


# ---------------------------------------------------------------------------
# Markdown table parsing
# ---------------------------------------------------------------------------

def parse_md_table(text: str, header_pattern: str) -> list[dict[str, str]]:
    """Find the first markdown table whose header matches *header_pattern*
    and return rows as list-of-dicts keyed by column header."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if re.search(header_pattern, line, re.IGNORECASE) and "|" in line:
            # Header row
            headers = [h.strip().strip("*") for h in line.split("|")[1:-1]]
            # Skip separator row
            if i + 2 >= len(lines):
                return []
            rows = []
            for row_line in lines[i + 2:]:
                if not row_line.strip().startswith("|"):
                    break
                cells = [c.strip().strip("*") for c in row_line.split("|")[1:-1]]
                if len(cells) == len(headers):
                    rows.append(dict(zip(headers, cells)))
            return rows
    return []


def clean_tool_name(name: str) -> str:
    """Normalize tool name: strip bold markers and whitespace."""
    return name.strip().strip("*").strip()


def clean_number(val: str) -> float | None:
    """Extract a float from a table cell, stripping $, commas, %, bold."""
    val = val.strip().strip("*").strip()
    val = val.replace("$", "").replace(",", "").replace("%", "")
    val = val.replace("--", "").replace("—", "").strip()
    if not val:
        return None
    try:
        return float(val)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Data extraction
# ---------------------------------------------------------------------------

def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def get_cost_source_data(text: str) -> list[dict]:
    """Parse the source data table from COST_AT_SCALE.md."""
    return parse_md_table(text, r"Tool.*Chunks/page.*Answer quality")


def get_answer_quality_summary(text: str) -> list[dict]:
    """Parse the summary table from ANSWER_QUALITY.md."""
    return parse_md_table(text, r"Tool.*Overall.*Queries")


# ---------------------------------------------------------------------------
# Comparison checks
# ---------------------------------------------------------------------------

def check_cost_vs_answer_quality():
    """Verify COST_AT_SCALE answer quality scores match ANSWER_QUALITY.md."""
    cost = load_file(REPORTS / "COST_AT_SCALE.md")
    aq = load_file(REPORTS / "ANSWER_QUALITY.md")

    source_data = get_cost_source_data(cost)
    if not source_data:
        check("X4", "COST_AT_SCALE.md has source data table", False, "table not found")
        return

    aq_table = get_answer_quality_summary(aq)
    aq_lookup = {}
    for row in aq_table:
        tool = clean_tool_name(row.get("Tool", ""))
        score = clean_number(row.get("Overall", ""))
        if tool and score is not None:
            aq_lookup[tool] = score

    for row in source_data:
        tool = clean_tool_name(row.get("Tool", ""))
        cost_score = clean_number(row.get("Answer quality (/5)", ""))
        aq_score = aq_lookup.get(tool)
        if tool and cost_score is not None and aq_score is not None:
            check(f"X4-{tool}",
                  f"COST_AT_SCALE answer quality for {tool} matches ANSWER_QUALITY.md",
                  abs(cost_score - aq_score) < 0.015,
                  f"COST={cost_score}, AQ={aq_score}")


def main():
    print("Running cross-report consistency checks...\n")

    missing_files = []
    for name in ["COST_AT_SCALE.md", "ANSWER_QUALITY.md"]:
        if not (REPORTS / name).exists():
            missing_files.append(name)

    if missing_files:
        print(f"  SKIP  Missing files: {', '.join(missing_files)}")
        print("\nCannot run consistency checks with missing files.")
        return 1

    check_cost_vs_answer_quality()

    print("\n".join(passes))
    if failures:
        print()
        print("\n".join(failures))
        print(f"\n{len(failures)} FAILED, {len(passes)} passed")
        return 1
    else:
        print(f"\nAll {len(passes)} checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
