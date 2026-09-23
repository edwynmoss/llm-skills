---
name: backend-spec
description: Define backend API, domain, middleware, persistence, concurrency and recovery contracts before implementation. Use for backend specifications and contract gap analysis; exclude implementation-only requests, frontend-only work and unrelated infrastructure administration.
---

# Backend specification

Resolve the shared library using `BACKEND_DOCS_ROOT` when configured; otherwise read `library-root.txt` beside this installed SKILL.md. For an uninstalled repository package only, use `../../docs/backend` relative to this file. Require `governance.md` at the selected absolute root. Report a broken configured/installed path rather than silently switching libraries. References below are relative to that root. Keep the standards in their maintained library; a consuming project owns its concrete contracts.

Read `governance.md`, then every module activated by its applicability router. Read `modules/verification.md` when defining acceptance. Missing authority blocks dependent decisions, not independent investigation. Do not load all modules for a small change or invent a full specification ceremony where an existing contract can be inherited.

1. Inspect supplied instructions, implementation, framework/database/provider versions, tests and manual/automated journeys. When only a brief or fictional fixture is supplied, follow the artifact boundary in `governance.md` and leave unavailable runtime/repository facts explicit. Otherwise establish source revision. Distinguish source observation, deployed configuration and product decisions.
2. Identify canonical entities, stable IDs, writers, consumers, derived values, authorization and lifecycle locks. Load `templates/service-contract.md` when its structure is needed; keep small deltas inline under governance's template-reading rule. A UI projection, request DTO or event payload does not independently own a business fact.
3. Route affected concerns through governance; load `gap-analysis.md` when a coverage investigation needs its concern matrix. Specify request/error semantics, middleware ordering, persistence constraints, transaction boundaries, contention and known/unknown outcomes where affected. Load `templates/request-pipeline.md`, `templates/data-contract.md` and `templates/mutation-recovery.md` when those working artifacts are needed.
4. Use `templates/migration-plan.md` for schema/data evolution and `templates/dependency-contract.md` for external calls, jobs or delivery guarantees. Keep numeric limits, consistency tolerances, retention and recovery objectives unresolved unless an authoritative project decision supplies them; record these through `decisions.md`.
5. Define observable assertions for affected behavior: negative cases, simultaneous requests, partial failure, retries, existing data, supported deployment overlap and affected UI/export/integration consumers. Load `templates/acceptance.md` when a structured ledger is needed. Name the real boundaries required and unavailable evidence.
6. Deliver resolved contracts, outstanding decisions, a bounded implementation scope and verification plan. For a narrow task, provide only the affected delta and inherited contract references.

This skill produces specifications; it does not authorize application edits, migrations, live queries, seeding, load tests, dependency installation, hook activation or deployment. Backend and UI work must use the same project-owned API and business semantics. Mentioning another skill does not invoke it. Do not manufacture an API, database or architecture for an empty workspace.
