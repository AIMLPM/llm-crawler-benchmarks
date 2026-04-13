"""Shared utilities for benchmark report generation."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple


def table_legend(columns: Sequence[Tuple[str, str]]) -> List[str]:
    """Format a column definitions blockquote for use after a Markdown table.

    Args:
        columns: sequence of (name, definition) pairs.
            name can include footnote markers like "[1] Avg words".

    Returns:
        A list of Markdown lines (one or more blockquote lines).

    Example::

        lines.extend(table_legend([
            ("Pages (a)", "total pages fetched from the site"),
            ("Time (b)", "wall-clock seconds for all pages"),
            ("Pages/sec (a÷b)", "throughput"),
        ]))

    Produces::

        > **Column definitions:** **Pages (a)** = total pages fetched from the site.
        > **Time (b)** = wall-clock seconds for all pages. **Pages/sec (a÷b)** = throughput.
    """
    parts = []
    for name, defn in columns:
        # Ensure definition ends with a period
        defn = defn.rstrip(".")
        parts.append(f"**{name}** = {defn}.")

    # Join all parts into one or more blockquote lines, wrapping at ~100 chars
    text = " ".join(parts)
    result_lines = []
    prefix = "> **Column definitions:** "

    # Simple wrapping: split into blockquote continuation lines
    remaining = prefix + text
    while len(remaining) > 120:
        # Find a good break point
        break_at = remaining.rfind(". ", 0, 120)
        if break_at < len(prefix):
            break_at = remaining.find(". ", 80)
        if break_at < 0:
            break
        result_lines.append(remaining[: break_at + 1])
        remaining = "> " + remaining[break_at + 2 :]

    result_lines.append(remaining)
    return result_lines
