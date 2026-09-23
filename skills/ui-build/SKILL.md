---
name: ui-build
description: Implement or repair application UI components, semantic styling, states, forms and recovery using resolved contracts and existing capabilities. Use for scoped UI coding and refactoring; exclude specification-only work, visual ideation alone and unrelated backend tasks.
---

# UI implementation

Locate the shared library before reading references: use `UI_UX_DOCS_ROOT` when configured; otherwise read `library-root.txt` beside this installed SKILL.md. For an uninstalled repository package only, use `../../docs/ux` relative to this SKILL.md. Resolve the selected path to an absolute directory and require `governance.md` there. If a configured or installed path is missing, report it rather than silently switching libraries. All reference paths below are relative to this resolved library root, not the current working directory. Read the library from its maintained location; do not copy its policies into the application repository.

Read `governance.md`, then every applicable module in its router. Use its common task routes and small-change delta. Always read `modules/capabilities.md` and `modules/verification.md` for implementation; a comparison record is needed only for an actual capability decision. Shared documentation must be present; a skill name does not load another skill.

Inputs: authorised scope, current implementation, resolved contracts and decisions, approved existing visual foundation, API guarantees, runtime/package versions and test tooling. If no separate spec exists, capture the smallest affected contract using the `templates/state-contract.md`; do not require a redesign or a full new spec for a tiny change.

1. Inspect relevant code, instructions, working-tree changes and dependencies. Trace canonical owners and consumers before edits. Preserve existing behaviour unless the requested change or resolved decision changes it.
2. Identify missing authority and conflicts. Isolate dependent work and continue safe independent work; never fabricate business limits, remote guarantees or approvals. Review defaults require a recorded adoption decision before consequential implementation.
3. When the change requires a capability choice, compare native, existing, official and other established capabilities with `templates/capability-selection.md`. Otherwise record reuse of the existing capability without a comparison exercise. Prefer composing a suitable solution; document any verified custom gap. Package suitability does not itself authorise installation.
4. Name affected layers/files and why simple composition or a specific justified pattern fits. Implement responsibilities in their existing owners. Apply CAP-06/CAP-07 to component boundaries and identity; VIS-07 through VIS-09 to token ownership, themes and runtime styling. Do not turn simple markup into unnecessary abstractions. Keep client/server invariants aligned and preserve canonical state.
5. Exercise applicable state transitions and recovery in rendered UI and real boundaries where available. Record exact tests, evidence and limitations in `templates/acceptance.md`. A successful build is not UI verification.
6. Inspect the diff; remove task-created scratch/build artifacts, stop task-started processes and preserve unrelated edits. Report changed files, decisions, verification and residual risks.

Outputs: scoped implementation and truthful evidence against contract IDs. Stop affected mutations where a consequential rule/guarantee remains unresolved. Do not claim workflow completion with required consumers unverified. No automatic hook activation, global configuration edits or application redesign.
