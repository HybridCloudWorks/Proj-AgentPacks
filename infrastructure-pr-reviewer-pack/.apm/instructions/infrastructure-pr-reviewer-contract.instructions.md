---
description: "Approval, handoff and completion-report rules for the infrastructure pr reviewer pack. Always on; the agents, skills and prompts in this pack refer to it."
applyTo: "**"
---
# Infrastructure pr reviewer contract

This instruction is installed with the pack so that every agent, skill and prompt can rely on it. It replaces references to pack documents that are not installed.

## Completion report

Schema version: 1.0.

Required sections: Executive Summary, Review Scope, Coverage and Evidence, Findings Summary, Findings, Evidence Gaps, Residual Risk, Disposition, Handoff.

Required finding fields: Finding ID, Severity, Confidence, File, Location, Technology, Category, Title, Execution path or trigger, Description, Impact, Remediation direction, Verify with.

Allowed severities: Critical, High, Medium, Low.

Allowed dispositions: Ready for human approval, Ready with conditions, Changes requested, Blocked by a human or external decision, Insufficient evidence for a safe recommendation.

Never describe an unexecuted check as passed; state what was not verified.
