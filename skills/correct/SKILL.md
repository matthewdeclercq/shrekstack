---
name: correct
description: >-
  Finds the mistakes agents keep repeating in a repo and makes each one
  impossible: architecture first, then types or a lint, then a test, and a
  written rule last. Use when the user keeps correcting agents for the same
  thing, or asks to stop a repeated mistake.
disable-model-invocation: true
---

# Correct

Change the repo so the next agent cannot make the mistake again. Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. A change that looks right from one file should be right for the whole repo.

## Find the classes

Read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice.

## Fix each class at the highest level that works

1. **Architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Types or a lint.** Make the bad state impossible to write. If bad code still compiles, add a lint or check whose error names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more.
3. **A test.** Fix or delete any test that still passes when the behavior it checks breaks, or fails when only the internals change.
4. **A written rule, last,** and only for judgment calls. Nothing fails when an agent skips it.

## Fix and prove

Fix the most frequent classes now, one commit each. Prove each new check fails on a real past mistake. Run it the same way locally and in CI. An exception goes on the offending line with a reason, an expiry date, and the owner's approval.

## Rule table

Keep a `Rules` table in `AGENTS.md`: each rule and what enforces it. When the owner corrects you, fix the mistake and add the rule. If the rule was already there and nothing enforces it, that is a repeat: fix it at a higher level in the same change. Drop a rule once its mistake cannot happen.

## Report

Each class with its evidence, the level you picked, and why a higher level did not work.

Adapted from pstack's correct skill (MIT, Lauren Tan).
