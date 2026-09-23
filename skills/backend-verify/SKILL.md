---
name: backend-verify
description: Review backend source or verify API, middleware, database, authorization, concurrency and recovery behavior against project contracts. Use for read-only backend audits, regression review and authorized tests; exclude implementation-only requests, frontend-only reviews and unrelated operational audits.
---

# Backend verification

Resolve the shared library using `BACKEND_DOCS_ROOT` when configured; otherwise read `library-root.txt` beside this installed SKILL.md. For an uninstalled repository package only, use `../../docs/backend` relative to this file. Require `governance.md` at the selected absolute root. Report a broken configured/installed path instead of falling back silently. Reference paths below are relative to that root.

Read `governance.md` and `modules/verification.md`, then the modules activated by the inspected feature. Inspect actual contracts and code; generic preferences are not automatically adopted project requirements. An audit can conclude that existing behavior is correct. Missing runtime access limits claims, not the usefulness of a bounded source review.

1. Establish requested scope, repository identity, revision, working-tree changes and local policies when a repository is supplied. For snippets or fictional fixtures, use the supplied-artifact boundary in `governance.md`; do not inspect unrelated repositories. For an unspecified real-code pilot, choose one existing API-to-storage or message-to-storage journey and state its exclusions. Do not turn a pilot into an unrequested platform audit.
2. Trace request/producer through identity and permissions, middleware, use case, domain, storage, transaction and all affected projections/consumers. Load `templates/service-contract.md` when its structure is needed and `gap-analysis.md` when a coverage investigation needs its concern matrix. Keep small deltas inline under governance's template-reading rule. Inspect callees and shared safeguards before asserting a missing check.
3. Map actual requirements to assertions and evidence; load `templates/acceptance.md` when a structured ledger is needed. Inspect test/setup side effects before executing: commands named test, plan, explain or validate can write, lock, contact providers, restore packages or start services. A no-change review does not authorize those side effects.
4. Distinguish source facts, runtime hypotheses and executed assertions. Classify test setup failure separately from a product assertion failure. Exercise real authorized API/database/provider boundaries where requested and available; concurrent and failure cases must control ordering rather than rely on lucky timing.
5. Report actionable findings with requirement, exact source, triggering sequence, consequence, evidence status and smallest confirming/refuting check. Keep specification gaps, defects, unsupported assumptions and environment limits distinct. Credit unique constraints, transaction guards, authorization scopes and idempotency already present.
6. Propose the smallest repair without editing during a verification-only request. Clean only task-owned artifacts and test data; stop task-started processes. Preserve existing user changes and provider records.

Report completion means the review is finished, not that the application is approved for production. No automatic installation, database introspection, migration, replay, seeding, live load test, issue creation or infrastructure audit is implied. Never claim platform-wide parity while required writers or consumers remain unverified.
