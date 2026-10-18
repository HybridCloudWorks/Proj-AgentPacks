# Worked example: gradual release of a Worker

Request: "Release the order-intake change to production. Roll back if errors go up." The user approved deploying Worker `orders-api` to the production environment of account "Shop Production" with a 10, 50, 100 percent rollout.

1. Confirm the target (cloudflare-change-control). `wrangler whoami` shows the configured login reaches "Shop Production"; the Worker and environment names match the approval.
2. Snapshot. `wrangler deployments list` and `wrangler versions list` are saved to the workspace; the D1 database is exported before the remote migration.
3. Change plan. Steps, verification and rollback per step are filled into the change-plan template. Rollback trigger: 5xx rate above the pre-release baseline for ten minutes, or any failed checkout synthetic.
4. Execute.
   - Apply the D1 migration to production (approved as part of this release; the code tolerates both schemas).
   - Upload the new version without routing traffic and test its preview URL with the synthetic checks.
   - Shift 10 percent of traffic to the new version; watch Workers Logs, error rates and the synthetics for the window; then 50 percent; then 100 percent.
5. Verify. The production health probe and synthetic checkout pass at 100 percent; error rate is at baseline. Evidence is recorded with environment `production`.
6. Record. The change log lists the version IDs, times, results and the rollback command (`wrangler rollback` to the previous version ID), noting that rollback would not undo the D1 migration.

Report: COMPLETE_VERIFIED, because every criterion passed and verification ran in the changed environment. Had the verification window still been open, the status would have been APPLIED_NOT_VERIFIED.
