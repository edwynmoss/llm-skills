# Standalone package validation

Validated locally on 2026-09-21 on Windows, using Python 3.12.14 and PowerShell 7.6.5. These results apply to the standalone package and its tooling. They do not prove application behavior or completion of the behavioral evaluation catalogues.

| Executed check | Result |
|---|---|
| UI/UX package integrity | Passed: 3 skill entries, 31 Markdown files, 111 local links, 72 canonical rules and 21 decisions |
| Backend package integrity | Passed: 3 skill entries, 39 Markdown files, 104 local links, 107 canonical rules and 24 decisions |
| Shared library regression suite | Passed: 2 test methods covering corruption detection and library isolation |
| Advisory hook regression suite | Passed: 22 tests, including invalidation when a linked root document disappears |
| Release-boundary regression suite | Passed: 6 test methods, including extra/missing files, synthetic disclosure patterns, links, inventory traversal and mixed-case URL schemes |
| Isolated UI/UX installer checks | Passed: 10 checks |
| Isolated backend installer checks | Passed: 10 checks |
| PowerShell script syntax | Passed for all included PowerShell scripts |
| Publication inventory and disclosure-pattern check | Passed: 97 reviewed files |
| Targeted content review | No remaining concrete disclosure, unavailable private evidence or contradictory host-compatibility claim found in the reviewed content |

The independent content review identified stale references to unavailable evaluation evidence and a case-sensitive URL-host check. Both were corrected and reviewed again. The URL regression suite now covers lowercase, uppercase and mixed-case schemes. Content scanning also checked for known source-specific identifiers and damaged text encoding without reproducing those identifiers in this package.

The six skill entry instructions remain unchanged from the reviewed source entries. Packaging changes generalize the presentation, remove private provenance and evaluation reports, define an explicit release inventory, and make the isolated test fixtures include the linked package-level documentation.

## Scope and limits

- Behavioral use of the guidance has only been tested with Codex. Other LLMs and agent hosts remain untested; host-neutral intent does not establish compatibility.
- The public evaluation catalogues are reusable test cases. Their inclusion is not a claim that every case was executed against this export. No earlier private project report is supplied as evidence.
- Installer checks use isolated fixtures. They do not install these entries into the maintainer's live environment. No application was changed or deployed by these checks.
- Hook tests verify local scripts and simulated events. Actual Codex PostToolUse dispatch was not exercised for this export; the optional runtime smoke check was not run.
- Windows checks were run locally. Linux/macOS installation and remote GitHub Actions execution were not tested.
- The inventory and pattern scanner have bounded coverage. They cannot certify confidentiality, security, accessibility or production reliability. Review Git history, author metadata and the actual publication contents separately as described in [PUBLICATION.md](PUBLICATION.md).

Reproduction commands are in the [README](README.md). Test fixtures use temporary directories and clean them up. Package checks run without generating Python bytecode or tracked test reports.

## Publication follow-up, 23 September 2026

The installer test harness now saves, clears and restores both library environment variables, so a preconfigured host cannot contaminate the coexistence check. Expected rejection cases no longer leave a failing native exit code after a successful suite. Both ten-check suites passed with deliberately preconfigured library values; both values were restored afterward. Production installer behavior is unchanged. Remote checks and merge status are recorded on the associated GitHub pull request.
