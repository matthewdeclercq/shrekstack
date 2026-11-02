---
name: commit-group
description: >-
  Groups uncommitted changes into logical commits and commits them. Use when
  the user asks to commit-group, group commits, or split a messy working tree
  into commits.
disable-model-invocation: true
---

# Commit Group

Turn a messy working tree into logical commits, then commit them all in order without waiting for approval. If the user says `plan only`, stop after the plan.

Two optional `AGENTS.md` headings (a body that starts with `TODO` counts as missing):

- `Git`: commit-message rules, and paths never to commit.
- `Commit groups`: what stays together or splits, extra excludes, a batch that always goes alone, and batch order.

## Inventory

Run `git status --short`, `git diff`, and `git ls-files --others --exclude-standard`, and read `git log -5 --oneline` for message style. If something is already staged, unstage it (`git restore --staged .`) unless the user asked to include it. Nothing to commit: say so and stop.

## Plan

- One batch per logical change, something a reviewer can read on its own, not per file type. Usually 2–8 batches.
- Apply `Commit groups` when it exists. Otherwise order batches so each builds on the ones before, and break nothing out on its own.
- A file with unrelated edits stays in one batch; say so in the summary.
- Never commit `.env`, credentials, keys, `*.pem`, `*.p12`, or a path `Git` excludes. A suspected secret: stop and flag it, and commit the rest only after the user confirms.
- Messages follow `Git` and the base rule's Git section, with why over a file list. No conventional prefixes unless recent history uses them.

## Commit

Show the plan (titles and draft messages), then for each batch in order:

1. `git add -- <this batch's paths>`, never `-A` or `.`.
2. Check `git diff --cached --stat` matches the batch.
3. Commit, with the message in a heredoc.

A hook fails: fix it or report it, then make a new commit. Never `--no-verify`, never amend unless the user asks, and do not push unless asked.

End with `git status --short` and the commits made, one line each.
