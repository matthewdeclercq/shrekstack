---
name: doc-steward
description: >-
  Structure and lifecycle rules for a repo's planning docs. Use whenever
  editing a doc the repo's doc map names, and when adding, reordering, or
  shipping a goal, locking or amending a decision, answering a challenged
  decision, auditing doc structure, or making a code change that alters a
  module, edge, or flow the architecture doc draws. Also writes the doc map
  in a repo that has none.
---

# Doc Steward

How the planning docs fit together. The map, `doc-map.md` in `.agents/`, names the doc that owns each kind of fact. Read it before editing a doc it names, and before a code change that alters a module, edge, or flow the architecture doc draws. No map: run Bootstrap.

Below, "the decision doc", "the goals doc", and so on mean the doc the map names for that role. Skip a rule whose doc the map does not name.

## Bootstrap

Run when the user asks, when the map is missing, or when it has no backlog, goals, or shipped row. Keep a row that is already right unless the user asks for a change. Do not edit product code. Do not copy a map from another repo.

The map is a doc, not a skill: never put it in a skills folder.

**Learn.** Read `AGENTS.md`, the README, the docs they link, and any docs directory. Ask only which doc is the one home for a kind of fact you cannot place. Do not invent the doc list.

**Write.** One table: each row is one kind of fact and the path of the doc that owns it. No fact in two rows. Name the backlog, goals, and shipped docs. When one is missing, copy its template from beside this skill (`templates/backlog.md`, `templates/goals.md`, `templates/shipped.md`) beside the other planning docs, or into a docs directory when there are none. When the repo has no architecture doc, write one from `templates/architecture.md`: fill its `<...>` links from the map, then draft from the code what the code shows, following rule 9: the system context, the modules diagram and layer table, one section and diagram per subsystem, persistence, and cross-cutting. Leave Principles and Technical decisions as `TODO`: those are the owner's calls (rule 10). Never replace a doc that exists. Add a row for each of these the repo has: the decision doc, the architecture doc, the dropped-design doc, a docs index, `AGENTS.md` (build and test, environment, hard constraints), and the UI conventions skill (reusable screen patterns, never screen inventories).

Under the table: the feature ID scheme, a prefix and the next free number (default `F`, from 1), and the goal command block limit when it is not 4000 characters.

**Prove.** Every home path exists. No skills folder holds the map. Every type and path a drafted architecture doc names exists in the code. Where another doc mentions a fact, it points at the home instead of restating it.

## Rules

1. **One home per fact.** Every other mention, in any doc, skill, `AGENTS.md`, or code comment, is a link, never a copy. A copy "so it is not missed" drifts.
2. **Precedence:** the decision doc, then the goals doc, then the backlog and shipped docs, then the architecture doc. Fix the losing doc; never leave a contradiction. `AGENTS.md` and the UI skill sit outside this chain.
3. **Stable feature IDs.** Never renumbered or reused. Issuing one takes the next number in the map and advances it. Each ID lives in exactly one of the backlog or shipped doc, and other docs refer to features by ID. A feature the owner drops is deleted with every reference to its ID; git history keeps it.
4. **Backlog is inventory, not a license.** Build only what the goals doc queues. Backlog status is `Open` (a goal queues it) or `Later`.
5. **Shipped is a list.** ID, name, one or two lines on what it does, and any guardrail no other doc holds. Being there is the status. Detail belongs to the code and its tests.
6. **Self-contained goals.** The goals doc is the only place open goals and their order live. Each open goal is a `## Goal N` section with its purpose, its dependencies, and one fenced command block: what to read, scope by ID, starting files, constraints, out of scope, and the definition of done. The definition of done lives only there.
7. **What the decision doc admits.** A row binds what the product does or never does, names what was refused, and rests on evidence, safety, law, or a failed design. When in doubt, do not lock. Title sections by product rule, not goal; a goal number appears only as a link to an open goal. Never in the decision doc:
   - **Status:** shipped or done marks, ID pass-lists, open-goal or key-file tables.
   - **Goal scoping:** "out of this goal", deferred notes. That is the goal's definition of done.
   - **Ledgers:** goal numbers in a cell, sections named after goals, "(amended <date>)" markers.
   - **Supersession stories:** keep only the surviving imperative ("do not reintroduce X").
   - **Process:** belongs in `AGENTS.md` or a skill.
   - **Chrome:** layout, order, colours. Reusable on a new screen goes in the UI skill; otherwise the code.
   - **Tuning:** timers, caps, file and type names.
   - **Catalogs:** toggle, column, and preset lists. Defaults go in acceptance criteria.
   - **Code shape:** `AGENTS.md` or the architecture doc.
8. **The dropped-design doc holds dropped designs only.** A design an agent might rebuild gets one entry when it dies; the decision row that replaced it keeps only the surviving imperative. Never a shipped feature, a goal, or an unlocked decision: unlocking deletes the row, and git history covers it.
9. **The architecture doc is a map, not a tour.** Its shape is the template's: a header that links the other docs and says the code wins, numbered principles, a system context diagram, a modules diagram with a layer table, one section per subsystem, persistence, cross-cutting, and the technical decisions table. Each subsystem gets one diagram, a few lines or bullets under it, and a pointer to its product rules. A new subsystem gets a diagram; a type never gets its own. Diagrams are Mermaid:
   - A node names a real type or path, with a second line for its job (`"Name<br/>job"`).
   - Subgraphs group by where code runs: device, server, build machine.
   - Cylinders for stores, rounded nodes for triggers and events, dashed edges for links that are not calls, and edge labels for how data moves.
   - A sequence diagram only where order matters.

   A module, adapter, store, or runtime pattern is missing only when it changes how the parts connect. When a module, edge, or type a diagram shows changes, update the diagram in the same edit. Never turn a diagram into a type catalog or redraw one whose facts still hold. A product rule there is a bug: replace it with a pointer.
10. **Technical decision rows record the owner's calls.** Their table lives at the end of the architecture doc unless the map names another home. A change that lands a new library, module cut, or runtime pattern adds its row in the same change: why, and what was refused, from the owner's call, the settling spike, or the landing commit. Never invent a call. Never reverse or reword a settled row without the owner.
11. **Size budgets for new writing.** Decision cells about 40 words or fewer. Goal purpose two sentences or fewer. Goal command blocks within the limit in the map, 4000 characters by default (the `/goal` condition limit): state deltas against decisions, point at the decision doc for policy, and leave wrap-up to the skills. UI skill table cells: one clause. Do not rewrite existing goals to fit unless the owner asks.

## Workflows

- **Add a goal:** append its section and a row at the end of the order table, and mark its backlog IDs `Open`. Lock a decision only if it passes rule 7; most goals lock nothing.
- **Reorder goals:** the order table only. Any other file that needs an edit is breaking rule 1: make it a pointer.
- **Lock or amend a decision:** the row passes rule 7 and names what was refused. Update the affected acceptance criteria in the backlog or shipped doc, the one restatement allowed; the decision doc wins.
- **Answer a challenged decision:** "change it" amends or deletes the row. "Unlock" deletes it, with no dropped-design entry. "No" adds one dated clause naming what was rejected and why, so it is not argued again.
- **Ship a goal:**
  1. Move its rows from the backlog to the same epic in the shipped doc, each cut to one or two lines: a guardrail only when no decision row holds it, and no type names, measurements, or build story. Move epic prose that now describes shipped behaviour, cut the same way.
  2. In the decision doc, move any note that would bring back a dead approach to the dropped-design doc as one entry, and strip goal bookkeeping from every row the goal touched (rule 7).
  3. Delete its section, its order-table row, and any header prose about it.
  4. Search for the goal number: no doc may still list it as open.
- **Audit:**
  - The order table and the `## Goal N` sections list the same goals in the same order.
  - Every goal has one fenced command block within the size limit.
  - The decision doc names a goal only when it is open.
  - No open-goal lists, goal order, or definition-of-done copies outside the goals doc.
  - One home per fact: where a doc restates a fact the map gives to another doc, replace it with a pointer. If the map names no owner for a fact, ask.
  - In the decision doc, search for `shipped`, `Done`, `Out of this`, and `Superseded`. Each hit is bookkeeping to strip unless it is a product rule. Every row names a refused path. Directions to UI ("Settings → …") still match the app.
  - In the architecture doc, no product rule is restated, and no diagram node or edge names code that is gone.
