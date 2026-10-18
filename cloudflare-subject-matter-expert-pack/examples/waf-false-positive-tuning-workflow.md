# Worked example: a managed-rule false positive on a checkout API

Request: "Since yesterday some checkout requests to `api.shop.example` get blocked with 403. Fix it without weakening protection." The user put the zone in scope and has a read-scoped token configured.

1. Evidence (Level 0). Sample Ray IDs from the support tickets are looked up in Security Events: every block comes from one managed rule in the OWASP-based ruleset, on `POST /v2/checkout`, triggered by a JSON field containing free-text gift messages. No custom rule or rate limit is involved. Origin lockdown is confirmed: the origin accepts only Cloudflare traffic through Authenticated Origin Pulls.
2. Retrieve. The current documentation for managed ruleset overrides and exceptions is fetched, plus the traffic sequence to confirm where the exception must sit.
3. Independent review. The primary hands the ruleset export and the event summary to `cloudflare-security-reviewer`, which confirms the finding and flags that the existing dashboard exception for `/v2/*` (skip all managed rules) is broader than needed: High severity, blocking for this change.
4. Proposed change. Replace the broad exception with one scoped to `http.request.uri.path eq "/v2/checkout"` and `http.request.method eq "POST"`, skipping only the single rule ID, and keep every other managed rule active. Each rule gets a description with owner and ticket. The full proposed list for the phase is run through the ruleset guard: one rule modified, none removed, no catch-all.
5. Rollout plan for cloudflare-change-control: export the current rulesets, apply the narrowed exception, watch Security Events and checkout error rates for the agreed window, roll back to the export if checkout errors rise.

Report: CHANGE_PREPARED_NOT_APPLIED, with the reviewer's finding attached. The rule change itself is a Level 2 action awaiting approval for this zone and ruleset.
