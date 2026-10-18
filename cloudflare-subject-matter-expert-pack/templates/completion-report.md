# Cloudflare completion report

Status: one of COMPLETE_VERIFIED, CHANGE_PREPARED_NOT_APPLIED, APPLIED_NOT_VERIFIED, ANALYSIS_ONLY, CHANGES_REQUIRED, BLOCKED_ON_HUMAN_DECISION.

Use the field names from `tests/report-contract.yml` when recording the report as JSON; `tooling/completion_contract.py` checks that shape.

| Field | What to record |
|---|---|
| outcome | One or two sentences on what changed or was found |
| acceptance_criteria | Each criterion with id, status (passed, failed, unverified) and evidence |
| target_scope | Account, zone, Worker, environment; redact identifiers in shared copies |
| files_changed | Paths |
| account_changes | Each live change made, or an empty list |
| decisions | Significant choices and why |
| sources_consulted | Documentation pages relied on, with dates |
| limits_and_entitlements | Limits and plan features the work depends on, with sources |
| checks | Each with command, environment (local, preview, staging, production), exit_code, status, evidence |
| security_review | Findings and their resolution |
| secrets_handling | How secrets were set or avoided; never the values |
| blast_radius | Who and what a failure would affect |
| cost_impact | New cost drivers |
| observability | Logs, metrics and alerts added or relied on |
| rollout | How the change reaches traffic |
| rollback | Exact steps and their limits |
| unverified | Everything not proven |
| remaining_risks | Risks after this work |
| followups | Separate next actions |

COMPLETE_VERIFIED needs every criterion passed, every check passed with exit code 0 and evidence, nothing unverified, and, when account changes were made, a passing check in the changed environment. When validation is unavailable, write exactly: "The Cloudflare change is prepared, but its completion is not verified."
