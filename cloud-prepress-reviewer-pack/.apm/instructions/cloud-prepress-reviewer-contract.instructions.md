---
description: "Approval, handoff and completion-report rules for the cloud prepress reviewer pack. Always on; the agents, skills and prompts in this pack refer to it."
applyTo: "**"
---
# Cloud prepress reviewer contract

This instruction is installed with the pack so that every agent, skill and prompt can rely on it. It replaces references to pack documents that are not installed.

## Completion report

Pack: cloud-prepress-reviewer.

Recommendations: READY_FOR_PR, READY_FOR_DEPLOYMENT_REVIEW, CHANGES_REQUIRED, BLOCKED_ON_HUMAN_DECISION, NOT_VERIFIED.

Required sections: scope_and_inputs, changed_paths_and_methods, evidence_ledger, findings, skipped_checks_and_limits, architecture_and_adr_status, security_iac_policy_and_identity_status, tests_build_and_preview_status, operations_rollback_cost_and_inputs, unresolved_risks_and_human_blockers, recommendation, engineer_handoff.

Finding fields: id, severity, status, file, line, scenario, impact, recommendation, verification.

Severity: Critical, High, Medium, Low.

Evidence labels: observed, inferred, designed, structurally-validated, preview-verified, live-read-verified, accepted-risk, not-verified.

Never describe an unexecuted check as passed; state what was not verified.
