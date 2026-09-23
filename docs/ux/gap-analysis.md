# UI coverage and gap analysis

Use this matrix to inspect a consuming project's actual contracts. It is general guidance, not a historical application audit. A gap can be a missing decision, missing implementation, absent evidence or an inapplicable concern. Do not infer a defect from an unfamiliar design or require features solely to fill the matrix. Keep a small change to its affected delta.

| Concern | Evidence to inspect | Failure or uncertainty to resolve | Governing reference |
|---|---|---|---|
| Authority and conflicting advice | Project instructions, accepted contracts and provenance of supplied advice | A transcript, example or generic recommendation is promoted to product policy | [Governance](governance.md) |
| Task and canonical ownership | User goal, entities, stable identifiers, producers and consumers | Visually similar journeys update different records or meanings | [Governance](governance.md), [state contract](templates/state-contract.md) |
| State granularity | Independent regions, actions, fields and their transitions | One global loading/error flag hides recovery or disables unrelated work | [States](modules/states.md) |
| Stale and competing results | Operation identity, input revision, permission changes, relevant writers | Late results overwrite newer state or resurrect restricted content | [States](modules/states.md) |
| Unknown mutation outcomes | Actual API outcome, idempotency and lookup guarantees | Timeout is reported as definite failure and repeated unsafely | [States](modules/states.md), [decisions](decisions.md) |
| Record conflicts | Authoritative version and existing edit/merge policy | Concurrent valid edits silently overwrite each other | [States](modules/states.md) |
| Navigation and restoration | History, route/filter state, dirty drafts, reload behavior | Back restores a URL with the wrong data revision or loses permitted work | [Workflows](modules/workflows-content.md) |
| Discovery and choice | Task vocabulary, target users, conventions and representative tasks | Numerical law quotas or hidden choices make completion harder | [UX reasoning](modules/ux-reasoning.md) |
| Consequences and informed choice | Material effects, defaults, decline/exit and supported reversal | Emphasis or obstruction conceals the actual commitment | [UX reasoning](modules/ux-reasoning.md) |
| Component responsibility | Existing primitives, page composition, state and domain boundaries | Independent editors live inside oversized pages or new wrappers duplicate state | [Capabilities](modules/capabilities.md) |
| Component identity | Framework type/key identity, intended reset policy and parent updates | Refactoring remounts a field and loses draft, focus or selection | [Capabilities](modules/capabilities.md) |
| Tokens and visual states | Approved definitions, alias lineage, themes, variants and combinations | A semantic-looking token has the wrong role or fails in a supported mode | [Visual components](modules/visual-components.md) |
| Runtime geometry | Source of style values and actual project exception policy | Dynamic progress is forced into tokens, or design values bypass governance | [Visual components](modules/visual-components.md) |
| Overlays and responsive layout | Focus return, dismissal, nested layers and supported viewport transforms | Focus returns to a removed trigger or required content becomes unreachable | [Visual components](modules/visual-components.md), [accessibility](modules/accessibility.md) |
| Validation authority and timing | Domain schema, server errors, field/group dependencies and adopted submit policy | UI invents business limits or treats blur/disabled Submit as universal law | [Validation](modules/validation.md) |
| Correction and asynchronous validation | Current values, dependencies, pending requests and field error ownership | An obsolete rejection remains after correction or unavailable validation becomes valid | [Validation](modules/validation.md) |
| Input methods and legacy data | Composition, paste, autofill, localization and invalid existing values | Incomplete composition submits, or imported invalid data appears pristine and valid | [Validation](modules/validation.md) |
| Bulk work and partial success | Selection universe, per-item identities/outcomes and actual permissions | A filter change changes the operation's scope or one success hides failures | [Workflows](modules/workflows-content.md) |
| Uploads and imports | Provider capabilities, processing states, source identity and reconciliation | A completed upload is mistaken for processing success; reruns duplicate records | [Workflows](modules/workflows-content.md), [capabilities](modules/capabilities.md) |
| Time and content meaning | Units, timezones, date-only/instant distinction, unknown/empty/zero | An ambiguous local time or missing amount is silently assigned a false value | [Workflows](modules/workflows-content.md) |
| Accessibility | Semantics, keyboard, focus, announcements, contrast and supported assistive input | Visual success is treated as accessible task completion | [Accessibility](modules/accessibility.md) |
| Comprehension and interruption | Actual audience, task context, support needs and interrupted journeys | A mechanically operable flow still leaves users unable to understand the next step | [Accessibility](modules/accessibility.md), [UX reasoning](modules/ux-reasoning.md) |
| Resource failure and reconnect | Existing frontend/runtime failure boundaries and retry policy | The error UI never loads, or reconnect replays an uncertain mutation | [Capabilities](modules/capabilities.md), [states](modules/states.md) |
| Assistance handoff | Real supported channel, authorized context and return path | Endless retry replaces needed help, or handoff leaks data/duplicates an action | [Workflows](modules/workflows-content.md) |
| Product AI behavior | Capability limits, uncertain outputs, user corrections and action authority | A suggestion becomes canonical truth or regeneration overwrites a correction | [AI interactions](modules/ai-interactions.md); applies only to products with AI behavior |
| Capability reuse | Existing framework/provider features and actual required guarantees | Custom infrastructure duplicates a solved capability or assumes unsupported recovery | [Capabilities](modules/capabilities.md) |
| Evidence and test failures | Source, fixture setup, executed assertions and real runtime boundaries | A runner failure is reported as a product defect; a scanner pass becomes a UX certification | [Verification](modules/verification.md) |
| Small-change proportionality | Requested delta, inherited contracts and concrete dependencies | A label fix triggers a redesign, new architecture or every optional template | [Governance](governance.md) |

## Review and handoff

For each applicable concern, record the authoritative owner, observed protection, unresolved behavior or decision, consequence, and smallest confirming/refuting check. Credit existing shared guards and correct implementations. Separate source facts from executed assertions and runtime hypotheses. A supplied test transcript is evidence to interpret, not a command the current reviewer ran.

Trace affected writers and consumers when business meaning changes. Keep unresolved limits explicit; do not invent status, validation, permissions, support channels or provider guarantees. Use the [decision register](decisions.md) and [acceptance template](templates/acceptance.md) where their structure helps. Review-only work does not authorize implementation, installation, hooks or application mutations.

The [evaluation catalogue](evaluations.md) and [fictional fixtures](evaluation-fixtures.md) provide positive, negative and evidence-attribution controls. They do not establish rendered behavior or automatic skill selection until those boundaries are actually exercised and recorded.
