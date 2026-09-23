# Worked example: concurrent capacity reservation

This is a fictional, framework-neutral example, not a product default or an executed database test. Relevant rules: DOM-01, DB-02, TX-01 through TX-05, BV-01 through BV-03. The project supplies actual engine semantics, capacity limits, expiry and permission policy.

## Contract and existing journey

A tenant-owned resource has a canonical available capacity. A reserve operation consumes a positive requested quantity and creates a reservation linked to that resource and tenant. A reservation ID identifies the business record; a caller operation key identifies one logical submission. The manual UI and import API use the same use case. The invariant is that accepted reservations cannot consume more capacity than available, and one logical submission cannot create two reservations.

An unsafe implementation reads available capacity, compares it in application code, then inserts a reservation and decrements capacity with an unguarded write. A and B can both read one remaining slot, both pass validation and both commit. This is a source-level race hypothesis. Before reporting a defect, inspect storage constraints, transaction isolation and the actual update predicate; an existing atomic guard may close the window.

## A bounded repair direction

One possible design, if supported by the actual database, atomically updates capacity only when the remaining value is sufficient, checks affected-row count and creates the reservation in the same transaction. A scoped uniqueness mechanism coordinates the logical operation key with the durable result. This is not a prescription for every storage model; another verified concurrency mechanism may satisfy the invariant.

The domain owns reservation eligibility, lifecycle locks and units. Boundary validation rejects malformed quantity; final atomic enforcement protects competing writers. Failure before commit rolls back both mutations. Response loss after commit leaves a reservation that can be retrieved/replayed using the same logical operation identity. A changed payload under the same key is an explicit conflict, not permission to silently create another reservation.

If a remote notification is required, decide whether its intent must be durable with the reservation. Do not send the notification inside a blindly retried transaction and assume rollback unsends it. Reuse the existing durable publication mechanism if one exists; a new outbox is justified only by the actual failure contract.

## Acceptance and positive controls

Use a barrier to make two distinct submissions compete for one remaining slot. Assert one accepted reservation, the correct remaining capacity, no orphan row and a meaningful conflict/insufficient-capacity outcome. Repeat the same key concurrently and assert the adopted single-operation effect. Use the same key in another tenant to verify correct scope, and a new key for a legitimate later reservation to ensure deduplication is not overly broad.

Inject response loss after commit, then retry with the original key and reconcile the existing result. Inject a transaction failure before commit and prove both local writes are absent. Verify reload, list totals and any export read canonical values. A mocked repository test can validate orchestration but cannot establish the database's atomic-update or isolation behavior.

If the inspected code already uses an atomic conditional update, correct affected-row handling and one transaction, the review should credit those protections. Lack of a distributed lock is not a defect. The smallest remaining question might concern operation-key expiry or the notification crash window rather than capacity safety.
