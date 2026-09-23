# Mutation, concurrency and recovery contract

Use for writes, duplicate requests, transactions, remote effects, jobs and unknown outcomes. Governed by TX-01 through TX-09. Do not select a mechanism until the forbidden state and competing writers are explicit.

## Intent and invariant

Record logical operation, canonical entity/operation identity, tenant/principal scope, business preconditions, lifecycle locks and all writers. Define the invariant in business terms, then provide a concrete forbidden interleaving. Name the existing guard if one already closes that interleaving.

| Boundary/step | Durable state before | Effect attempted | Success evidence | Failure/unknown possibilities | Atomicity/owner | Next safe action |
|---|---|---|---|---|---|---|
| Actual local or remote step | Include pending intent/receipt | Name exact mutation | Commit/receipt/version, not just returned future | Before dispatch, after dispatch, after commit | Connection/transaction/provider scope | Retry/reconcile/compensate/manual resolution |

## Contention mechanism

State constraint/conditional update/version/locking/isolation mechanism, exact engine support, conflict detection and outcome mapping. Define retryable failure classes, scope of repeated work, fresh reads, attempts/deadline owner and exhaustion behavior. List non-repeatable side effects that must not be blindly rerun. For leases, include renewal, expiry and stale-worker/fencing semantics.

## Idempotency lifecycle

| Concern | Adopted definition/evidence |
|---|---|
| Key scope | Caller/tenant, operation and identity owner |
| Request meaning | Canonical fingerprint and changed-payload behavior |
| Concurrent ownership | Atomic claim or existing equivalent |
| Durable record | How claim, mutation and result survive crashes |
| In-progress response | What duplicate callers may observe and do |
| Replay | Original result versus canonical reference, with current authorization |
| Retention/expiry | Business/operational owner and behavior after expiry |
| Uncertain outcome | Existing lookup/reconciliation, or explicit unresolved recovery |

Absence of these guarantees must remain a gap, not a promise generated from the presence of a request header. Distinguish a legitimate later operation from a duplicate attempt of the same operation.

## Outcome and transition table

Define only reachable domain states. For each state, record durable evidence, permitted actor/action, next transition, UI/API projection, retry eligibility and terminal condition. Distinguish rejected before effect, known rollback, known commit, externally pending and unknown. Search/filter/display state must not change business state.

## Deterministic acceptance

Cover two simultaneous distinct writes, simultaneous duplicate, same key with different payload, stale version, crash before/after commit, lost response, remote timeout, lease loss and retry exhaustion where applicable. Use controlled barriers/failure injection rather than arbitrary sleeps. Assert canonical state, versions, aggregate values, receipts, effect counts and caller outcomes.

Name which checks use real database/provider boundaries and which use doubles. Include a positive control for a legitimate second operation. Link all downstream UI, export, cache, document and job consumers through [acceptance](acceptance.md); missing evidence limits the completion claim.
