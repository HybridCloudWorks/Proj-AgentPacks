---
name: review-report-and-pr-gate
description: Produces the final pre-press findings report, merge or deployment recommendation, evidence ledger, unresolved risks, and precise engineer handoff without overstating validation.
---

# Review Report and PR Gate

Report scope, inputs, changed paths, methods, evidence, findings, skipped checks, and authorization boundary. Rank findings Critical/High/Medium/Low; reserve blocking status for proven or contractually required risks. Every finding includes stable ID, severity, file/line, concrete scenario, impact, recommendation, and verification.

Separate confirmed findings, validation hypotheses, accepted risks, and human blockers. Include preview/change counts, tests/build status, security/policy status, architecture/ADR status, cost/operability/rollback status, and secret-handling statement.

End with exactly one recommendation: `READY_FOR_PR`, `READY_FOR_DEPLOYMENT_REVIEW`, `CHANGES_REQUIRED`, `BLOCKED_ON_HUMAN_DECISION`, or `NOT_VERIFIED`. A clean static review is not approval to deploy.
