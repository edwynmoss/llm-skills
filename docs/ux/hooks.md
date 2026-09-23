# Advisory skill hooks

Revision 1.6 adds two optional, framework-neutral hooks. They operate on the skill installation and its source package, not application source. The hook runner and installer require Python 3.11 or newer, with no third-party packages. The context installer remains independent. Source owner: the maintainer of this shared library.

| Event | Scope and result |
|---|---|
| SessionStart: startup, resume, clear, compact | Check configured root, all three installed locators and entry bytes, entry references and the library revision. Emit one short context pointer or NOT VERIFIED. This is installation health, not a structural or UI test pass. |
| PostToolUse: Bash, apply_patch, Edit, Write | Hash only docs/ux Markdown/Python files, the three source entries, the hook runner, scripts/check-skill-library.py and linked root README/VALIDATION documents. Run the existing package checker once on the first eligible event in a session, then only when that fingerprint changes. Report VERIFIED or FAILED for package integrity only. |

The initial per-session package check intentionally establishes a baseline, including when the triggering tool did not edit the package. Later unrelated edits produce no additional result. The handler never evaluates shell input, opens transcripts, scans application trees or infers file changes from command text. External package changes are also detected at the next eligible event. Unsupported tool paths and a session with no eligible events may never trigger validation; absence of output is not a pass.

## Install and remove

Run from the maintained checkout after installing the three skills:

```powershell
python -I -B scripts/install-ui-ux-hooks.py --dry-run
python -I -B scripts/install-ui-ux-hooks.py
```

Use an actual Python 3.11+ executable if `python` resolves to an unavailable launcher. The installer records that interpreter's absolute path, so moving/upgrading the interpreter or checkout requires reviewed reinstallation with `--update`. It supports `--codex-dir` and `--skills-dir`; the latter defaults to ~/.agents/skills. It adds only two groups to user hooks.json and records the exact owned definitions in ui-ux-hooks-install.json. Unrelated groups and config.toml remain intact. Invalid configuration, inline hooks at the same user layer, disabled hooks, duplicate installation or modified owned groups stop installation before writes. `--update` permits a reviewed definition change; it does not overwrite a hand-edited owned group.

Codex requires review and trust for non-managed definitions. Open `/hooks` in the CLI, inspect the two UI/UX entries and trust those exact definitions. Do not trust unrelated entries as part of this setup. A changed definition requires fresh review; installation alone does not enable execution. Restart/reopen the applicable session to load changes. [Official event, configuration and trust contract](https://learn.chatgpt.com/docs/hooks).

To preview and remove only the installed groups:

```powershell
python -I -B scripts/install-ui-ux-hooks.py --remove --dry-run
python -I -B scripts/install-ui-ux-hooks.py --remove
```

Removal preserves unrelated hooks and rejects ambiguous edits. The bounded runtime cache at `$CODEX_HOME/cache/ui-ux-hooks-state.json` and its `.lock` companion may remain; they contain only hashed session/root identities and fingerprints, no prompts, commands, transcripts or source text. They are safe to remove when no hook is running. They are runtime state, not repository artifacts.

## Bounds and verification

Measure checker runtime in the target environment. The child checker has a five-second timeout and each Codex handler a ten-second timeout. Input is limited to 1 MiB; hash input to 256 files, 1 MiB per file and 16 MiB total; feedback to 3,500 characters. The state cache holds at most 32 sessions. An OS lock prevents concurrent cache writers and is released on process exit. Results are cached only after a second fingerprint confirms the source did not change during the check. Failed integrity checks are also deduplicated until content changes or a new session begins; failures are advisory, not suppressed passes.

Unavailable files, lock contention, timeout, malformed checker output and changing input yield NOT VERIFIED. Hook stdout is JSON and contains no blocking decisions, automatic continuations or tool-input rewrites. The runner invokes one fixed local checker; no installs, network, recursive agents, autofixes, commits or application commands. The hook executes source from the reviewed checkout, so maintain that checkout as trusted executable tooling. Revisit these bounds if package size or measured runtime grows.

Manual and CI commands remain independent:

```powershell
python -I -B docs/ux/scripts/check-package.py
python -I -B scripts/test-ui-ux-hooks.py
```

An optional runtime smoke check is `python -I -B scripts/smoke-ui-ux-hooks.py` with an installed Codex CLI. It uses a deterministic model stub on a temporary loopback server, an isolated CODEX_HOME and disposable skill locators. Only that isolated invocation bypasses hook trust for the two generated, reviewed definitions. It verifies real SessionStart context delivery, then invokes the exact post-tool command directly to check JSON feedback and duplicate suppression. It does not verify Codex PostToolUse dispatch. The server, CLI process and fixture tree are removed afterward; no external model is called and no application tool action is requested. Normal installations still use Codex's persisted trust review.

Tests use disposable offline fixtures and remove them. They cover actual passing/broken/repaired packages, installation drift, unchanged content, unrelated changes, cache contention, inconsistent/checker failures, bounded input and installation preservation/rollback. See [validation evidence](validation-report.md) for actual runtime results, rather than assuming the documented event is supported on every host.

## Deferred extensions

There is no Stop hook or application-check command registry. Adopt a consuming project's existing lint/component/token/accessibility checks only after measuring them and obtaining project-scoped authorization. Keep legitimate runtime geometry and platform conventions intact. A future completion hook must use structured execution evidence, start advisory and guard any continuation with stop_hook_active; do not infer test passes from assistant prose. Hooks supplement independent CI and rendered UX verification.
