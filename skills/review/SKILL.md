---
name: review
description: >-
  Reviews the agent's own change before a pull request is opened or updated:
  hooks, tidy, doc-sync, then blast radius and an adversarial pass. Use when
  the user asks for a review of the current change, or before opening or
  updating a PR.
disable-model-invocation: true
---

# Review

Lint and format belong to the repo's hooks. Review reports to the user; it does not write the PR description.

1. **Skip check.** Read `git diff --stat` and `git log`. Go straight to the note when the diff is only comments, formatting, a lockfile, generated files, or markdown that is not a skill or a rule. If an earlier review this session covered part of the branch, review only what is new since the commit it ended on.
2. **Hooks.** Run them once on the changed files: `pre-commit run --files <paths>`, or the repo's hook runner. Fix what they report. No hooks: say so in one line.
3. **Tidy.** Run [tidy](../tidy/SKILL.md). Do not repeat its checks.
4. **Doc sync.** Run [doc-sync](../doc-sync/SKILL.md), unless it already ran on this diff and nothing changed since.
5. **Blast radius**, below.
6. **Adversarial pass.** Read the diff once for bugs, logic errors, and edge cases. Fix what you find. If a fix can change the safety fact, prove it again.
7. **Note**, below.

## Blast radius

Find what the change could break outside the diff. A list of callers is not the result.

1. Read the diff. Note symbols added, changed, and deleted, and what the change does that the diff does not spell out.
2. Find the one fact the change is safe because of. Spend the time here, not on a list of maybes.
3. Look where a name search stops: the library's own source at the pinned version, and any local patch; data formats (API JSON, a DB column, a wire format, another language reading the same bytes); config and flags; code a few hops downstream.
4. Keep a risk only when it has a real chance and a real cost. Cite a real file:line. A search that finds nothing is still an answer. Never invent a caller or an API. Put checked-and-cleared items aside for the note.
5. Prove that fact with a script or test that calls the real code and fails if the fact is wrong. Use a check the repo already has when it does that. If the repo has `.agents/skills/verify-*/SKILL.md`, run it for the affected features. Record how far the proof got, or mark the fact unproven:
   1. Pointed at the line.
   2. Walked the bad case, and it cannot happen.
   3. Ran the real code.
   4. Reproduced it in the running app.

## Note

A few lines, no banners:

- If you skipped, why.
- What tidy and doc-sync fixed, or that nothing needed it.
- What blast radius found, the safety fact, how far it was proven, and the proof.
- What the adversarial pass caught and fixed.
- What was checked and cleared.
- If this work showed a shrekstack skill was wrong or missing something, or improved a repo skill shrekstack also has: a `shrekstack candidate` line saying what and why, without the repo-specific details.
- End with the commit the review covers: `Reviewed through <full sha>`.
