#!/usr/bin/env bash
# scripts/ci_local.sh — run the same checks GitHub Actions runs.
#
# Why: until now, CI failures only surfaced after push, flooding the
# user's inbox. This script runs the lint + test + invariants + install
# matrix locally so regressions are caught before commit.
#
# Usage:
#   scripts/ci_local.sh          # run all checks
#   scripts/ci_local.sh --fix    # autofix what ruff can fix
#
# Mirrors .github/workflows/ci.yml. If you change one, change the other.

set -e
cd "$(dirname "$0")/.."

# Pick a python: prefer .venv if present, else system python3.
if [ -x ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
    PIP=".venv/bin/pip"
    RUFF=".venv/bin/ruff"
else
    PYTHON="python3"
    PIP="pip"
    RUFF="ruff"
fi

FIX=""
if [ "$1" = "--fix" ]; then
    FIX="--fix"
    shift
fi

echo "=== install (matches: pip install -e \".[dev]\") ==="
$PIP install -e ".[dev]" --quiet || { echo "FAIL: install"; exit 1; }
echo "  ok"
echo

echo "=== ruff check (matches: ruff check .) ==="
$RUFF check . $FIX || { echo "FAIL: ruff"; exit 1; }
echo

echo "=== pytest (matches: python -m pytest tests/ -v) ==="
$PYTHON -m pytest tests/ -q || { echo "FAIL: pytest"; exit 1; }
echo

echo "=== lint_reports.py ==="
$PYTHON lint_reports.py || { echo "FAIL: lint_reports"; exit 1; }
echo

echo "=== check_invariants.py ==="
$PYTHON self_improvement/check_invariants.py || { echo "FAIL: invariants"; exit 1; }
echo

echo "=== check_cross_report_consistency.py ==="
$PYTHON self_improvement/check_cross_report_consistency.py || { echo "FAIL: cross-report"; exit 1; }
echo

echo "=== check_no_site_hardcoding.py ==="
$PYTHON self_improvement/check_no_site_hardcoding.py || { echo "FAIL: site-hardcoding"; exit 1; }
echo

echo "=== sites.test_pool ==="
$PYTHON -m sites.test_pool || { echo "FAIL: pool tests"; exit 1; }
echo

echo "ALL LOCAL CI CHECKS PASSED"
