# GitHub evidence ledger template

The record that `github-audit-evidence-and-compliance` asks for: one row per statement, so a reviewer can trace every claim in a completion report to what was observed. Keep it next to the report; it is not posted to GitHub.

## Ledger

| # | Statement | Label | Source | Timestamp (UTC) | Ref or endpoint | Actor | Query or command | Result summary | Sensitivity |
|---|---|---|---|---|---|---|---|---|---|
| E1 | <claim> | <CONFIRMED / INFERRED / HYPOTHESIS / NOT_VERIFIED> | <local file, API, run log, UI> | <yyyy-mm-ddThh:mmZ> | <SHA, `GET /repos/{owner}/{repo}/...`> | <login or App> | <exact read-only command> | <redacted summary> | <public / internal / sensitive> |

Rules:

- Use the label the evidence supports, not the one the conclusion needs. A workflow file is CONFIRMED evidence that the file exists, and at most INFERRED evidence that the feature it configures is enabled.
- Summarize sensitive results (alert payloads, audit-log entries, member lists) by count and category. Never paste secret values.
- When the ledger feeds a completion report, carry the NOT_VERIFIED rows into the report's Skipped checks in lowercase wording, so the report keeps a single recommendation value.

## Readiness coverage

Mark each area covered, partly covered or not covered, and cite ledger rows.

| Area | Coverage | Rows |
|---|---|---|
| Repository identity (host, owner/repo, visibility, archive state) | | |
| Branch protection and ruleset state on the target ref | | |
| Review approvals and CODEOWNERS | | |
| Required status checks on the current head SHA | | |
| Workflow security (permissions, pins, triggers) | | |
| Deployment environment protection | | |
| Security controls (code scanning, secret scanning, Dependabot) | | |
| Artifact provenance (digest, attestation, release) | | |
| Rollback target and owner | | |
| Unresolved exceptions and bypasses | | |

## Close-out

- Scope: <what the ledger covers>
- Limitations: <access the actor lacked, time window, sampling>
- Findings: <finding IDs from the completion report>
- Recommendation: <copied from the completion report>
- Owner: <team or role>
- Next evidence request: <the read that would close the largest gap, and who can run it>
