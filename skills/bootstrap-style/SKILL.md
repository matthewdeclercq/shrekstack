---
name: bootstrap-style
description: >-
  Installs the shrekstack response style in the user's own settings, so it
  applies to every repo they open and to nobody else. Use when the user asks
  to install the response style or run bootstrap-style.
disable-model-invocation: true
---

# Bootstrap Style

Run once per machine. Ask once which tools to set up: Claude Code, Cursor, or both. Never write the style into a repo.

- **Claude Code:** copy [`style.md`](style.md), unchanged, to `~/.claude/rules/style.md`. When a file is already there and differs, show the difference and ask before replacing it.
- **Cursor:** its user rules live in Cursor Settings, not a file. Print `style.md` in a code block and tell the user to paste it into Cursor Settings → Rules → User Rules, replacing an older copy.

Report what was written or what the user needs to paste, in a line each.
