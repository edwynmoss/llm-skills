# Service and end-to-end contract

Use for a new/changed journey or a material ownership gap. For a narrow change, record only its delta and links to inherited contracts. This template is intentionally unfilled; it is not an approved product specification. Governed by [governance](../governance.md), BGV-01 through BGV-06 and DOM-01 through DOM-08.

## Identity and scope

Record task, repository/remote, source revision, current edits, contract version, intended business outcome, initiating actor, authorized environment and explicit exclusions. Identify the existing manual journey and every alternative writer that must remain equivalent. Name actual framework, database, driver and provider versions only when observed; list missing version/configuration evidence.

Separate three kinds of authority: project decisions and acceptance; code/schema ownership; deployed configuration and provider guarantees. Link each rather than treating one as proof of the others. Keep secrets and raw private payloads out of this record.

## Producer and consumer matrix

| Entity/field/status and stable ID | Authoritative owner/storage | Input, derived, default, override or snapshot | Writers and mutation paths | Readers/projections/UI/documents/exports/integrations | Recompute/reconcile/clear/invalidate | Required evidence |
|---|---|---|---|---|---|---|
| Name actual fact | Name source and persistence | State effective-value rule | Include manual/API/import/job/admin | Name each affected consumer or unresolved risk | Include removed/reduced input and permission change | Link assertion/environment |

For each relationship, specify parent-to-child and child-to-parent navigation, canonical IDs, source evidence, cardinality, conflict/merge policy and deletion/reassignment behavior. Similar display names do not establish identity. Materialized projections need a named refresh owner and stale-state detection.

## Operation and lifecycle

| Operation/actor | Preconditions and permissions | Input meaning and validation owner | Atomic mutation/effect | Outcome and durable evidence | Recovery/retry/conflict | Consumer acceptance |
|---|---|---|---|---|---|---|
| Existing or requested action | Include tenant/object/field and lifecycle lock | Distinguish absent/null/empty/zero | Name transaction/remote boundaries | Accepted versus completed versus unknown | Identify safe next action | Include reload and required outputs |

Document business status meanings independently of transport status, parsing/linking progress and temporary UI state. Identify prohibited transitions and the common invariant owner used by all writers. State rounding/time/default inheritance rules only from adopted authority.

## Architecture and capability choice

Name affected presentation/protocol, application, domain, persistence and integration layers. Explain why each changes. Record existing services/validators/clients/transaction helpers reused. If proposing a package or GoF pattern, identify the actual missing capability/variation, alternatives, dependency/version evidence, cost and tested behavior. A simple function or composition can be the complete decision.

## Decisions and acceptance

Use [decisions](../decisions.md) for unresolved policy, with owner/options/consequences and exactly which work depends on it. Link [request pipeline](request-pipeline.md), [data contract](data-contract.md), [mutation/recovery](mutation-recovery.md), [migration plan](migration-plan.md) and [dependency contract](dependency-contract.md) only when applicable.

Finish with [acceptance](acceptance.md): changed invariants, real boundaries, representative positive/negative cases, evidence status and remaining consumers. Do not mark the system complete while a required projection or mutation path is merely assumed equivalent. Preserve a useful scoped report when a real environment is unavailable.
