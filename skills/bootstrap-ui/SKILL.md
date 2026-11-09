---
name: bootstrap-ui
description: >-
  Writes a repo's UI conventions skill from its screens, tokens, and
  patterns, then proves every path once. Use when the user asks to set up
  UI conventions or add a UI skill.
disable-model-invocation: true
---

# Bootstrap UI

Run in the target repo. Write `SKILL.md` in `.agents/skills/ui/`, covering every UI stack in the repo. Do not edit product code. Do not copy a UI skill from another repo.

Link the new folder the way [bootstrap-repo](../bootstrap-repo/SKILL.md) step 5 does, for the tools `Agent tools` in `AGENTS.md` names. Missing: run bootstrap-repo first. A real file or folder at a link path may hold hand-written work: before writing, ask whether to move it into `.agents/skills/ui/` and build on it, or start fresh.

## Learn

Read the UI code (screens, navigation, forms, colors or tokens). Ask only what those do not say: a pattern the code does not already show.

If the repo has no UI, stop and say so. Do not invent screens so the proof can pass.

## Write

Frontmatter `name: ui`. The description names the stack and when to run the skill. Keep the file short.

State this in the skill, and follow it: a fact goes in only if an agent would reuse it on a new screen. The code wins on screen contents. No inventories: button copy, field lists, icons, defaults.

Where a line below names a file, a pattern, or a command, take it from this repo's code. Do not invent one.

- **Not a design freeze.** Reference files are starting points.
- **Reference screens.** A table of pattern to file, so an agent copies an existing shell instead of inventing one. One clause per cell.
- **Tokens.** Semantic tokens stay in one file per UI stack. Name each, or where the first one goes when there is none. No raw colors in feature code.
- **Spacing and type.** One spacing scale, and one type scale per form factor, each named where it lives. No one-off values. Use the repo's own scales; with none, write this spacing scale into the skill: 4, 8, 16, 24, 32, 48, 64.
- **Vertical rhythm.** Vertical space comes from the spacing scale, and line heights fit its grid, so text and blocks line up.
- **Platform first.** On native apps, built-in components and system text sizes win over these scales.
- **Explainer text.** Avoid text that explains the UI; reach for clearer labels, layout, or defaults first.
- **Casing.** A table by element type. Examples illustrate the rule.
- **Navigation and forms.** The patterns this repo's code actually uses.
- **Anti-patterns.** A short list of what this repo's code already refuses.
- **Apply.** Code you add or change follows these standards. Fix breaks in the lines you touch, and list others you see.
- **Before committing.** Check phone and tablet, or narrow and wide, whichever this product has, and that the changed screens meet these standards.

## Prove

The skill is a draft until every path it cites exists, apart from where a first token file goes, and each link resolves to `.agents/skills/ui`. If a path is wrong, fix the skill and look again. Do not add a cited file to make it pass.
