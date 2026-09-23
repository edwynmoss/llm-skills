# UI experience contracts

**Define the experience. Reuse solved capabilities. Expose uncertainty. Verify behaviour.**

Part of LLM Skills. Behavioral use has only been tested with Codex; other hosts are untested. The installation and hook instructions below are Codex-specific. The standards and source entries can be supplied explicitly to another assistant with the necessary file/tool access; see the [host compatibility notes](../../README.md).

Revision **1.6-public.1** contains three local skills and one canonical standards library, with separately installed advisory hooks. It is a general-purpose, framework-neutral skill system with a user-level installer. Application implementation and plugin publication are separate tasks. Each consuming project supplies its actual domain, stack, design system and verification environment; pilot findings do not become project defaults.

| Entry | Use it for | Output |
|---|---|---|
| [ui-spec](../../skills/ui-spec/SKILL.md) | Discover gaps and define a feature's states before implementation | Scoped contracts, decisions and acceptance conditions |
| [ui-build](../../skills/ui-build/SKILL.md) | Implement or fix UI behaviour from resolved contracts | Scoped code changes and evidence; unresolved work explicitly isolated |
| [ui-verify](../../skills/ui-verify/SKILL.md) | Review UI source read-only or test rendered behaviour within authorised scope | Findings that separate source facts, executed checks and unverified runtime risks |

## Install once for your Codex account

Keep a reviewed checkout of this standalone package available on your computer. Run the commands below from the repository root. Its three entry skills are installed at user scope and read this single shared standards library; application repositories do not need copies. On Windows with PowerShell 7:

```powershell
pwsh -File ./scripts/install-ui-ux-context.ps1 -WhatIf
pwsh -File ./scripts/install-ui-ux-context.ps1
```

The installer defaults to `$HOME/.agents/skills`, respects `CODEX_HOME` for global instructions, sets the Windows user variable `UI_UX_DOCS_ROOT` to this package's `docs/ux`, and appends/replaces only the marked UI/UX section in global `AGENTS.md`. Each installed skill includes a `library-root.txt` locator, so it can resolve the shared library before an existing Codex process inherits the new environment. Source entry files and installed SKILL.md files are identical. The installer changes no MCP, hook or TOML configuration. An insufficient instruction budget stops installation before writes.

Existing differing skill files or locators require review and `-UpdateSkills`; unrelated files are preserved. If the same skills already exist in the older `.codex/skills` location, use `-SkillsDirectory` for that existing location to avoid duplicates. Active global overrides and ambiguous managed markers stop installation. Repeated installation of matching files makes no file changes. `-EnvironmentTarget Process` is available for isolated tests; normal desktop installation uses User scope. Do not move/delete the library without rerunning the installer from its new location and reviewing any existing `UI_UX_DOCS_ROOT` value. A running host with an older environment may need restarting after relocation.

The three source entry skills can still be read explicitly from the full repository checkout. If no configured root or installed locator exists, they resolve the sibling `docs/ux` from their own location. Keep `skills/` and `docs/ux/` together in that mode. The source `skills/` directory is not an extra repository discovery location. Do not install duplicate user/repository copies with the same names. Explicit use: `$ui-spec define states for this feature`; `$ui-build implement the resolved contract`; `$ui-verify review this flow without changes`. Naming one skill does not invoke another. Codex can discover matching skills automatically; restart if a new installation does not appear. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills).

The canonical package consists of `skills/ui-*`, `docs/ux/` and the installer/checker scripts. Keep them together. Review source changes before updating an installation; installation does not publish source or modify application repositories.

Start with [inspection and coverage](gap-analysis.md), [source provenance](sources.md), and [decisions](decisions.md). Operational routing and requirement meanings are in [governance](governance.md). Every entry requires governance and the modules applicable to its actual task. An irrelevant module gets an explicit exclusion, not blanket execution. For a tiny copy change, a scoped delta and its affected checks suffice.

For a no-change pilot, apply ui-verify from this package to one existing flow and use the [bounded review procedure](modules/verification.md). Inspect local instructions and command side effects, preserve stricter applicable project guardrails, and report inline without installing the package into the target repository. A passing scanner is evidence for its checks; runtime hypotheses still need runtime tests. Project-specific pilot reports are not included in this standalone package.

Revision 1.3 sharpens test-failure attribution and recognition of correct implementations. A failing test fixture is not proof of a live product defect, and a useful review can find no defect. [General review fixtures](evaluation-fixtures.md) cover a browser resource picker, an overlay-test failure and a native review queue. They support bounded source-review evaluations, not claims of browser/native runtime validation. Keep expected answers out of evaluator inputs and use [the evaluation protocol](evaluations.md) to record actual results.

Component boundaries and identity are explicit in [architecture](modules/capabilities.md); semantic token ownership, aliases, themes, variants and legitimate runtime-style exceptions are in [visual standards](modules/visual-components.md). The [worked component/token review](examples/component-token-review.md) distinguishes meaningful extraction from unnecessary wrapper files and raw design values from dynamic geometry.

Research refinements strengthen comprehension, informed choices and task-outcome evidence in the existing modules. Frontend-resource failure and actual support handoffs are conditional rules. A ninth [human-AI reference](modules/ai-interactions.md) loads only when the product itself has AI suggestions, extraction or actions; using Codex to code a normal interface does not activate it. Governance contains common reading routes and a small-change delta format, so no extra entry skill is needed.

Reusable templates: [state](templates/state-contract.md), [validation](templates/validation-contract.md), [capability selection](templates/capability-selection.md), [acceptance](templates/acceptance.md). Worked, explicitly fictional examples: [failed panel refresh](examples/panel-refresh.md) and [dependent form recovery](examples/dependent-form.md).

The state template now includes component responsibility and token-lineage tables; acceptance includes component identity, supported modes, comprehension and outcome evidence when affected. Inherit existing contracts for a small change rather than filling every template.

See [validation report](validation-report.md) for actual evidence and limits, [evaluation cases](evaluations.md) for expected skill behaviour, and [phased backlog](backlog.md) for pilot work. A follow-up rendered pilot can use one existing read-only panel with a manual Refresh action and independent surrounding content. Use its real API, tokens and test environment; do not introduce a refresh feature just to test these skills.

The installer uses the [managed global routing text](codex-global-instructions.md). An optional [repository AGENTS addition](agents-addition.md) remains available for repository-only adoption; do not duplicate it when user-level routing already applies. The context installer does not activate hooks. Optional [advisory hooks](hooks.md) have a separate installer, preview and removal path. No dependencies, application files or lockfiles are added. Shared policies live only under `docs/ux`; the entry skills route to them. Treat this directory tree as one versioned unit.

For a repeatable structural check, run `python docs/ux/scripts/check-package.py` from the repository root. The [standard-library checker](scripts/check-package.py) verifies local file links, rule/decision references and this package's restricted metadata format. It is not the full skill-creator validator or a behavioural evaluation.

Installer regression checks use disposable files under a directory you supply: `pwsh -File scripts/test-install-ui-ux-context.ps1 -WorkDirectory <existing-scratch-directory>`. They run with process-only environment changes and clean their fixture directory.

The UI library and `docs/backend` now share mechanical validation
and installation code in `scripts/check-skill-library.py` and
`scripts/install-development-context.ps1` at the repository root. Existing UI
commands remain wrappers with the same parameters and behavior; standards, roots
and managed instruction blocks remain separate. Hook integrity fingerprints
include the shared checker. Coexistence is covered by both installer suites.
