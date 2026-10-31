---
name: setup-ui
description: >-
  Writes a repo's UI conventions skill from its screens, tokens, and
  patterns, then proves every path once. Use when the user asks to set up
  UI conventions or add a UI skill. One model.
disable-model-invocation: true
---

# Setup UI

One model. Do not start another model or fan out.

Run in the target repo. Write `.cursor/skills/ui/SKILL.md`, covering every UI stack in the repo. Do not edit product code. Do not copy a UI skill from another repo.

## Learn

Read the UI code (screens, navigation, forms, colors or tokens) and how the repo lints. Ask only what those do not say: a pattern the code does not already show.

If the repo has no UI, stop and say so. Do not invent screens so the proof can pass.

## Write

Frontmatter `name: ui`. The description names the stack and when to run the skill. Keep the file short.

State this in the skill, and follow it: a fact goes in only if an agent would reuse it on a new screen. The code wins on screen contents. No inventories: button copy, field lists, icons, defaults.

Where a line below names a file, a pattern, or a command, take it from this repo's code. Do not invent one.

- **Not a design freeze.** Reference files are starting points. Explicit user direction wins.
- **Reference screens.** A table of pattern to file, so an agent copies an existing shell instead of inventing one. One clause per cell.
- **Tokens.** Semantic tokens stay in one file. Name it. No raw colors in feature code.
- **Casing.** A table by element type. Examples illustrate the rule.
- **Navigation and forms.** The patterns this repo's code actually uses.
- **Anti-patterns.** A short list of what this repo's code already refuses.
- **Before committing.** Check phone and tablet, or narrow and wide, whichever this product has. Name the repo's lint command. If it has none, write that there is none.
- **Unclear design.** Ask for a mockup or screenshot when a new design is unclear.

## Prove

The skill is a draft until every path it cites exists. If a path is wrong, fix the skill and look again. Do not add a cited file to make it pass.
