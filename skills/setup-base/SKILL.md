---
name: setup-base
description: >-
  Writes the shared shrekstack base rule into a repo for Cursor and Claude
  Code, and points AGENTS.md at repo-specific skills. Use when the user asks
  to install the base rule or run setup-base. One model.
disable-model-invocation: true
---

# Setup Base

One model. Do not start another model or fan out.

Run in the target repo. Read `base.md` beside this skill and write it to two places, overwriting both on every run. Do not edit product code. Never create, edit, or replace `CLAUDE.md`, including when it is a symlink to `AGENTS.md`. Write the skills line in `AGENTS.md` only.

## Write

`base.md` is the rule text, with no frontmatter. If it is not beside this skill, stop and say so.

- **Cursor.** Write `shrekstack-base.mdc` in `.cursor/rules/`. Start with this frontmatter, then a blank line, then the text of `base.md`:

  ```
  ---
  description: Generic rules for a repo that adopts this library. Project lists, commands, and paths stay in that repo's AGENTS.md.
  alwaysApply: true
  ---
  ```

- **Claude Code.** Write `shrekstack-base.md` in `.claude/rules/`. The text of `base.md` only. No frontmatter.

- **AGENTS.md.** Add this line once, on its own line:

  ```
  Repo-specific skills live in `.agents/skills/`.
  ```

  If a line is exactly that text, do not add another. If more than one line is exactly that text, keep the first. If `AGENTS.md` is missing, create it with only that line.

Create a directory if it is missing.

## Prove

The skill is a draft until the Cursor file is that frontmatter, a blank line, and the text of `base.md`, and the Claude file is that text alone. Run it again and both are replaced. `AGENTS.md` has the skills line once, and a second run does not add another. `CLAUDE.md` is not created, edited, or replaced. Product code is unchanged.
