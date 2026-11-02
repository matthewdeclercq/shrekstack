---
name: doc-steward
description: >-
  One home per fact, and how a decision change is recorded. Use when editing
  a doc the map names, adding, reordering, or shipping a goal, or locking,
  amending, or unlocking a decision.
disable-model-invocation: true
---

# Doc Steward

One home per fact. The map, `doc-map.md` in `.agents/`, names the home. Read it before editing a doc. No map: run [bootstrap-doc-steward](../bootstrap-doc-steward/SKILL.md).

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

If the map has no row for the doc, run bootstrap-doc-steward.

- **Add.** Append a section with its command block, and a row at the end of the order table. Lock a decision only when it passes rule 6.
- **Reorder.** Edit the order table only. A file that needs the new order is breaking rule 1: point it at the goals doc.
- **Ship.**
  1. Move the backlog rows it covers to the shipped doc and cut each to one or two lines.
  2. In the decision doc the map names, move any design note that would bring back a dead approach to the dropped-design doc as one entry, when the map names that doc. Strip goal numbers, status, and scoping notes from every row the goal touched.
  3. Remove its section, including its command block, and its order row.
  4. Search the repo. Nothing still lists that goal as open.

No map: run bootstrap-doc-steward. Do not guess an owner.
