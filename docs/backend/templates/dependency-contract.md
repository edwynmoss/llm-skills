# Provider, delivery and background-work contract

Use for external APIs/SDKs, broker work, webhooks, schedulers and object storage. Governed by INT-01 through INT-08 and JOB-01 through JOB-09. Record only applicable sections and actual dependencies.

## Identity and capability

Name provider/broker, exact API/client/version, environment/account, code/config owner, credential reference, canonical entity IDs and source evidence. Never include credential values. Record existing capability reused, required negative/recovery behavior, unsupported features and primary documentation checked. Official/popular status alone does not justify a dependency.

| Operation | Input/schema/version | Authentication and scope | Response/durable evidence | Error/unknown outcomes | Idempotency/lookup guarantees | Limits/pagination |
|---|---|---|---|---|---|---|
| Actual required operation | Required meaning, not only shape | User/service/provider identity | What acceptance/receipt proves | Distinguish before/after dispatch | Exact scope/lifetime or unknown | Continuation and partial coverage |

## Budget and retries

Record connect/read/overall deadlines, cancellation behavior, retry owner at every layer, eligible errors, maximum total work and adopted throttling/backoff. Include SDK defaults and queue redelivery in the analysis. Numeric limits must come from the project or measurement. A response timeout after possible dispatch needs reconciliation, not an assumed rollback.

## Durable delivery lifecycle

| Stage | Stable identity and payload | Durable owner | Acknowledgement meaning | Duplicate/order behavior | Crash/recovery owner | Permission semantics |
|---|---|---|---|---|---|---|
| Producer/queue/consumer/effect/receipt | Separate operation, event and attempt IDs | Existing DB/broker/workflow | Accepted versus completed | Scope, sequence and stale-event policy | Retry, quarantine or reconciliation | Acceptance-time/execution-time delegation |

Map DB commit/publication gaps, acknowledgement loss, lease expiry and process shutdown. Describe an existing outbox/durable workflow only if present or justified by the actual failure window. Do not promise system-wide exactly-once effects from broker delivery terminology.

## Mapping, files and partial evidence

Map provider statuses, errors, IDs, units and time semantics to canonical application meaning. Unknown critical fields must not silently become success. For paginated reads, record complete/incomplete coverage separately from returned records; removal reconciliation needs an adopted complete-source or tombstone contract.

For files, define staging, checksum/type/size validation, metadata commit, publication, URL/access expiry and cleanup. For webhooks, define raw-body verification, event identity, durable acceptance and unknown-entity handling. Authenticity and business deduplication are different checks.

## Recovery and acceptance

Specify dependency outage/degradation, known rejection, unknown outcome, delayed completion, poison work, exhausted retry and authorized replay. Name the operator/owner and safe next action. Reuse existing ledgers, routes and producers.

Test normal success, malformed/missing fields, changed schema, interrupted pagination, rate limits, response loss, duplicate/out-of-order delivery and shutdown as relevant. Record which guarantees were actually exercised against a real authorized provider/broker and which remain documentary or mocked evidence. Link [acceptance](acceptance.md).
