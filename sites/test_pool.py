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
    # Continuity anchors (carried across pool swaps).
    for name in ["react-dev", "stripe-docs"]:
        assert p.by_name(name) is not None, f"anchor site missing: {name}"
    # All categories + difficulties valid.
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
    """Different seeds must produce different samples on at least some
    category with enough members to offer variety. Robust to pool reshapes:
    we require that ANY pair of seeds, across a handful of trials, differs."""
    p = P.load_pool()
    # Find the largest category — that's where seed variance is observable.
    sizes = {}
    for s in p.sites:
        sizes[s.category] = sizes.get(s.category, 0) + 1
    largest = max(sizes.values())
    assert largest >= 3, f"pool has no category with >=3 sites; got sizes {sizes}"
    # Pick per_category so the largest category can choose a proper subset.
    per_cat = max(1, largest - 1)
    samples = [tuple(s.name for s in P.sample(p, seed=i, per_category=per_cat))
               for i in (1, 2, 17, 999)]
    assert len(set(samples)) >= 2, f"all 4 seeds produced the same sample: {samples[0]}"


def test_sample_requires_queries():
    p = P.load_pool()
    # Sample generously so every query-bearing site is pulled.
    s = P.sample(p, seed=1, per_category=50, requires_queries=True)
    assert all(x.has_queries for x in s), "requires_queries leaked a no-query site"
    expected = [x for x in p.sites if x.has_queries]
    assert len(s) == len(expected), f"expected all {len(expected)} query sites, got {len(s)}"


def test_sample_only_filter():
    p = P.load_pool()
    anchors = ["react-dev", "stripe-docs"]
    s = P.sample(p, seed=0, per_category=1, only=anchors)
    assert {x.name for x in s} == set(anchors)


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
    anchors = ["react-dev", "stripe-docs"]
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run_legacy"
        # Simulate: runs/<id>/<tool>/<site>/pages.jsonl
        for name in anchors:
            (run_dir / "markcrawl" / name).mkdir(parents=True)
            (run_dir / "markcrawl" / name / "pages.jsonl").write_text("{}\n")
        sites = P.sites_for_run(run_dir, p)
        assert {s.name for s in sites} == set(anchors)


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
