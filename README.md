# shrekstack

Matthew's personal shared skills library for Claude Code, Cursor, and his Grok bots. Skills live in `skills/<name>/SKILL.md`. The shared base rule is [skills/bootstrap-base/base.md](skills/bootstrap-base/base.md).

## Skills

- [commit-group](skills/commit-group/SKILL.md) turns an unstaged tree into logical commits and commits them.
- [code-cleanup](skills/code-cleanup/SKILL.md) removes dead code after proof, without a style refactor.
- [test-cleanup](skills/test-cleanup/SKILL.md) prunes tests that no longer lock a live rule.
- [doc-steward](skills/doc-steward/SKILL.md) keeps the planning docs in shape: which doc owns which fact, goals, decisions, and shipping.
- [doc-sync](skills/doc-sync/SKILL.md) fixes doc drift against the code and commits `Doc sync.`
- [tidy](skills/tidy/SKILL.md) checks the work just finished for anything to clean up or simplify.
- [review](skills/review/SKILL.md) reviews the agent's own change before a pull request, after tidy.
- [bootstrap-base](skills/bootstrap-base/SKILL.md) writes that base rule, the AGENTS.md headings skills read, and the CLAUDE.md link into the adopting repo.
- [bootstrap-verify](skills/bootstrap-verify/SKILL.md) writes a repo's verify skill and proves it once.
- [bootstrap-ui](skills/bootstrap-ui/SKILL.md) writes a repo's UI conventions skill and proves every path once.
- [maintain-verify](skills/maintain-verify/SKILL.md) brings that skill back in line after the code changes.

## Install

Install the plugin, so every repo gets the same skills and updates from this one. Skills then run as `/shrekstack:<name>`.

**Claude Code.**

```text
/plugin install shrekstack --marketplace matthewdeclercq/shrekstack
```

**Cursor and Grok bots.** Import this repo as a plugin from GitHub. `.cursor-plugin/` holds its manifest.

Then run [bootstrap-base](skills/bootstrap-base/SKILL.md) in each adopting repo to install the base rule and the AGENTS.md headings.

## AGENTS.md

Skills read these headings from the adopting repo's `AGENTS.md`. bootstrap-base writes a `TODO` stub for each one that is missing. A heading whose body starts with `TODO` counts as missing, and the skill that needs it asks.

- Build & test
- Entry points
- Proof traps
- File layout
- Code roots
- Doc folders
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
