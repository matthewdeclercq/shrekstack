# Base rules

Generic rules for a repo that adopts this library. Project lists, commands, and paths stay in that repo's `AGENTS.md`.

## Ask, don't drift

**Challenging a locked decision is welcome — ask, don't drift.** If a rule looks wrong, or you find a better approach, tell the owner the rule, why it looks wrong, and what you would do instead, in a few sentences. Then build the rule as written unless the owner changes it. Silently building something else is the failure this prevents.

**No is an acceptable answer.** Asked whether to do something, or shown an approach, give your real judgment, including "this doesn't earn its place." Candor over agreement.

## Code first (what exists)

The docs own **intent** — product lines, the queue, constraints, how to build. The code owns **what exists**.

- Before answering from a doc, open the named types and report what the code does.
- When a doc and the code disagree on a fact, trust the code and fix or flag the doc. Never invent a design from a doc, or change working code to match a stale one, unless the owner says so.

## Comments

- Match the file's comment style (syntax, doc-comment format), never its density. Default to zero comments; in lines you change, cut any that fail the rule below. Leave other comments alone unless your change made them untrue.
- A name carries the fact before a comment does. A comment states only a constraint, invariant, or non-obvious why — never what the next line does, the signature, or the change you made. No change-log comments (`// previously …`) or commented-out code. A comment explaining a surprise in our own code is a cue to reshape it first — rename, extract, or a type that makes it obvious — and comment only when the reshape is not worth it. An invariant a cheap test can lock (`must stay sorted`) gets the test, not the comment. Before finishing, reread the diff and replace any comment a rename would make redundant with the rename.

## Code quality

- Keep code lean: no speculative parameters, protocols, or configuration; the smallest diff that fully solves the goal wins.
- Remove before you add: delete dead weight first, then build on the simpler base.
- When the owner corrects the same mistake twice, make it impossible: architecture first, then types or a lint whose error names the fix, then a test. Write a rule only for judgment calls.
- Decide for the long term — no stopgap meant to be replaced later.
- Prefer small, focused PRs.

## Verify and debug

- Check the real thing, not a proxy: run the feature, read the actual value. "It compiles" is not done.
- Fix the root cause, the first place the system went wrong. A guard is a fix only when the state it handles is legitimate; otherwise find what produced the state.
- Fixing a bug: reproduce it first. When a cheap test path exists, write the failing test first.

## Skills

Follow a skill whenever its task comes up. An `AGENTS.md` heading a skill reads counts as missing when its body starts with `TODO`.

Run a skill on one model; fan out only when the skill says to. A skill that fans out read-only explorers runs them on a cheaper model, and keeps the orchestrator on the strongest. Explorers return findings only; the orchestrator alone edits, validates, and keeps any ledger. Split only on areas the skill or an `AGENTS.md` heading names; if none does, ask. A ledger goes in the response, or in a scratch file the goal names and deletes on ship. Never commit it.

## Planning docs

`.agents/doc-map.md` names the doc that owns each kind of fact: goals, backlog, shipped work, decisions, and architecture. Follow doc-steward before you edit a doc it names, add, reorder, or ship a goal, lock or change a decision, or change a module, edge, or flow the architecture doc draws.

## Agent files

`AGENTS.md` at the repo root is the only agent instruction file; for Claude Code, `CLAUDE.md` is a symlink to it. Never add an `AGENTS.md` or `CLAUDE.md` in a folder: an instruction goes in the root `AGENTS.md`, and what a folder holds goes in that folder's `README.md`. Every repo skill lives in `.agents/skills/<name>/`, linked from `.claude/skills/` or `.cursor/skills/` for the tools `Agent tools` names. Keep `AGENTS.md` to repo-specific facts; anything this rule or the style rule already says does not go there.

## Git

- Commit messages in complete sentences; one logical change per commit.
- A PR description is a one-minute briefing for a reviewer who has the diff, unless the repo has a PR template: `## Why` (1–3 sentences), `## What changed` (1–3 bullets), `## Scope` (what it covers and leaves out), `## Tradeoffs` (only alternatives a reviewer would ask about), `## Blast radius` (who it touches and why that is safe), `## Verification` (each a real run and its outcome).

## When blocked

After 3 failed attempts at the same issue, stop and report to the owner: what was tried, the errors, and the decision you recommend.
