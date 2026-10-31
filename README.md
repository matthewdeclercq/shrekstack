# shrekstack

Matthew's personal shared skills library for Claude Code, Cursor, and his Grok bots. Skills live in `skills/<name>/SKILL.md`. The shared base rule is [skills/setup-base/base.md](skills/setup-base/base.md).

[rules/merge.md](rules/merge.md) says which changes may auto-merge.

## Skills

- [commit-group](skills/commit-group/SKILL.md) turns an unstaged tree into logical commits and commits them.
- [code-cleanup](skills/code-cleanup/SKILL.md) removes dead code after proof, without a style refactor.
- [test-cleanup](skills/test-cleanup/SKILL.md) prunes tests that no longer lock a live rule.
- [doc-steward](skills/doc-steward/SKILL.md) writes the map of which doc owns which fact, and records a decision change.
- [doc-sync](skills/doc-sync/SKILL.md) fixes doc drift against the code and commits `Doc sync.`
- [tidy](skills/tidy/SKILL.md) checks the work just finished for anything to clean up or simplify.
- [review](skills/review/SKILL.md) reviews the agent's own change before a pull request, after tidy.
- [setup-base](skills/setup-base/SKILL.md) writes that base rule into the adopting repo.
- [setup-verify](skills/setup-verify/SKILL.md) writes a repo's verify skill and proves it once.
- [setup-ui](skills/setup-ui/SKILL.md) writes a repo's UI conventions skill and proves every path once.
- [maintain-verify](skills/maintain-verify/SKILL.md) brings that skill back in line after the code changes.

## Install

Copy is the default. Copy each `skills/<name>/` directory into the tool's skills directory. Run [setup-base](skills/setup-base/SKILL.md) in the adopting repo to install the base rule for Cursor and Claude Code.

**Cursor.** Copy into `.cursor/skills/<name>/` in the adopting repo. A Cloud Agent loads project skills from that repo. This repo also ships `.cursor-plugin/marketplace.json` and `.cursor-plugin/plugin.json` for import from GitHub.

Bump `version` in `.cursor-plugin/plugin.json` whenever skills change, because Cursor and Claude Code cache by version to detect updates.

**Claude Code.** Copy into `.claude/skills/<name>/`.

**Grok bots.** Copy into the bot project's `skills/` directory. The base text goes into each bot's own instructions.

## AGENTS.md

Each adopting repo's `AGENTS.md` needs these headings:

- Git
- Commit groups
- Build & test
- Entry points
- Proof traps
- File layout
- Doc folders
- Architecture doc
- Skills due
- Architecture due
- Testing defaults
- Test passes
- Code roots
- Planning docs
