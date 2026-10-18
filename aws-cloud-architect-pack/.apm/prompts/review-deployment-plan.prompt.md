---
description: "Review a CloudFormation, CDK or Terraform change for replacement, data loss, drift, policy widening and rollback before anyone applies it"
agent: aws-cloud-architect
---

# Review a deployment plan

## Inputs

- The change evidence: CloudFormation change set, `cdk diff`, `terraform plan`, or the IaC source if the user authorizes a read-only synth, diff or plan.
- Target account, Region and environment, and the deployment identity and pipeline gates.
- The stateful resources in scope and their backup or snapshot status.
- Any mutations the user is asking for (deploy, IAM or SCP edits, stack or resource deletion), each treated as its own request.

## Workflow

1. `aws-iac-deployment-and-lifecycle`: confirm the target, then classify every change as add, modify, replace or delete. Flag replacement of stateful resources, logical-ID or state-address changes, deletion and update-replace policies, termination protection, cross-stack references, lock files and state backups. Keep drift, import, refactoring and rollback as separate workflows.
2. `aws-security-identity-and-compliance`: review IAM, SCP, resource-policy, security-group and key-policy changes for widening, and check the scope of the deployment role.
3. `aws-resilience-dr-and-migration`: for each stateful change, state the data-loss exposure and the recovery path, and confirm that backups exist before the change.
4. `aws-operations-observability-and-troubleshooting`: stabilization signals, alarms to watch during rollout, and the rollback trigger.
5. `aws-docs-mcp-and-evidence`: check version-sensitive CLI, CDK or provider behavior that a finding depends on.
6. `aws-architecture-handoff-and-adr`: update or add an ADR when the review changes a design decision.

## Expected output

- Findings ordered by severity. Each one names the resource, change type, evidence, impact and required fix.
- A go or no-go recommendation with its conditions, and the exact approvals still needed, one per requested mutation.
- A completion report in the contract's format that says which plan or diff was observed and which was not re-run.

## Guardrails

Review is read-only. Running synth, diff or plan needs credentials for the target, so confirm the profile, account and Region first. Do not deploy, execute change sets, apply, import, force-unlock, delete stacks, or modify IAM or SCPs unless the user has given explicit authorization that names the target, the change and the rollback. Confirm again before acting. A single request to "apply, change policy and delete" needs three separate approvals. Follow the `aws-cloud-architect-contract` instruction.
