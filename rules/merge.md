---
description: Which changes may auto-merge, and which wait for the owner.
alwaysApply: true
---

# Merge

Low-risk changes may auto-merge: docs, skills, rules, internal scripts, and tests. A change is low-risk only when every part of it is.

Required checks may not be enforced by the host (for example, no branch protection), so the agent confirms they are green before merging; that review-step check is the gate.

Anything else needs the owner. So does anything that deploys, touches release or app-store config, billing, secrets or auth, deletes data, or that review flags. An edit to this file needs the owner.

## Repo paths

The repo's own copy of this file wins. Paths listed here need the owner.
