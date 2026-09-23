## Backend skills and shared standards

Use `backend-spec` for backend contracts and gap analysis, `backend-build` for backend implementation/refactoring, and `backend-verify` for read-only review or authorized behavioral verification. Read the selected skill and only its applicable shared modules. Use across projects when relevant; exclude frontend-only work and unrelated infrastructure administration.

Resolve the maintained library through `BACKEND_DOCS_ROOT` or the installed skill's `library-root.txt`. Each project owns its business rules, API, architecture, database/provider guarantees and operational decisions. Backend and UI skills use the same project-owned contracts; neither creates competing status, validation or permission semantics.

Trace canonical owners, mutation paths and consumers. Keep middleware focused, preserve storage invariants under contention, distinguish rejected/committed/unknown outcomes, and plan legacy-data and deployment compatibility when evolving schemas. Reuse existing capabilities and keep work proportional. Separate source facts, executed assertions and deployed evidence. Skill availability does not authorize migrations, seeding, live queries, replay, load tests, dependency installation, hooks or deployment beyond the user's actual scope.
