# Worked example: duplicate and late provider events

Fictional source-review scenario. Relevant rules: MID-05, JOB-01 through JOB-06, INT-04, TX-05 and SEC-02. Provider behavior and identifiers below must be replaced by the actual integration contract in a real project.

A signed provider event reports a document-processing outcome. The local system records a canonical document ID, provider job ID, event ID and processing revision. Signature validation authenticates the bytes; it does not prove the event is new, ordered or permitted to select any local document. The provider can retry a delivery and may deliver an older progress event after a completion event.

## Trace the boundaries

The request pipeline preserves the provider-required raw body for signature verification, validates the parsed envelope, resolves the provider job to the correct tenant/document, then accepts durable work according to the adopted response contract. Unknown or ambiguous identity is recorded for resolution; display names do not select a document. A business status such as ready must derive from canonical validated output, not merely from receiving a signed event.

The consumer applies a guarded transition using the provider job/revision and canonical lifecycle. A duplicate completion must not add the same extracted children or aggregate twice. A late progress event must not move a completed newer revision backward. A distinct valid later processing job must remain possible; deduplication keyed only by document ID would incorrectly suppress it.

The acknowledgement boundary matters. Acknowledging before durable acceptance can lose an event on process crash. Applying an effect and crashing before recording receipt can repeat it. Use the existing transaction/durable-work design to coordinate transition and receipt, or explicitly document another mechanism with equivalent guarantees. A broker acknowledgement alone is not evidence that all output consumers have reconciled.

## Verification sequence

First deliver a valid event and assert correct canonical mapping and transition. Deliver the identical event twice concurrently and inspect final children, aggregate, receipt and visible status. Deliver an older event after completion and verify it is ignored or handled according to the adopted version policy. Then deliver a legitimate new job's event and verify it is not suppressed.

Inject failure after effect persistence but before acknowledgement; redelivery must converge without double application. Tamper with the raw body and expect authentication failure. Use a valid signature with an unknown provider job and expect unresolved identity rather than guessed matching. Use a colliding local identifier from another tenant and verify isolation.

For a source-only review, report which guards and durable boundaries are observed, then distinguish the unexecuted crash/reordering hypotheses. A correct receipt unique constraint and conditional lifecycle update deserve explicit credit. Do not recommend a second webhook importer or notification producer when the existing path can be repaired at its owner.
