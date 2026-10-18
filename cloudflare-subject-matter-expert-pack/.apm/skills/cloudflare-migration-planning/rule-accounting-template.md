# Migration assessment and rule accounting

## Assessment

- Source stack and versions:
- Artifacts reviewed (file names, export dates):
- Missing exports and assumptions:
- Target account, plan and add-ons:
- Recommended Cloudflare target architecture:
- Success and source-decommission criteria:

## Accounting table

One row per source rule, or several rows when one source rule becomes several Cloudflare objects. The checker in this skill folder reads the same columns from CSV or JSON.

| source_id | source_name | disposition | target | reason | security_impact | owner | owner_decision |
|---|---|---|---|---|---|---|---|
| | | migrated / partial / not_migrated / needs_identity / needs_posture / manual_review | Cloudflare object; required for migrated and partial | required unless migrated | required for partial and not_migrated | required for not_migrated | "accepted" once the owner accepts a partial mapping |

## Counts

| Disposition | Count |
|---|---|
| migrated | |
| partial | |
| not_migrated | |
| needs_identity | |
| needs_posture | |
| manual_review | |

## Prerequisites in order

1. Identity and SCIM
2. Connectors, tunnels and on-ramps
3. DNS and routes
4. Lists and objects
5. TLS inspection exceptions
6. Policies and rules (created disabled or in log mode, with the migration prefix)
7. Logging and alerts

## Waves

| Wave | Scope (users, sites, hostnames) | Switch performed | Parallel-run period | Validation | Rollback steps | Owner |
|---|---|---|---|---|---|---|

## Decisions needed

| Decision | Options | Recommendation | Owner | Due |
|---|---|---|---|---|
