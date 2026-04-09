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

_No entries yet for this repo. Previous entries (FR-001 through FR-006)
applied to the [markcrawl](https://github.com/AIMLPM/markcrawl) repo's
README and were retained there during the repo split._

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
