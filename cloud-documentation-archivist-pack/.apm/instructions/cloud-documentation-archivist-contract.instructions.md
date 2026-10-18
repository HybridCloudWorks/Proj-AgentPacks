---
description: "Approval, handoff and completion-report rules for the cloud documentation archivist pack. Always on; the agents, skills and prompts in this pack refer to it."
applyTo: "**"
---
# Cloud documentation archivist contract

This instruction is installed with the pack so that every agent, skill and prompt can rely on it. It replaces references to pack documents that are not installed.

## Completion report

Recommendations: DOCUMENTATION_READY, REVIEW_REQUIRED, CHANGES_REQUIRED, BLOCKED_ON_SOURCE_OR_OWNER, NOT_VERIFIED.

Required sections: Scope and audience, Source and evidence, Content decision, Validation, Limitations, Ownership and next review.

Finding fields: id, severity, source, impact, remediation, verification.

Redaction: Reject secret-like, private-key, credential, customer-data, and personal-data values.

Never describe an unexecuted check as passed; state what was not verified.
