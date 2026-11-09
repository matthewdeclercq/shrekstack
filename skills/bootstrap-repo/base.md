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

- Keep code lean: no speculative parameters, protocols, or configuration; the simplest design that fully solves the goal wins.
- Put code where it changes together: reuse before you copy, and keep one feature's logic in one place. A special case (an `if` for one value, a parameter for one caller, a sleep or retry) means the design is missing something. Change the design or ask; don't patch around it.
- Remove before you add: delete dead weight first, then build on the simpler base.
- When the owner corrects the same mistake twice, make it impossible: architecture first, then types or a lint whose error names the fix, then a test. Write a rule only for judgment calls.
- Decide for the long term — no stopgap meant to be replaced later.
- Prefer small, focused PRs.

## Verify and debug

- Check the real thing, not a proxy: run the feature, read the actual value. "It compiles" is not done.
- Fix the root cause, the first place the system went wrong. A guard is a fix only when the state it handles is legitimate; otherwise find what produced the state.
- Fixing a bug: reproduce it first. When a cheap test path exists, write the failing test first.

## Skills

Follow a skill whenever its task comes up. An `AGENTS.md` heading a skill reads counts as missing when its body starts with `TODO`. `Proof traps` and `Testing defaults` can also sit in the `README.md` of an area `File layout` lists, covering that area only. A skill that reads one reads it in `AGENTS.md` and in the README of every area it touches.

Run a skill on one model; fan out only when the skill says to. A skill that fans out read-only explorers runs them on a cheaper model, and keeps the orchestrator on the strongest. Explorers return findings only; the orchestrator alone edits, validates, and keeps any ledger. Split only on areas the skill or an `AGENTS.md` heading names; if none does, ask. A ledger goes in the response, or in a scratch file the goal names and deletes on ship. Never commit it.

## Planning docs

`.agents/doc-map.md` names the doc that owns each kind of fact: goals, backlog, shipped work, decisions, and architecture. Follow doc-steward before you change a doc it names, or what one says.

## Agent files

`AGENTS.md` at the repo root is the only agent instruction file; Claude Code and Cursor read it directly. Never add a `CLAUDE.md` anywhere, since one makes Claude Code skip `AGENTS.md`, and never add an `AGENTS.md` in a folder: an instruction goes in the root `AGENTS.md`. Keep `AGENTS.md` slim: it loads on every task, so it holds only what any task may need, such as commands, hard rules, the area index, and facts that cross areas. A fact only one area needs, such as what the folder holds, its setup, its scripts, where its tests go, or a name looked up only inside it, goes in that folder's `README.md`. Every repo skill lives in `.agents/skills/<name>/`, linked from `.claude/skills/` or `.cursor/skills/` for the tools `Agent tools` names. Nothing this rule or the style rule already says goes in `AGENTS.md`.

## Git

- Commit messages in complete sentences; one logical change per commit.
- A PR description is a one-minute briefing for a reviewer who has the diff, unless the repo has a PR template: `## Why` (1–3 sentences), `## What changed` (1–3 bullets), and `## Verification` (each a real run and its outcome). Add `## Scope`, `## Tradeoffs`, or `## Blast radius` only when a reviewer would ask about it.

## When blocked

After 3 failed attempts at the same issue, stop and report to the owner: what was tried, the errors, and the decision you recommend.
