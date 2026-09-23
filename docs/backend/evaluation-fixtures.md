# Raw fixtures for bounded skill evaluation

These fictional snippets are evaluator inputs, not production code or recommended implementations. They contain no secrets and require no network/database setup. Expected observations are in [evaluations](evaluations.md), separate from these raw artifacts. Do not provide the expected-answer column to an independent evaluator. Source inspection is the authorized scope unless a case explicitly supplies an isolated runtime.

## Fixture A: inventory reservation

Project contract: tenant-owned inventory cannot go below zero. Each distinct reservation reduces available quantity and creates one canonical reservation. The supplied repository has no additional triggers, constraints, locks or helper behavior beyond the shown query implementation. The request has already passed an existing tenant permission guard.

```text
reserve(tenant, item, quantity):
    current = db.query("select available from inventory where tenant=? and id=?", tenant, item)
    if current.available < quantity: return InsufficientCapacity
    db.execute("update inventory set available=available-? where tenant=? and id=?", quantity, tenant, item)
    db.execute("insert into reservations(tenant,item,quantity) values(?,?,?)", tenant, item, quantity)
    return Accepted
```

Input to evaluator: review read-only for the stated invariant, distinguish source evidence and runtime hypotheses, and propose the smallest confirming check. No database engine/version or transaction wrapper is supplied.

## Fixture B: guarded reservation

Same business contract. The data adapter's `transaction` uses one real connection and rolls back both operations on failure. `execute` returns affected-row count. The selected engine supports an atomic conditional update with the shown predicate; quantity has been validated positive. There are no remote effects in this use case. Capacity and reservation writes are the only affected canonical mutations.

```text
reserve(tenant, item, quantity):
    transaction:
        changed = db.execute("update inventory set available=available-? where tenant=? and id=? and available>=?", quantity, tenant, item, quantity)
        if changed != 1: return InsufficientCapacity
        reservation = db.insert_reservation(tenant, item, quantity)
    return Accepted(reservation.id)
```

Input to evaluator: review read-only for capacity integrity. The task does not request duplicate-submission guarantees or a new architecture. State what the supplied adapter contract establishes and which runtime evidence remains unavailable.

## Fixture C: test setup failure

Production adapter supports `begin_transaction`, `execute`, `commit` and `rollback`. The service uses that interface. A unit-test fake implements `execute` only. The test runner fails during setup with “FakeDatabase has no attribute begin_transaction”; no business assertion executes.

Input to evaluator: assess this failure during a no-change review, classify the evidence and recommend the smallest next step. Do not edit the service or fixture.

## Fixture D: unknown provider outcome

A provider operation can create a remote asset. The request reaches the provider, which may commit before a network timeout. The supplied provider contract offers no idempotency key, no lookup by caller operation ID and no proven safe repeat. The application catches timeout and immediately retries three times, then reports “Nothing was created.” The task authorizes specification and source review only.

Input to evaluator: identify the contract gap and safe recovery boundaries without inventing provider capabilities or deploying a change.

## Fixture E: small protocol correction

An existing endpoint has a documented response header whose spelling is wrong in one serializer constant. The repository already has a schema test for that header. No business meaning, storage, authorization, middleware order or consumers beyond the contract test change. The user asks for the spelling fix using current conventions.

Input to evaluator: describe the proportional implementation route and verification. Do not require a new migration, outbox, service hierarchy or full product specification.

## Fixture F: paired document access

Project policy: workspace documents are private. An authenticated principal may read or edit a document only while an active member of its enabled workspace. This policy applies to HTTP and internal callers. The storage adapter has no implicit authorization or global query filter beyond the shown code. Existing helpers and SQL parameters work as stated.

```text
read_document(principal, id):
    document = store.find(id)
    if document is absent or not may_access(principal, document.workspace): return HiddenNotFound
    return project(document)

update_document(principal, id, title):
    require_authenticated(principal)
    document = store.find(id)
    if document is absent: return HiddenNotFound
    document.title = title
    store.save(document)
    audit.document_updated(document.id, principal.id)
    return Updated
```

Input to evaluator: review this supplied snippet read-only against the stated policy. Identify necessary allowed/denied controls and evidence limits. No real repository or runtime is supplied.

## Fixture G: deliberately different read and write permissions

Project policy: a published workspace document has a public summary. Editing its body is limited to its owner while the workspace is enabled and the document unlocked. The shared `authorized_update` helper checks the authenticated principal, owner, enabled workspace and unlocked record inside the same transaction as the update. A denial produces HiddenNotFound with no write or audit event. Both HTTP and internal callers use this helper.

```text
read_public_summary(id):
    return store.published_summary(id)

update_document(principal, id, body):
    return authorized_update(principal, id, body)
```

Input to evaluator: review the supplied contract and snippets without making changes. Report any demonstrated policy mismatch and distinguish source/contract reasoning from runtime proof.

## Fixture H: incomplete bulk-approval brief

User request: use backend-spec to define bulk document approval for an existing workspace product, without implementation. Team leads should select record IDs and see outcomes in both web and mobile clients. The manual approval path already checks workspace authority and lifecycle locks, updates the canonical document approval state and appends an audit record. Exports and an existing webhook projection consume that state.

The brief does not specify whether a team lead can approve every workspace document, whether one invalid item rejects the whole batch, or what a caller sees after losing the response. No stack, database/provider versions, numeric limits or delivery guarantees are supplied. The existing manual path remains supported. Give a useful specification and identify decisions that need an owner; do not implement, choose a new stack or inspect unrelated repositories. Return the result inline.

## Fixture I: executable partial-update project

The [document-update fixture](fixtures/document-update/README.md) supplies a small Python/SQLite project and its existing tests. Copy it to a disposable directory before implementation; the source fixture is deliberately defective and must remain unchanged for reproducible trials. Local in-memory SQLite writes and tests in that copy are authorized. No network, dependency installation or application repository mutation is part of the trial.

## Fixture J: pure serializer repair

Use backend-build. The supplied snippet and contract are the entire fictional project. Fix this serializer inline and verify it. The established response contract has exactly id and retryable; id must be preserved, retryable is a JSON boolean. Input code is always a trusted string. Exactly 'busy' and 'timeout' are retryable; every other string is not. This pure projection is called by an already-authorized request path and changes no persistence, transport status or retry mechanism.

```python
def error_response(error_id, code):
    return {'id': error_id, 'retryable': code in ('busy')}
```

Return the smallest corrected implementation and evidence, with no new architecture. No file editing, repository discovery or package installation. Isolated standard-library Python assertions through stdin with bytecode disabled are authorized; no project files or external calls.

## Fixture K: optional response warnings

Use backend-spec. Write a compact contract delta for an existing list response. Current JSON is `{items:[{id:string}],nextCursor:string|null}`. Add optional `warnings:string[]` at the top level; omit it when empty and preserve item order, ids and nextCursor exactly. Warnings are non-sensitive informational messages supplied by the existing query service, never errors or status changes. Existing authentication, tenant-scoped query, persistence and pagination behavior are unchanged. The web and mobile callers' documented contract ignores unknown top-level fields; no other consumers or generated clients exist in this fixture. The query service owns warning text; the serializer projects it. No middleware/storage change is requested. Specify behavior and focused acceptance checks inline; do not implement.

The brief is the entire fictional project. No repository discovery, edits, runtime or network operations.

## Fixture L: short receipt worker

Use backend-verify. Review this short receipt worker. Queue can redeliver until ack. Provider send may accept a receipt email then time out before replying; provider offers no documented dedupe or outcome lookup. Manual sending uses the same provider. Product has not decided whether possible duplicate receipt email or missed receipt is preferable.

```text
on_message(message):
    try:
        provider.send_receipt(message.order_id)
    except Timeout:
        queue.retry(message)
        return
    queue.ack(message)
```

No database, other guard or hidden middleware is present. Provide a bounded review and smallest safe next step. The supplied artifacts are the entire fictional system. No repository discovery, edits, runtime or network operations.

For a reading-cost trial of J–L, give only the selected raw fixture and the named installed skill, not this entire fixture collection or expected answers. Ask the evaluator to report every skill/library file actually read, whole-file versus section/line reads, rereads, guidance that changed a decision and guidance adding no value. Ask for actual executed checks where authorized. Tell the evaluator to follow the skill as written rather than optimize reading to please the evaluator. Use independent agents without earlier trial results for each revision; compare observable correctness as well as reading volume.
