---
name: doc-sync
description: >-
  Keeps a repo's docs and code comments true to its code: detects doc drift
  on the current branch, fixes it, and commits the result as "Doc sync." Use
  before opening a pull request, or when the user asks to sync docs or fix doc
  drift. Pass --full to audit every doc against the whole codebase.
disable-model-invocation: true
---

# Doc Sync

Keep this repo's docs true to its code. **This workflow auto-fixes:** apply the edits, commit them, then report what changed.

Be surgical. Change only what is drifted, missing, contradictory, or bloated. Never rewrite accurate prose or expand a section — the bias is toward fewer, tighter docs.

**The docs.** In scope: every doc the doc map names (`doc-map.md` in `.agents/`, from [doc-steward](../doc-steward/SKILL.md)), `AGENTS.md`, `README.md`, and `.agents/skills/`. The planning docs the map names (decision, goals, backlog, shipped, dropped-design) are report-only. If the map is missing, say to run doc-steward's Bootstrap first.

**The code.** `Code roots` in `AGENTS.md` lists the path prefixes that count as code. A heading whose body starts with `TODO` counts as missing. If it is missing, ask before checks 5 and 6; do not treat every changed file as code.

## Diff

By default, the branch against the default branch (`git merge-base HEAD origin/HEAD`), including uncommitted work. If `origin/HEAD` is not set, ask which branch. With `--full`, no diff: audit every doc in scope against the whole codebase (expensive; always fan out).

From the diff: `CHANGED` (files), and `CHANGED_CODE` (those under a prefix in `Code roots`). If `CHANGED` is empty and the run is not `--full`, say so and stop.

- **Skills due:** `--full`, or `CHANGED` touches a skill file.
- **Architecture due:** `--full`, or `CHANGED` adds, deletes, or renames a source file or folder.

**Fan out** when `--full`, more than 15 files changed, or the diff spans more than three top-level areas: spawn one read-only subagent per check below, each told to run that check and return findings only (doc location, claim, what is true). Apply every edit yourself. Otherwise work inline.

## Checks

Start every run with this skill's `scripts/dead-paths.py`. Run that file by its path. Do not assume the current directory is the skill directory or the target repo. `--root` is the target repo. Pass each doc in scope as its own `--doc-folder` value (a file or a directory):

```bash
python3 "<skill>/scripts/dead-paths.py" --root "<repo>" --doc-folder "<doc in scope>"
```

The script reads the `Code roots` heading in that repo's `AGENTS.md` when `--code-root` is omitted. Pass `--code-root` only to override that heading. A bare type name is checked against those roots. An extensionless path whose first directory is gone is still skipped. If `Code roots` is missing and you do not pass `--code-root`, the script does not guess roots and does not check bare type names. The script treats a file as that file and a directory as the markdown under it. Each line it prints is a doc naming a path the tree no longer has — a check 1, 3, or 4 fix. It sees paths only; the claims below stay yours. Exit 2 means no doc was passed.

**1 — Drift (every doc in scope but the planning docs).** Verify every concrete claim — paths, layout, commands, names, and links. Fix each false claim in place, keeping the phrasing around it. Never expand goal prose into `AGENTS.md`.

**2 — Coverage (`AGENTS.md` and `README.md`).** Anything `CHANGED` introduces that a contributor needs — a new folder, script, target, fixture, build step — gets a minimal entry in its natural section. No new top-level section unless it has no home; no planning-doc depth. The root `README.md` is the repo's front door — folder map and prereqs — and links to every other fact rather than copying it: only a new top-level folder or prereq goes there; scripts and build steps go in `AGENTS.md`.

**3 — Skills (when due).** In every skill, fix only dead paths and references to deleted docs — never rewrite a procedure. Also, from the repo's UI conventions skill at `.agents/skills/ui` (not the bootstrap skill that writes it), delete screen inventories (button copy, field lists, icons, defaults), not its reference-screen or casing tables.

**4 — Architecture (when due).** Factual claims only, in the architecture doc: module layout, named types and services, pipeline steps, storage paths, commands, test targets, and every mermaid node and edge, against the code and the section's prose. Fix the fact in place. Report a missing module only when it changes how the parts connect; never a type's internals. Never touch design intent or rationale. Fix a false node or edge in place and do not redraw the diagram (doc-steward rule 9).

**5 — Comments (`CHANGED_CODE` only).** Apply the Comments section of [base.md](../bootstrap-repo/base.md): delete comments that restate code, and fix or delete stale ones. Do not sweep files the diff did not touch.

**6 — Planning conflicts, report only.** List where `CHANGED_CODE` and a planning doc disagree: a rule the code breaks, a shipped row whose code is gone, a guardrail the code no longer meets. Never edit those docs or change code to match — the owner decides which side is wrong.

**Trimming, in every doc touched.** Cut sentences that restate a neighbour, duplicate examples, and filler. In an architecture doc, cut file catalogs, UI chrome, and restated product rules. Never strip gotchas, constraints, exact commands, or paths; when unsure, leave it.

## Out of scope

Never edit a planning doc unless the user widens scope; doc-steward owns them. Fix broken references *to* them, and drop references to deleted docs, in the other docs in scope.

## Commit

If the run edited files, commit only those paths (`git add -- <paths>`, never `-A`), check `git diff --cached --stat`, and commit with the subject `Doc sync.` No commit when nothing changed.

## Report

Short prose, no banners:

1. The diff in one line ("branch vs main, 44 files", or "`--full`").
2. Each fix, one line, grouped by file.
3. Planning conflicts from check 6, one line each (row, file:line, what differs) — or "none".
4. Anything deliberately skipped.
5. Whether `Doc sync.` landed.
