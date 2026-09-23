# Decision register

Library revision: 1.5-draft. Authoring the standard is authorised; product adoption of review defaults is not implied. Decision statuses are OPEN, PROPOSED, RESOLVED or SUPERSEDED, independent of requirement strength and evidence status. Each consuming project records decision owner, scope, alternatives, reason, dated authority, affected state/rule IDs, verification and revisit trigger.

| ID | Status / owner needed | Exact decision | Affected work | Independent work that can proceed |
|---|---|---|---|---|
| D01 | OPEN / product owner | Which users, tasks, platforms and exclusions define the pilot? | Feature scope and task success | Generic contracts and inspection |
| D02 | OPEN / domain owner | Canonical entities, stable IDs, field authorities and every affected consumer? | Mutations, derived status, parity claims | Producer/consumer inventory |
| D03 | OPEN / design owner | Which token source, aliases/tiers, components/variants, supported themes/modes and reference govern; who approves missing tokens or exceptions? | Component styling, shared token changes and migration | Semantics, boundary and token-consumer inspection |
| D04 | OPEN / accessibility owner | Which WCAG version/level or platform standard, browsers, AT and input support? | Release/conformance claim | Identify applicable checks; WCAG 2.2 AA is a proposal, not presumed target |
| D05 | OPEN / API owner | What confirms commit/non-commit, supports lookup, retry/idempotency and cancellation? | Pending, unknown outcome, Undo, recovery | Enumerate uncertainty; never promise safe repeat |
| D06 | OPEN / domain/API owner | How are record-version conflicts resolved across actors and tabs? | Concurrent edits/optimism | Version evidence and no-overwrite scenarios |
| D07 | OPEN / data owner | What may be retained, where, how long, under which identity, and in evidence? | Drafts, cache, logs, screenshots, logout clearing | No new persistence or real sensitive test data |
| D08 | OPEN / product owner | Which navigation/history/restoration and leave-pending policies apply? | Back, reload, tab close, resume | Trace existing route semantics |
| D09 | PROPOSED / form owner | Select interactive or submit-first feedback; review enabled-submit default versus explained disabled-until-valid | Form feedback/submit controls | Specify both alternatives; no silent choice |
| D10 | OPEN / service owner | Is remote check advisory or a prerequisite; freshness, timeout and Submit-while-checking policy? | Remote field states | Bind results to all dependencies |
| D11 | OPEN / domain owner | Accepted values, units, bounds, normalisation, conditional and legacy repair/save rules? | Validation logic | Capture authority and missing rules |
| D12 | OPEN / workflow owner | Selection universe, partial-success reporting and retry subset? | Bulk operations only | Selection identity model |
| D13 | OPEN / import owner | Merge, replace, clear, duplicate, conflict and re-import identity semantics? | Upload/import only | Separate transfer and processing |
| D14 | OPEN / domain owner | Date-only, local time or instant; timezone, ambiguous/nonexistent time handling and units? | Date/time workflows | Representation inventory |
| D15 | OPEN / service/product owners | Freshness tolerance, rate-limit handling, retry budget and tested performance conditions? | Refresh, reconnect, timeout and performance acceptance | Real elapsed/progress reporting |
| D16 | PARTIALLY RESOLVED / tooling owner | Is a measured manual check reliable/useful enough for a specific supported hook? | Revision 1.6 explicitly authorizes advisory library-health and package-integrity hooks; see [scope and bounds](hooks.md) | Application checks and Stop remain unadopted; independent manual/CI validation remains available |
| D17 | PROPOSED / maintainer | Adopt library additions and review defaults in a named pilot; who owns later revisions? | General policy rollout | Static validation and evaluation design |
| D18 | OPEN / product/research owner | Which research question, users, task boundaries, correct outcome, assistance/recovery measures, baseline and success criteria apply? | Usability claims and any authorised measurement/research | Define observable assertions; no recruitment or telemetry implied |
| D19 | OPEN / product/platform owner | What must remain usable when scripts, third-party resources, storage or browser capabilities fail; what fallback is actually supported? | Frontend resilience only when relevant | Dependency/failure inventory; preserve existing architecture |
| D20 | OPEN / service/support owner | Which assistance channel, availability, context-transfer permission, ownership and return path actually exist? | Human support handoff only when needed | Record current support limitations without fictional service promises |
| D21 | OPEN / product/domain/AI owner | What does AI output mean, what evidence supports it, who controls edits and actions, and which review/authority boundary applies? | User-facing AI features only | Describe uncertainty and inspect canonical validation; no AI feature automatically added |

U9 authorises incorporation of the discussed routing, component/token and research refinements into the package. It does not close D03 or D18-D21 for an unspecified application. None of these OPEN decisions blocks independent authoring of reusable rules.

## Conflict procedure

Keep each statement and source separate. Example: transcript recommendation = disabled-until-valid; library candidate = enabled Submit that reveals errors but sends no invalid mutation. These are alternatives, not compatible settings to merge. Actual transcript is unavailable here. A project decision must name one submission policy and one feedback timing profile. Existing verified project behaviour can justify a scoped override; it is not automatically good behaviour. Escalate unresolved accessibility, data loss or authorisation conflicts and continue unaffected work.

Override record: `OVR-ID; rule ID/revision; scope; original policy; chosen behaviour; reason; decision authority/date; constraints that still apply; acceptance evidence/status; expiry or revisit trigger`. An override cannot waive higher-priority instructions, authoritative server rules or a selected normative accessibility target. Only resolved decisions close implementation blockers; elapsed time and a drafted recommendation do not constitute approval.
