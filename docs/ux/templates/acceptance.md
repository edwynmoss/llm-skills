# Acceptance and evidence ledger

Feature/contract/library revision: [values]. Implementation commit or file snapshot: [value]. Environment, date, tester, browser/device/AT, dataset and network: [values]. Safe test account and evidence retention: [values]. Expected behaviour is derived from approved authority, not reverse-engineered from a passing test.

Review mode and side-effect boundary: [read-only source review, authorised rendered run, or implementation verification]. Applicable repository rules/guardrail scopes and exceptions: [paths]. Baseline and end-state comparison: [method, coverage, pre-existing/concurrent changes]. Skill invocation evidence: [manually applied, explicitly selected, or automatic selection actually observed]. For a bounded review keep the relevant rows inline; creating a report file is not required.

## Read-only findings (when applicable)

Follow VERIFY-05's evidence basis; severity is separate from certainty. Tests inspected but not run remain unexecuted. Existing baseline matches are not automatically defects or regressions.

| Finding / priority | Local authority or proposed improvement | Source and revision | Observed fact / inferred consequence and conditions | Evidence basis and scoped status | Smallest confirming or refuting check / repair direction |
|---|---|---|---|---|---|
| [ID and user consequence] | [actual requirement, exception or proposal] | [path and location] | [separate observation from hypothesis] | [source / executed / hypothesis; status of each claim] | [planned check, not claimed execution; no fix unless authorised] |

## Executed and planned assertions

| Test ID | Rule/state IDs and revisions | Deterministic setup + input/response order | Action | Expected visual/semantic/focus/data/consumer result | Recovery assertion | Actual observation and evidence path | Status / reason |
|---|---|---|---|---|---|---|---|
| [ID] | [IDs] | [fixture/version/request schedule] | [step] | [observable assertions] | [successful next step] | [output, capture, trace; no secret values] | [VERIFIED/FAILED/NOT VERIFIED/NOT APPLICABLE] |

Use an existing mock server or test tool for reproducible faults/races; control response delivery rather than relying on arbitrary sleeps. For cross-layer work, add a separate real-boundary journey row per affected consumer. A mock-only assertion cannot verify server enforcement or persistence.

For each failed command, add only the relevant failure-attribution fields from VERIFY-05: `command/exit; failure location; setup completed?; intended assertion reached?; attribution and evidence; product assertion status; next bounded check`. Keep command failure separate from product-assertion failure. Record existing protections and successful controls; a report does not require a defect quota.

Required applicability review: initial/refresh/incremental/partial states; empty variants; pending/known/unknown write outcomes; correction; two rapid inputs; access loss; stale and out-of-order responses; long/localised content; keyboard/focus/AT; leave/reload/resume; conditional/inapplicable fields; limits; locked and legacy records; defaults/overrides; reduced/removal/re-import inputs; every affected projection. Exclude unreachable cases with reasons.

Component/token changes additionally consider: parent rerender without unintended remount; intentional key/reset policy; retained field value/selection/focus; supported component variants; actual token source/aliases; role-appropriate contrast and focus across supported modes; all affected shared-token consumers; legitimate runtime geometry. Static hard-coded-value searches are candidate findings requiring classification, not automatic failures.

## Usability and task outcomes (when applicable)

Research question and scope: [value]. D18 owner/decision: [value]. Actual/likely user groups, relevant access/language needs and recruitment authority: [values]. Task wording without solution hints: [value]. Correct outcome and critical mistakes: [values]. Start/end boundary, assistance and recovery definitions: [values]. Baseline/thresholds or explicitly qualitative purpose: [authority]. Collection/consent/minimisation/retention: [D07 scope]. For a tiny change, reference existing evidence and explain why it still applies rather than inventing a study.

| Observation ID | Task / participant context without identifying data | Completion and correctness | Mistakes / assistance / recovery | Comprehension of consequence or return-to-task | Evidence and limitation |
|---|---|---|---|---|---|
| [ID] | [authorised fixture/session] | [actual outcome, not only submit event] | [what happened] | [observed response, not agent inference] | [VERIFIED observation or NOT VERIFIED; no population-rate claim from a small session] |

Conditional failure cases: blocked frontend resource/storage (CAP-08); genuine decline/cancel path (UX-08); actual support handoff and pending-operation preservation (FLOW-08); plausible incorrect AI result, edit/regeneration race and proposal-versus-commit distinction (AI-01 through AI-03). These are not mandates to add the features or collect telemetry.

Report totals by evidence category, not a single misleading percentage. Missing runtime, inaccessible API, absent test database or unsupported AT is NOT VERIFIED with exact blocker. A specification gap records decision ID and affected assertion. Cleanup: task-started processes and how stopped; created test records and removal; retained intentional evidence; removed artifacts; final diff/status review or non-Git limitation.
