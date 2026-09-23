"""Preflight: refuse to benchmark a stale markcrawl.

The bench installs markcrawl from PyPI with a floor pin (``markcrawl>=X``).
pip never upgrades an already-satisfied requirement, so an existing ``.venv``
silently keeps measuring whatever version it was built with — v0.10.5 sat in
the venv through three markcrawl releases before anyone noticed.

This check compares the installed version against PyPI's latest and exits
unless they match. ``--allow-stale-markcrawl`` overrides it for deliberate
runs against an older version (regression bisects, reproducing old numbers).

If PyPI is unreachable the check warns and continues: a network blip should
not kill a run, and the installed version is still recorded in the report.
"""

from __future__ import annotations

import importlib.metadata
import json
import logging
import sys
import urllib.request
from typing import Optional

from packaging.version import InvalidVersion, Version

logger = logging.getLogger(__name__)

PYPI_URL = "https://pypi.org/pypi/markcrawl/json"
ALLOW_FLAG = "--allow-stale-markcrawl"


def installed_version() -> Optional[str]:
    try:
        return importlib.metadata.version("markcrawl")
    except importlib.metadata.PackageNotFoundError:
        return None


def latest_pypi_version(timeout: float = 5.0) -> Optional[str]:
    """Return PyPI's latest markcrawl version, or None if unreachable."""
    try:
        with urllib.request.urlopen(PYPI_URL, timeout=timeout) as resp:
            return json.load(resp)["info"]["version"]
    except Exception as exc:  # network, HTTP, JSON — all non-fatal
        logger.warning(f"markcrawl freshness check: could not reach PyPI ({exc})")
        return None


def evaluate(installed: Optional[str], latest: Optional[str]) -> tuple[bool, str]:
    """Decide whether the run may proceed. Pure function — no I/O.

    Returns (ok, message). Only a known-older install blocks; unknown states
    (not installed, PyPI unreachable, unparseable versions) pass with a message.
    A newer-than-PyPI install (editable dev checkout) passes.
    """
    if installed is None:
        return True, "markcrawl is not installed; skipping freshness check"
    if latest is None:
        return True, f"markcrawl {installed} installed; PyPI latest unknown, proceeding"
    try:
        stale = Version(installed) < Version(latest)
    except InvalidVersion:
        return True, f"markcrawl {installed} vs PyPI {latest}: unparseable, proceeding"
    if stale:
        return False, (
            f"markcrawl {installed} is installed but PyPI has {latest}. "
            f"Upgrade with `.venv/bin/pip install -U markcrawl`, "
            f"or pass {ALLOW_FLAG} to benchmark the older version deliberately."
        )
    return True, f"markcrawl {installed} (PyPI latest {latest})"


def enforce(allow_stale: bool) -> None:
    """Run the preflight; exit(1) on a stale install unless allowed."""
    ok, message = evaluate(installed_version(), latest_pypi_version())
    if ok:
        logger.info(message)
        return
    if allow_stale:
        logger.warning(f"{message} Continuing ({ALLOW_FLAG} set).")
        return
    logger.error(message)
    sys.exit(1)
