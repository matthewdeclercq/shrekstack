---
name: test-cleanup
description: >-
  Prunes, merges, and places tests so each remaining test is a domain or adapter
  rule, a regression lock, or an integration proof that cannot be a unit test.
  Use for a test-hygiene pass — not for adding coverage or rewriting tests.
disable-model-invocation: true
---

# Test Cleanup

Delete or merge tests that no longer lock a live rule. Do not change production behaviour. Do not add tests for gaps the sweep notices.

What belongs in a test is the part of `Testing defaults` labeled `What to test`. Placement and "do not bulk-migrate" live in that section too, including the part labeled `Where tests go`. This skill is the sweep method.

Read `AGENTS.md` first. Use these headings (any heading level, text after the hashes exactly as written). A heading whose body starts with `TODO` counts as missing:

| Heading | What it holds | If it is missing or empty |
|---------|----------------|---------------------------|
| `Testing defaults` | What to test, where tests go, and which invariants are owner-rank | Ask before deleting or moving a test. Do not guess what to test. If the section exists but has no `What to test` label, ask which part that is |
| `Test passes` | Ordered passes for a full-suite sweep | Run the default passes under Passes |
| `Build & test` | The suite commands that own the files, and the commands that must be green after an edit | Ask. Do not guess a command |
| `File layout` | Test areas a multi-agent pass may split on | Ask before fanning out. Do not invent areas |

## Proof

Name the failure the next refactor would see if the test is gone. Cannot name it → keep or ask. A test whose name is the only record of the invariant stays, or the invariant moves onto the remaining test — never delete a lock whose failure you cannot state.

Reachability is the wrong proof (that is [code-cleanup](../code-cleanup/SKILL.md)). Compile already catches a deleted API.

## Rubric

**Keep** — a named domain or adapter rule; a regression that failed first and stayed; an integration proof that cannot be a unit test, when `Testing defaults` names that proof; a policy guard whose failure is catastrophic, when `Testing defaults` names that guard.

**Merge** — same setup, one assertion different (parameterize or one matrix); the same rule asserted in two targets (one home: the type's suite).

**Delete** — anything What to test forbids; a test whose only job is "this API is gone"; an enum matrix that encodes no rule. Drop goal-named comments; keep the assertion if the rule is live.

**Move** — only when the type already moved and `Testing defaults` says the test does not need its current home.

**Owner-rank, do not delete** — looks unused but might be the only lock on an invariant `Testing defaults` names as owner-rank. If it names none, ask before deleting.

Do not optimize for fewer files or coverage percentage.

## Loop

1. Scope the pass + stopping condition
2. Baseline — the suite that owns the files, per `Build & test`
3. Classify 1–5 candidates against the rubric (read the test and the production type)
4. Edit the proven batch → the owning suite green → the other suites `Build & test` names for that change green
5. Record the ledger row

## Passes (full-suite sweep)

A full-suite sweep starts by classifying every test file into the ledger. No edits on that pass.

Then run the passes under `Test passes`, in that order. Without that heading, run three passes from the rubric: delete, then merge, then move. Compare what tests **assert**, not what they are named, when a pass is about duplicates. Two names that read differently over the same assertion is the shape that gets missed.

## Ledger

One row per file (or per method when a file splits). Statuses: `keep`, `merge`, `delete`, `move`, `deferred`, `validated`. Include `## Owner-rank` (only-lock candidates) and `## Residue` (gaps noticed, not this goal).

The ledger goes in the response. A sweep that spans a goal loop writes it to a scratch file the goal names and deletes on ship — a full-inventory table checked into a doc folder is stale by its next commit.

## Multi-agent

Fan out read-only explorers when the pass spans more than one test area named in `File layout` or `Testing defaults`. Explorers return candidate tables only. The orchestrator alone edits, validates, and updates the ledger. Subagents do not inherit this skill — paste the surface, rubric, proof, and traps into each prompt. If neither heading names the split, ask. Do not invent areas.

## Output

Pass, candidates + named failure modes, edits, suites run, residue.
