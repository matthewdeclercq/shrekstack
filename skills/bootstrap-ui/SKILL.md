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

Link the new folder for each tool `Agent tools` in `AGENTS.md` names, with a relative symlink: `.claude/skills/ui` for Claude Code, `.cursor/skills/ui` for Cursor. Missing: run [bootstrap-repo](../bootstrap-repo/SKILL.md) first. A symlink already there is replaced. A real file or folder at either path may hold hand-written work: before writing, ask the user whether to move what it holds into `.agents/skills/ui/` and build on it, or start fresh. Do that, then remove the old copy and create the links.

## Learn

Read the UI code (screens, navigation, forms, colors or tokens) and how the repo lints. Ask only what those do not say: a pattern the code does not already show. If the repo already uses its own spacing or type scale on purpose, ask the user whether it or the scales below win, and write the winner.

If the repo has no UI, stop and say so. Do not invent screens so the proof can pass.

## Write

Frontmatter `name: ui`. The description names the stack and when to run the skill. Keep the file short.

State this in the skill, and follow it: a fact goes in only if an agent would reuse it on a new screen. The code wins on screen contents. No inventories: button copy, field lists, icons, defaults.

Where a line below names a file, a pattern, or a command, take it from this repo's code. Do not invent one.

- **Not a design freeze.** Reference files are starting points. Explicit user direction wins.
- **Reference screens.** A table of pattern to file, so an agent copies an existing shell instead of inventing one. One clause per cell.
- **Tokens.** Semantic tokens stay in one file per UI stack. Name each. No raw colors in feature code.
- **Spacing.** Padding, margin, and gap use only 2, 4, 8, 16, 24, 32, 48, 64, then multiples of 16. Vertical rhythm is 8pt. Name the file or tokens that hold the scale.
- **Type.** A set type scale, one per form factor the app has (for example desktop and mobile). Name where each lives. Line height is 1.5x font size for body text and about 1.2x for headings, rounded up to the next multiple of 4 (12 text: 18 becomes 20). No one-off font sizes.
- **Platform first.** On native apps, built-in components and text-size settings win over these numbers.
- **Layout.** Contrast: text meets WCAG AA (4.5:1, 3:1 for large text), and each view has one primary action. Repetition: reuse an existing component before making a new one. Alignment: elements share edges on the grid; no nudged offsets. Proximity: related items sit closer together than unrelated ones.
- **Explainer text.** Avoid subheadings, captions, and footer notes that explain the UI. If a screen seems to need one, improve the design first: clearer labels, layout, or defaults. Add it only if the screen still needs it. Errors, legal text, and warnings before destructive actions are exempt.
- **Fix on touch.** Spacing, type, and layout beat the existing code. An agent editing a screen fixes every break of them on that screen.
- **Casing.** A table by element type. Examples illustrate the rule.
- **Navigation and forms.** The patterns this repo's code actually uses.
- **Anti-patterns.** A short list of what this repo's code already refuses.
- **Before committing.** Check phone and tablet, or narrow and wide, whichever this product has. Check the changed screens against spacing, type, and layout. Name the repo's lint command. If it has none, write that there is none.
- **Unclear design.** Ask for a mockup or screenshot when a new design is unclear.

## Prove

The skill is a draft until every path it cites exists and each link resolves to `.agents/skills/ui`. If a path is wrong, fix the skill and look again. Do not add a cited file to make it pass.
