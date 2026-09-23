# Request, middleware and protocol contract

Use when routing, parsing, identity, filters, errors or request lifetime change. Governed by API-01 through API-09 and MID-01 through MID-08. Inspect the framework's actual registration and execution model; the order below is a table to fill, not a prescribed sequence.

## Boundary definition

Record protocol/operation/version, caller types, gateway/proxy boundary, trusted identity sources, credential transport, request schema, response schema and compatibility obligations. Define absent/null/empty/default semantics, field permissions, normalization, limits and units. Link canonical business validation rather than copying competing rules into a transport-specific schema.

| Outcome condition | Handler/use case reached? | State/effect possible? | Status/code/headers/body | Safe caller recovery | Evidence |
|---|---|---|---|---|---|
| Success or reachable failure | Name exact boundary | No effect, committed, pending or unknown | Stable public semantics | Correct/retry/reconcile/stop as adopted | Named assertion |

Cover validation, authentication, authorization, not-found/existence disclosure, optimistic conflict, domain lock, admission limit, dependency failure, disconnect and unexpected fault where reachable. Distinguish accepted durable work from completed work. Do not require every operation to implement every outcome.

## Actual pipeline

| Stage/registration path | Order and scope | Required context/input | Produced context or transformation | Short-circuit/exception behavior | Cleanup/response unwind | Bypass routes |
|---|---|---|---|---|---|---|
| Actual framework stage | Include nested groups/gateway | Principal/raw bytes/metadata/deadline | State exact ownership | Who sees failure? | After success/error/disconnect | Deliberate public/preflight/stream paths |

Record how trusted proxy information is established; how identity and tenant reach queries/jobs; whether raw-body signatures precede transformations; who maps errors; and when response headers/streaming commit. Explain any stage that intentionally runs before authentication and its bounded resource/disclosure behavior.

## Resource and context lifetime

Name request-scoped and singleton dependencies, context propagation mechanism, pool/session cleanup and detached work. A background envelope should contain explicit durable identity, not a captured request object. Define cancellation propagation, overall deadline, retry owner and what a disconnect means after a possible commit.

For streams/files, specify buffering, content validation, partial delivery, publication, expiry and cleanup. For limits, cite the project decision and whether scope is user, tenant, endpoint or shared resource. Do not choose numeric defaults from this template.

## Verification

Record expected stage trace for a valid request and each meaningful rejection/error path. Assert that denied requests do not execute prohibited effects, and that valid requests still succeed. Include missing route, public exception, preflight, cross-tenant ID, oversized body, altered signature, thrown error and disconnect when applicable. Verify status/headers/body and final resource state together.

State whether tests exercise the real host pipeline or only isolated middleware functions. A unit test of one filter cannot prove global registration or a gateway's behavior. Link missing real-boundary evidence in [acceptance](acceptance.md).
