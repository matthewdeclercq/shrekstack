---
name: prune-code
description: >-
  Proves and removes dead, obsolete, or duplicate code while preserving runtime
  contracts. Use for deletion-focused cleanup or goal-loop cruft reduction — not
  in-place readability refactors.
disable-model-invocation: true
---

# Prune Code

Remove dead code, obsolete contracts, true duplicates, and dead comments without changing live behavior. Prove before deleting, from reachability and contracts, not tool reports. No style refactors.

`AGENTS.md` headings, and `Proof traps` in the `AGENTS.md` of each area in scope too; when one is missing, ask rather than guess:

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

Statuses: `candidate`, `safe-to-remove`, `changed`, `validated`, `deferred`, `rejected`. A cleanup that spans a goal keeps deferred refactors and next steps in the ledger too.

## Comments

In scope, cut every comment the base rule's Comments section forbids. Cutting a comment changes no behavior, so it skips the proof step. Do not reshape code here; log it as `deferred` instead:

- A comment that explains a surprise in our own code: keep it, and log the rename, extract, or type that would make it obvious.
- A lint suppression whose rule guards correctness: log the code fix the rule wants.

## Fan out

Fan out when the scope covers two or more `File layout` areas, one area is too big to prove alone, the change adds or removes fixture files (one slice proves each remaining file still has a reader), or it is a broad cruft pass. Launch read-only explorers together, one per `File layout` area. Each returns a candidate table. Paste the surface, the loop, and the proof traps into each explorer's prompt.

## Report

Surface, candidates and evidence, edits, validation, residue.
