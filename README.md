# shrekstack

Matthew's personal shared skills library for Claude Code, Cursor, and his Grok bots.

The public pstack pack (`backnotprop/pstack`, also `cursor/plugins` under `pstack`) is a `skills/<name>/SKILL.md` tree, plus `agents/`, `docs/`, and a plugin manifest. It has no `rules/` directory. This repo uses that skills tree. `rules/base.md` is the shared base rules, which pstack does not have.

Matthew's `tidy` skill will be added later. It is not in this library yet.

## Layout

```text
skills/<name>/SKILL.md
skills/<name>/scripts/     # only when that skill has a script
rules/base.md
README.md
```

Each `SKILL.md` starts with `name` and `description` frontmatter. `name` matches the parent folder. The four skills also set `disable-model-invocation: true`, so an agent runs one when you invoke it, not because the description happened to match.

| Skill | What it does |
| --- | --- |
| [commit-group](skills/commit-group/SKILL.md) | Turns an unstaged tree into logical commits and commits them |
| [code-cleanup](skills/code-cleanup/SKILL.md) | Removes dead code after proof, without a style refactor |
| [test-cleanup](skills/test-cleanup/SKILL.md) | Prunes tests that no longer lock a live rule |
| [doc-sync](skills/doc-sync/SKILL.md) | Fixes doc drift against the code and commits `Doc sync.` |

`doc-sync` ships [scripts/dead-paths.py](skills/doc-sync/scripts/dead-paths.py). It lists paths a doc names that the tree no longer has. Pass the target repo with `--root` and the doc files or directories as arguments, `--doc-folder`, or `--config`. With none of those, it exits 2 and does not pick a default list.

## Rules

[rules/base.md](rules/base.md) is the generic part of a project `AGENTS.md`: ask, don't drift; the code wins when a doc disagrees; the comment policy; lean code and the smallest diff; where a skill script lives; commit messages in complete sentences, one change per commit; a blocker only after 3 or more failed attempts.

Project-specific lists do not live here. A repo that adopts the skills puts them in its own `AGENTS.md` under the headings below.

## Headings the skills read

A heading matches at any level when the text after the hashes is exact. The skill's own table says what it does when that heading is missing or empty. It does not guess a list, a path, or a command.

| Heading | Skills | What the repo puts there |
| --- | --- | --- |
| `Git` | commit-group | Extra commit-message rules, and paths that must never be committed |
| `Commit groups` | commit-group | What stays together, what splits, default excludes, a default separate batch, batch order |
| `Build & test` | commit-group, code-cleanup, test-cleanup | That repo's lint and test commands |
| `Entry points` | code-cleanup | Where reachability starts |
| `Proof traps` | code-cleanup | Contracts to confirm before a delete |
| `File layout` | code-cleanup, test-cleanup | Disjoint areas a fan-out may split on |
| `Doc folders` | code-cleanup, doc-sync | Files and directories in scope for doc checks |
| `Architecture doc` | doc-sync | The one doc the architecture check may edit |
| `Skills due` | doc-sync | Extra paths that make the skills check due |
| `Architecture due` | doc-sync | Extra paths that make the architecture check due |
| `Testing defaults` | test-cleanup | What to test, where tests go, owner-rank invariants. The skill looks for the labels `What to test` and `Where tests go` |
| `Test passes` | test-cleanup | Ordered passes for a full-suite sweep |
| `Code roots` | doc-sync | Path prefixes that count as code |
| `Doc ownership` | doc-sync | Which doc keeps a fact |
| `Planning docs` | doc-sync | Docs to report against and not edit |

## How Cursor loads skills and rules

Cursor discovers a skill folder that contains `SKILL.md` from these directories, including nested project directories: `.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, `.codex/skills/`, and the same four under the home directory. User-level skills in `~/.cursor/skills/` stay on that machine until Sync Skills for Cloud Agents is on. Cursor does not copy `~/.agents/skills/` or unsynced local skills to Cloud Agents. On a self-hosted worker, use project skills from the repo or bake them into the worker image. Source: [Cursor Agent Skills](https://cursor.com/docs/skills).

`name` is required and must match the parent folder. `description` is required. `disable-model-invocation: true` loads the skill only when you invoke `/` plus the skill name. A `scripts/` directory is the documented place for code the skill runs. Source: the same page.

Cursor loads `AGENTS.md` from the project root and from subdirectories. More specific files win. A plain markdown file in `.cursor/rules/` is ignored. A project rule is an `.mdc` file with frontmatter. `alwaysApply: true` includes it every session. An `@path` mention in a rule or in `AGENTS.md` is a pointer: the agent can read the file with its tools, and the contents are not inlined. Anything that must always be in context has to be pasted into `AGENTS.md` or into the `.mdc` body. Source: [Cursor Rules](https://cursor.com/docs/rules).

Cursor does not import skills or rules from a GitHub repository on their own. The documented install is a plugin published through a marketplace, and the repository needs a marketplace manifest under its Cursor plugin directory. This repo does not ship that manifest. Source: the skills and rules pages above.

## How Claude Code loads skills and rules

Claude Code loads `.claude/skills/<name>/SKILL.md` for the project and `~/.claude/skills/<name>/SKILL.md` for you. A skill folder entry may be a symlink to a directory elsewhere. Claude Code reads `SKILL.md` from the target and loads that skill once if several locations point at the same target. Source: [Extend Claude with skills](https://code.claude.com/docs/en/skills).

`description` is the field Claude Code uses to decide when to apply a skill. `disable-model-invocation: true` stops Claude from invoking it on its own. Source: the same page.

Claude Code reads `AGENTS.md` when the working directory and its parents have no `CLAUDE.md` or `CLAUDE.local.md`. That direct read needs Claude Code v2.1.277 or later. Inside an `AGENTS.md` it does read, `@path` imports are expanded. Markdown files in `.claude/rules/` with no `paths` frontmatter load at session start. The `.claude/rules/` directory supports symlinks. A symlink whose target is outside the working directory is an external import: it does not load until you approve it, and after that only rules without a `paths` field load. `~/.claude/rules/` applies to every project on the machine without that per-project approval. Source: [How Claude remembers your project](https://code.claude.com/docs/en/memory).

Keep a `CLAUDE.md` symlink to `AGENTS.md` in every repo:

```bash
ln -s AGENTS.md CLAUDE.md
```

Claude Code documents that symlink when you do not need Claude-only text in `CLAUDE.md`. The Edit and Write tools refuse to write through the symlink and point at `AGENTS.md`. On Windows, prefer a `CLAUDE.md` whose contents are the line `@AGENTS.md`, because creating the symlink needs extra privileges and Git may check it out as a one-line text file. Source: the memory page above.

## How a Grok bot loads skills and rules

A Grok bot built with the Agent SDK (`@grok/agent-sdk`) keeps its files under `bot/`. A packaged skill is `SKILL.md` in a directory under the bot `skills/` directory, with sibling files beside it, and the frontmatter must include `description`. The SDK advertises the description and loads the skill when the task calls for it. A local session then has the skill at `.cursor/skills/<name>/SKILL.md` in the session workspace. Source: [Agent SDK skills](https://cursor.com/docs/agent-sdk/reference/skills) and [project layout](https://cursor.com/docs/agent-sdk/reference/project-layout).

Always-on text is `instructions.md` in the bot directory, not a skill. The SDK does not write an `AGENTS.md` into the workspace. A parent directory's `AGENTS.md` can still reach a local session. Source: [Instructions](https://cursor.com/docs/agent-sdk/reference/instructions) and [Agent config](https://cursor.com/docs/agent-sdk/reference/agent-config).

Subagent directories do not discover their own `skills/` folder. Source: [Subagents](https://cursor.com/docs/agent-sdk/reference/subagents).

## How a repo adopts this library

Copy each `skills/<name>/` directory into the tool's skill directory, or symlink the skill directory when that tool documents symlinks.

Claude Code, from the adopting repo, with this repo checked out beside it:

```bash
mkdir -p .claude/skills
ln -s /absolute/path/to/shrekstack/skills/<name> .claude/skills/<name>
```

Cursor's documented project path is a real `SKILL.md` under `.cursor/skills/<name>/` (or `.agents/skills/<name>/`, or the Claude and Codex paths Cursor also scans). Copy the skill directory there. The skills page does not say that a symlink is followed.

For Claude Code rules, symlink [rules/base.md](rules/base.md) into `.claude/rules/` (external targets need the one-time import approval), or put an `@path` import in `AGENTS.md`. For Cursor, paste `rules/base.md` into `AGENTS.md`, or copy it into `.cursor/rules/<name>.mdc` with `alwaysApply: true`. An `@path` line in `AGENTS.md` does not inline the file.

For a Grok bot, copy each skill directory into the bot project's `skills/` directory so the bot has `SKILL.md` plus any `scripts/` sibling. Copy `rules/base.md` into the bot's `instructions.md`, or merge it with the instructions already there.

The adopting repo still needs its own `AGENTS.md` headings from the table above. The skills read that file for groupings, entry points, doc folders, and lint and test commands, then run those commands.
