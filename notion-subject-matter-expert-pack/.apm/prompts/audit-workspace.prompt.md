---
description: "Audit a Notion workspace area for findability, freshness, ownership and sharing exposure"
agent: notion-subject-matter-expert
---

# Audit a Notion workspace area

## Inputs

The teamspace, page tree or databases to audit, the reason for the audit, and any sharing evidence the user or an administrator can supply (the connector usually cannot read permissions).

## Workflow

Apply the audit checklist in notion-workspace-architecture and the schema checks in notion-database-design. Delegate the exposure part to notion-governance-reviewer when delegation is available. Keep the audit read-only: report findings by location and category, and do not quote sensitive content or change sharing to fix what you find.

## Expected output

Located findings with severity, evidence, impact, recommended change and blocking flag; coverage achieved and what could not be seen; a prioritized remediation list for the user to approve. Report as ANALYSIS_ONLY unless the user approved remediation.
