# General review fixtures

Revision F1, authored for library 1.3. These are fictional, minimal source artifacts and supplied test transcripts, not runnable applications or new product requirements. Names, paths and token roles belong only to each fixture. Source reasoning can be evaluated; browser/native behaviour cannot be certified from these artifacts. Each task is read-only. A supplied transcript is evidence to interpret, not a command the evaluator has executed.

Give an evaluator one scenario's request and artifacts, the entry skill and applicable shared library. Keep expected outcomes, prior findings, run reports and the evaluation catalogue out of the input. Do not install software, create a demo application or access a real repository to complete these tasks.

## Scenario A: browser resource picker

Request: Review this resource picker without changes. Assess recovery, component/style choices and keyboard access. Report source findings and what remains unverified.

Local contract: a failed read must remain distinguishable from a successful empty result; only the latest search can replace visible results. Card navigation may use an optional destination, otherwise `/resources/{id}`. Existing components stay colocated unless another owner or reuse need justifies moving them. Token roles below are approved by this fictional project. Pointer position is runtime data and may use inline geometry. No supported-browser run is available.

`picker-controller.js` (source excerpt, not an executable harness):

```javascript
let revision = 0;
let view = { kind: 'idle', items: [] };
async function search(query) {
  const current = ++revision;
  view = { kind: 'loading', items: [] };
  try {
    const items = await service.search(query);
    if (current !== revision) return;
    view = { kind: items.length ? 'ready' : 'empty', items };
  } catch (error) {
    if (current !== revision) return;
    view = { kind: 'error', items: [], message: 'Could not load resources. Try again.' };
  }
}
```

`picker-view` (template notation):

```text
error branch: ErrorPanel(view.message, retryCurrentQuery)
empty branch: EmptyState('No matching resources')
ready branch: items.map(item => ResourceCard(item))
ResourceCard is a stable module-level component in this feature file.
Each card contains <a href={item.destination || '/resources/' + item.id}>Open {item.title}</a>.
The drag marker uses style.transform = translate(pointerX, pointerY).
The card uses background: var(--surface); color: var(--text-primary).
```

`theme-contract`: `--surface` and `--text-primary` resolve to the project's approved background/text roles in each supported theme. No computed contrast measurements are supplied. Identifiers in this fixture are trusted canonical IDs; no route-encoding variation is under review. `retryCurrentQuery` reruns `search` with the unchanged input. No business rule or persistence change is requested.

## Scenario B: overlay test transcript

Request: Assess these test failures without changing code. State what they establish about the overlay, whether the intended assertions ran, and the smallest next step.

Local contract: hidden overlay roots must not dismiss a visible overlay; each outside pointer activation must have at most one callback pending. The test uses a platform-element double. The real platform element supports `getClientRects()`.

`overlay.js`:

```javascript
function visibleRoots(roots) {
  return roots.filter(root => root.getClientRects().length > 0);
}
```

`overlay.test.js` setup excerpt:

```javascript
const root = { contains: () => false };
registerOverlay(root, callback);
dispatchOutsidePointer(); // visibility filtering runs here, before assertions
```

Supplied transcript from fixture environment T1:

```text
command: node --test overlay.test.js
exit: 1
test: releases rejected callback listener - FAILED
test: prevents overlapping callbacks - FAILED
TypeError: root.getClientRects is not a function
at overlay.js:2
both traces terminate during dispatchOutsidePointer, before assertions
```

No real-browser trace, complete callback implementation or successful rerun is supplied. The evaluator has not executed this command.

## Scenario C: native review queue

Request: Review this native desktop review queue without changes. Trace the displayed count and detail access. Use its existing platform; do not redesign it as a web application.

Local contract: the service owns review status. The displayed pending count must equal the service projection after reconciliation. Repeating completion of an already-completed item succeeds without changing persisted status. Every row has a detail screen; `externalDestination` is optional. A native Button supports the platform's keyboard activation. Row pointer gestures alone do not expose a keyboard action. The row remains mounted during actions. No native runtime is supplied.

`queue-presenter` (framework-neutral pseudocode):

```text
complete(id):
    result = await service.complete(id)
    if result.success:
        items[id].complete = true
        pendingCount = max(0, pendingCount - 1)

open(item):
    navigate(item.externalDestination ?? detailRoute(item.id))
```

`queue-view`:

```text
Row(item):
    onPointerTap: open(item)
    if item.externalDestination exists:
        NativeButton(accessibleName='Open details', activate=open(item))
    if not item.complete:
        NativeButton(accessibleName='Complete', activate=complete(item.id))
```

There is no per-item pending guard or action queue. Calls can overlap while awaiting the service. Two responses for the same item may both return success. The count initially includes multiple pending items. Only the shown actions can navigate from this row; no hidden shared keyboard action exists. The service is scoped to the current authorised user; permission enforcement is outside this review. No response-order experiment or reload has been executed.
