# Backend coverage and gap analysis

Use with [governance](governance.md) and [service contract](templates/service-contract.md). This is an applicability-driven review, not a requirement to add every feature. Start from one concrete journey, inspect its real owners and choose the smallest meaningful scope. A gap can be missing authority, missing behavior, a test deficiency or an evidence limit; keep those categories separate.

| Concern | Question to resolve from evidence | Existing protection to credit | Typical failure to investigate | Required next evidence |
|---|---|---|---|---|
| API meaning | What does accepted/success/unknown mean to each caller? | Existing schema and stable error mapping | 200 hides rejection, timeout reported as no effect, omitted input clears data | Request/response and canonical state assertion |
| Domain ownership | Which owner enforces the invariant for every writer? | Shared use case/policy and lifecycle guard | Import/job bypasses approval, duplicate calculations drift | Trace manual and alternative paths |
| Middleware | What actually runs and short-circuits? | Verified framework registration and scoped context | Bypass route, wrong order, swallowed cancellation, leaked tenant | Actual host-pipeline positive/negative trace |
| Authorization | Who may act on which object/field and when? | Scoped selectors, object policy, field projection | Cross-tenant join/cache/export, stale delegation | Principal/tenant matrix at real boundary |
| Persistence | What prevents invalid stored state under contention? | Unique/check/FK/conditional-write guarantee | Precheck race, orphan, precision loss, absent field overwrite | Selected-engine invalid/concurrent write |
| Transactions | What is atomic and where can outcome be unknown? | Existing guarded transaction and receipt | Split connection, lost update, duplicate remote effect | Controlled interleaving and crash-window assertion |
| Migrations | Can existing data and old/new versions coexist? | Compatible phased migration and rehearsed restore | Locking rewrite, unhandled legacy rows, old writer drops new state | Representative upgrade and compatibility rehearsal |
| Async work | What does each acknowledgement prove? | Durable work record and idempotent completion | Lost publication, duplicate completion, stale event, orphan retry | Broker/consumer/effect failure sequence |
| Integrations | Which guarantees are documented and exercised? | Existing adapter, bounded retry and outcome lookup | Incomplete pagination deletes records, retry multiplies effects | Exact provider contract and authorized probe |
| Cache/performance | What is the source, freshness contract and bottleneck? | Correct key dimensions, invalidation and measured query | Cross-context reuse, stale revocation, stampede, unbounded fan-out | Update/revoke/failure plus comparable workload |
| Operations | What does health/freshness mean and who responds? | Existing owner/routing/checkpoint | Alive worker with stale results, duplicate timer, secret telemetry | Signal semantics, controlled failure/recovery |
| Verification | Did the intended assertion execute against the right boundary? | Meaningful existing integration/contract tests | Fixture crash mislabeled defect, mock pass called database proof | Exact command/setup/assertion/environment |

For each selected gap record: scenario; applicability/rule IDs; observed source; authority; category; consequence; smallest addition or decision; owner; verification; and dependent consumers. Do not treat absence of a standalone document as proof the code lacks a contract; inspect schema, tests and shared guards first. Conversely, a document promising idempotency does not prove the implementation honors it.

Prioritize concrete consequence over architectural taste: unauthorized access, lost/duplicated effects and corrupted canonical relationships differ from an optional abstraction improvement. Severity does not increase evidence certainty. A source-only race hypothesis remains conditional until the actual interleaving or a sufficient proof is established. Credit valid positive controls and allow a no-defect result.

When the user requests all writers/consumers or no regression, expand the matrix to every affected path rather than silently sampling one. If a consumer cannot be accessed, record it as an unresolved risk. A complete gap-analysis report can still contain unverified runtime assertions, but it cannot claim complete application parity.
