---
name: review
description: >-
  Reviews the agent's own change before a pull request is opened or updated.
  Use when the user asks for a review of the current change, or before
  opening or updating a PR. One model. A trivial or already-reviewed diff
  stops after the note. Otherwise hooks, then tidy, then this review.
disable-model-invocation: true
---

# Review

One model. Do not start another model, an arena, or interrogate.

Lint, format, and dead code belong to the repo's pre-commit hooks. Never commit with `--no-verify`.

Read `git diff --stat` and `git log` before any other work. Skip the rest when the diff is only comments, formatting, a lockfile, generated files, or markdown that is not a skill or a rule, or when the worktree is clean and the PR already says `Reviewed through <sha>` for HEAD.

If that note names an older sha, review only `git diff <sha>..HEAD`.

Run the hooks once on the changed files: `pre-commit run --files <paths>`, or the repo's hook runner. If the repo has no hooks, say so in one line and continue. Fix what they report.

Then run [tidy](../tidy/SKILL.md). Do not repeat its checks.

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

If the repo has `.cursor/skills/verify-*/SKILL.md`, run it for the affected features as part of proving the change is safe.

## Adversarial pass

Read the diff once for bugs, logic errors, and edge cases. Fix what you find. If that edit can change the safety fact, run the proof again.

## Review caught

Add a short note to the PR body:

- If you skipped, say why, and stop.
- What tidy fixed. If nothing, say so.
- What blast radius found, the safety fact, how far it was proven, and the proof.
- What the adversarial pass caught and fixed.
- What was checked and cleared.
- End with `Reviewed through <full sha>`.

No banners. A few lines.

## Shrekstack candidate

Did this work change a skill that came from shrekstack in a way that would help every repo? If yes, add a short `shrekstack candidate` note to the PR body: what changed and why, with the repo-specific details left out.
