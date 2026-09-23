# Governance and applicability

Revision 1.6-public.1. This is the single owner of rule metadata, adoption and routing. Detailed behaviour belongs to the modules, not to entry skills. Source labels resolve in [sources](sources.md).

## General-purpose boundary

This library applies across products and UI frameworks. Inherit the consuming project's actual domain, architecture, components, tokens, platform conventions and test tools. A pilot repository, worked example or external design system supplies evidence or illustration; none supplies defaults for another project. Do not require a particular business integration, repository host, operating system, framework, component library, token spelling or test runner. Translate the invariant into the actual platform's equivalent behaviour; mark platform-specific checks inapplicable with a reason. For example, DOM/ARIA checks apply to web UI, while native UI needs its platform semantics and interaction evidence.

U11 records the package policy for this general boundary and verification refinements; it does not approve additional product features. Capture project-specific facts in that project's scoped contract rather than expanding this shared library with product branches. Add a general rule only when a demonstrated failure is not already covered; an additional example or evaluation case often suffices. Finding no defect is a valid review outcome. Do not prescribe extraction, a token migration or a new dependency merely to produce changes.

## Rule envelope RULE-BASE

Each rule row inherits this real named envelope, with its explicit row values taking precedence. Required columns are ID; applicability and strength; authority/status and rationale; behaviour; exceptions/dependencies; observable acceptance. Dependencies additionally include applicable project instructions, the source register and a resolved feature scope. Exception default is none *within applicability*; outside applicability record NOT APPLICABLE with reason. A row cannot make a missing product value optional merely by inheriting this envelope.

Strength and approval are separate axes:

- **MUST**: invariant within scope, unless a higher-priority instruction supersedes it. A proposed MUST is not yet an approved product rule.
- **DEFAULT WITH OVERRIDE**: recommended behaviour; record adoption or an override. Defaults in this draft are FOR REVIEW and cannot silently resolve consequential choices.
- **CONDITIONAL**: mandatory when the stated predicate holds; this never mandates adding that feature.
- **PRODUCT DECISION REQUIRED**: no implementation default. Record exact missing value, decision owner and affected work; continue independent work.

Authority/status: USER REQUIREMENT is from U, U9, U10 or A; VERIFIED GUIDANCE is an externally verified fact, not project adoption; OBSERVED is dated project evidence; PROPOSED is authored policy; APPROVED requires a recorded product decision. APPROVED AUTHORING POLICY records adoption by this package maintainer; it does not resolve a consuming project's product decisions or approve a particular default, API guarantee or token. Rule IDs persist; semantic changes increment contract/library revision and supersede old evidence.

| ID | Applicability / strength | Authority/status; rationale | Expected behaviour | Exceptions / dependencies | Observable acceptance |
|---|---|---|---|---|---|
| GOV-01 | All use; MUST | U2/U10/U11; USER REQUIREMENT; preserve decision source and existing policy | Label facts, advice, observations and proposals separately. Inspect applicable repository instructions and scoped guardrails; generic allowances do not waive stricter local requirements. Apply the general-purpose boundary above. Resolve conflicts by instruction authority, including explicit user direction; record unresolved product alternatives | A passing baseline permits no inference of debt-free UI. A generic preference is not an adopted project requirement; use local exceptions through their owning process | Reviewer can trace each consequential behaviour to authority or an OPEN decision; no silent rule/baseline weakening, imported pilot convention or invented project violation |
| GOV-02 | New feature/context; MUST | U2/U5; USER REQUIREMENT; avoid fictional product | Capture task, users, canonical entities, API contracts, tokens/components, accessibility target, supported environments, privacy and evidence tooling. Mark absent inputs explicitly | Reuse verified intake for scoped edits; D01-D11 | No unresolved placeholder is presented as implementation-ready |
| GOV-03 | Multi-owner or cross-layer data; CONDITIONAL | A; USER REQUIREMENT; one business truth | Fill producer/consumer matrix below; identify input versus derived fact, defaults versus overrides, IDs, mutations, reconciliation and all downstream projections | A genuinely presentational delta may cite existing owner and affected surface only | Trace a mutation through persistence and every affected consumer; untraced consumers are risks |
| GOV-04 | Narrow change; DEFAULT WITH OVERRIDE | PROPOSED; prevent process-driven redesign | Reuse existing contracts and foundation; document only changed state/copy/interaction and impacted checks. Expand only for evidence of wider impact | Scope expansion requires stated reason; D17 adoption | Button-label fix retains unrelated layout, routes, dependencies and state ownership |
| GOV-05 | Contract/rule changes; MUST | PROPOSED; stale tests are misleading | Record revision, changed IDs, decision reason, consumers and invalidated evidence. Keep retired IDs as superseded; do not reuse meaning | Depends on adopted maintenance owner D17 | Old revision's passing evidence cannot close a changed contract |

## Required reading by applicability

Every entry reads this file. Use the following predicates to load full relevant modules, including their rule tables. Keep one compact applicability record for the task; record meaningful exclusions, especially adjacent workflows that might be mistakenly activated. Previously read unchanged references need not be reloaded at every message. Do not read all examples or produce a full-spec ceremony for every task. Required references are not optional once the applicability predicate holds.

| Task involves | Required module |
|---|---|
| User goal, hierarchy, actions, navigation or discovery | [UX reasoning](modules/ux-reasoning.md) |
| Rendered control, copy, layout or styling | [Visual/components](modules/visual-components.md), [accessibility/device/performance](modules/accessibility.md) |
| Data acquisition, action, persistence, pending or recovery | [States and recovery](modules/states.md) |
| Field/group, validation or submission | [Validation](modules/validation.md), states and accessibility |
| Search, list manipulation, upload, wizard, autosave, editing, destructive action, notification, time or content extremes | [Workflows/content](modules/workflows-content.md), plus states/validation as affected |
| Implementation, package or SDK choice, hooks/composables | [Capabilities/architecture](modules/capabilities.md) |
| Acceptance planning, implementation check, review or proposed automation | [Verification](modules/verification.md) |
| Product exposes generated suggestions, extraction, predictions or AI actions | [Human-AI interaction](modules/ai-interactions.md), states and capabilities; validation when accepted values enter canonical records |

## Common task routes

All routes include governance. These are reading paths and output expectations, not automatic invocation of multiple skills. ui-build also reads capabilities and verification; a simple edit can conclude that no capability-selection comparison is needed. Escalate a route only when inspected evidence expands its impact.

| Task | Applicable references / bounded focus | Expected artifact |
|---|---|---|
| Read-only UI code review or skill pilot | ui-verify plus verification's bounded review procedure; architecture, visual/accessibility, states and workflow modules only as the selected flow requires. ui-spec is optional for an actual contract gap | Inline findings and evidence ledger; named scope, local policy, source facts versus runtime risks, executed checks and no-change evidence. No installation, app repair or automatic full audit |
| Label, hint or small existing style change | Visual/components, accessibility; workflows/content for changed value/content meaning; capabilities and verification if coding. Inherit existing state/foundation rather than reopening all product decisions | Delta record below; label/name, affected layout/state/theme checks. No new library, full redesign or user-study quota |
| Component extraction or variant change | Capabilities CAP-03/CAP-06/CAP-07, visual/components, accessibility, verification; states/validation when ownership or lifetime changes | Responsibility and API boundary, inherited contracts, state/focus-preservation evidence |
| Semantic token/theme change | Visual/components VIS-07 through VIS-09, accessibility, capabilities, verification; GOV-03 consumer tracing for shared scope | Token owner/alias/state-mode matrix, affected consumers, resolved exception or D03 gap |
| Failed panel refresh | States, visual/components, accessibility, verification; capabilities if implementation | Scoped read/recovery contract and independent-content assertions |
| Dependent form | Validation, states, visual/components, accessibility, verification; capabilities if implementation | Field/dependency authority, chosen profiles, request revisions, correction/recovery assertions |
| Import or bulk action | Workflows/content, states, validation where applicable, capabilities, verification; visual/accessibility for UI | Canonical IDs, scope/reconciliation and per-item outcome contract; no unrelated workflow added |
| New journey or claimed usability improvement | UX reasoning, accessibility, verification; other modules by actual workflow | D18 research/outcome plan or relevant inherited evidence; no unexecuted usability claim |
| AI suggestion or action | Conditional AI module plus feature's normal route | D21 autonomy/evidence/correction contract; generation is not verification or commit |

## Small-change delta and explicit handoff

For GOV-04 use: `task/scope; inspected component and existing contract revision; intended change; inherited owner/foundation; affected rule/state IDs; unresolved decisions (or none); focused assertions/evidence`. A local label edit can keep this inline in the work report; no extra repository file is required. If the existing component has no separate contract, document observed behaviour and the smallest required delta. A purely presentational change need not invent state IDs; reference the actual component/control and state unaffected by the change.

Pass resolved contracts, open decisions and evidence between activities. Naming ui-spec/ui-build/ui-verify does not invoke another skill. Routine verification stays part of implementation even if ui-verify is not separately selected. Missing authority blocks only dependent work. Relevant library standards remain mandatory; a small-change route reduces artifact size, not correctness or accessibility.

Under GOV-01, record the local rule's path, scope and exception mechanism when it affects the task. For example, VIS-09 permits legitimate runtime styling in general, but does not authorise inline styles in a repository component that explicitly prohibits them. Use its supported mechanism or report the conflict. Conversely, an existing baseline match is not automatically a new regression, and an unadopted library preference is a recommendation rather than a repository defect. Review requests do not authorise changing those policies.

## Intake and producer/consumer matrix

Record actual files, versions and evidence dates, not just layer names. A fact has one owner. Effective inherited values use the item override when present, otherwise the project default, unless an explicit historical snapshot is required.

| Entity/field/status + stable ID | Authoritative source/storage | Writers / manual and automated mutations | Readers / UI / documents / exports / integrations | Derived values and dependencies | Recalculate / clear / reconcile / invalidate | Required real journey and evidence |
|---|---|---|---|---|---|---|
| Fill with inspected facts | Input/derived/default/override/snapshot | Include reload, retry, import, delete and permissions | Name each affected consumer or unresolved risk | No duplicate calculation owner | Include reduced/removed input | Mark verification independently |

Stopping is scoped: unresolved API write guarantees block that write's recovery implementation, not unrelated layout inspection. An unknown accessibility target blocks a conformance claim, not identification of keyboard defects. Absence of a visual reference for product-wide styling does not require redesigning an already approved button. Never add features merely to satisfy an applicability checklist.
