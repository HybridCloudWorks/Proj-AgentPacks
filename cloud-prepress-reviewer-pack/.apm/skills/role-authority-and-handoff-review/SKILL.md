---
name: role-authority-and-handoff-review
description: Verifies agent roles, tool permissions, ownership, reviewer boundaries, handoff contracts, approval gates, and whether the next actor can safely continue the work.
---

# Role, Authority, and Handoff Review

Check that the requested Agent or workflow has the right role, tools, model/runtime assumptions, specialist routes, and authorization boundary. Detect role drift where a reviewer can silently implement, deploy, publish, or change policy.

Verify handoff inputs: changed-file list, requirements, architecture/ADR, environment, preview or test evidence, findings, unresolved risks, required inputs, rollback, owner, and explicit next action. Ensure a reviewer does not claim the implementer or deployment agent completed work.

Treat missing owner, approval, credential ownership, architecture decision, or required input as a human blocker. Keep actionable engineering remediation in TODO/work items rather than hiding it in a human-only REVIEW section.
