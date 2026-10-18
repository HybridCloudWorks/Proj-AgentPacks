---
description: "Validate Google Cloud infrastructure code with static checks and a plan"
agent: google-cloud-architect
---

# Validate Google Cloud infrastructure code

## Inputs

The Terraform or OpenTofu root module, its variables and backend configuration, the target project or environment, the identity to plan with and the design it should implement. Do not ask for or accept service account key files.

## Workflow

Apply gcp-iac-validation. Run formatting and validation locally, review the code against the design and the guardrails, and run a plan only against the target the user named. Read the plan for replacements, deletions, IAM and exposure changes, then delegate an independent security read to gcp-security-reviewer for high-risk changes. Do not apply, destroy, import or edit state.

## Expected output

Findings with location and severity, the plan summary (adds, changes, replacements, destroys) with risky changes called out, the commands run with targets and exit codes, what the plan cannot prove, and the completion report. Apply the `google-cloud-architect-contract` instruction.
