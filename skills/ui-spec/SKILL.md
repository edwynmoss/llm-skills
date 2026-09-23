---
name: ui-spec
description: Define UI state, component, token, validation and recovery contracts; discover missing product decisions before building a feature. Use for UI specifications and state gap analysis, not application implementation, visual ideation alone or unrelated backend work.
---

# UI specification

Locate the shared library before reading references: use `UI_UX_DOCS_ROOT` when configured; otherwise read `library-root.txt` beside this installed SKILL.md. For an uninstalled repository package only, use `../../docs/ux` relative to this SKILL.md. Resolve the selected path to an absolute directory and require `governance.md` there. If a configured or installed path is missing, report it rather than silently switching libraries. All reference paths below are relative to this resolved library root, not the current working directory. Read the library from its maintained location; do not copy its policies into the application repository.

Read `governance.md` first and follow its applicability router and common task routes. Read every module the task activates; do not treat detailed contracts as optional. Missing shared files block dependent work: report the broken path rather than reconstructing policies from memory.

Inputs: requested task, applicable instructions, current code/design references if present, API/domain authority, existing tests and supplied source material. Inspect before proposing. An empty workspace permits a framework-neutral specification with explicit unresolved decisions, not an invented product.

1. Record inspected evidence, canonical entities, owners, affected journeys and scope. Separate observations, requirements, source advice and proposals.
2. Create a compact coverage/gap matrix using `gap-analysis.md`. Give gaps scenarios, applicability, smallest additions, priority and verification. Reuse existing project decisions where verified.
3. Use the `templates/state-contract.md`, `templates/validation-contract.md` and `templates/acceptance.md` templates as applicable. Resolve relevant concurrency, correction and recovery paths, component boundaries and token ownership. Trace consumers under GOV-03. Plan comprehension/outcome evidence for changed journeys; load conditional AI guidance only for a product AI feature.
4. Record consequential unknowns with the `decisions.md`; ask only for decisions needed for affected work. Continue independent contracts. Use capability selection when a real capability gap exists.
5. Report resolved scope, blockers, candidate defaults and verification plan. A narrow edit gets only the affected contract delta under GOV-04.

Outputs: a reviewable scoped specification, state/field IDs and transitions, rule applicability, source/decision register and observable acceptance criteria. No application changes unless separately requested; this skill does not authorise deployment, packages or hooks. Do not invoke another skill merely by mentioning its name.

Stop affected design decisions when authority, visual foundation for product-wide styling, business rules or API guarantees are absent. Do not label a proposal approved. Finish independent specification work and name exactly what remains unresolved.
