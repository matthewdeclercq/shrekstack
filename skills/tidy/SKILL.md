---
name: tidy
description: After a task is done, check the work just finished for anything to clean up or simplify. Use when the user asks "anything to clean up?", "can we simplify this?", or types /tidy.
---

# Tidy

Look only at what this task changed, not the whole codebase.

1. Find the change: uncommitted edits and new files. If the work is already committed, use the commits since this branch split from the default branch (`origin/HEAD`).
2. Look for:
   - Dead code: unused functions, parameters, imports, or leftovers from earlier tries.
   - Debris: debug prints, temp files, scratch scripts, TODOs added this session.
   - Comments that repeat the code or describe the change.
   - Repeats: new code that copies a helper that already exists.
   - Over-building: options, layers, or settings that nothing uses yet.
   - Comments the change made untrue. Docs are [doc-sync](../doc-sync/SKILL.md)'s.
   - Tests this task added that overlap or check nothing real.
3. Do not flag lint, format, or dead-code issues a pre-commit hook already enforces. The project's own rules (`AGENTS.md`, its skills) win over this list.
4. Fix everything you find without asking first. Never invent findings.
5. Run the project's build and tests. Leave lint and format to its hooks.
6. Report what you fixed as a short list, most important first: one line each with the file, the line and the change. If nothing was worth changing, say so.
