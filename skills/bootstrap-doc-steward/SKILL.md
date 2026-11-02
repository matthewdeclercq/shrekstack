---
name: bootstrap-doc-steward
description: >-
  Writes the target repo's map of which doc owns which kind of fact, and
  creates backlog, goals, and shipped docs when the repo has none. Use when
  setting up doc ownership, or when doc-steward finds no map.
disable-model-invocation: true
---

# Bootstrap Doc Steward

Writes the map that [doc-steward](../doc-steward/SKILL.md) follows.

Run when the user asks, when the map is missing, or when it has no backlog, goals, or shipped row. Keep a row that is already right unless the user asks for a change.

Run in the target repo. The map is `doc-map.md` in `.agents/`. It is a doc, not a skill: never put it in a skills folder. Do not edit product code. Do not copy a map from another repo.

An older version kept the map as `map.md` in `.agents/skills/doc-steward/` or `.cursor/skills/doc-steward/`. If one exists and the new map does not, move it to the new path. Then remove `.claude/skills/doc-steward` only when it is a symlink into `.agents/skills/doc-steward`, and remove `.agents/skills/doc-steward` when it is empty. Leave any folder that holds a `SKILL.md`: that is the installed skill.

## Learn

Read `AGENTS.md` (`Doc folders`, `Planning docs`, `Architecture doc`), the README, and the docs those name. Ask only what those do not say: which doc is the one home for a kind of fact you cannot place. If a heading is missing, ask. Do not invent the doc list.

## Write

The map is the only home for who owns what. One table. Each row is one kind of fact and the path of the doc that owns it. No fact in two rows. When the repo locks product decisions, one row names that doc. When it keeps dropped designs an agent might rebuild, one row names that doc. Leave a row out when the repo has no such doc. If another doc already lists who owns what, point it at the map.

Name the backlog doc, the goals doc, and the shipped doc in that table. When one is missing, copy its template from beside this skill (`templates/backlog.md`, `templates/goals.md`, `templates/shipped.md`) to the path that row will use: beside the other planning docs, or in a docs directory when the repo has no planning docs. Keep the file name. Name a doc that already exists. Do not replace it.

Under the table, write the feature ID scheme: a prefix and the next free number. Default to prefix `F`, starting at 1, when the repo has none. If the repo caps goal size, one line in the map says so. Nothing else.

## Prove

Every home path exists. No skills folder holds the map. Where another doc mentions a fact, it points at that home instead of restating it. If a home is wrong, fix the map and look again.
