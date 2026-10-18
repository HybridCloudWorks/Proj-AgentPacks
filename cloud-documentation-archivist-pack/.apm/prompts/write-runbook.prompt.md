---
description: "Create or review an operational runbook, recovery procedure or incident record from alerts, incidents and operator evidence"
agent: cloud-documentation-archivist
---

# Write or review a runbook

## Inputs

- The trigger: an alert, a symptom or a support request. Also the service, environment and severity in scope.
- Evidence: incident timelines, postmortems, alert definitions, dashboards, chat or ticket exports, and existing runbooks.
- The owner or on-call team, the escalation path, and who can authorize each mitigating action.
- For a review: the runbook to review and the incidents or changes since it was last exercised.

## Workflow

1. Apply runbooks-and-operational-docs. Cover the trigger, scope, severity, owner, prerequisites, access, safety checks, decision points, commands, expected results, escalation, rollback, recovery, verification, cleanup and follow-up. Put read-only diagnostics before any change. Record the risks to stateful systems: backups, possible data loss, concurrency and customer impact. The operator must know when to stop and who can authorize the next action.
2. Apply research-synthesis-and-source-traceability to build the timeline and symptoms from cited evidence. Keep confirmed causes apart from hypotheses.
3. Apply docs-security-privacy-and-redaction. Incident material often holds tokens, connection strings, customer names and internal hostnames. Replace each with a placeholder. If you find a live credential, stop and tell the owner it needs containment and rotation; masking it is not enough.
4. Apply templates-and-content-models to choose the runbook or incident-postmortem template.
5. Apply documentation-validation-and-link-checking. Link alerts, dashboards, decision records, change records and postmortems instead of copying them.

Do not run mitigation or recovery commands to test the runbook. Mark the procedure untested until there is evidence of an exercise. In a review, report each problem with the contract's finding fields.

## Expected output

The runbook (and the incident record, if asked for), an honest last-exercised value, an evidence table, any findings, and the files changed.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report. Report an unexercised procedure as NOT_VERIFIED.
