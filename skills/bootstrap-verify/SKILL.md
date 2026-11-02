---
name: bootstrap-verify
description: >-
  Writes a repo's verify skill: how to build it, run it, and check it the
  way a user would, then proves that skill once. Use when the user asks to
  set up verification or add a verify skill.
disable-model-invocation: true
---

# Bootstrap Verify

Run in the target repo. Write `.agents/skills/verify-<app>/SKILL.md`. Do not edit product code. Name `<app>` from the product, in kebab-case.

Symlink `.claude/skills/verify-<app>` -> ../../.agents/skills/verify-<app>. If that link is already the relative target, leave it. Otherwise unlink it without following it, or remove a real file or directory at that path, then create that one link. After the new folder is written, remove a leftover `.cursor/skills/verify-<app>`.

## Learn

Read `AGENTS.md` (`Build & test`, `Entry points`), the README, the run scripts, and any harness already in the repo. Ask only what those do not say: which surface a user actually touches, and how you can tell the app is ready.

If it does not build or start, stop and say so. Do not patch the app so the proof can pass.

## Write

Frontmatter `name: verify-<app>`. The description names the app, the surface, and when to run it. Keep the file short.

- **Build.** The repo's build command.
- **Launch.** The repo's run command, from the state a new user gets, and the readiness signal. Ready means usable, not merely running. Say how to stop it.
- **Check.** One read-only health check.
- **Drive.** The main user paths, with this repo's real commands and selectors. Do not invent handles.
- **Evidence.** For a path, the action and the state it left. A user path, not a test-only endpoint. Write captures under `evidence/` next to the skill. Add that folder to the repo's `.gitignore` unless `git check-ignore` already says it is ignored.
- **Cleanup.** Kill only what this run started. Leave the evidence.
- **Features.** The top few user-facing features: what it is, how to reach it, how to drive it, and the end state a user can see. Keep the list in this file, or in `features.md` beside it when the list would bury the steps.

End with one line: upkeep is shrekstack's maintain-verify skill.

## Prove

The skill is a draft until the `.claude/skills/verify-<app>` link resolves to the real folder, and this passes once, followed as written:

1. Build.
2. Launch and see the readiness signal.
3. Run the health check.
4. Drive one feature the way a user would.
5. Capture the evidence.
6. Clean up. The evidence is still there, `git status` does not show it, and nothing you started is still running.

Name any setup step you stood in for. If a step fails, fix the skill and rerun that step. Do not weaken the path to make it pass.
