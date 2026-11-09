---
name: untangle
description: >-
  Restructures code so pieces that change together sit together, pieces that
  don't are not tied, and special cases follow from the design. Use for a
  structural refactor of an area or the whole repo. Ends by running
  prune-code and prune-tests on the same scope.
disable-model-invocation: true
argument-hint: "[area or concern to focus on]"
---

# Untangle

Ask one question of the code: **should these pieces change together?** Fix every place it answers wrong, without changing intended behavior. A typical change should land in one place.

`AGENTS.md` headings, and `Proof traps` in the `AGENTS.md` of each area in scope too; when one is missing, ask rather than guess:

- `File layout`: the areas to scope and fan out on.
- `Build & test`: the baseline, and the check after each fix.
- `Entry points` and `Proof traps`: code reached by name, which a move or rename breaks without a compile error.

## What to look for

- **Hidden links:** pieces that must change together, where the code doesn't show it. Copied logic or values; a module reading a global or file another one sets; one feature split across layer folders; a call order or convention callers just have to know.
- **Needless links:** pieces tied together that change for different reasons. Callers reaching into internals; stable code importing something more volatile; a general function with a parameter only one caller understands; a shallow module whose interface moves with its internals.
- **Surplus:** pieces with no reason of their own to change. Pass-through wrappers; extension points and config for things that never vary.
- **Special cases:** an `if` for one value, a parameter for one caller, a swallowed exception, a retry or sleep, a disabled test. Each is a requirement the design never accounted for. Use them to work out what the design needs; do not fix them one by one.

Dead code and tests that check nothing wait for step 7. Note them in the log as you find them; do not delete them before then.

## Loop

1. **Scope.** The area or concern given, or ask. The whole repo only when the owner asks for it. Say when you will stop.
2. **Baseline.** Run `Build & test`. Note anything already failing.
3. **List.** Change nothing yet. Write every problem from the list above into the log, each with its file:line.
4. **Redesign.** Work out the fixes as if today's requirements had been known from the start. Look for the one fix behind several problems; it often looks nothing like them. Check each fix against the question: pieces that change together end up together, pieces that don't aren't tied, and everything depends on what changes less. Write each fix above the problems it solves.
5. **Fix, one at a time.** Make one fix, remove the special cases it makes unnecessary, and keep the ones the system still needs. Run `Build & test`. Run [blast-radius](../blast-radius/SKILL.md) when the fix moves a public contract, crosses areas, or touches a proof trap. Mark the fix `done` or `deferred` with why.
6. **Recheck.** Launch read-only explorers, one per `File layout` area in scope, to look for what is left. Paste the question and the list above into each prompt. Add what they find, and go back to step 4 until nothing left is worth fixing.
7. **Prune.** Run [prune-code](../prune-code/SKILL.md), then [prune-tests](../prune-tests/SKILL.md), on the same scope, giving each the log's notes as its first candidates. Tests go last: they are the safety net for every step before.

Defer new dependencies, persistence or wire format changes, and product-scope changes to the owner. A bug the redesign fixes on the way is fine; do not go looking for others. When a fix changes a module, edge, or flow the architecture doc draws, follow [doc-steward](../doc-steward/SKILL.md).

## Tools

- **Skeleton:** script away function bodies so the whole scope fits in context.
- **Import graph:** script one that shows what imports what, and rerun it after each fix.
- **Git history:** what changes together, and how often each piece changes.

## Log

Keep it in a scratch file, so compaction loses nothing.

```markdown
- [done] Make the general `Dialog` give focus back to whatever had it before it opened.
  - `ui/LogoutDialog.tsx:30` waits 100ms after closing so the message input can take focus.
  - `ui/SettingsDialog.tsx:61` sets a global `skipRefocus` flag to stop the logout dialog stealing focus.
- [deferred: changes the stored order format] Define a `PaymentProvider` that Stripe and PayPal both implement.
  - `checkout/submit.ts:9` depends directly on `payments/stripe.ts`.
  - `refunds/refund.ts:22` wraps every Stripe call in `if (order.provider === "paypal")`.
```

## Done when

- As few special cases are left as possible. How many remain is the best measure of how close you are.
- Imports point toward code that changes less, and each exception left is in the log with why.
- The explorers find nothing worth fixing.
- prune-code and prune-tests have run on the scope.
- `Build & test` passes, and intended behavior matches the baseline, apart from bugs a fix removed.

## Report

Scope; each fix done, with the problems it removed; special cases left, and why each stays; what was deferred, and why; what prune-code and prune-tests removed; validation; and residue.

Adapted from [untangle-codebase](https://github.com/caldoai/skills/blob/main/skills/untangle-codebase/SKILL.md) (MIT, © 2026 Maze).
