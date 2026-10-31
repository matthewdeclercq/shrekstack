---
name: setup-base
description: >-
  Writes the shared shrekstack base rule into a repo for Cursor and Claude
  Code. Use when the user asks to install the base rule or run setup-base.
  One model.
disable-model-invocation: true
---

# Setup Base

One model. Do not start another model or fan out.

Run in the target repo. Read `base.md` beside this skill and write it to two places, overwriting both on every run. Do not edit `AGENTS.md` or product code.

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

Create a directory if it is missing.

## Prove

The skill is a draft until the Cursor file is that frontmatter, a blank line, and the text of `base.md`, and the Claude file is that text alone. Run it again and both are replaced. `AGENTS.md` and product code are unchanged.
