# Backend acceptance and evidence ledger

Use proportionally for specification, implementation or review. Governed by BV-01 through BV-08. A small change may keep this record inline; a cross-layer feature needs explicit coverage of every affected owner/consumer. Do not fill absent evidence with inferred passes.

## Scope and environment

Record requested outcome, authorized actions, repository/revision, working-tree state, contract/rule revisions, fixture/data provenance, exact stack/engine/provider versions and environment. Separate local source, deployed artifact, provider configuration and business acceptance. List inaccessible sources and consumers early.

| Assertion / contract IDs | Producer/mutation/consumer | Setup and data | Deterministic action/failure | Expected canonical and caller-visible result | Actual evidence / command / exit | Basis | Status |
|---|---|---|---|---|---|---|---|
| Concrete meaningful behavior | Include real boundary | Positive/negative fixture | Include controlled interleaving if needed | Storage, relationships, outputs and recovery | State what actually ran | Source / executed / hypothesis | VERIFIED / FAILED / NOT VERIFIED / NOT APPLICABLE with reason |

## Applicable coverage

Consider creation, editing, reload, search/filter/pagination, missing/invalid data, ambiguity, duplicate and simultaneous request, unknown outcome, retries, reduced input, deletion/reassignment, default/override, maximum supported children, approved/locked state, permission change and legacy records. Include API/middleware, selected real database/transactions, jobs/providers, derived state, UI, documents/drawings, exports and integrations where affected. Exclude unreachable cases with a reason rather than creating unused features.

For migrations, include supported old/new application combinations, representative data, lock/runtime behavior, interrupted backfill, concurrent edits and actual recovery evidence. For caches, include update/delete/revoke, failed refresh, hot-key contention and old entries after deployment. For async work, include durable acceptance, duplicate/out-of-order delivery, acknowledgement loss, exhaustion and shutdown.

## Failure attribution

| Command failure | Did setup complete? | Did intended assertion execute? | Product mismatch or fixture/environment issue? | Evidence limit | Smallest next check |
|---|---|---|---|---|---|
| Exact command and exit | Record actual stage | Yes/no/unknown | Keep unresolved if evidence is insufficient | Which claim remains unverified | Reproduce without weakening contract |

A test double lacking a real provider method is not evidence that production lacks it. A missing database service does not establish a failed business invariant. An assertion mismatch still requires checking the expected value against the authoritative contract. No-change review permits proposing fixture repairs without making them.

## Findings and positive controls

For each finding record priority/consequence, adopted requirement versus advice, exact source, observed fact, inferred runtime effect/preconditions, evidence basis/status and minimal confirmation or repair. Credit existing constraints, guards and correct cases. Do not require a defect count or label unfamiliar architecture wrong without a concrete violated responsibility.

## Completion and cleanup

Report implemented, tested, deployed and accepted independently. List required unverified writers/consumers and the practical next validation step; do not claim platform-wide parity while they remain open. Check diff/index, lockfiles, generated output, environment/config changes and user edits. Remove only task-owned temporary data/artifacts, stop task-started processes and identify deliberately retained evidence or unresolved cleanup. A complete review report can truthfully contain unverified runtime assertions.
