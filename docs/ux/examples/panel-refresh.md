# Worked example: a failed panel refresh

Illustrative contract EX-PANEL, revision 1. All product facts below are **fictional resolved assumptions for this example only**, not evidence of an application. Behavioural execution: NOT VERIFIED. Purpose: show that a refresh failure in one read-only region need not disable unrelated content.

## Assumed task, authority and foundation

User reads an Activity panel while the independent Notes panel remains editable. Activity API returns records with stable IDs and server `asOf` time; a successful read is authoritative for its request key. Activity does not gate Notes. This example permits last successful activity data for this tab session until access revocation; it is labelled as last updated, never claimed current after failure. No persistent cache. A permission-context revision changes on revocation/sign-out.

Example foundation EF-PANEL-1 is a fully named illustrative mapping: `Region` = semantic section with Activity heading; `InlineNotice` = persistent text under heading; `Button` = native button; `List` = semantic ul; text = 16px/1.5 system UI, heading = 20px/1.4; spacing sm/md = 8/16 CSS px; surface = white, primary text = #111111, muted text = #454545, error text = #8B0000, focus outline = 3px #005FCC with 2px offset; control minimum 44px height; radius = 4px; no shadow, images or theme switch. These are illustration values, not a production design recommendation; no rendered contrast validation has been executed.

Locale en-GB, displayed time `HH:mm UTC` from server time, no implicit device timezone. Test widths 320, 768 and 1280 CSS px plus 200% text resize; at narrow width action wraps below heading, text/list wraps, page owns vertical scroll, nothing sticky. Target assumed WCAG 2.2 AA for the example; keyboard and NVDA/Chrome are named test conditions, not verified support.

Truth map: server owns activity records and asOf; region read owner stores one permitted snapshot and request generation; view derives presentation; independent Notes state is untouched; no documents/exports/integrations are affected in this fictional scope.

## BASE-PANEL-1 (real named inheritance)

All P-* states below explicitly inherit BASE-PANEL-1. Owner = Activity section/read owner. Nature = read-only; blocking scope = Activity only; no writes or action confirmation. Key = `(userContext, permissionRevision, activityScope, requestGeneration)`; only current key may affect UI. Generation increments on every new request/invalidation. Request cleanup aborts transport where supported and always invalidates callbacks.

Anatomy = heading, persistent notice slot, action button, list/empty body. Each row below supplies exact notice, body, button and data certainty. Focus stays on the user's current element during every response, including failure/recovery; if revoked content held focus, move to Activity heading with temporary programmatic focus. Refresh button remains focusable while running using `aria-disabled=true`, with an activation guard and `aria-describedby` notice; Enter/Space and pointer share guard. Other page controls remain available.

One polite live region announces the notice once per accepted state transition; no duplicated alert and toast. List is not a live region. Motion = none, including reduced motion. Long records wrap; full content remains available; no truncation. All rows use EF-PANEL-1 and locale/layout above. No automatic retries/dismissal. Read timeout in this fictional service contract = 15 seconds; reaching it retires the request generation and fails the read, without claiming the underlying list is empty. A late result from that timed-out generation is ignored. User may navigate away anytime; unmount drops region snapshot and callbacks. Sign-out/revocation immediately clears restricted snapshot and invalidates request; late responses cannot restore it.

Rule envelope for every P-* state: applicability = this region only; strength = CONDITIONAL on this fictional feature; status = ILLUSTRATIVE ASSUMPTION; rationale = separate content from refresh availability; exceptions = none within example; dependencies = BASE-PANEL-1, EF-PANEL-1 and fixture API above; evidence = tests PX below, all NOT VERIFIED.

| State | Identity / nature and entry | Visible copy/body and actions | Data, timing and transitions | Deterministic evidence |
|---|---|---|---|---|
| P-INITIAL | No usable snapshot; excludes empty. Read pending, uncertain, recoverable; mount starts g1 | `Loading activity…`; no list; Refresh unavailable, reason in notice | No retained data; accepted nonempty reply -> P-READY, zero -> P-EMPTY, read failure/15s -> P-UNAVAILABLE | PX1: hold first read then deliver success/zero/error separately |
| P-READY | Authoritative nonempty read accepted for current key; freshness = reported asOf | `Last updated {HH:mm UTC}.`; list; Refresh available | Snapshot memory retained; Refresh -> P-REFRESHING; revision remains labelled | PX2: g1 delivers two fixture records and 10:00 UTC; inspect list/time |
| P-EMPTY | Confirmed zero records; excludes no results/goal-completed because no filter/work queue | `No activity yet.` plus `Last updated {HH:mm UTC}.`; empty body; Refresh available | Snapshot zero still records successful asOf; Refresh -> P-REFRESHING | PX3: deliver [] and verify no create CTA is invented |
| P-REFRESHING | Snapshot exists, new read pending; includes previously empty snapshot; uncertain current truth | `Refreshing activity. Showing data from {HH:mm UTC}.`; retained list/empty body; Refresh guarded with reason `Refresh in progress` | Snapshot permitted; no mutation. Latest accepted result -> P-READY/P-EMPTY; error/timeout -> P-FAILED | PX4: retain two records, hold g2, type into Notes; Notes still works |
| P-FAILED | Refresh failed, snapshot remains usable as explicitly dated evidence; excludes write rejection | `We couldn't refresh activity. Showing data from {HH:mm UTC}.`; same list/empty body; button `Retry` available | Persistent until retry/success/navigation; Retry -> P-REFRESHING with new generation; no timer clears error | PX5: fail g2, inspect retained data and persistent notice, retry g3 success |
| P-UNAVAILABLE | Initial read failed; no snapshot; not empty | `We couldn't load activity.`; no list; `Retry` available | Retry -> P-INITIAL; surrounding page intact; no invented cause | PX6: first read fails; Notes still usable; retry yields data |
| P-REVOKED | Permission event revokes current region, certainty = access denied; not transient network error; not user-retryable | `Activity is no longer available to you.`; no restricted body; no Retry; independent page navigation available | Clear snapshot immediately; invalidate read; new access requires authoritative permission context and remount -> P-INITIAL | PX7: revoke during g2 then deliver old success; no data/announcement restored |

Global transitions apply to each P-* state: unmount -> disposed (no DOM, handlers or retained region data); permission revocation -> P-REVOKED; mismatched response -> same state with no side effects. P-REVOKED cannot transition to data on a read response. No error state can transition to empty without authoritative successful zero result. Refresh cannot disable Notes or erase a note draft.

## Acceptance sequence

PX5's expected recovery: load records at 10:00 UTC; focus Refresh and activate; fail g2 with a read error; persistent P-FAILED text appears while records and Notes remain; focus has not moved; activate Retry; deliver g3 records at 10:05 UTC; P-READY notice replaces error and announces once. PX8 race: hold g2, change permission/scope revision, start current read, deliver current result then g2; g2 cannot overwrite, clear notice or announce. Test long activity text with error + focus + narrow width, and keyboard navigation throughout. Test session cleanup and initial-empty versus failed-empty-snapshot distinction.

Evidence to obtain: rendered captures at each state, keyboard/focus and AT observations, controlled network trace of request keys, Notes preservation assertion and real API contract check. All are NOT VERIFIED here. No preview, fake app or test runner was created for this example.
