# shrekstack

Matthew's shared skills for Claude Code, Cursor, and his Grok bots.

## Install

**Claude Code.**

```text
/plugin install shrekstack --marketplace matthewdeclercq/shrekstack
```

**Cursor and Grok bots.** Import this repo as a plugin from GitHub.

Then run bootstrap-repo in each repo. Skills run as `/shrekstack:<name>`.

## Skills

Once per repo:

- [bootstrap-repo](skills/bootstrap-repo/SKILL.md) installs the [base rule](skills/bootstrap-repo/base.md) and [response style](skills/bootstrap-repo/style.md), adds the `AGENTS.md` headings the skills read, and links `CLAUDE.md`.
- [bootstrap-verify](skills/bootstrap-verify/SKILL.md) writes the repo's verify skill and proves it once.
- [bootstrap-ui](skills/bootstrap-ui/SKILL.md) writes the repo's UI conventions skill.

Day to day:

- [tidy](skills/tidy/SKILL.md) cleans up the work just finished.
- [review](skills/review/SKILL.md) checks a change before a pull request.
- [commit-group](skills/commit-group/SKILL.md) turns a messy working tree into logical commits.
- [doc-sync](skills/doc-sync/SKILL.md) fixes docs that no longer match the code.
- [doc-steward](skills/doc-steward/SKILL.md) keeps the planning docs in shape.
- [prune-code](skills/prune-code/SKILL.md) removes dead code after proof.
- [prune-tests](skills/prune-tests/SKILL.md) removes tests that no longer lock a live rule.
- [maintain-verify](skills/maintain-verify/SKILL.md) updates the verify skill after the code changes.

## Writing skills

A script only one skill runs lives in that skill's `scripts/` folder. A script that mostly runs other tools is Bash; one that mostly parses text is Python 3.
