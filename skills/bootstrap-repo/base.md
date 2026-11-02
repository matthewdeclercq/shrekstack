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

- Match the style and comment density of the file you edit; most functions here need zero comments.
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

Follow a skill whenever its task comes up. Run a skill on one model; fan out only when the skill says to. A script only one skill runs lives in that skill's `scripts/` folder; a root `scripts/` folder holds the rest. A script that mostly runs other tools is Bash; one that mostly parses text is Python 3. A skill that fans out read-only explorers runs them on a cheaper model, and keeps the orchestrator, which edits and validates, on the strongest.

## Git

- Commit messages in complete sentences; one logical change per commit.
- A PR description is a one-minute briefing for a reviewer who has the diff, unless the repo has a PR template: `## Why` (1–3 sentences), `## What changed` (1–3 bullets), `## Scope` (what it covers and leaves out), `## Tradeoffs` (only alternatives a reviewer would ask about), `## Blast radius` (who it touches and why that is safe), `## Verification` (each a real run and its outcome).

## When blocked

After 3 failed attempts at the same issue, stop and report to the owner: what was tried, the errors, and the decision you recommend.
