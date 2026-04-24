#!/usr/bin/env python3
"""Fail if any tool runner hardcodes pool hostnames.

Rationale: markcrawl previously hardcoded behavior for specific benchmark
sites — the kind of silent gaming this benchmark is designed to prevent.
This check scans per-tool runners and adapters for literal hostnames that
come from sites/pool_v1.yaml; they should flow in through the runner
interface, not be baked into source.

    python self_improvement/check_no_site_hardcoding.py

Exit code 0 = clean. Non-zero = hardcoded hostnames found.

Scope: scans our own adapters — `runners/` and top-level worker scripts
(`crawlee_worker.py`). Third-party vendored source under `tools/` is
explicitly skipped. Benchmark orchestration scripts (`benchmark_*.py`,
`sites/`, `reports/`, `self_improvement/`, `generate_readme.py`) are
allowed to reference sites — they are the ground truth.

Comments (# ...) and module docstrings are exempt: the goal is to catch
site-specific *code logic*, not narrative notes about observed behavior.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sites.pool import load_pool  # noqa: E402

SCAN_DIRS = [ROOT / "runners"]
SCAN_FILES = [ROOT / "crawlee_worker.py"]

IGNORED_SUFFIXES = {".pyc", ".log", ".md", ".json", ".lock"}
IGNORED_DIRS = {"__pycache__", "node_modules", ".git", "dist", "build"}


def _candidate_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_DIRS:
        if not root.is_dir():
            continue
        for p in root.rglob("*.py"):
            if not p.is_file():
                continue
            if any(part in IGNORED_DIRS for part in p.parts):
                continue
            if p.suffix in IGNORED_SUFFIXES:
                continue
            files.append(p)
    for p in SCAN_FILES:
        if p.is_file():
            files.append(p)
    return files


def _strip_comments_and_docstrings(text: str) -> str:
    """Return source with `# ...` comments and docstrings blanked out.

    Preserves line numbers so offense line numbers line up with the file.
    """
    # Blank module/class/function docstrings via AST.
    try:
        tree = ast.parse(text)
    except SyntaxError:
        tree = None
    lines = text.splitlines()
    if tree is not None:
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                body = getattr(node, "body", [])
                if (body and isinstance(body[0], ast.Expr)
                        and isinstance(body[0].value, ast.Constant)
                        and isinstance(body[0].value.value, str)):
                    start = body[0].lineno - 1
                    end = body[0].end_lineno  # inclusive 1-indexed -> exclusive 0-indexed
                    for i in range(start, min(end, len(lines))):
                        lines[i] = ""
    # Strip `# ...` comments (simple heuristic — ignores `#` inside strings,
    # which is fine here since we only care about URLs/hostnames).
    out = []
    for line in lines:
        idx = line.find("#")
        if idx >= 0:
            # Only strip when `#` isn't inside a string literal. Cheap check:
            # count unescaped quotes before `#`; if balanced, `#` is a comment.
            prefix = line[:idx]
            if prefix.count('"') % 2 == 0 and prefix.count("'") % 2 == 0:
                line = prefix
        out.append(line)
    return "\n".join(out)


def main() -> int:
    pool = load_pool()
    hostnames = set()
    for s in pool.sites:
        host = urlparse(s.url).netloc.lower()
        if host.startswith("www."):
            host = host[4:]
        if host:
            hostnames.add(host)

    patterns = {h: re.compile(r"\b" + re.escape(h) + r"\b", re.IGNORECASE) for h in hostnames}

    offenses: list[tuple[Path, int, str, str]] = []
    for f in _candidate_files():
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        scrubbed = _strip_comments_and_docstrings(text)
        for lineno, line in enumerate(scrubbed.splitlines(), 1):
            for host, pat in patterns.items():
                if pat.search(line):
                    offenses.append((f.relative_to(ROOT), lineno, host, line.strip()))

    if offenses:
        print(f"FAIL: {len(offenses)} hardcoded pool hostname reference(s) found:\n")
        for path, lineno, host, snippet in offenses:
            print(f"  {path}:{lineno}  [{host}]  {snippet[:120]}")
        print("\nTool runners must receive site URLs through their interface, not")
        print("hardcode them. If a reference is legitimate (e.g. a URL-sanity test),")
        print("move it out of runners/ and tools/, or add a narrow allowlist here.")
        return 1

    print(f"PASS: no pool hostnames hardcoded in {len(_candidate_files())} scanned files.")
    print(f"      ({len(hostnames)} hostnames checked from pool {pool.version})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
