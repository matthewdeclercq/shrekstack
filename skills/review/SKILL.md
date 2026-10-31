---
name: review
description: >-
  Reviews the agent's own change before a pull request is opened or updated.
  Use when the user asks for a review of the current change, or before
  opening or updating a PR. One model. tidy runs first.
disable-model-invocation: true
---

# Review

Run [tidy](../tidy/SKILL.md) on this change first. Do not repeat its checks.

Then review what remains, in order. One model. Do not start another model, an arena, or interrogate.

## Blast radius

Find what the change could break outside the diff. A list of callers is not the result.

1. Read the diff. Note symbols added, changed, and deleted, and what the change does that the diff does not spell out.
2. Find the one fact the change is safe because of. Spend the time here, not on a list of maybes.
3. Look where a name search stops: the library's own source at the pinned version, and any local patch; data formats (API JSON, a DB column, a wire format, another language reading the same bytes); config and flags; code a few hops downstream.
4. Keep a risk only when it has a real chance and a real cost. Cite a real file:line. A search that finds nothing is still an answer. Never invent a caller or an API. Put checked-and-cleared items aside for the note.
5. Prove that fact. Run a script or test that calls the real code and fails if the fact is wrong. Use a check the repo already has when it does that. Record how far the proof got, or mark the fact unproven:
   1. Said so. That does not count.
   2. Pointed at the line.
   3. Walked the bad case and it cannot happen.
   4. Ran the real code.
   5. Reproduced it in the running app.

## Adversarial pass

Read the diff once for bugs, logic errors, and edge cases. Fix what you find. If that edit can change the safety fact, run the proof again.

## Review caught

Add a short note to the PR body, in this order:

- What tidy fixed. If it fixed nothing, say so.
- What blast radius found, the safety fact, how far it was proven, and the proof.
- What the adversarial pass caught and fixed.
- What was checked and cleared.

No banners. A few lines.
