# shrekstack

This is my swamp!

Agents act like the Three Blind Mice when they can’t see what’s true. Plans get scattered, the docs and code disagree, and nobody remembers the why. Slop piles up over time, and agents get slower and make more mistakes.

Shrekstack keeps order in the swamp while your agents build it. It gives every fact one home and keeps it current:

- **Single source of truth.** Goals, backlog, shipped work, decisions and architecture each live in their own doc, kept up to date by agents.
- **Docs match the code.** Preventing drift becomes a core part of the agents responsibility.
- **Proven work.** Agents test the app like a user and clean up after themsleves.

You make the product calls. Agents do the busywork.

To get started, install the plugin and run `/bootstrap-repo`.

## Skills

Once per repo:

- [bootstrap-repo](skills/bootstrap-repo/SKILL.md) installs the [base rule](skills/bootstrap-repo/base.md) and [response style](skills/bootstrap-repo/style.md), folds every agent file into a lean root `AGENTS.md` and one per area, moves every skill into `.agents/skills/`, drafts the headings the skills read from the code, runs doc-steward for the planning docs, and links it all for Claude Code, Cursor, or both.
- [bootstrap-verify](skills/bootstrap-verify/SKILL.md) writes the repo's verify skill and proves it once.
- [bootstrap-ui](skills/bootstrap-ui/SKILL.md) writes the repo's UI conventions skill.

Day to day:

- [ship-it](skills/ship-it/SKILL.md) gets a change ready for a pull request by running the five below, in this order.
- [tidy](skills/tidy/SKILL.md) cleans up the work just finished.
- [blast-radius](skills/blast-radius/SKILL.md) finds what a change could break and proves it is safe.
- [doc-steward](skills/doc-steward/SKILL.md) keeps the planning docs in shape.
- [commit-group](skills/commit-group/SKILL.md) turns a messy working tree into logical commits.
- [doc-sync](skills/doc-sync/SKILL.md) fixes docs that no longer match the code.

Now and then:

- [untangle](skills/untangle/SKILL.md) restructures code so what changes together sits together, then runs prune-code and prune-tests.
- [prune-code](skills/prune-code/SKILL.md) removes dead code after proof.
- [prune-tests](skills/prune-tests/SKILL.md) removes tests that no longer lock a live rule.
- [maintain-verify](skills/maintain-verify/SKILL.md) updates the verify skill after the code changes.
