# Backend contracts

Part of LLM Skills. Behavioral use has only been tested with Codex; other hosts are untested. Installation instructions below target Codex. Reuse through another assistant requires explicit source/reference access and separate validation; see the [host compatibility notes](../../README.md).

Revision **1.2-public.1**. A general-purpose counterpart to the UI/UX library: detailed contracts for APIs, domain logic, middleware, security, databases, concurrency, migrations, background work, integrations, caching/performance, operations and verification. Each consuming project supplies its actual architecture, business decisions and runtime guarantees. No framework, database, cloud, ORM or business integration is prescribed.

| Entry | Use it for | Result |
|---|---|---|
| [backend-spec](../../skills/backend-spec/SKILL.md) | Define behavior and discover consequential gaps before implementation | Owners, invariants, boundary/outcome contracts, decisions and acceptance |
| [backend-build](../../skills/backend-build/SKILL.md) | Implement or repair scoped backend behavior | Changes in existing semantic owners plus truthful verification |
| [backend-verify](../../skills/backend-verify/SKILL.md) | Read-only review or explicitly authorized runtime checks | Source facts, existing protections, actionable findings and unverified boundaries |

## Depth and structure

The entry skills stay compact; depth lives in the references. [Governance](governance.md) defines applicability, authority, strength, canonical ownership, proportional routes and completion. Each rule has a stable ID, activation condition, authority/reason, expected behavior, exceptions/dependencies and observable acceptance. Modules include procedural reasoning and failure/positive controls beyond their rule tables.

| Module | Main contracts |
|---|---|
| [API](modules/api-contracts.md) | Input meaning, partial updates, error/status semantics, pagination, evolution, streams and caller recovery |
| [Domain/architecture](modules/domain-architecture.md) | Canonical facts, use-case ownership, lifecycle, inheritance, identity and justified capability/pattern choices |
| [Middleware](modules/middleware.md) | Actual ordering, short circuits, identity/context lifetime, raw bodies, deadlines and cleanup |
| [Security/tenancy](modules/security-tenancy.md) | Operation/object/field access, tenant isolation across consumers, revocation, safe inputs and sensitive data |
| [Persistence](modules/persistence.md) | Schema meaning, constraints, relationships, ORM/query behavior, resource scope, replicas and representation |
| [Concurrency](modules/concurrency.md) | Atomicity, competing writes, retries, idempotency lifecycle, unknown outcomes, leases and compensation |
| [Migrations](modules/migrations.md) | Legacy data, old/new compatibility, DDL effects, resumable backfills, destructive changes and recovery |
| [Background work](modules/background-work.md) | Durable acceptance, acknowledgements, duplicates/order, publication gaps, timers, replay and shutdown |
| [Integrations](modules/integrations.md) | Provider capabilities, focused adapters, budgets, pagination, remote effects and degraded behavior |
| [Caching/performance](modules/caching-performance.md) | Projection lineage, context keys, invalidation, freshness, contention and measured resource budgets |
| [Operations](modules/operations.md) | Configuration ownership, safe telemetry, health/freshness, lifecycle, recovery and release evidence |
| [Verification](modules/verification.md) | Source versus execution, real-boundary coverage, deterministic races, failure attribution and no-change reviews |

Read only modules activated by the actual task. A typo fix does not need a migration plan; a shared status or permission change must trace every affected writer/consumer. The library supports detailed work without forcing every task through every template.

## Working artifacts

Seven templates cover [service ownership](templates/service-contract.md), [request pipeline](templates/request-pipeline.md), [data](templates/data-contract.md), [mutation/recovery](templates/mutation-recovery.md), [migration](templates/migration-plan.md), [dependencies](templates/dependency-contract.md) and [acceptance](templates/acceptance.md). Keep small deltas inline; load a template when its structure is needed rather than reading every linked working format. Applicable technical modules remain required in full, and migration/backfill generation still requires its explicit plan prerequisite.

Use [gap analysis](gap-analysis.md) to distinguish missing behavior, authority and evidence; [decisions](decisions.md) keeps project-specific limits and policies explicit; [sources](sources.md) bounds external guidance. Backend and UI work share the consuming project's API/domain truth rather than redefining statuses, validation or permissions in separate libraries.

Worked examples: [concurrent reservation](examples/concurrent-reservation.md), [duplicate webhook](examples/duplicate-webhook.md), [tenant cache](examples/tenant-cache.md), [migration rollout](examples/migration-rollout.md), and [correct read-only review](examples/read-only-review.md). They are fictional teaching material, not runtime evidence or project defaults. [Evaluation cases](evaluations.md) and [raw fixtures](evaluation-fixtures.md) support later behavioral testing with positive and negative controls.

## Install and validate

Run from a reviewed checkout of this standalone package with PowerShell 7:

```powershell
pwsh -File scripts/install-backend-context.ps1 -WhatIf
pwsh -File scripts/install-backend-context.ps1
```

The installer copies three entry files into the user .agents/skills directory, writes library-root.txt locators, sets BACKEND_DOCS_ROOT to this checkout's docs/backend and adds only the marked backend routing section to global AGENTS.md. It respects CODEX_HOME and accepts SkillsDirectory/CodexDirectory overrides. Existing differing entries require reviewed -UpdateSkills. No application copy, provider connection, hook activation, dependency installation or database operation is part of installation. Keep the checkout available; reopen Codex for hosts retaining older environment/skill snapshots.

UI and backend entry scripts share installation mechanics in scripts/install-development-context.ps1; they retain separate roots, names, environment variables and instruction markers. The shared checker likewise validates each library independently. This is a small reuse boundary for two real packages, not a generic plugin framework.

```powershell
python -I -B docs/backend/scripts/check-package.py
python -I -B scripts/test-skill-library.py
pwsh -File scripts/test-backend-context.ps1 -WorkDirectory $env:TEMP
```

The structural checker validates references, rule ownership/envelopes, decisions and the supported flat metadata subset. It does not prove skill selection or backend correctness. The context tests use disposable fixtures and process-only environment changes. [Validation report](validation-report.md) records actual evidence and limits; [adoption backlog](backlog.md) identifies further behavioral/runtime evaluation.

The public package retains supplied-artifact boundaries, recovery routing, evidence labels, paired authorization controls and conditional template reading. Fictional fixtures support future evaluation; see [validation evidence](validation-report.md) for checks actually run on this package.

The existing UI hooks remain UI-package checks. Backend hooks are deferred until an appropriate manual check and runtime trigger are adopted; migrations, seeds, replay and live provider calls must never become hidden hook side effects.
