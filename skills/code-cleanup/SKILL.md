---
name: code-cleanup
description: >-
  Proves and removes dead, obsolete, or duplicate code while preserving runtime
  contracts. Use for deletion-focused cleanup or goal-loop cruft reduction — not
  in-place readability refactors.
disable-model-invocation: true
---

# Code Cleanup

Remove dead code, obsolete contracts, and true duplicates without changing live behavior. Prove before deleting, from reachability and contracts, not tool reports. No style refactors.

`AGENTS.md` headings. A body that starts with `TODO` counts as missing; ask rather than guess:

- `Entry points`: where reachability starts.
- `Proof traps`: contracts to confirm before deleting. Reachability alone is not proof while this list is unknown.
- `Build & test`: lint and test commands for the baseline and after each batch.
- `File layout`: disjoint areas to split a fan-out on.

## Loop

1. Scope the surface and when to stop.
2. Baseline: lint and tests.
3. Trace reachability from the entry points.
4. Prove 1–5 candidates: imports, wiring, tests, persistence keys, use from other areas, and the proof traps.
5. Delete the proven batch, run lint and tests, and record the result.

Defer layer moves, new dependencies, persistence changes, and product-scope changes.

## Ledger

```markdown
| ID | Candidate | Evidence | Status |
| --- | --- | --- | --- |
| C-1 | helper under the old name | no refs; the caller uses the other helper | validated |
```

Statuses: `candidate`, `safe-to-remove`, `changed`, `validated`, `deferred`, `rejected`. The ledger goes in the response. A cleanup that spans a goal keeps it, with deferred refactors and next steps, in a scratch file the goal names and deletes on ship. Never commit it.

## Fan out

Fan out when the scope covers two or more `File layout` areas, one area is too big to prove alone, the change adds or removes fixture files (one slice proves each remaining file still has a reader), or it is a broad cruft pass. Launch read-only explorers together, one per area. If `File layout` does not name the split, ask; do not invent areas. Explorers return candidate tables only. The orchestrator alone edits, validates, and keeps the ledger. Paste the surface, the loop, and the proof traps into each explorer's prompt.

## Report

Surface, candidates and evidence, edits, validation, residue.
