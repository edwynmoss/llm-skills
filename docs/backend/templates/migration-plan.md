# Migration and data rollout plan

Use before generating schema/data evolution source. Governed by MIG-01 through MIG-08. This template does not authorize execution against a database. State source-file authoring, isolated rehearsal, production application and destructive cleanup permissions separately, honoring existing session authorization.

## Decision and affected truth

Record confirmed model change, canonical fields/entities, reason, current schema and data evidence, target schema/meaning, exact engine/version and all writers/readers. Include background jobs, imports, exports, admin tools, cached projections and rollback application versions. Identify legacy nulls, duplicates, orphan relationships, ambiguous identities and historical snapshots.

## Compatibility phases

| Phase | Schema/data state | Supported readers/writers | Authoritative representation | Action/artifact | Preconditions and gate | Recovery/forward fix |
|---|---|---|---|---|---|---|
| Actual phase, not a required checklist step | Expansion/population/adoption/contraction as needed | Old/new app and async payload versions | Explicit precedence during overlap | Reviewed migration/backfill/config | Evidence needed to continue | What can actually be restored |

Do not add dual writes unless necessary; if used, define consistency and reconciliation. A new field is not authoritative merely because it exists. Do not remove the old representation while an active consumer still depends on it.

## Operational effect

Specify lock level/waits, scans/rewrite, transaction rules, index build behavior, replication/storage impact, estimated duration from rehearsal, timeout/abort controls and partial artifacts. Use exact versioned engine guidance. Record representative workload and what the rehearsal cannot establish about production scale.

## Backfill and conflict handling

| Selection/checkpoint | Canonical source and transform | Batch transaction | Concurrent-edit guard | Retry/rerun semantics | Progress and unresolved rows |
|---|---|---|---|---|---|
| Stable boundary/order, committed high-water mark | Versioned calculation and identity | Exact atomic unit | Preserve newer writes | Convergent update or explicit conflict | Scanned/changed/skipped/conflicted/failed |

Define interruption after read, after writes, after commit and before checkpoint acknowledgement. A partial result must not be reported complete. Ambiguous identity requires resolution; neither newest timestamp nor name similarity chooses a winner by default. Reduced/removed inputs must reconcile old dependent state.

## Destruction and recovery

List irreversible facts, backup/restore scope, restore rehearsal, recovery objectives, permission boundary and decision owner. Application rollback, down migration and data recovery are separate. State what a down migration cannot reconstruct. Prefer a supported forward repair when rollback would discard new valid data.

## Acceptance and cleanup

Assert old/new supported journeys, legacy upgrade, create/edit/reload, constraints, concurrent writes, pause/resume, invalid input, derived projections and every affected output. Record exact schema/data state after each authorized phase. Applied DDL alone is not rollout acceptance.

Retain intentional migration source and approved evidence. Remove failed generated experiments and disposable fixtures only when task-owned. Do not rewrite historical migrations, seed production data or delete old records merely to produce a clean test run. Link final status and unresolved consumers in [acceptance](acceptance.md).
