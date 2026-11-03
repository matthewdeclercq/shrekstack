---
name: bootstrap-repo
description: >-
  Writes the shared shrekstack base rule and response style into a repo for
  Cursor and Claude Code, folds every agent instruction file into one lean
  root AGENTS.md, drafts the AGENTS.md headings shrekstack skills read from the
  code, and links CLAUDE.md. Use when the user asks to install the base rule or run bootstrap-repo.
disable-model-invocation: true
---

# Bootstrap Repo

Run in the target repo. Do not edit product code. Touch only the rule files, the agent instruction files, and the folder READMEs step 3 names. Leave everything uncommitted so the owner reviews one diff.

1. **Rules.** Write each file in this table, from beside this skill, into the repo twice: unchanged as a `.md` in `.claude/rules/`, and as a `.mdc` in `.cursor/rules/` with frontmatter, a blank line, then the text. Overwrite all four on every run. Delete `shrekstack-base` and `shrekstack-style` (`.md` and `.mdc`) left by an older run.

   | Source | Name in the repo | Cursor `description` |
   |--------|------------------|----------------------|
   | `base.md` | `base` | Generic rules for a repo that adopts this library. Project lists, commands, and paths stay in that repo's AGENTS.md. |
   | `style.md` | `style` | How agents talk to the owner in chat. |

   The Cursor frontmatter:

   ```
   ---
   description: <Cursor description>
   alwaysApply: true
   ---
   ```

2. **Find the agent files.** List every `AGENTS.md` and `CLAUDE.md` in the repo, at the root and in any folder, skipping gitignored and vendored paths. Read them all. If the root `AGENTS.md` is a directory, or a symlink to something outside the repo, leave it, say so, and skip steps 3 and 5. If the root `CLAUDE.md` is a real file, ask once whether to fold it into `AGENTS.md` or start fresh; fold every other file without asking.

3. **One root AGENTS.md.** The repo ends with one agent file, `AGENTS.md` at the root. Sort every line of the files from step 2, checking each fact against the code first:

   - **Keep in AGENTS.md:** repo-specific commands, environment setup, hard constraints, paths never to commit, and anything a heading in step 4 holds. One copy, under its heading.
   - **Move to the folder's `README.md`:** what a folder holds and how its parts fit. Text from a nested agent file goes to the README of its folder; create that README when there is none. A folder README never holds agent instructions.
   - **Cut:** anything `base.md` or `style.md` already says, generic advice any agent already follows, a fact the code shows is false, a second copy of a fact, and plans, goals, or decisions. Name the plans in the report so the owner can hand them to doc-steward.

   Then delete every nested `AGENTS.md` and `CLAUDE.md`. Write `AGENTS.md` in this order: the repo name as the title, one sentence from the README on what the repo is, the line ``Repo-specific skills live in `.agents/skills/`.``, the kept facts under short headings, then the headings in step 4. Keep a heading the old files already had when it is right.

4. **Draft the skill headings from the code.** Read the manifests, CI workflows, run scripts, Dockerfiles, framework config, and tests. Write what the code shows; never guess. Write `TODO: ` and why only when the repo holds no evidence, such as no tests at all.

   - `Build & test`: install, build, lint, test, and run commands. Prefer what CI runs.
   - `Entry points`: one line per app, service, CLI, worker, or job: the file it starts from (a `main`, a server bootstrap, a manifest `bin` or `main`, a Dockerfile `CMD`, a framework's entry folder).
   - `Proof traps`: code reached by name rather than import, as the paths or patterns found. Look for file-based routing, handlers registered by string, reflection and dynamic imports, plugin or console entry points in a manifest, names in config or env, CLI commands, webhooks, MCP tool names, persistence keys and migrations, fixtures loaded by path, generated code, and anything exported for outside callers.
   - `File layout`: the disjoint areas work can split across, one list item per area: a path and what it holds. Areas never overlap; a shared folder is its own area. Each top-level code folder (`api/`, `web/`, `mcp/`, `mocks/`) is usually one.
   - `Code roots`: one list item per path prefix that counts as code, tests included. Never docs.
   - `Testing defaults`: three list items. `What to test`: the kinds of test the repo already writes and what they lock. `Where tests go`: the placement the existing tests follow. `Owner-rank`: tests guarding auth, money, data loss, persistence formats, or a regression named after a bug, by path.

5. **CLAUDE.md.** End with `CLAUDE.md` a relative symlink to `AGENTS.md` (`ln -s AGENTS.md CLAUDE.md`), replacing what was there.

Report in a few lines: the rule files written and removed; each agent file folded, and where its facts went; what was cut, in a phrase each; the plans to hand to doc-steward; and the drafted headings for the owner to check, `Proof traps` and `Owner-rank` first, since a miss there lets a skill delete live code or a test that matters. List any `TODO` left.
