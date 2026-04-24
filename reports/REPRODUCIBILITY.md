# Reproducibility

Every benchmark run is bit-reproducible from a single file: the run's
`manifest.json`. This page explains the manifest format and shows how to
replay an existing run or verify one yourself.

## Why this matters

Fixed benchmark suites are gameable — once a tool knows the exact sites and
queries it will be scored on, it can be tuned to those targets. We avoid that
by sampling each run from a larger, rotating [site pool](../sites/pool_v1.yaml)
and recording the sample in a manifest. Two properties fall out:

1. **Reproducibility.** Anyone can replay a specific run by loading its
   manifest and re-running against the same sites with the same seed.
2. **Anti-gaming.** The pool evolves between releases (see the
   `version` field in `pool_v1.yaml`), so a tool tuned to one quarter's
   snapshot cannot coast on it the next.

These are often treated as opposing goals. With a manifest they aren't:
each run is frozen and replayable, but the *next* run isn't constrained
to the same slice.

## The manifest format

Every run writes `runs/<run_id>/manifest.json`. Example:

```json
{
  "run_id": "run_20260418_221158",
  "benchmark_version": "2026.04",
  "pool_version": "v1.1",
  "pool_hash": "sha256:<64 hex chars>",
  "pool_path": "pool_v1.yaml",
  "seed": 42,
  "sample_strategy": {"per_category": 1, "requires_queries": true},
  "sampled_sites": [
    {"name": "fastapi-docs", "category": "api_docs",
     "difficulty": ["static"], "has_queries": true},
    ...
  ],
  "tool_versions": {"markcrawl": "0.3.1", "crawl4ai": "0.4.0", ...},
  "git_sha": "<commit hash of this repo at run time>",
  "timestamp_utc": "2026-04-18T22:11:58+00:00"
}
```

Field meanings:

| Field | Purpose |
|---|---|
| `pool_version` | Which version of `pool_v1.yaml` produced this run (v1.0, v1.1, ...) |
| `pool_hash` | SHA-256 of the pool file. If it doesn't match your local copy, the pool has drifted |
| `seed` | Random seed fed into the stratified sampler — determines which sites were picked |
| `sample_strategy` | How `seed` was applied (e.g., one site per category, queries required) |
| `sampled_sites` | The sites actually crawled. This is what the report numbers are computed over |
| `tool_versions` | Exact version of each crawler used. Replay against different versions to measure regression |
| `git_sha` | Commit of this benchmark repo at run time |
| `benchmark_version` | Methodology version (see `generate_readme.py`) |

## Replaying a run

Given a run's manifest, reproduce it with:

```bash
# 1. Check out the repo at the run's git_sha (so the methodology matches)
git checkout <git_sha>

# 2. Install the same tool versions (pin markcrawl, crawl4ai, etc.)
pip install markcrawl==<version_from_manifest>

# 3. Re-run the benchmark with the recorded sample
python benchmark_all_tools.py \
    --sites $(jq -r '.sampled_sites[].name' runs/<run_id>/manifest.json | paste -sd,) \
    --seed $(jq -r '.seed' runs/<run_id>/manifest.json)
```

`--sites` pins the exact site list. `--seed` is recorded for parity with
the original run even though `--sites` already fixes the sample (the seed
matters when replaying end-to-end from the pool rather than from the
manifest).

## Verifying a run without rerunning

If you only want to check that the reported numbers match the raw data:

```bash
python benchmark_quality.py --run <run_id>
python benchmark_retrieval.py --run <run_id> --report-only
python benchmark_answer_quality.py --run <run_id> --report-only
```

All three scripts read `manifest.json` automatically and operate on exactly
the sampled sites.

## Pool evolution

The pool is public
([`sites/pool_v1.yaml`](../sites/pool_v1.yaml)) and versioned. Adding or
removing sites bumps the minor version (v1.0 → v1.1). Major structural
changes (category taxonomy, required fields) bump the major version.

Old runs remain fully replayable even after the pool evolves: the manifest
records which pool version and hash produced the run, and
`sites.pool.sites_for_run()` raises a loud error if a manifest references
sites the current pool doesn't know about.

## Anti-gaming invariants

In addition to the rotation above, a CI lint
(`self_improvement/check_no_site_hardcoding.py`) scans our own tool
adapters (`runners/`) for literal pool hostnames. If a tool adapter hardcodes
behavior for a specific benchmark site, the check fails. This is defense
against the specific failure mode we caught once in markcrawl itself:
silently baking site-specific handling into the crawler.
