# Authority and source register

Checked 2026-09-20. This library's detailed rules are engineering guidance authored for the user's stated architecture and traceability requirements. External references support the narrow facts below; they do not supply a complete project policy or proof of local behavior. Recheck exact deployed versions when implementing engine/framework/provider-specific mechanisms. Do not copy a particular vendor's guarantees into another stack.

| Source | Authority and bounded use | Limit |
|---|---|---|
| USER | User requested a general backend counterpart as detailed as the frontend, covering middleware and databases; supplied instructions require canonical ownership, scoped changes, real-boundary validation and cleanup | Does not select business limits, architecture, provider or database for a consuming project |
| POLICY | Maintainer-authored reusable criteria, templates, scenarios and evaluation expectations | Guidance is adopted for this skill; project-specific decisions remain explicit |
| S01: [RFC 9110 HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html) | HTTP method/idempotence and conditional-request semantics | Intended request effects are not a guarantee of identical responses or arbitrary external-effect deduplication |
| S02: [RFC 9457 problem details](https://www.rfc-editor.org/rfc/rfc9457.html) | Standardized HTTP error representation | Does not require replacing a compatible existing error contract or choose domain error codes |
| S03: [OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | Default-deny and authorization checks on relevant requests/resources | Actual roles, sharing, delegation and disclosure are project decisions; source review is not penetration testing |
| S04: [PostgreSQL 18 transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html) | Example of engine-specific isolation and serialization-retry behavior | PostgreSQL example only; not a universal SQL/NoSQL isolation contract |
| S05: [PostgreSQL 18 ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html) | Example of operation-specific DDL locking/validation requirements | Not a zero-downtime guarantee; exact operation, data, version and workload must be verified |
| S06: [RabbitMQ confirms and acknowledgements](https://www.rabbitmq.com/docs/confirms) | Publisher and consumer acknowledgement are distinct boundaries | Does not establish system-wide exactly-once effects or another broker's semantics |
| S07: [OpenTelemetry sensitive-data guidance](https://opentelemetry.io/docs/security/handling-sensitive-data/) | Telemetry needs deliberate minimization and sensitive-data handling | Instrumentation is not a retention/access policy or a compliance certification |
| S08: [Codex skill packaging](https://learn.chatgpt.com/docs/build-skills) | Skill metadata and instructions support selective discovery/loading | Loading does not prove automatic selection, correct decisions or application verification |

The AWS retries article was located but its redirected page did not expose substantive content through the research tool. It is not used as authoritative evidence here. Retry guidance in this library is explicitly authored policy plus the applicable actual protocol/provider contract. No quoted source passages are reproduced.

## Per-project evidence to add

Record current primary framework documentation for middleware ordering, dependency scopes and cancellation; actual driver/ORM documentation for transaction enlistment, tracking and pooling; database documentation for constraints, isolation, DDL and query plans; provider documentation for authentication, paging, limits, retries, idempotency and status lookup; and deployment documentation for lifecycle, identity and configuration precedence. Link exact inspected source and observation dates.

Local implementation, live configuration and business decisions have different owners. A dated runbook can establish historical context; a running artifact/configuration readback establishes current deployment. Keep these evidence types separate and retain unresolved conflicts. No research source authorizes an external mutation or chooses a project's numeric budgets.
