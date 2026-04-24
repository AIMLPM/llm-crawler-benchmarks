# Feedback Registry

**Purpose:** Persistent record of user and reviewer feedback that drove changes
to the project. Before removing, reorganizing, or simplifying any content, an
LLM reviewer MUST check this registry to see if that content was added for a
documented reason.

**Rule:** If a change would remove or weaken something listed here, the reviewer
must either (a) keep it, or (b) explain in the commit message why the feedback
no longer applies and remove the registry entry.

---

## How to use this file

**Before removing content:** Search this registry for the file or feature you're
about to change. If there's an entry, read the "Why it matters" field. If you
still think the removal is correct, document your reasoning in the commit message
and update this entry.

**After incorporating feedback:** Add a new entry below. Include enough context
that a future reviewer who has never seen the original conversation understands
why this content exists.

---

## Registry entries

_FR-001 through FR-006 applied to the
[markcrawl](https://github.com/AIMLPM/markcrawl) repo's README and were
retained there during the repo split. Numbering continues from FR-007 below
to avoid collision when searching git history across both repos._

### FR-013: Do not bold markcrawl rows in tables

- **Date:** 2026-04-16
- **Source:** User, during report review ("I see that we have 'markcrawl'
  in bold in the charts... I think we should remove the bold as it seems
  to add a bias")
- **What was added:** Removed the bold-markcrawl formatting from every
  report generator (`benchmark_all_tools.py`, `benchmark_retrieval.py`,
  `benchmark_pipeline.py`, `benchmark_answer_quality.py`,
  `quality_scorer.py`, `generate_readme.py`). Flipped
  `lint_reports.py` check #6 from "markcrawl row should be bolded" to
  "markcrawl row must not be bolded." Updated CLAUDE.md Formatting and
  README.md page-specific rules to match.
- **Why it matters:** Bolding the authoring tool's row in head-to-head
  comparison tables is a visual bias that undermines the benchmark's
  credibility with senior reviewers. The sort order and numbers already
  communicate ranking; extra emphasis on markcrawl implies a marketing
  intent. This supersedes the earlier convention that came over from the
  markcrawl repo's README context.
- **Protected content:** `_bold_if_mc()` in `generate_readme.py` remains a
  no-op wrapper (do not re-enable); the flipped linter check in
  `lint_reports.py` (#6); the CLAUDE.md bullets under "Formatting" and
  README.md rules that explicitly say *do not* bold markcrawl.
- **Do NOT:** Re-introduce `f"**{tool}**" if tool == "markcrawl" else tool`
  patterns in any generator; re-enable `_bold_if_mc` to actually bold;
  flip the linter back to requiring bold; add bolding to the markcrawl
  row "just for scannability."

### FR-007: Summary tables must include all 7 tools, ranked

- **Date:** 2026-04-16
- **Source:** User, during style-guide authoring (codified in CLAUDE.md,
  "Tone and credibility" section)
- **What was added:** Rule in CLAUDE.md that summary tables must show every
  tool, sorted by the primary metric, with markcrawl placed only where it
  actually ranks.
- **Why it matters:** Omitting tools that beat markcrawl on a given metric
  would make the benchmark look like marketing. The repo's credibility
  depends on readers seeing losses as plainly as wins. This is also what the
  `lint_reports.py` `all-tool inclusion` check enforces.
- **Protected content:** The all-tools summary tables in
  `SPEED_COMPARISON.md`, `QUALITY_COMPARISON.md`, `RETRIEVAL_COMPARISON.md`,
  `ANSWER_QUALITY.md`; the `lint_reports.py` check that enforces inclusion.
- **Do NOT:** Remove tools from summary tables because they beat markcrawl;
  re-sort to put markcrawl first when it did not earn that rank; remove the
  linter check.

### FR-008: No emojis in benchmark reports

- **Date:** 2026-04-16
- **Source:** User, repeated corrections during report review (codified in
  CLAUDE.md "Formatting")
- **What was added:** Linter rule + style-guide rule banning emojis from all
  `reports/*.md`. Recent commits (`6d5a839`, `07d84c1`) specifically fixed
  emoji lint failures that slipped into generated reports.
- **Why it matters:** Emojis make benchmark reports read as marketing rather
  than engineering artifacts. Senior/principal engineers explicitly flagged
  this as a credibility signal.
- **Protected content:** `lint_reports.py` emoji check; the "No emojis"
  bullet in CLAUDE.md Formatting section; absence of emojis in all report
  generators (`benchmark_*.py`, `quality_scorer.py`, etc.).
- **Do NOT:** Add emojis to report output, even "just one" for emphasis;
  weaken the linter check; allow emojis because a generator function looks
  cleaner with them.

### FR-009: One-line answer must state a concrete finding, not describe the report

- **Date:** 2026-04-16
- **Source:** User feedback during report review (codified in CLAUDE.md
  "Structure (all reports)")
- **What was added:** Rule that every report's first sentence must contain a
  concrete result -- a number, ranking, or verdict -- not a meta-description
  of what the report measures. Enforced by the `lint_reports.py` one-line
  answer check.
- **Why it matters:** Readers who bounce after the first sentence (most of
  them) need the finding, not a restatement of the title. "This benchmark
  measures answer quality across 7 tools" fails; "Yes, but modestly" or
  "MarkCrawl achieves 5.99 pages/sec across 227 pages" succeeds.
- **Protected content:** First-sentence convention in every report; the
  `lint_reports.py` one-line answer check.
- **Do NOT:** Open a report by describing what it measures; weaken the
  linter check; let generators emit "This report compares..." intros.

### FR-010: Retrieval results must show raw hit counts alongside percentages

- **Date:** 2026-04-16
- **Source:** User feedback during retrieval report review (codified in
  CLAUDE.md "Page-specific rules" for RETRIEVAL_COMPARISON.md)
- **What was added:** Retrieval tables render "42% (39/92)" rather than bare
  percentages, so readers can see sample size and judge whether a gap is
  meaningful. 95% confidence intervals accompany aggregate MRR.
- **Why it matters:** A bare "42%" hides whether the denominator is 10 or
  1000. Senior reviewers need to distinguish noise from signal. The
  per-site coverage disclosure is what makes claims like "scrapy+md is an
  outlier" (line 90 of RETRIEVAL_COMPARISON.md) defensible rather than
  cherry-picked.
- **Protected content:** `_fmt_rate()` in `benchmark_retrieval.py` and its
  "NN/DD (PP%)" output; 95% CI computation on MRR; per-site page-count
  columns.
- **Do NOT:** Strip raw counts to "clean up" tables; remove CIs; collapse
  per-site breakdowns into aggregates only.

### FR-011: Honest framing of retrieval similarity -- tools cluster, differences are modest

- **Date:** 2026-04-16
- **Source:** User feedback on RETRIEVAL_COMPARISON.md "What this means"
  section (codified in CLAUDE.md "Page-specific rules")
- **What was added:** The narrative explicitly acknowledges that retrieval
  MRR is similar across most tools, explains why (same seed URLs, same
  chunking/embedding pipeline), and redirects readers to "retrieval mode
  matters more than crawler choice." Outlier detection now flags tools that
  sit noticeably below the cluster rather than averaging them in.
- **Why it matters:** A crawler benchmark that claims big retrieval wins
  for its own tool when differences are within noise destroys trust.
  Honestly framing the similar-cluster finding and naming outliers
  explicitly is exactly what makes the rest of the report credible.
- **Protected content:** The "What this means" section of
  `RETRIEVAL_COMPARISON.md`; the outlier-detection logic in
  `benchmark_retrieval.py` (`generate_retrieval_report()`, around the
  `emb_mrrs_sorted` block); the "retrieval mode matters more than crawler
  choice" paragraph.
- **Do NOT:** Replace the cluster framing with a markcrawl-wins narrative;
  remove the outlier-detection branch; drop the "retrieval mode matters
  more" redirect.

### FR-012: Cost tables must anchor to pricing assumptions

- **Date:** 2026-04-16
- **Source:** User feedback during COST_AT_SCALE.md review (codified in
  CLAUDE.md "Formatting" and "Page-specific rules")
- **What was added:** Every cost table includes (or links to) the specific
  pricing inputs used -- embedding model + rate, vector DB pricing, LLM
  rate. Storage costs and query costs are reported separately because they
  scale with different inputs (pages vs query volume).
- **Why it matters:** An engineering manager deciding whether to switch
  tools based on "$17/month" needs to know that number came from OpenAI
  text-embedding-3-small at $0.02/1M tokens, not from hidden assumptions.
  Combining storage and query costs into one table obscures the growth
  curve.
- **Protected content:** Pricing-assumption parentheticals and links in
  `COST_AT_SCALE.md`; the storage-vs-query separation; the named scenarios
  (small app, mid-size, large-scale).
- **Do NOT:** Drop the pricing-source parentheticals to "clean up" tables;
  merge storage and query costs into one table; update final dollar numbers
  without also updating the linked formulas.

---

## Adding new entries

Use this template:

```markdown
### FR-NNN: Short title

- **Date:** YYYY-MM-DD
- **Source:** Who gave the feedback (user, LLM reviewer, external tester)
- **What was added:** What changed and where
- **Why it matters:** The problem that prompted the change
- **Protected content:** Specific elements that must not be removed
- **Do NOT:** Specific actions that would undo this feedback
```

Increment the FR number sequentially. Use the next available number.
