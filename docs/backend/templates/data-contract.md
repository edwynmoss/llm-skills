# Data ownership, schema and projection contract

Use for persisted fields, relationships, queries, cache lineage and storage semantics. Governed by DB-01 through DB-09, CACHE-01 through CACHE-08 and the project-owned business model. Fill only affected facts; inherit unchanged schema contracts explicitly.

## Storage context

Record engine/version, driver/ORM version, deployment topology, primary/replica routing, execution role, pool/session behavior and inspected schema revision. Distinguish observed settings from assumptions. Name the authoritative owner for the business entity and any alternative writers.

| Field/relationship | Canonical meaning and stable ID | Representation/precision/units | Null/default/override/snapshot semantics | Validation/constraint owner | Writers and permissions | Readers/derived consumers |
|---|---|---|---|---|---|---|
| Actual affected fact | One authoritative meaning | Include time/calendar or rounding where relevant | Absence differs from zero/false | Boundary/domain/storage each named | Include jobs/import/admin | UI, export, document, integration, cache |

## Invariant and relationship enforcement

| Invariant | Participating records and scope | All competing writers | Storage constraint or atomic mechanism | Application feedback/mapping | Legacy violations and reconciliation | Real-engine assertion |
|---|---|---|---|---|---|---|
| Forbidden business state | Include tenant/lifecycle scope | Do not stop at the API | Exact supported mechanism | Preserve useful error semantics | No guessed identity winner | Controlled competing/invalid write |

Document parent/child cardinality, tenant matching, reassignment, cascading/restriction, soft/hard deletion and source evidence. Define whether removed input clears, archives, detaches or deletes each dependent. Retention policy and historical snapshots need an authoritative decision.

## Query and consistency contract

Name query source, generated query/projection, filters, authorization scope, ordering/tie-breaker, pagination and expected cardinality. Identify tracking/lazy-loading effects, connection/transaction lifetime and limits. Describe the actual workload/distribution used to assess query count, plan and resource cost.

State read-after-write requirements and which reads may use replicas or eventual projections. Do not treat a stale read as proof that a committed row does not exist. Describe how a caller observes pending projection or reconciles stale data when material to the task.

## Derived data and caches

| Projection/cache | Source facts and revision | Key/context dimensions | Refresh/invalidation owner | Commit/invalidation ordering | Failure/staleness policy | Consumer/recovery test |
|---|---|---|---|---|---|---|
| Actual materialized result | No competing owner | Tenant, permissions, query and version as needed | Name every mutation trigger | Define race window | Never infer unavailable means empty | Update/delete/revoke and failed refresh |

## Evolution and evidence

Link [migration plan](migration-plan.md) if schema or persisted meaning changes. Include legacy, null, duplicate, maximum-size, approved/locked, override/default and reduced-input cases as applicable. Verify exact numeric/time round trips and relationship completeness.

Record whether acceptance used the real engine/version. An in-memory substitute or a different SQL database can validate application mapping but leaves engine-specific constraints, collation, isolation, DDL and plans unverified. Capture that distinction in [acceptance](acceptance.md).
