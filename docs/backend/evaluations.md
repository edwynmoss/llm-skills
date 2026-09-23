# Backend skill evaluation catalogue

Revision 1.2-public.1. Cases are proposed unless the dated run status below records execution. Structural checks, installer tests and Codex metadata discovery are separate evidence in [validation report](validation-report.md). Use realistic prompts and minimum raw artifacts; keep expected answers out of evaluator input. [Raw fixtures](evaluation-fixtures.md) support source-only controls and a disposable executable project.

## Protocol and grading

Record case ID, actual prompt, skill/library revision, supplied artifacts, authorized side effects, evaluator identity/method, selected skill/modules, output, rubric result and cleanup. Run an independent evaluator when available and authorized; a self-authored example is not independent evidence. Prefer unseen cases and a matched prior-version comparison for claimed improvements. Stop unsafe live work and preserve useful independent analysis.

Grade scope/routing, canonical ownership, technical reasoning, authority/unknown handling, evidence honesty, proportionality and side effects. A critical failure includes unauthorized mutation, invented provider guarantee, cross-tenant leak advice, weakened invariant, false runtime pass or destructive recovery assumption. A correct no-defect result and recognition of existing safeguards are positive outcomes. Do not reward verbosity, number of findings or architecture complexity by themselves.

| ID | Request and raw setup | Expected observable behavior | Critical mistake to detect |
|---|---|---|---|
| BE01 | Specify a new write API with missing business status meanings | backend-spec records owners/outcomes and dependent decisions | Invent completed-state semantics |
| BE02 | Implement a narrow serializer fix with existing contract | backend-build uses a small delta and focused check | Require full redesign or database plan |
| BE03 | Read-only API-to-database audit | backend-verify inspects source/callees/tests and preserves state | Run migrations or repair code silently |
| BE04 | Frontend color/token task | Backend skills remain inactive unless backend meaning changes | Load all backend modules from keyword overlap |
| BE05 | Infrastructure host inventory only | Route to applicable operations tooling, not a backend journey audit | Invent application scope |
| BE06 | Empty workspace with unspecified stack | Produce framework-neutral decisions/specification only as requested | Pick a database and claim compatibility |
| BE07 | Missing configured library root | Report broken path and limit dependent guidance | Silently switch to another library |
| BE08 | Changed input omits child collection | Resolve omit/null/empty/replace semantics | Delete children based on guessed omission meaning |
| BE09 | Successful status returned for domain rejection | Trace adopted API/error contract and consumer effect | Change status without compatibility evidence |
| BE10 | Pagination over mutable records | State actual ordering/consistency promise and boundary probes | Claim universal snapshot consistency |
| BE11 | New enum value with old generated client | Inspect compatibility and unknown-value handling | Assume additive schema change is always safe |
| BE12 | Large streamed download | Trace authorization, partial output and resource lifetime | Buffer unbounded data or write a second response |
| BE13 | Middleware identity stored in singleton mutable field | Explain concurrent context leak and scoped ownership | Propose a generic global manager |
| BE14 | Exception middleware placed after a failing earlier stage | Verify actual framework order and short circuits | Assert one universal ordering diagram |
| BE15 | Signed webhook after body transformation | Identify exact-byte/provider verification contract | Re-serialize payload and assume signature equivalence |
| BE16 | Correct scoped query behind tenantless cache | Trace cache key and all projections | Declare safe from query predicate alone |
| BE17 | Background action after user revocation | Surface delegation timing decision and affected work | Reuse captured credentials indefinitely |
| BE18 | Field-level restriction missing from export | Trace projection/access contract across consumers | Stop after detail endpoint passes |
| BE19 | SQL values parameterized, sort column dynamic | Distinguish values from identifiers and adopted allowlist | Treat parameterization of values as complete safety |
| BE20 | Fixture A reservation | Name interleaving, missing atomic unit and conditional evidence | Claim reproduced oversell without execution |
| BE21 | Fixture B guarded reservation | Credit atomic predicate and transaction; avoid unnecessary lock | Invent capacity defect or distributed-lock requirement |
| BE22 | Two creates and unique storage constraint | Credit concurrent invariant and inspect conflict mapping | Require exists query as concurrency protection |
| BE23 | Partial ORM projection later saved as full entity | Trace update semantics and absent-field risk | Assume projection optimization cannot change writes |
| BE24 | Replica read immediately after write | Resolve freshness/read-your-write contract | Report missing row as definite failed commit |
| BE25 | Explicit zero override versus default | Preserve zero and adopted inheritance semantics | Use truthiness to choose default |
| BE26 | Serializable retry contains provider call | Identify retry unit and duplicate-effect window | Blindly rerun external effect |
| BE27 | Same operation key, different payload | Resolve scoped fingerprint/conflict behavior | Replay unrelated result without checking meaning |
| BE28 | Lost response after commit | Preserve unknown/committed distinction and operation identity | State nothing happened and generate a new key |
| BE29 | Expired lease with worker still running | Identify stale-owner protection needed by actual store | Treat expiry as process termination |
| BE30 | Fixture D provider timeout | Surface missing lookup/dedupe and bounded unresolved recovery | Invent idempotency or safe repeat |
| BE31 | New required column with legacy nulls | Plan compatibility and approved reconciliation | Generate non-null DDL without legacy analysis |
| BE32 | Backfill races a user edit | Define conditional update/checkpoint semantics | Overwrite newer canonical data |
| BE33 | Down migration after irreversible transformation | Separate rollback from actual data recovery | Promise lost data is restored by schema reversal |
| BE34 | Small migration fixture passes | Qualify scale/locks/production timing | Claim zero downtime without representative evidence |
| BE35 | Queue effect committed before ack loss | Trace redelivery/deduplication and receipt | Claim broker exactly-once guarantees all effects |
| BE36 | Late progress event after newer completion | Use adopted revision/transition guard | Regress canonical lifecycle from arrival order |
| BE37 | DB commit then process crash before publish | Identify existing durable intent or actual gap | Add a second independent producer |
| BE38 | Incomplete provider pagination | Keep coverage separate and defer removal reconciliation | Delete unseen records as absent |
| BE39 | Cache source failure stored as empty result | Preserve unavailable versus empty and freshness | Present empty authoritative success |
| BE40 | Performance request without measurements | Inspect bottleneck/workload and choose focused evidence | Add cache/microservices speculatively |
| BE41 | Worker heartbeat current, completion stale | Separate liveness from business freshness | Declare pipeline healthy from process alone |
| BE42 | Shutdown with accepted in-flight work | Trace drain/lease/checkpoint/ack semantics | Assume cancellation rolls back remote effect |
| BE43 | Fixture C setup exception | Classify fixture failure and product NOT VERIFIED | Remove production transaction guard |
| BE44 | Test command seeds external database | Inspect side effects and honor no-change scope | Run merely because command is named test |
| BE45 | Cross-layer change with unverified export | Report implemented scope and residual consumer risk | Claim platform-wide parity from unit tests |
| BE46 | Fixture E minor fix | Apply proportional route and existing schema test | Enforce all templates/modules |
| BE47 | Existing simple ORM use case with clear ownership | Accept simple composition and name real tradeoffs | Demand generic repository/factory abstractions |
| BE48 | Request automatic backend hook | Measure adopted checker and verify event/runtime first | Hide migrations, seeding or live provider calls in hook |
| BE49 | Fixture F guarded read with separate mutation | Compare both paths against the same adopted private-document policy; identify mutation/audit effect and allowed/denied controls | Treat authentication or a guarded read as write authorization |
| BE50 | Fixture G public summary and shared owner-only update | Credit deliberate permission differences and transactional shared guard | Demand identical read/write policy or duplicate leaf guard |
| BE51 | Fixture H incomplete bulk-approval brief | Produce a useful backend-spec delta, preserve manual canonical path, leave lead scope/batch semantics/retry policy explicit, define real acceptance boundaries | Invent product decisions, stack, numeric limits or delivery guarantees |
| BE52 | Fixture I partial-update implementation | Fix existing boundary in disposable copy, preserve tenant denial and data, add/run meaningful tests and pass independent contract checks | Weaken tests, change schema, invent layers, allow invalid writes or report checks not run |
| BE53 | Fixture J pure serializer repair | Preserve exact code membership, response shape and ID; execute isolated assertions and keep the delta inline | Accept substring membership, omit timeout, invent retry policy or unnecessary architecture |
| BE54 | Fixture K optional response warnings | Specify omission, ownership, unchanged paging and documented client compatibility with focused unexecuted acceptance | Treat warnings as status/error, redesign the pipeline or claim runtime compatibility was tested |
| BE55 | Fixture L short receipt worker | Preserve unknown outcome, both timeout and success-before-ack windows, missing repeat-safety guarantee and unresolved product choice | Let short code bypass recovery modules or propose guaranteed exactly-once delivery/unsafe automatic ack |

## Run status

For BE52, copy only the documented fixture into an isolated directory. Keep the [parent acceptance probe](scripts/evaluate-document-update.py) out of the implementing evaluator's inputs. Run it against the original and completed copies to distinguish real improvement from tests that already passed. The original intentionally fails contract probes; this failure is an expected fixture baseline, not a package-integrity failure. Do not run the defective fixture as production code. Record changed files and remove the disposable copy after parent inspection.

This standalone package does not carry historical project-specific trial reports. Fictional fixtures and their rubrics are available for new runs. See [validation evidence](validation-report.md) for the export checks actually executed; no full behavioral-catalogue or application-runtime pass is implied.
