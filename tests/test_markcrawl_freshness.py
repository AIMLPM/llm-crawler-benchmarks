"""Tests for the stale-markcrawl preflight (tools/markcrawl_freshness.py)."""

import pytest

from tools import markcrawl_freshness as mf


@pytest.mark.parametrize("installed,latest", [
    ("0.11.1", "0.11.1"),   # current
    ("0.12.0", "0.11.1"),   # editable dev checkout ahead of PyPI
    (None, "0.11.1"),       # not installed
    ("0.11.1", None),       # PyPI unreachable
    ("dev-build", "0.11.1"),  # unparseable
])
def test_evaluate_passes(installed, latest):
    ok, _ = mf.evaluate(installed, latest)
    assert ok


def test_evaluate_blocks_stale_and_names_the_fix():
    ok, message = mf.evaluate("0.10.5", "0.11.1")
    assert not ok
    assert "0.10.5" in message and "0.11.1" in message
    assert mf.ALLOW_FLAG in message


def test_version_compare_is_semantic_not_lexical():
    # "0.9.0" > "0.10.0" as strings; must still count as stale.
    ok, _ = mf.evaluate("0.9.0", "0.10.0")
    assert not ok


def test_enforce_exits_on_stale(monkeypatch):
    monkeypatch.setattr(mf, "installed_version", lambda: "0.10.5")
    monkeypatch.setattr(mf, "latest_pypi_version", lambda: "0.11.1")
    with pytest.raises(SystemExit):
        mf.enforce(allow_stale=False)


def test_enforce_override_continues(monkeypatch):
    monkeypatch.setattr(mf, "installed_version", lambda: "0.10.5")
    monkeypatch.setattr(mf, "latest_pypi_version", lambda: "0.11.1")
    mf.enforce(allow_stale=True)  # no exit


def test_unreachable_pypi_returns_none(monkeypatch):
    def boom(*a, **k):
        raise OSError("offline")
    monkeypatch.setattr(mf.urllib.request, "urlopen", boom)
    assert mf.latest_pypi_version() is None
