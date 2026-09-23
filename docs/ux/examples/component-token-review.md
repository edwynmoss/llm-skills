# Worked review: component boundaries and semantic styling

Illustrative review EX-COMPONENT, revision 1. This is a bounded specification/review exercise, not an implemented application. Every file name, component and token below is a fictional fixture assumption. No real project's token names, framework, business rules or approvals are inferred. Behavioural evidence is NOT VERIFIED.

## Fixture and task

Assume a React project already has `ProjectPage`, `useProjectEditor`, `ProjectSchema`, an API adapter, `Button`, `Dialog` and a semantic token file. The requested change is to correct the existing editor's component boundaries and inconsistent error styling. Scope includes one editor and its existing theme support. It does not include new fields, a new component library or product-wide redesign.

Observed fixture defects: ProjectPage defines a stateful `EditorForm` component type inside its render function; it embeds an independently operated confirmation dialog; error text selects raw `red.600`; the dark-theme branch overrides that colour locally; the progress element has a genuinely data-derived width. The project already exposes approved error-text and error-border roles. It supports light and dark themes. These are illustrative observations, not findings in a real repository.

## Component decision

| Responsibility | Selected owner / boundary | Reason and preservation contract |
|---|---|---|
| Route context and layout | ProjectPage composes existing editor and dialog | No business validation, provider code or independent dialog workflow in route markup |
| Editing workflow | Existing useProjectEditor remains single draft/action owner | Do not duplicate draft state when extracting rendering; schema and adapter remain authoritative |
| Form rendering | EditorForm defined at module scope and located using project conventions | CAP-07 avoids nested component-type identity changes; parent rerender preserves input value, selection and focus. Separate file only if responsibility/readability warrants it |
| Confirmation UI | A focused feature-specific confirmation component composes existing Dialog | Reuse library focus/dismissal behaviour; don't add another trap or invent a global modal manager |
| Small hint/label markup | Remains with the relevant field | Extraction would add no meaningful ownership or reuse benefit |
| Button variants | Existing Button API | Reuse actual variants; independent disabled/busy semantics remain explicit; no replacement primitive |

A boundary change must not move domain rules into the new component or turn a controlled form into a second state owner. Preserve the existing stable key; an intentional record switch may reset state only according to the existing resolved contract. Callback expressions and JSX inside a parent are not automatically component-type declarations.

## Token decision

For this fictional fixture only, the approved role names are `--text-error`, `--border-error`, `--focus-ring`, `--space-md` and `--surface-default`. The foundation owns their raw values and light/dark mappings. No values are invented in this review.

| Property | Accepted treatment | Rejected treatment / reason |
|---|---|---|
| Inline error text | Existing `--text-error` role through project styling convention | Raw `red.600` chosen by appearance; local dark-mode colour override competes with foundation |
| Error border | Existing `--border-error` role | Reusing text-error role merely because it looks similar; roles have different contrast contexts |
| Layout gap | Existing approved spacing scale | A new gap number chosen ad hoc with no design rationale |
| Focus | Existing control/library focus style and approved focus role | Replacing visible focus with error colour or removing it during busy state |
| Actual progress width | Validated bounded numeric progress passed through existing Progress component or scoped runtime custom property | Creating one token per percentage; fabricated progress; unsanitised CSS text from an external response |
| Missing warning role, if newly requested | Inspect existing roles; record D03 gap and dependent decision | Silently create a feature palette or substitute an unrelated success role |

An illustrative declaration such as `color: var(--text-error)` can be valid even in an inline style when that matches project conventions. A utility class can also be semantic-token backed. The syntax is not sufficient evidence either way. Inspect ownership and computed rendering. The hypothetical Progress component's min/max and accessible-value semantics must follow its actual API, not a guessed percentage contract.

## Acceptance and negative cases

| ID | Reproduction | Expected result / evidence required |
|---|---|---|
| CX1 | Type a draft, select text, focus a field; trigger unrelated parent rerender | Draft, selection and focus persist; no unintended remount. Actual rendered interaction evidence, NOT VERIFIED here |
| CX2 | Switch the edited canonical record under the existing explicit reset policy | Only the intended state resets; no draft leaks across record identity; existing unsaved-change policy still applies |
| CX3 | Display error plus focused input in light/dark and busy/disabled combinations reachable in the fixture | Tokens resolve; error/focus retain distinct meaning; relevant contrast and keyboard behaviour meet the chosen target |
| CX4 | Inspect effective token lineage and all affected consumers | Role aliases reach the approved foundation; no local palette/theme override or broken alias is concealed |
| CX5 | Change actual progress from one supplied value to another | Runtime width/accessible value update truthfully without introducing tokens for data; static design values stay governed |
| CX6 | Change only a button label in the same project | Use GOV-04 delta; inspect name/layout. Do not extract unrelated components or reopen the entire token system |
| CX7 | Request a missing token without an approved equivalent | Record D03 and continue independent boundary/inspection work; do not claim styling resolved |

Acceptance statuses are NOT VERIFIED until executed against a real fixture. This example demonstrates how CAP-06/CAP-07 and VIS-07 through VIS-09 divide responsibility; it does not impose React or these token names on other projects.
