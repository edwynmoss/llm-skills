---
name: backend-build
description: Implement or repair backend APIs, middleware, domain workflows, database access, jobs and integrations using existing architecture and resolved contracts. Use for scoped backend coding and refactoring; exclude specification-only, verification-only and frontend-only requests.
---

# Backend implementation

Resolve the shared library using `BACKEND_DOCS_ROOT` when configured; otherwise read `library-root.txt` beside this installed SKILL.md. For an uninstalled repository package only, use `../../docs/backend` relative to this file. Require `governance.md` at the selected absolute root. Report a broken configured/installed path rather than silently switching libraries. All references below are relative to that root.

Read `governance.md`, `modules/domain-architecture.md` and `modules/verification.md`, then every other module activated by the task. The library is general; reuse the project's actual framework, storage model, contracts and tooling. A missing standalone spec calls for the smallest relevant contract delta, not an invented product or a compulsory redesign.

1. Inspect code, callers, current edits, deployment assumptions and tests before changing anything. Map the canonical owner and every affected writer/consumer; load `templates/service-contract.md` when its structure is needed. Keep small deltas inline under governance's template-reading rule. Preserve existing manual and automated journeys.
2. If consequential project choices remain unresolved, load `decisions.md`. Do not invent authorization policy, idempotency, ordering, isolation, retention, timeout or provider guarantees. Continue work that does not depend on the missing decision.
3. Name changed layers/files and the simplest implementation. Reuse existing native/framework capabilities, clients, validators, transaction handling and observability. Add an abstraction only for a demonstrated variation or integration boundary; name any GoF pattern and its concrete benefit.
4. Keep request handlers and middleware focused; put business invariants and workflows with their established owner. Persist facts through the existing data boundary and reconcile derived state. Instantiate `templates/data-contract.md` and `templates/mutation-recovery.md` where storage or effects change.
5. For migrations, use `templates/migration-plan.md` before generating files. Creating a reviewed migration file and running it against a database are separate operations. For remote effects or background delivery, use `templates/dependency-contract.md`. Never turn a local transaction retry into an unreviewed repeat of a remote effect.
6. Run proportionate tests through actual authorized boundaries and record assertions, outcomes and limits; load `templates/acceptance.md` when a structured ledger is needed. Database behavior requires the selected engine/version where material; mocks and in-memory substitutes alone cannot prove isolation, DDL or query behavior. Verify affected UI, exports, jobs and integrations for cross-layer completion claims.
7. Inspect the diff and working tree, clean task-owned artifacts, stop task-started processes and preserve concurrent work. Report implemented, executed, deployed and outstanding scope separately.

Outputs are a scoped implementation and evidence. No automatic production mutation, backfill, provider activation, package upgrade, hook activation or deployment follows from loading this skill. Stop only dependent work where authority or safe test scope is missing; never weaken invariants to obtain a passing test.
