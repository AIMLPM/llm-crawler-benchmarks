"""Site pool loader, stratified sampler, and run manifest.

Rationale: fixed 8-site suites are gameable. A larger pool with a
recorded seed + stratified sampling per run makes tuning-to-the-suite
much harder while keeping runs fully reproducible (anyone can replay a
run by reading its manifest.json).

See self_improvement/feedback_registry.md FR-014 for the design decision
to keep the pool open (no held-out scoring set) rather than hide sites.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import yaml

POOL_PATH = Path(__file__).parent / "pool_v1.yaml"

VALID_CATEGORIES = frozenset({
    "api_docs",
    "framework_docs",
    "blog",
    "wiki",
    "ecommerce",
    "saas_marketing",
    "tutorial",
    "reference",
    "news",
    "forum",
    "sandbox",  # test-crawling playgrounds (quotes-toscrape, books-toscrape)
})

VALID_DIFFICULTIES = frozenset({
    "static",
    "dynamic_js",
    "infinite_scroll",
    "paginated",
    "auth_walled",
    "captcha_adjacent",
    "heavy_ads",
})


@dataclass(frozen=True)
class Site:
    name: str
    url: str
    category: str
    difficulty: Tuple[str, ...]
    max_pages: int
    render_js: bool
    description: str
    has_queries: bool = False

    def as_legacy_dict(self) -> dict:
        """Return the shape existing runners expect (COMPARISON_SITES entry)."""
        d = {
            "url": self.url,
            "max_pages": self.max_pages,
            "description": self.description,
        }
        if self.render_js:
            d["render_js"] = True
        return d


@dataclass
class Pool:
    version: str
    released: str
    sites: List[Site]
    path: Path
    sha256: str

    def by_name(self, name: str) -> Optional[Site]:
        for s in self.sites:
            if s.name == name:
                return s
        return None

    def names(self) -> List[str]:
        return [s.name for s in self.sites]

    def by_category(self) -> Dict[str, List[Site]]:
        out: Dict[str, List[Site]] = {}
        for s in self.sites:
            out.setdefault(s.category, []).append(s)
        return out


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def load_pool(path: Path = POOL_PATH) -> Pool:
    """Load and validate pool_v1.yaml. Raises on structural errors."""
    if not path.exists():
        raise FileNotFoundError(f"pool file not found: {path}")
    raw = yaml.safe_load(path.read_text())
    if not isinstance(raw, dict) or "sites" not in raw:
        raise ValueError(f"{path}: missing top-level 'sites' list")

    version = str(raw.get("version", "unspecified"))
    released = str(raw.get("released", ""))

    sites: List[Site] = []
    seen_names: set = set()
    for i, entry in enumerate(raw["sites"]):
        name = entry.get("name")
        if not name:
            raise ValueError(f"{path} entry {i}: missing 'name'")
        if name in seen_names:
            raise ValueError(f"{path}: duplicate site name '{name}'")
        seen_names.add(name)

        cat = entry.get("category")
        if cat not in VALID_CATEGORIES:
            raise ValueError(
                f"{path} site '{name}': category '{cat}' not in "
                f"{sorted(VALID_CATEGORIES)}"
            )

        diff = tuple(entry.get("difficulty") or [])
        for d in diff:
            if d not in VALID_DIFFICULTIES:
                raise ValueError(
                    f"{path} site '{name}': difficulty '{d}' not in "
                    f"{sorted(VALID_DIFFICULTIES)}"
                )

        sites.append(Site(
            name=name,
            url=str(entry["url"]),
            category=cat,
            difficulty=diff,
            max_pages=int(entry.get("max_pages", 50)),
            render_js=bool(entry.get("render_js", False)),
            description=str(entry.get("description", "")),
            has_queries=bool(entry.get("has_queries", False)),
        ))

    return Pool(
        version=version,
        released=released,
        sites=sites,
        path=path,
        sha256=_sha256_file(path),
    )


def sample(
    pool: Pool,
    *,
    seed: int,
    per_category: "int | Dict[str, int]",
    required_categories: Iterable[str] = (),
    requires_queries: bool = False,
    only: Optional[Iterable[str]] = None,
) -> List[Site]:
    """Deterministic stratified sample from the pool.

    - seed: any int; same seed + same pool = same sample.
    - per_category: int applied uniformly, or {category: N} for per-category
      counts.
    - required_categories: each listed category must contribute at least one
      site; raises if the pool can't satisfy this.
    - requires_queries: only sample sites where has_queries is true (needed
      for retrieval + answer-quality benchmarks).
    - only: if given, restrict to sites whose name is in this iterable
      (bypasses sampling — used for --sites CLI flag).
    """
    if only is not None:
        wanted = set(only)
        chosen = [s for s in pool.sites if s.name in wanted]
        missing = wanted - {s.name for s in chosen}
        if missing:
            raise ValueError(f"sites not in pool: {sorted(missing)}")
        return chosen

    eligible = [s for s in pool.sites if (not requires_queries or s.has_queries)]
    by_cat: Dict[str, List[Site]] = {}
    for s in eligible:
        by_cat.setdefault(s.category, []).append(s)

    rng = random.Random(seed)
    chosen: List[Site] = []

    if isinstance(per_category, int):
        per_cat_map = {cat: per_category for cat in by_cat}
    else:
        per_cat_map = dict(per_category)

    for cat, cat_sites in by_cat.items():
        n = per_cat_map.get(cat, 0)
        if n <= 0:
            continue
        # random.sample raises if n > len; clamp to available.
        n = min(n, len(cat_sites))
        chosen.extend(rng.sample(cat_sites, n))

    present_cats = {s.category for s in chosen}
    for req in required_categories:
        if req not in present_cats:
            raise ValueError(
                f"required category '{req}' not satisfied by sample "
                f"(per_category={per_cat_map}, requires_queries={requires_queries})"
            )

    chosen.sort(key=lambda s: s.name)
    return chosen


def _atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=False)
            f.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def write_manifest(
    run_dir: Path,
    *,
    pool: Pool,
    seed: int,
    sampled: List[Site],
    sample_strategy: dict,
    tool_versions: Optional[Dict[str, str]] = None,
    git_sha: Optional[str] = None,
    benchmark_version: Optional[str] = None,
) -> Path:
    """Write runs/<run_id>/manifest.json atomically. Returns the manifest path."""
    manifest = {
        "run_id": run_dir.name,
        "benchmark_version": benchmark_version or "unspecified",
        "pool_version": pool.version,
        "pool_hash": pool.sha256,
        "pool_path": str(pool.path.name),
        "seed": int(seed),
        "sample_strategy": sample_strategy,
        "sampled_sites": [
            {"name": s.name, "category": s.category,
             "difficulty": list(s.difficulty), "has_queries": s.has_queries}
            for s in sorted(sampled, key=lambda x: x.name)
        ],
        "tool_versions": tool_versions or {},
        "git_sha": git_sha or "",
        "timestamp_utc": datetime.now(tz=timezone.utc).isoformat(),
    }
    path = run_dir / "manifest.json"
    _atomic_write_json(path, manifest)
    return path


def read_manifest(run_dir: Path) -> Optional[dict]:
    """Return the manifest for a run, or None if it doesn't exist (legacy run)."""
    p = run_dir / "manifest.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        raise ValueError(f"{p}: corrupt manifest: {e}") from e


def sites_for_run(run_dir: Path, pool: Pool) -> List[Site]:
    """Return the Site list for an existing run.

    If the run has a manifest, use its sampled_sites. If not (legacy), fall
    back to any subdirectories under the first tool dir that look like
    site directories with pages.jsonl — cross-referenced against the pool.
    Raises if neither path works.
    """
    manifest = read_manifest(run_dir)
    if manifest:
        names = [s["name"] for s in manifest.get("sampled_sites", [])]
        sites = [pool.by_name(n) for n in names]
        missing = [n for n, s in zip(names, sites) if s is None]
        if missing:
            # Manifest references sites the current pool doesn't know about.
            # That's a pool-version mismatch — surface it loudly.
            raise ValueError(
                f"manifest in {run_dir} references sites not in current pool "
                f"{pool.path.name}: {missing}. Run recorded pool_version="
                f"{manifest.get('pool_version')}, current={pool.version}."
            )
        return [s for s in sites if s is not None]

    # Legacy path: inspect the run dir for site subdirs.
    discovered: set = set()
    for tool_dir in run_dir.iterdir():
        if not tool_dir.is_dir():
            continue
        for site_dir in tool_dir.iterdir():
            if site_dir.is_dir() and (site_dir / "pages.jsonl").exists():
                discovered.add(site_dir.name)
    if not discovered:
        raise ValueError(f"no manifest and no site subdirs found in {run_dir}")
    sites = [pool.by_name(n) for n in sorted(discovered)]
    missing = [n for n, s in zip(sorted(discovered), sites) if s is None]
    if missing:
        raise ValueError(
            f"legacy run {run_dir.name} contains sites not in current pool: {missing}"
        )
    return [s for s in sites if s is not None]


__all__ = [
    "POOL_PATH",
    "Pool",
    "Site",
    "VALID_CATEGORIES",
    "VALID_DIFFICULTIES",
    "load_pool",
    "read_manifest",
    "sample",
    "sites_for_run",
    "write_manifest",
]
