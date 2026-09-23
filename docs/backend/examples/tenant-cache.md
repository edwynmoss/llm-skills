# Worked example: a correct query behind an incorrectly scoped cache

Fictional example. Relevant rules: SEC-01 through SEC-03, CACHE-01 through CACHE-03, DB-07 and BV-02. No real tenant data is involved.

An endpoint returns a tenant's project summary. Its database query correctly filters by trusted tenant ID and object permission. The cache key contains only project ID and requested month. Local project IDs can overlap across tenants, so the first tenant's cached projection can be served to a second tenant without executing the correct query. The existence of a safe query does not establish cache isolation.

## Ownership and repair scope

The database record remains authoritative. The cached summary is a projection with a key that must distinguish the contexts affecting its contents. Tenant is required here; permission/role dimensions or field projection may also matter. Do not automatically place a full token or unbounded user identity in the key. Inspect the actual sharing policy and define a bounded representation of the relevant authorization context.

Trace every summary consumer: detail UI, list totals, export and background email if present. Determine whether each uses the same cache and whether mutations invalidate all required projections. Fixing one endpoint key does not prove an export no longer reads the old cache. If a rollout changes the cache schema/key, plan old entries and old application instances rather than flushing all products' caches indiscriminately.

Permission revocation introduces a separate freshness decision. A correctly tenant-scoped cached summary can still contain fields no longer visible to the caller. Decide whether current permission is checked before serving, entries are invalidated, or an explicit short-lived delegation applies. A TTL chosen for performance is not automatically an accepted access-revocation policy.

## Controlled evidence

Create two synthetic tenants with the same local project ID and different summary values. Warm the cache through tenant A, then request through B and assert B's authorized data. Repeat with roles that differ in field visibility. Test legitimate sharing if the project supports it; denying all cross-tenant access would break that positive control.

Update a summary input and reload under the adopted read-after-write promise. Revoke a role and verify the agreed access behavior. Fail the source during refresh and prove the cache does not turn unavailable into an empty authoritative result. Inspect the actual cache key/value and final response in an authorized test environment.

If the code already includes tenant and permission-aware projection plus correct invalidation, the review should not manufacture a defect from the mere presence of caching. Remaining evidence may concern multi-instance invalidation or old-entry compatibility. Report those boundaries specifically rather than claiming a complete security audit from one cache fixture.
