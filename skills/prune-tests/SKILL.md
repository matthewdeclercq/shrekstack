---
name: prune-tests
description: >-
  Prunes, merges, and places tests so each remaining test is a domain or adapter
  rule, a regression lock, or an integration proof that cannot be a unit test.
  Use for a test-hygiene pass — not for adding coverage or rewriting tests.
disable-model-invocation: true
---

# Prune Tests

Delete or merge tests that no longer lock a live rule. Do not change production behaviour, and do not add tests for gaps you notice.

`AGENTS.md` headings, and `Testing defaults` in the README of each test area in scope too, which adds to the root one:

- `Testing defaults`: what to test (`What to test`), where tests go (`Where tests go`), and which invariants are owner-rank (`Owner-rank`). Missing: ask before deleting or moving any test.
- `Build & test`: the suite commands. Missing: ask.
- `File layout`: test areas to split a fan-out on. Missing: ask before fanning out.
- `Test passes`, optional: the order of passes for a full sweep.

## Proof

Judge each test against two imagined edits. **Break the behavior** (a wrong value, a skipped or doubled effect): a test that still passes proves nothing. **Change only the internals**, keeping every observable result: a test that now fails is pinned to the implementation. Keep a test that catches the first and survives the second; rewrite or delete the rest.

Name the failure the next refactor would see without the test. If you cannot, keep it or ask. A test whose name is the only record of an invariant stays, or the invariant moves onto the test that remains. Reachability is the wrong proof here ([prune-code](../prune-code/SKILL.md)), and the compiler already catches a deleted API.

## Rubric

- **Keep:** a named domain or adapter rule; a regression that failed first and stayed; an integration proof that cannot be a unit test, or a policy guard whose failure is catastrophic, when `Testing defaults` names it.
- **Merge:** same setup with one assertion different (parameterize, or one matrix); the same rule asserted in two places (keep it in the type's suite).
- **Delete:** anything `What to test` forbids; a test whose only job is "this API is gone"; an enum matrix that encodes no rule. Drop goal-named comments, but keep the assertion if the rule is live.
- **Move:** only when the type already moved and `Testing defaults` says the test does not belong where it is.
- **Owner-rank, never delete:** looks unused but might be the only lock on an invariant `Testing defaults` names as owner-rank. If it names none, ask.

Do not optimize for fewer files or coverage percentage.

## Loop

1. Scope the pass and when to stop.
2. Baseline: the suite that owns the files.
3. Classify 1–5 candidates against the rubric, reading the test and the code it covers.
4. Edit the batch. The owning suite, and any other suite the change touches, go green.
5. Record the ledger row.

A full-suite sweep first classifies every test file into the ledger, with no edits. Then it runs the passes in `Test passes`, or delete, merge, move by default. For duplicates, compare what tests assert, not what they are named.

## Ledger

One row per file, or per method when a file splits. Statuses: `keep`, `merge`, `delete`, `move`, `deferred`, `validated`. Add an owner-rank list and a residue list (gaps noticed, not this pass).

## Fan out

When the pass spans more than one test area, launch read-only explorers, one per area. Each returns a candidate table. Paste the surface, rubric, and proof into each prompt, with that area's own `Testing defaults` when its README has one.

## Report

Pass, candidates and their failure modes, edits, suites run, residue.
