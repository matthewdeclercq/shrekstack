---
name: doc-sync
description: >-
  Keeps the docs listed in the target repo's AGENTS.md, and code comments, in
  sync with the codebase — detects doc drift, auto-fixes it, and commits the
  result as "Doc sync." Use when the user asks to sync docs, fix doc drift,
  update AGENTS.md or README, or run doc-sync with scope agents, readme,
  architecture, skills, comments, or all.
disable-model-invocation: true
---

# Doc Sync

Keep this repo's docs true to its code. **This workflow auto-fixes:** apply the edits, commit them, then report what changed.

Be surgical. Change only what is drifted, missing, contradictory, or bloated. Never rewrite accurate prose or expand a section — the bias is toward fewer, tighter docs. Which doc owns which fact: `doc-map.md` in `.agents/` ([doc-steward](../doc-steward/SKILL.md)). If that file is missing, say to run doc-steward's Bootstrap first.

Read `AGENTS.md` first. Use these headings (any heading level, text after the hashes exactly as written). A heading whose body starts with `TODO` counts as missing:

| Heading | What it holds | If it is missing or empty |
|---------|----------------|---------------------------|
| `Doc folders` | Files and directories in scope for checks 1–5 | Ask. Do not pick a doc list |
| `Architecture doc` | The one doc check 5 may edit | Ask when scope is `architecture` or check 5 is due. Do not guess which doc is the architecture doc |
| `Code roots` | Path prefixes that count as code for comment edits and for the planning-conflict report | Ask before check 6 or 7. Do not treat every changed file as code |
| `Planning docs` | Docs to report against and never edit, unless the user widens scope | Ask which docs are report-only. Until the owner answers, do not edit a doc you are unsure about |

## Setup

Arguments come from the user message (e.g. `all`, `agents --working`, `skills --full`).

**Scope** — first non-flag word:

| Scope | Checks |
|-------|--------|
| `agents` / `readme` | 1–2 on that file |
| `architecture` | 5, on the doc named under `Architecture doc` |
| `skills` | 4 |
| `comments` | 6 |
| `all` or omitted | 1–7, with 4 and 5 only when due (below) |

**Diff source** — flag:

| Flag | Diff |
|------|------|
| omitted | Branch vs the default branch (`git merge-base HEAD origin/HEAD`), including uncommitted work. If `origin/HEAD` is not set, ask which branch |
| `--working` | `git diff HEAD` |
| `--staged` | `git diff --cached` |
| `--from <ref>` | vs `<ref>`, including uncommitted |
| `--full` | No diff: audit every in-scope doc against the whole codebase (expensive; always fan out) |

From the diff: `CHANGED` (files), and `CHANGED_CODE` (those under a prefix in `Code roots`). If `CHANGED` is empty and the run is neither `--full` nor `skills`, say so and stop. If check 6 or 7 is in scope and `Code roots` is missing, ask before those checks. Do not treat every changed file as code.

- **Skills due:** scope `skills`, `--full`, or `CHANGED` touches a skill file.
- **Architecture due:** scope `architecture`, `--full`, or `CHANGED` adds, deletes, or renames a source file or folder.

**Fan out** when `--full`, more than 15 files changed, or the diff spans more than three top-level areas: spawn one read-only subagent per check below, each told to run that check and return findings only (doc location, claim, what is true). Apply every edit yourself. Otherwise work inline.

## Checks

Start every run with this skill's `scripts/dead-paths.py`, after `Doc folders` is known. Run that file by its path. Do not assume the current directory is the skill directory or the target repo. `--root` is the target repo. Pass each `Doc folders` entry as its own `--doc-folder` value (a file or a directory):

```bash
python3 "<skill>/scripts/dead-paths.py" --root "<repo>" --doc-folder "<doc folders entry>"
```

The script reads the `Code roots` heading in that repo's `AGENTS.md` when `--code-root` is omitted. Pass `--code-root` only to override that heading. A bare type name is checked against those roots. An extensionless path whose first directory is gone is still skipped. If `Code roots` is missing and you do not pass `--code-root`, the script does not guess roots and does not check bare type names. The script treats a file as that file and a directory as the markdown under it. Each line it prints is a doc naming a path the tree no longer has — a check 1, 4, or 5 fix. It sees paths only; the claims below stay yours. Exit 2 means the doc list was not passed: ask, do not pick a default list.

**1 — Drift (every file `Doc folders` names, including `AGENTS.md` and `README.md` when they are listed).** Verify every concrete claim — paths, layout, commands, names, and links. Fix each false claim in place, keeping the phrasing around it. Never expand goal prose into `AGENTS.md`.

**2 — Coverage (`AGENTS.md` and `README.md`, when `Doc folders` lists them).** Anything `CHANGED` introduces that a contributor needs — a new folder, script, target, fixture, build step — gets a minimal entry in its natural section. No new top-level section unless it has no home; no planning-doc depth. The root `README.md` is the repo's front door — folder map and prereqs — and links to every other fact rather than copying it: only a new top-level folder or prereq goes there; scripts and build steps go in `AGENTS.md`. If `Doc folders` does not list one of those files, ask before editing it.

**3 — Consistency.** One correct version of each fact across the files `Doc folders` names. The map names the owner: it keeps the fact, the others point. If the map is missing, say to run doc-steward's Bootstrap first. If it names no owner for that fact, ask. Do not guess an owner.

**4 — Skills (when due).** In every skill, fix only dead paths and references to deleted docs — never rewrite a procedure. Also, from the repo's UI conventions skill at `.agents/skills/ui` (not the bootstrap skill that writes it), delete screen inventories (button copy, field lists, icons, defaults), not its reference-screen or casing tables.

**5 — Architecture (when due).** Factual claims only, in the doc named under `Architecture doc`: module layout, named types and services, pipeline steps, storage paths, commands, test targets, and every mermaid node and edge, against the code and the section's prose. Fix the fact in place. Report a missing module only when it changes how the parts connect; never a type's internals. Never touch design intent or rationale. If the map says how a diagram may change, follow it. Otherwise fix the false node or edge in place and do not redraw the diagram.

**6 — Comments (`CHANGED_CODE` only).** Apply the Comments section of [base.md](../bootstrap-base/base.md): delete comments that restate code, and fix or delete stale ones. Do not sweep files the diff did not touch.

**7 — Planning conflicts, report only (`all`).** List where `CHANGED_CODE` and a doc under `Planning docs` disagree: a rule the code breaks, a shipped row whose code is gone, a guardrail the code no longer meets. Never edit those docs or change code to match — the owner decides which side is wrong.

**Trimming, in every doc touched.** Cut sentences that restate a neighbour, duplicate examples, and filler. In an architecture doc, cut file catalogs, UI chrome, and restated product rules. Never strip gotchas, constraints, exact commands, or paths; when unsure, leave it.

## Out of scope

Never edit a path listed under `Planning docs` unless the user widens scope. Fix broken references *to* them (and drop references to deleted docs) in the files `Doc folders` names, and in skills.

## Commit

If the run edited files, commit only those paths (`git add -- <paths>`, never `-A`), check `git diff --cached --stat`, and commit with the subject `Doc sync.` No commit when nothing changed.

## Report

Short prose, no banners:

1. Scope and diff source in one line ("`all`, branch vs main, 44 files").
2. Each fix, one line, grouped by file.
3. Planning conflicts from check 7, one line each (row, file:line, what differs) — or "none".
4. Anything deliberately skipped.
5. Whether `Doc sync.` landed.
