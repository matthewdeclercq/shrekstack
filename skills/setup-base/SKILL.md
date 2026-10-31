---
name: setup-base
description: >-
  Writes the shared shrekstack base rule into a repo for Cursor and Claude
  Code, a short AGENTS.md when one is missing, a CLAUDE.md symlink, and
  starter hooks. Use when the user asks to install the base rule or run
  setup-base. One model.
disable-model-invocation: true
---

# Setup Base

One model. Do not start another model or fan out.

Run in the target repo. Read `base.md` beside this skill and write it to two places, overwriting both on every run. Do not edit product code. Read [stacks.md](stacks.md) for the starter, the commands, and the hooks. Do not guess a command or a tool.

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

- **AGENTS.md.** The skills line, on its own line, is:

  ```
  Repo-specific skills live in `.agents/skills/`.
  ```

  If `AGENTS.md` is missing, write the starter in `stacks.md`, including that line once. If it exists, do not rewrite it and do not replace it with a starter. Follow `stacks.md` for a symlink or a non-file. Otherwise add the line when no line is exactly that text. If more than one line is exactly that text, keep the first and delete the extras.

- **CLAUDE.md.** After `AGENTS.md` is a file in the repo, at the repo root: if `CLAUDE.md` is missing, create a relative symlink whose target text is `AGENTS.md` (`ln -s AGENTS.md CLAUDE.md`). If it is already a symlink that resolves to that `AGENTS.md`, do nothing. If it is a regular file, or a symlink to anything else, leave it. Never replace it.

- **Hooks.** If the repo already has a hook install from `stacks.md`, leave it and report each missing kind. Otherwise write the one config `stacks.md` names for the single detected stack. Write nothing when no stack, or more than one, matches.

Create a directory if it is missing.

## Notes

Use the end-note sentences in `stacks.md`. Name a `CLAUDE.md` you left in place, and any hook gap. Do not tell the user to create the symlink.

## Prove

The skill is a draft until the Cursor file is that frontmatter, a blank line, and the text of `base.md`, and the Claude file is that text alone. Run it again and both are replaced. A missing `AGENTS.md` is the starter, and an existing one gains only the skills line. A second run does not add the line again and does not regenerate the starter. A missing `CLAUDE.md` is that relative symlink; a regular file or other symlink is unchanged. A new hook config matches `stacks.md`; an existing install is unchanged. Product code is unchanged.
