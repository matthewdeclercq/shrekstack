---
name: ship-it
description: >-
  Gets the agent's own change ready for a pull request: tidy, blast radius, an
  adversarial pass, a planning-doc audit, doc-sync, then logical commits. Use
  when the user types /ship-it.
disable-model-invocation: true
---

# Ship it

Run every step that changes a file before committing, with doc-sync last of them, once the code is final, so each commit carries its own doc fixes. Lint and format belong to the repo's hooks, which run on each commit. Ship-it reports to the user; it does not push or write the PR description.

1. **Skip check.** Read `git status --short`, `git diff --stat`, and `git log`. When the change is only comments, formatting, a lockfile, generated files, or markdown that is not a skill, a rule, or a doc `.agents/doc-map.md` names, commit it (step 7) and go straight to the note. If an earlier ship-it this session covered part of the branch, check only what is new since the commit it ended on.
2. **Tidy.** Run [tidy](../tidy/SKILL.md), before anything is committed, so debris never lands. Do not repeat its checks.
3. **Blast radius.** Run [blast-radius](../blast-radius/SKILL.md).
4. **Adversarial pass.** Read the diff once for bugs, logic errors, and edge cases. Fix what you find. If a fix can change the safety fact, prove it again. Delete any scratch script this step wrote, or keep it as a test.
5. **Planning docs.** If the change touches a doc `.agents/doc-map.md` names, run [doc-steward](../doc-steward/SKILL.md)'s Audit and fix what it finds.
6. **Doc sync.** Run [doc-sync](../doc-sync/SKILL.md) on the final code. It leaves its fixes uncommitted.
7. **Commit.** Run [commit-group](../commit-group/SKILL.md). Fixes from the steps above go into the batch they belong to, not a batch of their own. A doc-sync fix for drift this change did not cause goes in one batch of its own. Nothing to commit: carry on.
8. **Note**, below.

## Note

A few lines, no banners:

- If you skipped, why.
- What tidy, the planning-doc audit, and doc-sync fixed, or that nothing needed it.
- What blast radius found, the safety fact, how far it was proven, and the proof.
- What the adversarial pass caught and fixed.
- What was checked and cleared.
- The commits made, one line each. No hooks ran: say so in one line.
- If this work showed a shrekstack skill was wrong or missing something, or improved a repo skill shrekstack also has: a `shrekstack candidate` line saying what and why, without the repo-specific details.
- End with the commit the note covers: `Shipped through <full sha>`. Uncommitted work left behind (a suspected secret, a path `Git` excludes): name it.
