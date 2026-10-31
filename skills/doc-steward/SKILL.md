---
name: doc-steward
description: >-
  One home per fact, and how a decision change is recorded. Setup writes the
  target repo's map of which doc owns which kind of fact. Use when setting up
  doc ownership, editing a doc the map names, or locking, amending, or
  unlocking a decision.
disable-model-invocation: true
---

# Doc Steward

One home per fact. The map names the home. Read it before editing a doc.

## Setup

Run when the user asks, or when `map.md` in `.cursor/skills/doc-steward/` is missing. If the map exists, do not rewrite it unless the user asks.

One model. Do not start another model or fan out.

Run in the target repo. Write `map.md` in `.cursor/skills/doc-steward/`. Do not edit product code. Do not copy a map from another repo.

### Learn

Read `AGENTS.md` (`Doc folders`, `Planning docs`, `Architecture doc`), the README, and the docs those name. Ask only what those do not say: which doc is the one home for a kind of fact you cannot place. If a heading is missing, ask. Do not invent the doc list.

### Write

The map is the only home for who owns what. One table, nothing else. Each row is one kind of fact and the path of the doc that owns it. No fact in two rows. When the repo locks product decisions, one row names that doc. When it keeps dropped designs an agent might rebuild, one row names that doc. Leave a row out when the repo has no such doc. If another doc already lists who owns what, point it at the map.

### Prove

Every home path exists. Where another doc mentions a fact, it points at that home instead of restating it. If a home is wrong, fix the map and look again.

## Rules

1. **One home per fact.** Every other mention is a pointer, never a copy. A copy so it is not missed drifts. When two docs disagree, fix the one that does not own the fact.
2. **A decision change is recorded in the decision doc the map names.** Never invent a call. Never reverse or reword a settled row without the owner. If the map names no doc for the change, ask. Do not invent one. A row says what the product does or must never do, what was refused, and why. When in doubt, do not lock. Status, process, catalogs, and code shape stay in the rows that own them.
   - **Change** amends the row and names what was refused. The one restatement allowed is the acceptance line in the doc the map says owns that feature. The decision doc wins.
   - **Unlock** deletes the row. No dropped-design entry. Git history covers it.
   - **Keep** adds one dated clause naming what was rejected and why, so it is not argued again.
   - A design an agent might rebuild, when it dies, gets one entry in the dropped-design doc the map names. The decision row keeps only the surviving line.

No map: run setup. Do not guess an owner.
