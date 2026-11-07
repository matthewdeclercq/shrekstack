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

Look for `.agents/skills/verify-*/SKILL.md`. None found: stop and point at [bootstrap-verify](../bootstrap-verify/SKILL.md). More than one: run the pass below for each.

## Since last update

Run from ship-it, the window is what ship-it is checking: this branch's changes, including uncommitted work. Otherwise, take the last commit that touched the verify skill's folder; if it has never been committed, every feature is affected. A feature is affected when its file changed since then, or the code it drives did: the paths its file names, or the `Entry points` when it names none. Nothing affected: `clean`, and stop.

## Fix

A command, selector, or path moved, and the behavior still works: update that step or feature.

The app no longer does what the skill says: leave that text. That is a product regression, not a doc edit.

## Re-drive

Launch, see the readiness signal, and run the health check. Then drive only the affected features, through every entry point their files list. Capture evidence. Clean up. The evidence remains, and nothing you started is still running.

The skill was wrong: fix it and drive that feature once more. The app was wrong: `blocked`. Revert any edit that hides the break. Do not weaken a path to make it pass.

## Done

- `clean` — nothing affected, or the live pass matched and the skill is unchanged.
- `changed` — the skill matches, and each affected feature was driven.
- `blocked` — the feature, the missing behavior, and why the pass stopped. Drift fixed elsewhere can stay.
