---
name: maintain-verify
description: >-
  Brings a repo's verify skill back in line with the code after it changes.
  Use when the user asks to update the verify skill. Edits only that
  skill's files.
disable-model-invocation: true
---

# Maintain Verify

Edit only files under the verify skill. Never edit product code.

Outcomes: `clean`, `changed`, `blocked`.

## Locate

Look for `.agents/skills/verify-*/SKILL.md`. None found: stop and point at [setup-verify](../setup-verify/SKILL.md). More than one: run the pass below for each whose named paths overlap the diff. No overlap among them: `clean`, and stop.

## Since last update

Take the last commit that touched that directory (`git log -1` on it). If it has never been committed, stop and point at [setup-verify](../setup-verify/SKILL.md).

Diff the working tree against that commit, only on paths named in that directory (`git diff <sha> -- <paths>`, plus untracked files on those paths). A command that names no file counts when the diff touches an entry point that command starts. If the skill names no paths, diff the `Entry points` paths and nothing else.

No overlap: `clean`. Stop. Do not re-drive.

## Fix

A command, selector, or path moved, and the behavior still works: update that step or feature.

The app no longer does what the skill says: leave that text. That is a product regression, not a doc edit.

## Re-drive

Launch, see the readiness signal, and run the health check. Then drive only the features whose text changed or whose paths were in the diff. Capture evidence. Clean up. The evidence remains, and nothing you started is still running.

The skill was wrong: fix it and drive that feature once more. The app was wrong: `blocked`. Revert any edit that hides the break. Do not weaken a path to make it pass.

## Done

- `clean` — no overlap, or the live pass matched and the skill is unchanged.
- `changed` — the skill matches, and each affected feature was driven.
- `blocked` — the feature, the missing behavior, and why the pass stopped. Drift fixed elsewhere can stay.
