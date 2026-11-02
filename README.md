# shrekstack

Matthew's personal shared skills library for Claude Code, Cursor, and his Grok bots. Skills live in `skills/<name>/SKILL.md`. The shared base rule is [skills/setup-base/base.md](skills/setup-base/base.md).

## Skills

- [commit-group](skills/commit-group/SKILL.md) turns an unstaged tree into logical commits and commits them.
- [code-cleanup](skills/code-cleanup/SKILL.md) removes dead code after proof, without a style refactor.
- [test-cleanup](skills/test-cleanup/SKILL.md) prunes tests that no longer lock a live rule.
- [doc-steward](skills/doc-steward/SKILL.md) writes the map of which doc owns which fact, and records a decision change.
- [doc-sync](skills/doc-sync/SKILL.md) fixes doc drift against the code and commits `Doc sync.`
- [tidy](skills/tidy/SKILL.md) checks the work just finished for anything to clean up or simplify.
- [review](skills/review/SKILL.md) reviews the agent's own change before a pull request, after tidy.
- [setup-base](skills/setup-base/SKILL.md) writes that base rule, the AGENTS.md headings skills read, and the CLAUDE.md link into the adopting repo.
- [setup-verify](skills/setup-verify/SKILL.md) writes a repo's verify skill and proves it once.
- [setup-ui](skills/setup-ui/SKILL.md) writes a repo's UI conventions skill and proves every path once.
- [maintain-verify](skills/maintain-verify/SKILL.md) brings that skill back in line after the code changes.

## Install

Install the plugin, so every repo gets the same skills and updates from this one. Skills then run as `/shrekstack:<name>`.

**Claude Code.**

```text
/plugin install shrekstack --marketplace matthewdeclercq/shrekstack
```

**Cursor.** Import this repo as a plugin from GitHub. `.cursor-plugin/` holds its manifest.

**Grok bots, or a repo that must pin its own copy.** Copy each `skills/<name>/` directory into the bot's `skills/`, `.claude/skills/`, or `.cursor/skills/`. A copy does not get updates. The base text goes into each bot's own instructions.

Then run [setup-base](skills/setup-base/SKILL.md) in each adopting repo to install the base rule and the AGENTS.md headings.

Bump `version` in both `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json` whenever skills change, to the same number. CI checks they match. Claude Code updates an installed plugin only when that version changes.

## AGENTS.md

Skills read these headings from the adopting repo's `AGENTS.md`. setup-base writes a `TODO` stub for each one that is missing. A heading whose body starts with `TODO` counts as missing, and the skill that needs it asks.

- Build & test
- Entry points
- Proof traps
- File layout
- Code roots
- Doc folders
- Planning docs
- Architecture doc
- Testing defaults

These are optional. Each has a default in the skill that reads it:

- Git
- Commit groups
- Test passes

## Handoff brief

State the outcome, a check that can pass or fail, what the agent may do on its own, and when to stop. A span of time is not a check.

```text
Goal: <outcome>
Finished: <check that passes or fails>
Without asking: <what the agent may do on its own>
Stuck: <dead end>. Stop and write why.
```
