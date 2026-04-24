"""Smoke tests for sites.pool. Run: python3 -m sites.test_pool"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from sites import pool as P


def test_load_pool():
    p = P.load_pool()
    assert p.version.startswith("v"), p.version
    assert len(p.sites) >= 8, f"expected >= 8 sites, got {len(p.sites)}"
    # Original 8 must be present.
    for name in ["quotes-toscrape", "books-toscrape", "fastapi-docs",
                 "python-docs", "react-dev", "wikipedia-python",
                 "stripe-docs", "blog-engineering"]:
        assert p.by_name(name) is not None, f"original site missing: {name}"
    # All categories valid.
    for s in p.sites:
        assert s.category in P.VALID_CATEGORIES
        for d in s.difficulty:
            assert d in P.VALID_DIFFICULTIES


def test_sample_deterministic():
    p = P.load_pool()
    a = P.sample(p, seed=42, per_category=1)
    b = P.sample(p, seed=42, per_category=1)
    assert [s.name for s in a] == [s.name for s in b], "sample not deterministic"


def test_sample_different_seeds_differ():
    p = P.load_pool()
    a = P.sample(p, seed=1, per_category=2)
    b = P.sample(p, seed=2, per_category=2)
    assert [s.name for s in a] != [s.name for s in b], "different seeds produced same sample"


def test_sample_requires_queries():
    p = P.load_pool()
    s = P.sample(p, seed=1, per_category=10, requires_queries=True)
    assert all(x.has_queries for x in s), "requires_queries leaked a no-query site"
    assert len(s) >= 8, "should include all 8 original sites"


def test_sample_only_filter():
    p = P.load_pool()
    s = P.sample(p, seed=0, per_category=1, only=["fastapi-docs", "python-docs"])
    assert {x.name for x in s} == {"fastapi-docs", "python-docs"}


def test_manifest_roundtrip():
    p = P.load_pool()
    s = P.sample(p, seed=7, per_category=1, requires_queries=True)
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run_test"
        run_dir.mkdir()
        P.write_manifest(
            run_dir, pool=p, seed=7, sampled=s,
            sample_strategy={"per_category": 1, "requires_queries": True},
            tool_versions={"markcrawl": "0.2.0"},
            git_sha="abc123",
            benchmark_version="2026.04",
        )
        m = P.read_manifest(run_dir)
        assert m is not None
        assert m["seed"] == 7
        assert m["pool_hash"] == p.sha256
        assert {x["name"] for x in m["sampled_sites"]} == {x.name for x in s}

        sites2 = P.sites_for_run(run_dir, p)
        assert {x.name for x in sites2} == {x.name for x in s}


def test_sites_for_run_legacy():
    """A run dir without manifest.json should be discoverable from disk layout."""
    p = P.load_pool()
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run_legacy"
        # Simulate: runs/<id>/<tool>/<site>/pages.jsonl
        (run_dir / "markcrawl" / "fastapi-docs").mkdir(parents=True)
        (run_dir / "markcrawl" / "fastapi-docs" / "pages.jsonl").write_text("{}\n")
        (run_dir / "markcrawl" / "python-docs").mkdir(parents=True)
        (run_dir / "markcrawl" / "python-docs" / "pages.jsonl").write_text("{}\n")
        sites = P.sites_for_run(run_dir, p)
        assert {s.name for s in sites} == {"fastapi-docs", "python-docs"}


def test_pool_hash_stable():
    """Loading twice should produce the same sha256 (no non-determinism in I/O)."""
    a = P.load_pool().sha256
    b = P.load_pool().sha256
    assert a == b


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    if failed:
        raise SystemExit(f"{failed} failure(s)")
    print(f"\nAll {len(tests)} tests passed.")
