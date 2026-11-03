---
name: bootstrap-repo
description: >-
  Writes the shared shrekstack base rule and response style into a repo for
  Claude Code, Cursor, or both, folds every agent instruction file into one lean
  root AGENTS.md, moves every skill into .agents/skills/, drafts the AGENTS.md
  headings shrekstack skills read from the code, sets up the planning docs
  through doc-steward, and links it all for each tool.
  Use when the user asks to install the base rule or run bootstrap-repo.
disable-model-invocation: true
---

# Bootstrap Repo

Run in the target repo. Do not edit product code, except the path fixes in step 9. Touch only the rule files, the agent instruction files, the skill folders, the folder READMEs step 4 names, and the docs doc-steward writes in step 8. Leave everything uncommitted so the owner reviews one diff.

1. **Tools.** Read `Agent tools` in `AGENTS.md`. When it is missing or `TODO`, ask once: Claude Code, Cursor, or both. Each later step sets up only the tools chosen, and removes what an earlier run set up for a tool no longer chosen.

2. **Rules.** Write each file in this table, from beside this skill: for Claude Code, unchanged as a `.md` in `.claude/rules/`; for Cursor, as a `.mdc` in `.cursor/rules/` with frontmatter, a blank line, then the text. Overwrite them on every run. Delete `shrekstack-base` and `shrekstack-style` (`.md` and `.mdc`) left by an older run.

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

3. **Find the agent files.** List every `AGENTS.md` and `CLAUDE.md` in the repo, at the root and in any folder, skipping gitignored and vendored paths. Read them all. If the root `AGENTS.md` is a directory, or a symlink to something outside the repo, leave it, say so, and skip steps 4 and 7. If the root `CLAUDE.md` is a real file, ask once whether to fold it into `AGENTS.md` or start fresh; fold every other file without asking.

4. **One root AGENTS.md.** The repo ends with one agent file, `AGENTS.md` at the root. Sort every line of the files from step 3, the root `AGENTS.md` included: never keep an existing file as the base and append to it. Check each fact against the code first:

   - **Keep in AGENTS.md:** repo-specific commands, environment setup, hard constraints, paths never to commit, and anything a heading in step 6 holds. One copy, under its heading, as one line or a short list. Cut the explanation, examples, and sample code around a kept fact unless they are a command.
   - **Move to the folder's `README.md`:** what a folder holds and how its parts fit. Text from a nested agent file goes to the README of its folder; create that README when there is none. A folder README never holds agent instructions.
   - **Move to a skill:** a step-by-step procedure for one area, such as a schema change. Put it in `.agents/skills/<name>/SKILL.md` with a description that says when it applies.
   - **Hand to doc-steward in step 8:** plans, goals, decisions, and write-ups of how the whole system fits together. Set them aside; they never stay in `AGENTS.md`.
   - **Cut:** anything `base.md` or `style.md` already says, generic advice any agent already follows, a fact the code shows is false, and a second copy of a fact.

   Then delete every nested `AGENTS.md` and `CLAUDE.md`. Write `AGENTS.md` in this order: the repo name as the title, one sentence from the README on what the repo is, the line ``Repo-specific skills live in `.agents/skills/`.``, `Agent tools` with one list item per tool chosen in step 1, the kept facts under short headings, then the headings in step 6. Keep a heading the old files already had when it is right.

5. **Skills.** Every repo skill lives in `.agents/skills/<name>/`. Move each skill folder (one holding a `SKILL.md`) found in a `.claude/skills/` or `.cursor/skills/` at any depth into `.agents/skills/`, skipping symlinks that already point there. When two skills share a name, ask which to keep or how to rename. Then, for each folder in `.agents/skills/`, create a relative symlink for each tool chosen: `.claude/skills/<name>` for Claude Code, `.cursor/skills/<name>` for Cursor, each pointing at `../../.agents/skills/<name>`. Link each skill on its own, never the whole skills folder. Remove skill folders left empty.

6. **Draft the skill headings from the code.** Read the manifests, CI workflows, run scripts, Dockerfiles, framework config, and tests. Write what the code shows; never guess. Write `TODO: ` and why only when the repo holds no evidence, such as no tests at all.

   - `Build & test`: install, build, lint, test, and run commands. Prefer what CI runs.
   - `Entry points`: one line per app, service, CLI, worker, or job: the file it starts from (a `main`, a server bootstrap, a manifest `bin` or `main`, a Dockerfile `CMD`, a framework's entry folder).
   - `Proof traps`: code reached by name rather than import, as the paths or patterns found. Look for file-based routing, handlers registered by string, reflection and dynamic imports, plugin or console entry points in a manifest, names in config or env, CLI commands, webhooks, MCP tool names, persistence keys and migrations, fixtures loaded by path, generated code, and anything exported for outside callers.
   - `File layout`: opens with the line `Before working in an area, read its README.` Then the disjoint areas work can split across, one list item per area: a path, what it holds, and a link to its `README.md` when it has one. Areas never overlap; a shared folder is its own area. Each top-level code folder (`api/`, `web/`, `mcp/`, `mocks/`) is usually one.
   - `Code roots`: one list item per path prefix that counts as code, tests included. Never docs.
   - `Testing defaults`: three list items. `What to test`: the kinds of test the repo already writes and what they lock. `Where tests go`: the placement the existing tests follow. `Owner-rank`: tests guarding auth, money, data loss, persistence formats, or a regression named after a bug, by path.

7. **CLAUDE.md.** For Claude Code, end with `CLAUDE.md` a relative symlink to `AGENTS.md` (`ln -s AGENTS.md CLAUDE.md`), replacing what was there. Cursor reads `AGENTS.md` itself; with Cursor alone, remove the link.

8. **Planning docs.** Run [doc-steward](../doc-steward/SKILL.md)'s Bootstrap. Give it what step 4 set aside, to place in the docs its map names, checking each fact against the code. It writes only the docs the repo lacks and never replaces one that exists.

9. **Fix the paths this run broke.** Search the whole repo, code included, for the path of every file this run deleted or moved: the agent files, the skill folders, and the old rule files. Point each mention, in a comment, string, doc, or skill, at the file that now holds the fact. Change only the path. When the fact was cut, leave the mention and list it in the report.

Report in a few lines: the tools set up; the line count of the agent files before and of `AGENTS.md` after; the rule files written and removed; each agent file folded, and where its facts went; each skill moved; what was cut, in a phrase each; the paths fixed, and those left for the owner; the docs doc-steward wrote, and where the set-aside text went; and the drafted headings for the owner to check, `Proof traps` and `Owner-rank` first, since a miss there lets a skill delete live code or a test that matters. List any `TODO` left.
