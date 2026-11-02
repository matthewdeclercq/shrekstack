---
name: setup-base
description: >-
  Writes the shared shrekstack base rule into a repo for Cursor and Claude
  Code, an AGENTS.md starter or its missing headings, a CLAUDE.md symlink,
  and starter hooks. Use when the user asks to install the base rule or run
  setup-base.
disable-model-invocation: true
---

# Setup Base

Run in the target repo. Do not edit product code. Run this skill's script by its path, with `--root` set to the target repo:

```bash
python3 "<skill>/scripts/setup_base.py" --root "<repo>"
```

The script does all the writing. Do not write or edit those files by hand, and do not guess a command or a tool it left as `TODO`.

- **Rule.** `base.md` beside this skill, written to the Cursor and Claude Code rule folders. Overwritten on every run.
- **AGENTS.md.** A starter when the file is missing: the first sentence of the README, the skills line, the build, test, and run commands it can detect, and a `TODO` stub for every heading shrekstack skills read. An existing file gains only the skills line and the missing headings. A symlink outside the repo, or anything that is not a file, is left alone.
- **CLAUDE.md.** A relative symlink to `AGENTS.md` when the path is empty. Anything already there is left alone.
- **Hooks.** A formatter, a linter, and a secrets check for the one stack it detects, in `.pre-commit-config.yaml`, or husky with lint-staged when the repo already depends on both. An existing hook install is left alone, and each missing kind is reported.

After a new `.pre-commit-config.yaml`, run `pre-commit autoupdate` when `pre-commit` is installed, so the pins are current.

## Report

Pass on every line the script prints. Then list the `TODO` headings and commands in `AGENTS.md` and ask the owner to fill them in: shrekstack skills treat a `TODO` heading as missing and stop to ask.

If the script exits 2, report its message and stop.
