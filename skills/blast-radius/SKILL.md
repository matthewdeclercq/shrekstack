---
name: blast-radius
description: >-
  Finds what a change could break outside its diff, and proves the one fact
  the change is safe because of. Use before a risky change lands, when the
  user asks what a change could break, or when ship-it runs it.
---

# Blast radius

Find what the change could break outside the diff. A list of callers is not the result.

The change: uncommitted edits and new files, plus the commits since this branch split from the default branch (`origin/HEAD`).

1. Read the diff. Note symbols added, changed, and deleted, and what the change does that the diff does not spell out.
2. Find the one fact the change is safe because of. Spend the time here, not on a list of maybes.
3. Look where a name search stops: the `Proof traps` in `AGENTS.md` and in the README of each area the diff touches; the library's own source at the pinned version, and any local patch; data formats (API JSON, a DB column, a wire format, another language reading the same bytes); config and flags; code a few hops downstream.
4. Keep a risk only when it has a real chance and a real cost. Cite a real file:line. A search that finds nothing is still an answer. Never invent a caller or an API. Put checked-and-cleared items aside for the report.
5. Prove that fact with a script or test that calls the real code and fails if the fact is wrong. Use a check the repo already has when it does that. If the repo has `.agents/skills/verify-*/SKILL.md`, run it for the affected features. Keep a new proof as a test when it locks a rule worth keeping; otherwise delete it. Record how far the proof got, or mark the fact unproven:
   1. Pointed at the line.
   2. Walked the bad case, and it cannot happen.
   3. Ran the real code.
   4. Reproduced it in the running app.

## Report

A few lines: the risks kept, each with its file:line; the safety fact, how far it was proven, and the proof; and what was checked and cleared.
