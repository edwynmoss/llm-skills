# Worked example: useful review without inventing a defect

Fictional positive-control review. Relevant rules: BGV-03, DB-02, TX-02, DOM-06 and BV-01 through BV-05.

The user asks: “Review this create endpoint; no changes.” Source shows a thin handler calling a use case, a tenant-scoped permission check, a transaction that inserts a record, a database unique constraint on tenant plus external reference, and conflict mapping to the established API error. Unit tests cover mapping; an integration test file appears to cover duplicate creation but has not been executed in this session.

## Proper source conclusion

The reviewer can verify that the inspected source delegates orchestration, scopes authorization, declares the unique invariant and maps the known conflict. They should inspect the actual schema/migration and repository call to confirm the constraint is not merely a comment or mock assumption. If those sources agree, absence of a separate pre-insert exists query is not a defect: the storage constraint is the stronger concurrent guard.

No generic repository interface, distributed lock or Strategy is required merely to satisfy an architecture preference. A focused use case using the existing ORM can be consistent with the repository's design. If all relevant behavior already has an owner, recommend no extraction. Credit the legitimate duplicate rejection and preserve the positive case where a different external reference succeeds.

## Evidence limits and command choice

Reading an integration test establishes intended coverage, not an executed pass. Inspect its runner and fixtures before invoking it. If the test command automatically starts a database, applies migrations and seeds records, a no-change review does not silently authorize that setup. The report can remain complete with database behavior NOT VERIFIED and a precise proposed isolated test.

If an authorized test run is available and fails because the fixture's database service is unreachable, report the command failure and setup stage. Do not label duplicate prevention broken. If the assertion runs and two duplicates are persisted, investigate actual deployed schema, transaction boundaries and expected contract before changing code.

## Example report shape

Scope: inspected handler, use case, schema constraint, conflict mapping and their named callers at the stated revision. Source facts: canonical tenant-scoped identity, one transaction and a declared uniqueness guard. Existing protections: concurrent duplicate prevention is designed at storage, with useful public mapping. Runtime limit: actual selected database and deployed schema were not exercised. Proposed check: two controlled same-reference creates plus a distinct-reference positive control against the authorized test database, asserting canonical rows and both responses.

Cleanup statement should match actual work: no application edits or test setup were performed; inspected working-tree changes were preserved. It should not claim the entire repository was unchanged from a mere status check, nor imply production safety from source review. A report with no confirmed defects can still be precise and useful.
