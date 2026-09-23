# Capability selection record

Capability ID / scope / contract revision: [values]. Existing implementation and ownership: [inspected files]. Required success, failure, recovery, accessibility and cleanup behaviour: [rule/state IDs]. Exact runtime/framework versions and dependency constraints: [evidence]. This template does not authorise installing a package.

| Candidate | Already present? | Primary docs/version/date | Required behaviours supported / missing | Runtime compatibility | Maintenance/licence | Accessibility/security evidence | Integration/bundle/migration cost | Disposition and uncertainty |
|---|---|---|---|---|---|---|---|---|
| Native/framework | [value] | [value] | [value] | [value] | [value] | [value] | [value] | [value] |
| Existing package/integration | [value] | [value] | [value] | [value] | [value] | [value] | [value] | [value] |
| Official SDK / established alternative where relevant | [value] | [value] | [value] | [value] | [value] | [value] | [value] | [value] |

Decision: [reuse/configure/compose/extend/replace/custom] and authority. Verified custom gap, if any: [smallest missing behaviour and evidence]. Boundaries and owner: [values]. API/service guarantees to confirm: [values]. Dependencies/lockfile impact and installation authorisation: [values]. Validation and rollback/migration plan: [values]. Unavailable evidence: [explicit fields; do not equate unknown with suitable].

A comparison may be short when a native operation plainly satisfies the contract. A provider integration requires checking the actual official SDK before writing a bespoke HTTP client. Suitability does not follow from popularity or already being installed.
