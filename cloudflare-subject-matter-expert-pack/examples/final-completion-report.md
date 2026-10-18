# Worked completion report

Status: CHANGE_PREPARED_NOT_APPLIED

Outcome: the narrowed WAF exception for `POST /v2/checkout` is prepared and reviewed; it has not been applied to the zone.

| Criterion | Status | Evidence |
|---|---|---|
| Legitimate checkout requests are no longer blocked | unverified | Expected from the scoped skip of one rule ID; needs the change applied and Security Events reviewed |
| No managed rule is disabled beyond that one rule on that path | passed | Ruleset guard output: one modified rule, none removed, no catch-all |
| Broad `/v2/*` exception removed | passed | Proposed rule list and reviewer confirmation |

- Target scope: zone `api.shop.example` (identifier redacted), phase for managed rules, production.
- Files changed: `security/zone-rulesets.json` (proposed list).
- Account changes: none.
- Decisions: skip a single managed rule on one method and path instead of a broader exception.
- Sources consulted: managed ruleset override and traffic sequence documentation, retrieved 2026-10-18.
- Limits and entitlements: the zone's plan includes the managed ruleset in use; confirmed in the dashboard export.
- Checks: `python3 scripts/ruleset_guard.py --current current.json --proposed proposed.json`, environment local, exit code 0, passed, output attached.
- Security review: `cloudflare-security-reviewer` finding High, blocking until the broad exception is replaced; resolved by this change.
- Secrets handling: none involved; the read token stayed in the environment.
- Blast radius: checkout API requests on one zone.
- Cost impact: none.
- Observability: Security Events and checkout error rate watched during rollout.
- Rollout: apply after approval, watch for the agreed window.
- Rollback: re-apply the exported current ruleset.
- Unverified: live behavior after the change.
- Remaining risks: other free-text fields may trigger the same rule on other endpoints.
- Follow-ups: review the rule's matches across the API after one week.

The Cloudflare change is prepared, but its completion is not verified.

The JSON fixtures under `tests/fixtures` exercise the report validator only; they are synthetic and are never reused as a real completion claim.
