---
description: "Approval, handoff and completion-report rules for the terraform expert engineer pack. Always on; the agents, skills and prompts in this pack refer to it."
applyTo: "**"
---
# Terraform expert engineer contract

This instruction is installed with the pack so that every agent, skill and prompt can rely on it. It replaces references to pack documents that are not installed.

## Completion report

Pack: terraform-expert-engineer.

Required sections: objective, scope_and_authorization, changed_files, commands_and_results, plan_or_state_impact, evidence_classification, risks_and_limitations, next_safe_action.

Rules: redact state, plan, credentials, sensitive variables, and backend secrets, distinguish static, local, live-cloud, inferred, and unavailable evidence, do not claim apply, lock, policy, HCP, AVM certification, or provider acceptance proof without direct evidence, ask before apply, destroy, state mutation, force-unlock, HCP permission changes, policy weakening, or production work.

Never describe an unexecuted check as passed; state what was not verified.
