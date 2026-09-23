# Validation contract template

Use with [state contract](state-contract.md), not as a second form-state owner. Bracketed slots are unresolved by design. Copy one field/group record per meaningful validation boundary.

## Form policy

Form ID/revision: [value]. Rule authority: [schema/API/domain paths + versions]. Approval/decision IDs: [values]. Feedback timing profile: [INTERACTIVE or SUBMIT-FIRST, deliberate D09 selection]. Submission policy: [enabled reveal-without-invalid-mutation or explained disabled-until-valid; D09]. Single error renderer: [native/library/custom owner]. Enter/composition/button path: [handler semantics]. Focus after unsuccessful submit: [summary/first applicable error/exact alternative]. Announcement: [exact template, priority, deduplication]. While remote check pending/unavailable: [D10]. Draft/edit/final/step/Back/Cancel validation scopes: [definitions].

| Field/group property | Contract |
|---|---|
| ID, label, owner | [stable field/group ID and domain authority] |
| Status | [required/optional/conditional with exact predicate] |
| Accepted values | [types, enumeration/range/length, units and inclusivity; authority evidence, no invented limits] |
| Normalisation | [display versus canonical value, whether reversible, Unicode/whitespace/case rules supplied by authority] |
| Dependencies | [values/versions that change applicability or accepted values] |
| Checking trigger | [computation events, composition handling, debounce only if resolved] |
| Feedback trigger | [selected timing profile; touched/submitted/imported review distinctions] |
| Remote check | [service contract, key including dependencies, advisory/required, freshness, timeout, pending/outage/submit handling] |
| Message and placement | [exact local/remote/group copy, stable error association and summary mapping] |
| Error priority | [deterministic order and reasons; prerequisite handling; warning effect] |
| Clearing/correction | [rule-passed condition, obsolete remote invalidation, next evidence state, no clearing on focus/time] |
| Preservation | [failed submit/Back/reload/conditional hide; serialisation; storage/privacy/lifetime] |
| Responsibilities | [client precheck versus server independent enforcement, authorization and final acceptance] |
| State mapping | [incomplete/invalid/warning/local pass/checking/rejected/unavailable/review IDs where applicable] |
| Acceptance | [untouched, partial, bounds, corrected, paste/autofill/IME, dependent change, late response, outage, server rejection and recovery IDs] |

Do not present a field as valid solely because it is untouched. No checked value may inherit a previous value's remote evidence. For server errors that cannot be safely mapped to a field, define form-level placement and recovery rather than guessing a field.
