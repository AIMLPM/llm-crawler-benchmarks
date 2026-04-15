#!/usr/bin/env python3
"""Graduated crawl4ai verification test.

Runs crawl4ai at increasing page counts to verify the streaming +
capped-concurrency fix works at scale.  Stops early if any tier fails.

Tiers:
  T1:  50 pages  (baseline sanity check)
  T2: 200 pages  (medium scale)
  T3: 500 pages  (full benchmark scale)

Usage:
    python test_crawl4ai_graduated.py                # all tiers
    python test_crawl4ai_graduated.py --tier 1       # just T1
    python test_crawl4ai_graduated.py --site python-docs  # different site
"""
import argparse
import json
import os
import shutil
import sys
import time

# Import from the benchmark module
from benchmark_all_tools import COMPARISON_SITES
from runners.crawl4ai_runner import run as run_crawl4ai

TIERS = [
    {"name": "T1-sanity",  "max_pages": 50,  "min_success_pct": 60},
    {"name": "T2-medium",  "max_pages": 200, "min_success_pct": 50},
    {"name": "T3-full",    "max_pages": 500, "min_success_pct": 40},
]


def run_tier(tier: dict, base_dir: str, site_name: str) -> dict:
    """Run a single tier in discovery mode and return results dict."""
    max_pages = tier["max_pages"]
    out_dir = os.path.join(base_dir, f"{tier['name']}_{site_name}")
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  {tier['name']}: {max_pages} pages on {site_name} (discovery mode)")
    print(f"{'='*60}")

    start = time.time()
    try:
        pages = run_crawl4ai(
            url=COMPARISON_SITES[site_name]["url"],
            out_dir=out_dir,
            max_pages=max_pages,
            url_list=None,
        )
    except Exception as exc:
        elapsed = time.time() - start
        print(f"  CRASHED after {elapsed:.1f}s: {exc}")
        return {
            "tier": tier["name"], "max_pages": max_pages,
            "pages_saved": 0, "time_s": elapsed,
            "passed": False, "error": str(exc),
        }

    elapsed = time.time() - start
    success_pct = (pages / max_pages * 100) if max_pages > 0 else 0
    passed = success_pct >= tier["min_success_pct"]

    # Read telemetry summary if it exists
    summary_path = os.path.join(out_dir, "_telemetry_summary.json")
    telemetry = {}
    if os.path.exists(summary_path):
        with open(summary_path) as f:
            telemetry = json.load(f)

    result = {
        "tier": tier["name"],
        "max_pages": max_pages,
        "pages_saved": pages,
        "success_pct": round(success_pct, 1),
        "time_s": round(elapsed, 1),
        "pages_per_second": round(pages / elapsed, 2) if elapsed > 0 else 0,
        "passed": passed,
        "peak_rss_mb": telemetry.get("peak_rss_mb", 0),
        "error_categories": telemetry.get("error_categories", {}),
        "avg_page_s": telemetry.get("avg_page_s", 0),
        "max_page_s": telemetry.get("max_page_s", 0),
        "avg_md_bytes": telemetry.get("avg_md_bytes", 0),
        "max_md_bytes": telemetry.get("max_md_bytes", 0),
    }

    # Print tier result
    status = "PASS" if passed else "FAIL"
    print(f"\n  Result: {status}")
    print(f"  Pages: {pages}/{max_pages} ({success_pct:.0f}%)")
    print(f"  Time:  {elapsed:.1f}s ({result['pages_per_second']:.1f} pages/s)")
    print(f"  Peak RSS: {result['peak_rss_mb']:.0f} MB")
    if result["error_categories"]:
        print(f"  Errors: {json.dumps(result['error_categories'])}")
    if result["avg_page_s"]:
        print(f"  Page timing: avg {result['avg_page_s']:.3f}s, max {result['max_page_s']:.3f}s")
    if result["avg_md_bytes"]:
        print(f"  Page sizes:  avg {result['avg_md_bytes']//1024}KB, max {result['max_md_bytes']//1024}KB")

    return result


def main():
    parser = argparse.ArgumentParser(description="Graduated crawl4ai verification test")
    parser.add_argument("--site", default="fastapi-docs", help="Site to test (default: fastapi-docs)")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3], help="Run only this tier")
    parser.add_argument("--output-dir", default="/tmp/crawl4ai_graduated_test",
                        help="Base output directory")
    args = parser.parse_args()

    site_name = args.site
    if site_name not in COMPARISON_SITES:
        print(f"Unknown site: {site_name}. Available: {', '.join(COMPARISON_SITES)}")
        sys.exit(1)

    site_config = COMPARISON_SITES[site_name]
    tiers_to_run = [TIERS[args.tier - 1]] if args.tier else TIERS

    # Run tiers sequentially (discovery mode), stop on failure
    print(f"Testing crawl4ai on {site_name} (discovery mode)...")
    results = []
    all_passed = True
    for tier in tiers_to_run:
        result = run_tier(tier, args.output_dir, site_name)
        results.append(result)
        if not result["passed"]:
            all_passed = False
            print(f"\n  STOPPING: {tier['name']} failed — skipping remaining tiers")
            break

    # Final summary
    print(f"\n{'='*60}")
    print("  GRADUATED TEST SUMMARY")
    print(f"{'='*60}")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  {r['tier']:12s}  {status}  {r['pages_saved']:>3d}/{r['max_pages']:<3d} pages  "
              f"{r['time_s']:>6.1f}s  {r.get('peak_rss_mb', 0):>5.0f}MB")

    if all_passed:
        print(f"\n  ALL TIERS PASSED — crawl4ai verified at {max_needed}-page scale")
    else:
        print(f"\n  FAILED — check telemetry in {args.output_dir}/")

    # Write combined results
    results_path = os.path.join(args.output_dir, "graduated_results.json")
    os.makedirs(args.output_dir, exist_ok=True)
    with open(results_path, "w") as f:
        json.dump({"site": site_name, "results": results, "all_passed": all_passed}, f, indent=2)
    print(f"  Results saved: {results_path}")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
