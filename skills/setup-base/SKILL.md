---
name: setup-base
description: >-
  Writes the shared shrekstack base rule into a repo for Cursor and Claude
  Code, the AGENTS.md headings shrekstack skills read, and a CLAUDE.md
  symlink. Use when the user asks to install the base rule or run setup-base.
disable-model-invocation: true
---

# Setup Base

Run in the target repo. Do not edit product code. Never overwrite or rewrite anything already there except the two rule files.

1. **Rule.** Write `base.md` from beside this skill as `shrekstack-base.md` in `.claude/rules/`, unchanged, and as `shrekstack-base.mdc` in `.cursor/rules/`, with this frontmatter, a blank line, then the text. Overwrite both on every run.

   ```
   ---
   description: Generic rules for a repo that adopts this library. Project lists, commands, and paths stay in that repo's AGENTS.md.
   alwaysApply: true
   ---
   ```

2. **AGENTS.md.** Create it if it is missing, with the repo name as the title and one sentence from the README on what the repo is. Make sure it has the line ``Repo-specific skills live in `.agents/skills/`.`` exactly once. Add each heading below that it does not already have, at the end:

   - `Build & test`: the build, test, and run commands, read from the repo. Write `TODO` for one you cannot find; do not guess.
   - `Entry points`, `Proof traps`, `File layout`, `Code roots`, `Doc folders`, `Planning docs`, `Architecture doc`, `Testing defaults`: a body of `TODO: ` and what the heading holds, from the skill that reads it.

   If AGENTS.md is a directory, or a symlink to something outside the repo, leave it and say so.

3. **CLAUDE.md.** If nothing is at that path, symlink it to `AGENTS.md` (`ln -s AGENTS.md CLAUDE.md`). If something is there, leave it and say what it is.

Then list the `TODO`s and ask the owner to fill them in. Skills treat a heading whose body starts with `TODO` as missing.
