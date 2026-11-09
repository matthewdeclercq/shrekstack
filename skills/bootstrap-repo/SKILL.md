---
name: bootstrap-repo
description: >-
  Writes the shared shrekstack base rule, and the response style when asked, into a repo for
  Claude Code, Cursor, or both, folds every agent instruction file into a lean
  root AGENTS.md and one per area, moves every skill into .agents/skills/, drafts the AGENTS.md
  headings shrekstack skills read from the code, sets up the planning docs
  through doc-steward, and links it all for each tool.
  Use when the user asks to install the base rule or run bootstrap-repo.
disable-model-invocation: true
---

# Bootstrap Repo

Run in the target repo. Do not edit product code, except the path fixes in step 9. Touch only the rule files, the agent instruction files, the folder READMEs step 4 splits, the spike write-ups step 4 writes, the skill folders, and the docs doc-steward writes in step 8. Leave everything uncommitted so the owner reviews one diff.

1. **Tools.** Read `Agent tools` in `AGENTS.md`. When it is missing or `TODO`, ask once: Claude Code, Cursor, or both. Each later step sets up only the tools chosen, and removes what an earlier run set up for a tool no longer chosen.

2. **Rules.** Write each file in this table, from beside this skill: for Claude Code, unchanged as a `.md` in `.claude/rules/`; for Cursor, as a `.mdc` in `.cursor/rules/` with frontmatter, a blank line, then the text. Overwrite them on every run. `style.md` is optional: when the repo has no `style` rule yet, ask once whether to install it, and say that every agent working in the repo, a teammate's included, will follow it. Delete `shrekstack-base` and `shrekstack-style` (`.md` and `.mdc`) left by an older run.

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

3. **Find the agent files.** List every `AGENTS.md` and `CLAUDE.md` in the repo, at the root and in any folder, skipping gitignored and vendored paths. Also list every `README.md` in a folder below the root, except one a skill reads itself (such as a verify skill's `features/README.md`) and one in a folder the app bundles or ships (an asset, package, or extension folder whose README is copied into the build); leave those two kinds as they are. Read them all. If the root `AGENTS.md` is a directory, or a symlink to something outside the repo, leave it, say so, and skip steps 4 and 7. If the root `CLAUDE.md` is a real file, ask once whether to fold it into `AGENTS.md` or start fresh; fold every other file without asking.

4. **Lean AGENTS.md files.** The repo ends with a root `AGENTS.md`, plus an `AGENTS.md` at the top of an area from step 6's `File layout` that has facts of its own. Sort every line of the files from step 3, the root `AGENTS.md` included: never keep an existing file as the base and append to it. Check each fact against the code first, and keep only what the code shows today: re-check a number, a size, or a claim such as "runs in CI" against the code, the CI workflows, and the tree before moving it, and drop it when you cannot.

   - **Keep in the root AGENTS.md:** repo-wide commands, environment setup, and hard constraints, paths never to commit, and the root part of each heading in step 6. One copy, under its heading, as one line or a short list. Cut the explanation, examples, and sample code around a kept fact unless they are a command.
   - **Move to the area's `AGENTS.md`:** any fact only that area needs, such as its setup, its scripts, and its part of the headings in step 6.
   - **README vs AGENTS.md:** a folder's `README.md` from step 3 keeps a short list of what the folder holds and what each part does. Move its commands, rules, and deploy steps to that area's `AGENTS.md` (or the root one), and cut from the `AGENTS.md` anything the README already lists.
   - **Move to a spike write-up:** measurements, test results, and cost history. Put each in `docs/spikes/<topic>.md`, and keep in `AGENTS.md` only the one-line rule it led to, if any.
   - **Move to a skill:** a step-by-step procedure for one area, such as a schema change. Put it in `.agents/skills/<name>/SKILL.md` with a description that says when it applies.
   - **Hand to doc-steward in step 8:** plans, goals, decisions, and write-ups of how the whole system fits together. Set them aside; they never stay in `AGENTS.md`.
   - **Cut:** anything `base.md` or `style.md` already says, generic advice any agent already follows, a line telling agents to read an `AGENTS.md`, a fact the code shows is false, and a second copy of a fact.

   Then delete every nested `CLAUDE.md`, and every nested `AGENTS.md` not at the top of an area. Write the root `AGENTS.md` in this order: the repo name as the title, one sentence from the README on what the repo is, the line ``Repo-specific skills live in `.agents/skills/`.``, `Agent tools` with one list item per tool chosen in step 1, the kept facts under short headings, then the headings in step 6. Keep a heading the old files already had when it is right.

5. **Skills.** Every repo skill lives in `.agents/skills/<name>/`. Move each skill folder (one holding a `SKILL.md`) found in a `.claude/skills/` or `.cursor/skills/` at any depth into `.agents/skills/`, skipping symlinks that already point there. When two skills share a name, ask which to keep or how to rename. Then, for each folder in `.agents/skills/`, create a relative symlink for each tool chosen: `.claude/skills/<name>` for Claude Code, `.cursor/skills/<name>` for Cursor, each pointing at `../../.agents/skills/<name>`. Link each skill on its own, never the whole skills folder. Remove skill folders left empty.

6. **Draft the skill headings from the code.** Read the manifests, CI workflows, run scripts, Dockerfiles, framework config, and tests. Write what the code shows; never guess. Write `TODO: ` and why only when the repo holds no evidence, such as no tests at all.

   - `Build & test`: install, build, lint, test, and run commands. Prefer what CI runs.
   - `Entry points`: one line per app, service, CLI, worker, or job: the file it starts from (a `main`, a server bootstrap, a manifest `bin` or `main`, a Dockerfile `CMD`, a framework's entry folder).
   - `Proof traps`: code reached by name rather than import, as the paths or patterns found. Look for file-based routing, handlers registered by string, reflection and dynamic imports, plugin or console entry points in a manifest, names in config or env, CLI commands, webhooks, MCP tool names, persistence keys and migrations, fixtures loaded by path, generated code, and anything exported for outside callers. A trap confined to one area goes under `Proof traps` in that area's `AGENTS.md` instead.
   - `File layout`: the disjoint areas work can split across, one list item per area: a path and what it holds. Areas never overlap; a shared folder is its own area. Each top-level code folder (`api/`, `web/`, `mcp/`, `mocks/`) is usually one.
   - `Code roots`: one list item per path prefix that counts as code, tests included. Never docs.
   - `Testing defaults`: three list items. `What to test`: the kinds of test the repo already writes and what they lock. `Where tests go`: the placement the existing tests follow. `Owner-rank`: tests guarding auth, money, data loss, persistence formats, or a regression named after a bug, by path. An area whose tests differ gets `Testing defaults` in its `AGENTS.md`, with only what differs.

7. **No CLAUDE.md.** A `CLAUDE.md` makes Claude Code skip `AGENTS.md`. Remove the root `CLAUDE.md` and `.claude/CLAUDE.md`, a symlink an older run left included. Leave a personal `CLAUDE.local.md`.

8. **Planning docs.** Run [doc-steward](../doc-steward/SKILL.md)'s Bootstrap. Give it what step 4 set aside, to place in the docs its map names, checking each fact against the code. It writes only the docs the repo lacks and never replaces one that exists.

9. **Fix the paths this run broke.** Search the whole repo, code included, for the path of every file this run deleted or moved: the agent files, the skill folders, and the old rule files. Point each mention, in a comment, string, doc, or skill, at the file that now holds the fact, and to its section when the mention names one. Open that section and confirm it holds what the mention promises; if no section does, point at the file and list the mention in the report. Change only the path. When the fact was cut, leave the mention and list it in the report.

10. **Trim.** Reread every file this run wrote or changed, each `AGENTS.md` beside its folder's `README.md` and the root one beside each area's. Cut a fact that appears twice (keep the copy the rules above give a home), a line that repeats `base.md` or `style.md`, and a claim the code does not back. Check each line moved in step 4 against the code once more.

Report in a few lines: the tools set up; the rule files written and removed; each agent file folded, and where its facts went; any `CLAUDE.local.md` left; each skill moved; what was cut, in a phrase each, the trim in step 10 included; each spike write-up written; the paths fixed, and those left for the owner; the docs doc-steward wrote, and where the set-aside text went; and the drafted headings for the owner to check, `Proof traps` and `Owner-rank` first, since a miss there lets a skill delete live code or a test that matters. List any `TODO` left.

End by offering what comes next, once the owner has checked the drafted headings: [bootstrap-verify](../bootstrap-verify/SKILL.md) when `.agents/skills/` holds no `verify-*` skill, and [bootstrap-ui](../bootstrap-ui/SKILL.md) when the repo has screens and no `ui` skill. Ask once which to run, and run nothing until the owner answers. When neither applies, skip the offer.
