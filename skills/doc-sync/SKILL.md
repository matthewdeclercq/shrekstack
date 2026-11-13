---
name: doc-sync
description: >-
  Keeps a repo's docs true to its code: detects doc drift
  on the current branch and fixes it. Use before opening a pull request, or
  when the user asks to sync docs or fix doc drift. Pass --full to audit
  every doc against the whole codebase.
---

# Doc Sync

Keep this repo's docs true to its code. **This workflow auto-fixes:** apply the edits, then report what changed. It never commits.

Be surgical. Change only what is drifted, missing, contradictory, or bloated. Never rewrite accurate prose or expand a section — the bias is toward fewer, tighter docs.

**The docs.** In scope: every doc the doc map names (`doc-map.md` in `.agents/`, from [doc-steward](../doc-steward/SKILL.md)), every `AGENTS.md`, `README.md`, and `.agents/skills/`. The planning docs the map names (decision, goals, backlog, shipped, dropped-design) and spike write-ups are report-only unless the user widens scope; doc-steward owns them. If the map is missing, say to run doc-steward's Bootstrap first.

**The code.** `Code roots` in `AGENTS.md` lists the path prefixes that count as code. If it is missing, ask before check 5; do not treat every changed file as code.

## Diff

By default, the branch against the default branch (`git merge-base HEAD origin/HEAD`), including uncommitted work. If `origin/HEAD` is not set, ask which branch. With `--full`, no diff: audit every doc in scope against the whole codebase (expensive; always fan out).

From the diff: `CHANGED` (files), and `CHANGED_CODE` (those under a prefix in `Code roots`). If `CHANGED` is empty and the run is not `--full`, say so and stop.

- **Skills due:** `--full`, or `CHANGED` touches a skill file.
- **Architecture due:** `--full`, or `CHANGED` adds, deletes, or renames a source file or folder.

**Fan out** when `--full`, more than 15 files changed, or the diff spans more than three top-level areas: one explorer per check below, each returning doc location, claim, and what is true. Otherwise work inline.

## Checks

Start every run with this skill's `scripts/dead-paths.py`. Run that file by its path. Do not assume the current directory is the skill directory or the target repo. `--root` is the target repo. Pass each doc in scope as its own `--doc-folder` value (a file or a directory):

```bash
python3 "<skill>/scripts/dead-paths.py" --root "<repo>" --doc-folder "<doc in scope>"
```

It reads `Code roots` itself; its docstring has the details. Each line it prints is a doc naming a path the tree no longer has — a check 1, 3, or 4 fix. A hit in a report-only doc is reported, not fixed. It sees paths only; the claims below stay yours.

**1 — Drift (every doc in scope but the report-only ones).** Verify every concrete claim — paths, layout, commands, names, and links. Fix each false claim in place, keeping the phrasing around it. Never expand goal prose into `AGENTS.md`.

**2 — Coverage (the `AGENTS.md` files and `README.md`).** Anything `CHANGED` introduces that a contributor needs — a new folder, script, target, fixture, build step — gets a minimal entry in its natural section. No new top-level section unless it has no home; no planning-doc depth. Place each entry by the base rule's README split; what only one area uses goes in that area's `AGENTS.md`, the rest in the root one.

**3 — Skills (when due).** In every skill but a `verify-*` one, fix only dead paths and references to deleted docs — never rewrite a procedure. A verify skill is report-only: name [maintain-verify](../maintain-verify/SKILL.md), which re-drives what it fixes.

**4 — Architecture (when due).** Factual claims only, in the architecture doc: module layout, named types and services, pipeline steps, storage paths, commands, test targets, and every mermaid node and edge, against the code and the section's prose. Fix each false fact, node, or edge in place. Never touch design intent or rationale. What counts as missing, and how a diagram may change, is doc-steward rule 9.

**5 — Planning conflicts, report only.** List where `CHANGED_CODE` and a planning doc disagree: a rule the code breaks, a shipped row whose code is gone, a guardrail the code no longer meets. Never change code to match — the owner decides which side is wrong.

**Trimming, in every doc touched.** Cut sentences that restate a neighbour, a fact a `README.md` and an `AGENTS.md` both hold, duplicate examples, and filler. Never strip gotchas, constraints, exact commands, or paths; when unsure, leave it. In the root `AGENTS.md`, move a fact only one area needs to that area's `AGENTS.md`.

In the other docs in scope, fix broken references *to* the planning docs, and drop references to deleted docs.

## Report

Bullets, no banners:

1. The diff in one line ("branch vs main, 44 files", or "`--full`").
2. Each fix, one line, grouped by file.
3. Planning conflicts from check 5, one line each (row, file:line, what differs) — or "none".
4. Anything deliberately skipped.
5. That the fixes are uncommitted.
