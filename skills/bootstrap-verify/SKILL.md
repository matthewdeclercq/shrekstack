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

Link the new folder for each tool `Agent tools` in `AGENTS.md` names, with a relative symlink: `.claude/skills/verify-<app>` for Claude Code, `.cursor/skills/verify-<app>` for Cursor. Missing: run [bootstrap-repo](../bootstrap-repo/SKILL.md) first. A symlink already there is replaced. A real file or folder at either path may hold hand-written work: before writing, ask the user whether to move what it holds into `.agents/skills/verify-<app>/` and build on it, or start fresh. Do that, then remove the old copy and create the links.

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
- **Features.** A `features/` folder beside the skill: a `README.md` index with the baseline state every recipe starts from, and one file per user-facing feature, the main ones to start. Each says what the user sees, every way a user gets to it, how to drive it (preconditions, then each action with its exact command and the result to see), and its gotchas. A missing precondition is a failure, with its reason written down; never weaken the recipe to pass.

End with one line: upkeep is shrekstack's maintain-verify skill.

## Prove

The skill is a draft until each link resolves to the real folder, and this passes once, followed as written:

1. Build.
2. Launch and see the readiness signal.
3. Run the health check.
4. Drive one feature the way a user would.
5. Capture the evidence.
6. Clean up. The evidence is still there, `git status` does not show it, and nothing you started is still running.

Name any setup step you stood in for. If a step fails, fix the skill and rerun that step. Do not weaken the path to make it pass.
