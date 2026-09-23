# State contract template

Copy into a consuming project's feature specification, not into the shared library. This template is intentionally unresolved. Every bracketed slot needs a real value, a linked decision blocker, or a reasoned NOT APPLICABLE before implementation. A state catalogue entry alone is not a contract. Apply STATE-01 through STATE-07 as relevant.

## Feature envelope

- Feature ID / contract revision / owner / scope: [values].
- Task and canonical entity IDs: [values and actual authority paths].
- Inspected code, design, API versions, project rules: [evidence].
- Rule applicability and exclusions: [IDs/reasons].
- Requirement strength / approval status / source: [separate values].
- Approved component and token mappings: [real names/paths/revisions].
- Supported locale, viewport/input/AT and performance conditions: [resolved matrix or D04/D15].
- Content axis / action axis / validation axis: [states; no combined catch-all status].
- Producer/consumer matrix: [GOV-03 table or justified narrow scope].

## Component and token ownership (when affected)

Use existing project paths/names; do not create every listed layer. A small change can inherit this mapping by exact contract/reference revision and record only the changed row. Architectural choices follow CAP-06/CAP-07; styling follows VIS-07 through VIS-09.

| UI responsibility | Existing component/path or justified extraction | Props/events/variant contract | State/domain/integration owner | Identity, focus and lifecycle behaviour | Evidence / open decision |
|---|---|---|---|---|---|
| [page/feature/section/component/primitive as actually present] | [reuse/compose/extract and reason] | [valid combinations; controlled owner] | [single authoritative owner] | [preserve or intentional reset] | [test/decision ID] |

| Styled property / semantic purpose | Consuming component/state/variant | Approved token and definition path | Alias/source lineage | Supported theme/mode mapping | Runtime value or exception | Rendered acceptance |
|---|---|---|---|---|---|---|
| [e.g. error text; use actual role name] | [affected states including combinations] | [actual project token, not illustrative name] | [existing tiers; no forced new architecture] | [actual modes, no invented theme] | [none, justified dynamic quantity, or override] | [contrast/focus/readability/layout evidence] |

Shared-token changes: [list affected consumers and migration/verification, including any not traced]. Missing tokens/aliases: [D03 decision, alternatives and dependent work]. Simple unchanged markup remains local unless responsibility/reuse justifies extraction. No blanket inline-style or utility-class prohibition is implied.

Conditional supplements: [D18 outcome/comprehension plan when journey changes; D19 frontend-resource fallback; D20 real assistance handoff; D21 AI evidence, user-edit ownership and action authority]. Include only applicable fields; unresolved decisions stay visible.

## Named base contract, if used

Base ID/revision: [real definition in this spec or resolvable link]. List fields supplied by this base. Every child explicitly names the base and overrides; no “standard behaviour”, implicit global inheritance or circular bases. Expand effective values during review. Missing base values remain unresolved in every child.

## State record (repeat per applicable state)

| Property | Required definition |
|---|---|
| Identity | [stable state ID, meaning, similar states explicitly excluded] |
| Nature | [read/write; certainty; recoverability; blocking scope; data freshness] |
| Ownership | [application/page/section/component/field/action; canonical versus projected data] |
| Entry | [event, guard, entity/user context, request/form/dependency/record revision] |
| Presentation | [component anatomy, placement, exact text/template and interpolation source; tokens; alternative layouts] |
| Actions | [available and unavailable actions, reasons, keyboard activation, pending duplicate guard] |
| Data | [preserve/clear/restore; authoritative update; storage owner, lifetime and privacy limits] |
| Time | [start/progression/dismissal/timeout/retry/recovery; factual progress; no assumed server cancellation] |
| Access and context | [focus entry/exit/fallback; keyboard; names/error associations; announcements; motion; responsive and locale details] |
| Concurrency | [compatible states, scoped precedence, latest-result keys, out-of-order handling, identity/access change, cleanup] |
| Transitions | [table below: events/guards/effects/next/forbidden; terminal and unmount behaviour] |
| Verification | [deterministic setup, controlled response order, assertions, evidence IDs and status] |
| Exceptions / blockers | [scope, reason, decision/override ID, authority and verification; none if resolved] |

| From | Event | Guard/revision | Side effects | Next state(s) | Forbidden transition / why | Test/evidence |
|---|---|---|---|---|---|---|
| [ID] | [user/system event] | [condition] | [canonical mutation/projection/announcement] | [content/action/validation IDs] | [excluded target] | [acceptance ID] |

Review question: can an implementer choose where the error goes, what Retry means, when data disappears, what a late response does, or where focus returns without noticing an open decision? If yes, the contract is not resolved.
