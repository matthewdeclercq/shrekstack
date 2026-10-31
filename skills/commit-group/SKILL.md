---
name: commit-group
description: >-
  Groups unstaged changes into logical git commits and commits them automatically.
  Use when the user asks to commit-group, group commits, split unstaged changes,
  or organize a messy working tree into commits.
disable-model-invocation: true
---

# Commit Group

Turn a messy **unstaged** working tree into **logical commits** — inventory, plan batches, then **commit all batches in order** without waiting for approval.

Read the target repo's `AGENTS.md` before planning. Use these headings (any heading level, text after the hashes exactly as written):

| Heading | What it holds | If it is missing or empty |
|---------|----------------|---------------------------|
| Git | Commit-message rules beyond this skill, and paths that must never be committed | Use the commit-message rules in this skill. Ask before excluding any path that is not in the secret list below |
| `Commit groups` | What stays together, what splits apart, default excludes, a default separate batch, and batch order | Ask. Do not guess a grouping, a separate batch, or an order |
| `Build & test` | Lint and test commands for optional validation | Do not guess a command. Ask when the user asked to validate. A missing section does not block the commits |

## Modes

| User says | Action |
|-----------|--------|
| `commit-group` / `group my commits` | Inventory → plan → **commit all batches** |
| `commit all` | Same as above |
| `commit batch N` / `commit 1` | Stage and commit **only** batch N (re-inventory if needed) |
| `plan only` / `revise` | Inventory + batch plan only — **do not commit** |

If anything is already staged (`git diff --cached` non-empty), unstage first (`git restore --staged .`) unless the user explicitly asked to include staged changes.

---

## Phase 1 — Inventory

Run in parallel:

```bash
git status --short
git diff --stat
git diff
git ls-files --others --exclude-standard
```

Also skim `git log -5 --oneline` for message style.

**Never stage or commit during inventory alone** (unless the user invoked `commit batch N` and inventory is just a quick refresh).

---

## Phase 2 — Plan batches

Group by **one logical change** (buildable/reviewable slice), not by file type alone.

Apply what `Commit groups` says to keep together, split apart, exclude, and break out as a default separate batch. Do not copy a grouping from another repo.

**Partial files:** if one file mixes unrelated edits, keep one batch and note it in the summary — do not block on approval.

### Always exclude (never stage/commit)

- `.env`, credentials, API keys, `*.pem`, `*.p12`

Also exclude every path the Git heading says never to commit. If that heading is missing, ask before assuming any further excludes. Still apply the list above.

### Commit messages

Per the Git heading when that section exists. Otherwise:

- Complete sentences; focus on **why**, not a file list
- One logical change per commit
- No conventional-prefix requirement unless the repo already uses them in recent history

Keep batches to **2–8** when possible; merge tiny related edits, split unrelated work.

---

## Phase 3 — Commit (default)

Unless the user said `plan only` or `revise`, **immediately** commit every planned batch **in order**:

1. Briefly show the batch plan (titles + draft messages — no approval gate)
2. For each batch, **sequentially**:
   - `git add -- <exact paths for this batch only>` — never `git add -A` or `git add .`
   - `git diff --cached --stat` — confirm scope matches the batch
   - Commit via HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
Message here.

EOF
)"
```

3. After the last batch: `git status --short` and a summary table of commits created

Stop on pre-commit hook failure; fix or report; **new commit**, do not amend a failed commit.

### Git safety (non-negotiable)

- **Never** `git config`, force push, hard reset, or `--no-verify` unless the user explicitly asks
- **Never** amend unless: user asked, HEAD is your commit this session, and not pushed
- **Never** commit secrets — if suspected, stop and flag instead of committing
- Do not push unless the user asks

### Optional validation

After a batch that touches code, offer the lint and test commands in `Build & test`, and run them if the user asked. Run the targeted command when a batch is clearly scoped to one area that section names; skip the full suite unless the user requests. If `Build & test` is missing, ask when the user asked to validate, and do not guess a command. Do not block the commits on that question.

---

## Judgment calls

Use sensible defaults — do not pause for approval:

- One file with mixed stories → one batch, mention in summary
- Suspected secrets → stop and flag; commit everything else only after user confirms

Ask for these. Do not guess them:

- Batch ordering → the order `Commit groups` gives. If it gives none, ask
- A default separate batch → only the one `Commit groups` names, included automatically. If it names none, ask; do not invent one

When the tree is empty, say so — do not create empty commits.
