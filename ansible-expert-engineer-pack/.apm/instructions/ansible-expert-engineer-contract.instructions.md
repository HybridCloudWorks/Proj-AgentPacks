---
description: "Approval, handoff and completion-report rules for the ansible expert engineer pack. Always on; the agents, skills and prompts in this pack refer to it."
applyTo: "**"
---
# Ansible expert engineer contract

This instruction is installed with the pack so that every agent, skill and prompt can rely on it. It replaces references to pack documents that are not installed.

## Completion report

Required sections: result, evidence, changed_files_or_proposal, unresolved_risks, next_safe_action.

Required distinctions: observed_fact_vs_inference, skipped_check_vs_passed_check, local_validation_vs_remote_proof, dry_run_vs_real_execution.

Never describe an unexecuted check as passed; state what was not verified.
