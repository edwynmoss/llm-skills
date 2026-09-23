## UI/UX skills and shared standards

For UI behaviour specifications and state gap analysis, use `ui-spec`; for UI implementation or refactoring, use `ui-build`; for read-only UI review and behavioural verification, use `ui-verify`. Read the selected skill and only its applicable shared references. Use these skills across projects when the task fits; do not activate them for unrelated backend work or visual ideation alone.

Resolve the shared library through `UI_UX_DOCS_ROOT` or the installed skill's `library-root.txt`. The library is maintained separately from application repositories. Each project still owns its business rules, architecture, components, semantic tokens and platform conventions. Generic guidance does not waive applicable project requirements.

Keep work proportional to the requested change. Reuse existing capabilities, extract components by responsibility, preserve state/focus identity and distinguish design values from runtime geometry. Define affected states and recovery without inventing API guarantees. Separate source facts, executed checks and runtime hypotheses; inspect test side effects during no-change reviews. Skill availability grants no additional permission to modify applications, install dependencies, activate hooks or deploy.
