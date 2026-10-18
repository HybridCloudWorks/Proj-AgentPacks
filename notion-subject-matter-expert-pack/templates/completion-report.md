# Notion work completion report

Use the field names in `tests/report-contract.yml`; `tooling/completion_contract.py` checks a JSON report against it.

- Status: COMPLETE_VERIFIED, PREPARED_NOT_VERIFIED, ANALYSIS_ONLY, CHANGES_REQUIRED or BLOCKED_ON_HUMAN_DECISION.
- Acceptance criteria: each with `id`, a status of passed, failed or unverified, and evidence.
- Notion changes: each with `action` (created, updated, appended, moved, archived, schema_changed), `target`, `location` and `url`.
- Checks: each with `check`, `method` (fetch, command, manual), `status` and `evidence`; command checks also record `exit_code`.
- Placement and links, sources, decisions, permissions and sharing impact, schema impact, data sensitivity, notifications and automations, independent review, unverified items, remaining risks, rollback, follow-ups.

COMPLETE_VERIFIED requires at least one criterion, every criterion and check passed, nothing unverified, and, when the workspace changed, a URL for every change and a passing fetch check. Otherwise choose the status that fits, and when the work cannot be confirmed in the workspace, include the exact sentence: "The Notion work is prepared, but it is not verified in the workspace."
