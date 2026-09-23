# LLM Skills

Six framework-neutral skills for specifying, building and verifying application UI and backend behavior. Detailed standards load by relevance; each project owns its business rules, architecture and runtime guarantees.

The engineering guidance is intended for LLM coding assistants. **Behavioral use has only been tested with Codex.** Other LLMs and agent hosts are untested. The included installers and advisory hooks target Codex specifically; no equivalent integration or automatic discovery is claimed for other hosts.

| Work | Specify | Build | Verify |
|---|---|---|---|
| UI/UX | ui-spec | ui-build | ui-verify |
| Backend, middleware and persistence | backend-spec | backend-build | backend-verify |

Read the [UI/UX guide](docs/ux/README.md) and [backend guide](docs/backend/README.md). They share installation and validation mechanics, while keeping their standards and scope separate. Examples and evaluation fixtures are fictional. A deliberately defective backend fixture exists only for isolated evaluation; its README defines that boundary.

## Use with another LLM or agent host

Provide the selected skills/<name>/SKILL.md and allow the assistant to read the applicable references in docs/ux or docs/backend. Keep those directories together. Each source entry can resolve its library relative to its own location when no configured root or installed locator exists. Use the host's supported context/tool mechanism; mentioning a skill name alone does not make its files available.

The host must support the required file access and any authorized implementation or verification tools. Preserve that host's instruction hierarchy and permissions. Do not assume Codex paths, hooks, trust settings or installation commands apply elsewhere. Verify task selection, reference loading and actual outcomes in the target host before relying on it.

## Install for Codex on Windows

Requirements: Python 3.11 or newer for package checks and optional hooks; PowerShell 7 for the context installers. No third-party Python packages are required.

From a reviewed checkout:

```powershell
pwsh -File scripts/install-ui-ux-context.ps1 -WhatIf
pwsh -File scripts/install-ui-ux-context.ps1
pwsh -File scripts/install-backend-context.ps1 -WhatIf
pwsh -File scripts/install-backend-context.ps1
```

These commands install the entries at user scope, write local library locators and add separate managed sections to Codex guidance. Keep this checkout available. Differing existing installations require review and -UpdateSkills. Installation preserves unrelated instructions and does not configure providers, change application files or enable hooks. Reopen the applicable Codex session if it retains an older skill/environment snapshot.

The entries can also be read explicitly from this checkout: keep skills/ and docs/ together. Automatic discovery of the source skills/ folder is not implied. The persistent user-environment installation path is Windows-specific; another platform needs an appropriate user-level setup and validation.

[Optional UI hooks](docs/ux/hooks.md) use a separate installer and trust review. They validate the skill package, not an application's quality or runtime behavior.

## Validate

```powershell
python -I -B docs/ux/scripts/check-package.py
python -I -B docs/backend/scripts/check-package.py
python -I -B scripts/test-skill-library.py
python -I -B scripts/test-ui-ux-hooks.py
python -I -B scripts/check-release.py
python -I -B scripts/test-release.py
pwsh -File scripts/test-install-ui-ux-context.ps1 -WorkDirectory $env:TEMP
pwsh -File scripts/test-backend-context.ps1 -WorkDirectory $env:TEMP
```

[Validation evidence](VALIDATION.md) distinguishes packaging checks from behavioral evaluations. [Publication guidance](PUBLICATION.md) defines the reviewed file boundary and privacy limits. No production reliability, accessibility conformance or security certification is implied.

## License

No license has been selected and no license grant is included.
