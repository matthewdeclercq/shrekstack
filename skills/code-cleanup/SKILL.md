---
name: code-cleanup
description: >-
  Proves and removes dead, obsolete, or duplicate code while preserving runtime
  contracts. Use for deletion-focused cleanup or goal-loop cruft reduction — not
  in-place readability refactors.
disable-model-invocation: true
---

# Code Cleanup

Remove dead code, obsolete contracts, and true duplicates without changing live behavior.

Deletes unused surfaces after proof; does not refactor live code for style.

Work from reachability and contracts, not tool reports. Read the target repo's `AGENTS.md` first.

Use these headings (any heading level, text after the hashes exactly as written):

| Heading | What it holds | If it is missing or empty |
|---------|----------------|---------------------------|
| `Entry points` | Where reachability starts | Ask. Do not pick a root |
| `Proof traps` | Contracts to confirm before deleting | Ask. Do not delete while the contract list is unknown |
| `Build & test` | Lint and test commands for the baseline and for validation | Ask. Do not guess a command |
| `File layout` | Disjoint areas a multi-agent pass may split on | Ask before fanning out. Do not invent areas. A surface the user already named can be worked inline |
| `Doc folders` | Doc trees the ledger must not be checked into | Do not check the ledger into the repo. Ask before writing it into any tree that might hold docs |

## Loop

1. Scope surface + stopping condition
2. Baseline — lint and tests per `Build & test`
3. Trace reachability from `Entry points`
4. Prove 1–5 candidates (imports, wiring, tests, persistence keys, cross-area usage)
5. Edit proven batch → validate with `Build & test` → record result

Defer layer moves, new dependencies, persistence changes, and product-scope changes.

## Proof traps

Confirm the contracts listed under `Proof traps` before deleting. Reachability alone is not enough while that list is unknown.

## Ledger

**One-turn** — compact table in the response:

```markdown
| ID | Candidate | Evidence | Status |
| --- | --- | --- | --- |
| C-1 | `FooHelper` | no refs; the caller uses `BarHelper` | validated |
```

**Goal loop** — same table, plus `## Review After Cleanup` (deferred refactors, not action items) and `## Next Steps`, in a scratch file the goal names and deletes on ship. Do not check the ledger into a folder listed under `Doc folders`. If `Doc folders` is missing, do not check the ledger in.

Statuses: `candidate`, `safe-to-remove`, `changed`, `validated`, `deferred`, `rejected`.

## Multi-agent

For large diffs or multi-area surfaces, **fan out** — launch parallel readonly explorers in one turn, one per disjoint slice. Do not serially walk the tree yourself when the scope spans more than one area `File layout` names.

**Fan out when:**

- Scope covers 2 or more areas named in `File layout`
- The diff adds or removes files under a fixture or sample tree `File layout` names — one slice proves each remaining file still has a reader
- A single area is too large for one agent to prove thoroughly
- The goal is a broad cruft pass, not a known 1–5 candidate batch

**Split by** the areas `File layout` names — as many as needed, launched together. If `File layout` does not name the split, ask. Do not invent areas.

Explorers return candidate tables only. The orchestrator alone edits, validates, and updates the ledger. Subagents do not inherit this skill — paste the surface, loop steps, and proof traps into each dispatch prompt.

## Output

Surface, candidates + evidence, edits, validation result, residue.
