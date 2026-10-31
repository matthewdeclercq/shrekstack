---
name: doc-steward
description: >-
  One home per fact, and how a decision change is recorded. Setup writes the
  target repo's map of which doc owns which kind of fact, and creates backlog,
  goals, and shipped docs when the repo has none. Use when setting up doc
  ownership, editing a doc the map names, adding, reordering, or shipping a
  goal, or locking, amending, or unlocking a decision.
disable-model-invocation: true
---

# Doc Steward

One home per fact. The map names the home. Read it before editing a doc.

## Setup

Run when the user asks, when `map.md` in `.cursor/skills/doc-steward/` is missing, or when that map has no backlog, goals, or shipped row. Keep a row that is already right unless the user asks for a change.

One model. Do not start another model or fan out.

Run in the target repo. Write `map.md` in `.cursor/skills/doc-steward/`. Do not edit product code. Do not copy a map from another repo.

### Learn

Read `AGENTS.md` (`Doc folders`, `Planning docs`, `Architecture doc`), the README, and the docs those name. Ask only what those do not say: which doc is the one home for a kind of fact you cannot place. If a heading is missing, ask. Do not invent the doc list.

### Write

The map is the only home for who owns what. One table. Each row is one kind of fact and the path of the doc that owns it. No fact in two rows. When the repo locks product decisions, one row names that doc. When it keeps dropped designs an agent might rebuild, one row names that doc. Leave a row out when the repo has no such doc. If another doc already lists who owns what, point it at the map.

Name the backlog doc, the goals doc, and the shipped doc in that table. When one is missing, copy its template from beside this skill (`templates/backlog.md`, `templates/goals.md`, `templates/shipped.md`) to the path that row will use: beside the other planning docs, or in a docs directory when the repo has no planning docs. Keep the file name. Name a doc that already exists. Do not replace it.

Under the table, write the feature ID scheme: a prefix and the next free number. Default to prefix `F`, starting at 1, when the repo has none. If the repo caps goal size, one line in the map says so. Nothing else.

### Prove

Every home path exists. Where another doc mentions a fact, it points at that home instead of restating it. If a home is wrong, fix the map and look again.

## Rules

1. **One home per fact.** Every other mention is a pointer, never a copy. A copy so it is not missed drifts. When two docs disagree, fix the one that does not own the fact.
2. **Precedence.** The decision doc, then the goals doc, then the backlog and shipped docs as one rank, then the architecture doc. Skip a doc the map does not name. Fix the losing doc. Any other doc sits outside this chain.
3. **Stable feature IDs.** The map names the scheme. An ID is never renumbered or reused. Issuing an ID takes the next number and advances it in the map. Each ID lives in exactly one of the backlog doc or the shipped doc. Other docs refer to a feature by ID. Dropping a feature deletes it and every reference to its ID. Git history keeps it.
4. **Backlog is a list, not permission to build.** Only what the goals doc queues gets built.
5. **Self-contained goals.** The goals doc is the only place open goals and their order live. Each goal has its own fenced command block: what to read, the IDs in scope, where to start, constraints, out of scope, and the definition of done. The definition of done lives only in that block. When the map states a size cap, the block stays within it.
6. **A decision change is recorded in the decision doc the map names.** Never invent a call. Never reverse or reword a settled row without the owner. If the map names no doc for the change, ask. Do not invent one. A row says what the product does or must never do, what was refused, and why. When in doubt, do not lock. Status, process, catalogs, and code shape stay in the rows that own them.
   - **Change** amends the row and names what was refused. The one restatement allowed is the acceptance line in the doc the map says owns that feature. The decision doc wins.
   - **Unlock** deletes the row. No dropped-design entry. Git history covers it.
   - **Keep** adds one dated clause naming what was rejected and why, so it is not argued again.
   - A design an agent might rebuild, when it dies, gets one entry in the dropped-design doc the map names. The decision row keeps only the surviving line.

## Goals

If the map has no row for the doc, run setup.

- **Add.** Append a section with its command block, and a row at the end of the order table. Lock a decision only when it passes rule 6.
- **Reorder.** Edit the order table only. A file that needs the new order is breaking rule 1: point it at the goals doc.
- **Ship.**
  1. Move the backlog rows it covers to the shipped doc and cut each to one or two lines.
  2. Remove its section, including its command block, and its order row.
  3. Search the repo. Nothing still lists that goal as open.

No map: run setup. Do not guess an owner.
