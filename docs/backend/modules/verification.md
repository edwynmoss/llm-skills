# Backend verification, evidence and bounded automation

Inherit [governance](../governance.md). Record assertions, outcomes and limits inline for a small delta; load [acceptance ledger](../templates/acceptance.md) when its structure is needed. Evidence statuses: VERIFIED means the stated assertion was observed at the named revision/environment; FAILED means an executed assertion differed; NOT VERIFIED means unexecuted, blocked or insufficient evidence; NOT APPLICABLE requires a predicate-based reason. Status is separate from evidence basis and severity.

Record command outcome separately from the assertion it was intended to test:

| Observation | Report the command/check | Report the business assertion |
|---|---|---|
| Runtime missing or fixture setup throws before assertions | Setup/runner failure, with stage and exit code if observed | NOT VERIFIED; do not call the product broken |
| Setup completes; expected denied mutation writes a row | Executed assertion mismatch | FAILED for that assertion in that fixture |
| Source clearly omits a required authorization check | Source-supported finding with path and triggering conditions | Runtime reproduction NOT VERIFIED until exercised; source certainty does not imply a demonstrated exploit |
| Only a supplied failure transcript is available | Reported setup failure or reported assertion result, attributed to the artifact | No claim that the current evaluator executed it |
| A focused test passes with a mocked dependency | Executed check passed for its stated boundary | Unexercised database/provider/middleware behavior remains NOT VERIFIED |

For prebuilt test artifacts, state whether they were rebuilt or reused and how source correspondence was checked, if checked. Preserve concurrent work: a clean starting tree does not justify a clean-final-tree claim when another task changes unrelated files. Report the reviewed files separately from whole-checkout state.

| ID | Applicability / strength | Authority and rationale | Expected behavior | Exceptions / dependencies | Observable acceptance |
| BV-01 | Review/test claim; MUST | USER; source, execution and deployed state differ | Label source observation, executed check and runtime hypothesis separately. State revision, scope, authority, actual command/assertion and environment; distinguish tests read from tests run | Missing runtime permits a useful source review, not a runtime pass | Every material conclusion can be reproduced or has a precise confirming/refuting check |
| BV-02 | Cross-layer/workflow change; MUST | USER; unit mocks cannot establish system parity | Trace every required writer, mutation, relationship, derived value and consumer; exercise the strongest practical authorized real client/API/use-case/database/output journey | Mocks supplement orchestration/race tests; unavailable consumers remain explicit risks | Canonical identities and invariants remain consistent across manual and automated paths and downstream outputs |
| BV-03 | Concurrency/recovery claim; CONDITIONAL | USER; timing luck is not proof | Use controlled interleavings, barriers and deterministic failure injection around actual boundaries. Assert final effects, receipts, versions and recovery, not merely method calls | Live fault injection requires appropriate scope; exact engine/provider semantics matter | Duplicate, stale, partial and uncertain outcomes converge as contracted; a legitimate second operation is preserved |
| BV-04 | Test failure; MUST | USER; fixture errors are not product defects | Record whether setup completed and intended assertion ran. Distinguish assertion mismatch, setup/runner failure, unavailable dependency and unresolved attribution | Repair tests only within authorized scope; never weaken production guards for a green result | Report names the failed command and limits product claims until the intended assertion is exercised |
| BV-05 | Read-only audit; MUST | USER; inspection must preserve state | Inspect commands for package restore, seeding, snapshots, DDL, writes, locks, external calls and generated files before running them. Preserve current edits and compare scoped before/after evidence | Explicitly authorized isolated fixtures may write within that scope | No silent application/provider mutation, dependency install, baseline update or server start; report coverage of preservation checks |
| BV-06 | Regression scope; MUST | USER; existing records and consumers matter | Select cases from the impact matrix: create/edit/reload, delete/reduced input, retries, permission changes, legacy/locked records, overrides/defaults, maximum supported children and affected outputs | Exclude unreachable cases explicitly; no blind Cartesian-product requirement | Tests cover changed invariants and affected producers/consumers; unrelated suites are not repeatedly run without reason |
| BV-07 | Cleanup and reporting; MUST | USER; evidence includes side effects | Stop task-started processes; remove only task-owned fixtures, test data and generated artifacts; inspect diff/index/config/lockfiles. Preserve user/concurrent changes and name unresolved cleanup | Never blanket-delete shared resources or revert another actor's edits | Final report identifies what changed, what passed, what remains, and any artifacts deliberately kept |
| BV-08 | Hook/automation proposal; CONDITIONAL | USER; a trigger does not certify correctness | First run a useful check manually, measure runtime/false results and inspect side effects. Verify supported events/runtime; use narrow scope, bounded output/time, dedupe and nonrecursive failure handling | No backend hook activation in this authoring/install scope; independent CI remains available | Unavailable/timeout means NOT VERIFIED; no migration, seed, live provider call or broad autofix hidden in a hook |

## Bounded source-review procedure

When a repository is supplied, confirm its identity and source revision, then inspect current edits so the review can preserve them. Otherwise use the supplied-artifact boundary in governance. Select the user's named flow, or one representative existing journey for an unspecified real-code pilot. State the chosen API/use case and storage/consumer boundary. Inspect applicable instructions, schema, middleware registration, authorization, use-case/domain code, queries, transactions, jobs and tests only as the flow activates them. Follow shared callees before declaring a guard absent.

Record a compact coverage map: boundary inspected; invariant owner; source location; existing protection; potential gap; evidence needed. A known unique constraint may close a duplicate-create concern even when a controller has no precheck. A provider adapter may already classify unknown outcomes. A test named atomicity may only mock transaction methods. Read the assertions and fixture setup before deciding what the test establishes.

Use a finding format: priority and consequence; adopted requirement or proposed improvement; source location/revision; observed fact; conditional runtime effect; evidence basis/status; smallest confirmation/refutation; minimal repair direction. Do not manufacture severity from unfamiliar architecture or frame every improvement as a defect. A no-defect result is valid when evidence supports the inspected contract.

## Evidence basis and failure attribution

| Basis | What it establishes | What it does not establish |
|---|---|---|
| Source observation | A particular guard, query predicate, transaction boundary, mapping or missing path exists at the inspected revision | Actual deployment, race schedule, provider guarantee or user-visible failure |
| Executed check | Named assertions ran against the stated fixture/environment and produced recorded outcomes | Unasserted consumers, different engines/versions, production load or unobserved recovery |
| Runtime hypothesis | A plausible consequence under explicit preconditions with a test that could refute it | A reproduced incident or an automatically verified defect |

A failing test command may fail before any product assertion. Inspect fixture creation, migrations, credentials, provider doubles, clocks and test runner errors. If a double lacks a method the real provider has, fix or propose fixing the double rather than weakening the product. If a database cannot start, report command failure and product assertions NOT VERIFIED. If the intended assertion executes and differs, record the mismatch and investigate whether the fixture expectation matches the authoritative contract.

## End-to-end gate by affected boundary

For API/storage work, exercise an actual request or real client through routing, serialization, middleware, authorization, use case, selected test database and reload. Check canonical rows, relationships, version/receipt records and derived projections. For jobs, include durable acceptance and broker/consumer acknowledgement where required. For provider semantics, use an authorized sandbox or controlled real boundary. For migrations, rehearse legacy data and supported old/new versions on the actual engine.

Trace UI, documents, drawings, exports, search, cache and integrations only when affected—but do not silently omit a required consumer because it is harder to launch. Mark it unverified and qualify completion. A frontend display that looks right can still read a stale or competing field. A backend 200 can still represent only accepted work. The shared project contract determines which outcome counts as complete.

Choose edge cases from the invariant: no required data, ambiguous identity, duplicate request, simultaneous mutation, lost response, reduced input, removed child, deleted parent, permission revocation, approved/locked record, inherited default, explicit zero override, legacy record and maximum supported size. Include positive controls proving legitimate behavior still works. Use deterministic ordering instead of repeated random racing.

## Tools and automation

A static package checker verifies links, rule IDs and metadata; it does not validate backend decisions. A linter/typecheck/build proves its named properties, not transaction safety. An in-memory database proves its own semantics. A shell command called plan or explain can execute effects depending on flags and provider. Inspect actual behavior and target configuration before execution, especially in a no-change review.

Future hooks should invoke a project's already-adopted bounded checker after proving it useful manually. Keep migration/seed/replay and real-provider work explicit. No test command should silently provision infrastructure or modify a production database. Use an allowlisted command and relevant paths; record missing tools or timeouts as NOT VERIFIED; prevent recursive agents and repeated completion loops. The frontend hooks remain scoped to their own package and do not automatically validate this backend library.

The [evaluation catalogue](../evaluations.md) measures skill behavior separately from script correctness. Run unseen realistic cases when feasible, retain positive controls, and record actual prompts/outcomes. Proposed cases are not executed evidence. A self-authored example is explanatory material, not independent evaluation or production acceptance.
