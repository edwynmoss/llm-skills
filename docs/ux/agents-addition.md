# Optional repository AGENTS addition

Optional repository-only alternative. User-level installation instead applies `codex-global-instructions.md` through the managed installer; do not add duplicate routing. Review against existing project instructions. Source skills are under `skills/`; normal adoption uses the user-level installer. Do not create a second discovered repository copy of the same skills.

```text
For UI behaviour specifications, use ui-spec; for UI implementation, ui-build;
for read-only UI review or behavioural verification, ui-verify, when its scope applies.
Read the selected SKILL.md and its required applicable shared references;
mentioning another skill does not invoke it.

Keep work proportional to the requested change. Reuse approved existing
contracts, tokens, components and integrations. Define affected states and
recovery, preserve canonical ownership, and record consequential unknowns
instead of inventing business rules or API guarantees. Review defaults in
docs/ux are proposals until adopted for the relevant scope.

Use the common task routes and small-change delta in docs/ux/governance.md.
Generic allowances do not waive applicable repository rules; follow GOV-01.
Extract components by responsibility and preserve state/focus identity;
do not impose a file for every wrapper or ban ordinary inline markup.
Trace semantic tokens to approved owners and supported modes. Distinguish
hard-coded design choices from legitimate runtime geometry. Load the AI
reference only for AI functionality in the product itself.

Tie evidence to rule/state IDs and revisions. Distinguish static inspection
from rendered behaviour and real end-to-end verification. Do not report
unexecuted checks as passed. The skills grant no additional permission to
install dependencies, change global configuration, activate hooks or deploy.
For no-change reviews, use the bounded procedure in docs/ux/modules/verification.md;
inspect command side effects and distinguish source facts from runtime hypotheses.
```
