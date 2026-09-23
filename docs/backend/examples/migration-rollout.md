# Worked example: replacing a stored business field safely

Fictional example, not a generated migration or a claim of zero downtime. Relevant rules: BGV-02, DB-01, MIG-01 through MIG-08 and OPS-08.

A service stores a combined address string and needs structured address fields. Existing UI, import, export and background dispatch still read/write the combined field. Historical records vary in format, and some cannot be parsed unambiguously. New application instances will overlap with old instances during deployment.

## Decisions before source generation

The domain owner decides whether the original string remains source evidence, whether structured fields become authoritative, and how ambiguous records are corrected. The skill cannot invent an address parser's business correctness or silently split every string by commas. Identify all writers and readers, including scheduled dispatch and rollback images. Define what old code does when new fields exist and what new code does when they remain unresolved.

One possible phased design adds compatible nullable fields and a resolution state, populates only unambiguous records using a versioned transformation, updates writers through the canonical use case, switches readers after required coverage, then considers retiring the old representation. This is an example of a plan, not a mandatory architecture. If a simpler compatible field addition satisfies the product need, use it.

During overlap, define precedence and concurrent-edit behavior. A backfill must not overwrite a user's newer corrected address with a value parsed from an old string. A conditional version check or equivalent guard can identify that conflict. Ambiguous rows remain visible for resolution; a count of processed rows must not classify them as complete.

## Rehearsal and recovery

Inspect the exact engine operation for locks, validation scans and rewrite behavior. Rehearse representative legacy records, long values, nulls, ambiguous formats and concurrent edits. Test old reader/new writer and new reader/old writer combinations that the rollout actually supports. Include export and dispatch, not just the primary UI.

Stop the backfill after a committed batch and before its acknowledgement, then resume. Assert stable traversal, correct checkpoint and no duplicate or skipped work. Test a record edited between read and update. Reconcile counts by category: resolved, unchanged, conflicted, ambiguous and failed. Do not mark command exit zero as semantic completion.

An application rollback may still need the old field; a destructive down migration cannot recover user-entered structured details unless an explicit recovery source exists. Define forward repair and restore evidence before contraction. Keep historical source evidence according to the approved retention policy. Production execution remains a separate authorized operation with measured gates and live readback.

This example is complete as a teaching contract. It is not evidence that any particular database migration, parser or production journey has passed.
