---
name: ui-verify
description: Review UI code or test rendered UI against component, token, accessibility and recovery contracts. Use for read-only UI audits, verification and regression review; exclude visual ideation, specification-only requests and unrelated code reviews.
---

# UI verification

Locate the shared library before reading references: use `UI_UX_DOCS_ROOT` when configured; otherwise read `library-root.txt` beside this installed SKILL.md. For an uninstalled repository package only, use `../../docs/ux` relative to this SKILL.md. Resolve the selected path to an absolute directory and require `governance.md` there. If a configured or installed path is missing, report it rather than silently switching libraries. All reference paths below are relative to this resolved library root, not the current working directory. Read the library from its maintained location; do not copy its policies into the application repository.

Read `governance.md` and `modules/verification.md`, then every other module activated by the feature. Read real contracts and current decisions; do not judge against invented product behaviour. Missing references or a missing runtime limit the evidence, not the honesty of the report.

Inputs: implementation/revision, accepted contracts, environment and permissions, supported devices/AT, test accounts/fixtures and existing test tools. For a read-only request, use the bounded review procedure in verification; do not require installation or a running app to produce useful source findings. Mark unexecuted behaviour NOT VERIFIED while stating precisely what the source establishes.

1. Establish scope, revision, current edits and applicable repository rules. Use the governance task route; map applicable rule/state IDs to assertions with `templates/acceptance.md`. Include component identity, token lineage, supported modes and recovery where relevant. A naming or raw-value scan alone is not architectural or visual verification.
2. Inspect source owners, callees, consumers and relevant tests. When rendered verification is within scope and available, operate keyboard, pointer and supported assistive technology; exercise real boundaries for cross-layer claims. A no-change review must not silently start setup, seeding, autofix or baseline updates. Missing runtime evidence leaves those assertions NOT VERIFIED.
3. Distinguish product defects, specification gaps, unsupported assumptions and test-environment limits. Classify test failures using verification's failure-attribution procedure; record whether setup and the intended assertion were reached. Credit existing protections and accept a no-defect result. An undocumented business rule becomes a decision gap, not a guessed expected result.
4. Report evidence basis separately from status, following VERIFY-05. Give source locations, observed facts, inferred consequences, applicable authority and the smallest check that could confirm or refute each runtime risk. Separate executed commands from tests merely read. A scanner pass or manual skill application does not prove rendered correctness or automatic skill selection.
5. Propose the smallest repair; editing is outside a verification-only request unless separately authorised. Never weaken requirements to obtain a pass. Stop unsafe live tests and continue independent checks.
6. Clean up task-created data/artifacts and stop task-started processes; record anything that could not safely be removed.

Outputs: reproducible findings, state/consumer coverage, evidence links, unverified risks and cleanup record. Completion means the report is complete, not that an application is automatically approved. Rerun only checks affected by fixes, failures or unresolved concerns.
