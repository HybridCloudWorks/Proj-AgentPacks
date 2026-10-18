---
description: "Design HCP Terraform or Terraform Enterprise workspaces, run flow and Stacks"
agent: terraform-expert-engineer
---

# Design an HCP Terraform workflow or Stack

## Inputs

- Organization, project, and the workspaces or Stack; VCS-driven or uploaded configuration; execution mode and agent pools.
- Terraform version, variable sources and variable sets, and whether dynamic provider credentials are available.
- Run tasks, policy sets, auto-apply settings, and who holds which workspace permissions.
- For Stacks: the components, the environments, regions or accounts to deploy to, and any upstream or downstream Stacks.

## Workflow

1. Apply terraform-cloud-and-stacks. Keep HCP Terraform workspaces distinct from Terraform CLI workspaces, and do not assume local files or local credentials exist in remote runs.
2. Design workspace-scoped least privilege. Prefer dynamic provider credentials, agent pools or private networking to static secrets, and control sensitive variables and state access explicitly.
3. Trace the run flow through plan, policy, cost, run tasks, approval and apply, and separate speculative plans from runs that can apply. Record each run task's enforcement level, stage, payload, timeout and failure behaviour; plan JSON sent to a run task is sensitive.
4. Decide whether a Stack fits better than ordinary workspaces. Before writing one, verify CLI and HCP feature availability, current syntax and deployment limits. Components go in `.tfcomponent.hcl` files and deployments in `.tfdeploy.hcl` files; keep component inputs, providers, dependencies, deployment groups and auto-approve conditions explicit, and treat each deployment's state as a boundary.
5. For linked Stacks, write the output contract: what is published, when the consumer reads it, how sensitive it is, and what happens when it fails. A published output is not a secret boundary.
6. Use terraform-state-backends-and-imports to move existing state into workspaces, and terraform-policy-and-governance for policy sets.

Do not queue, approve, cancel or apply runs, change variables or permissions, attach run tasks, or change auto-apply without explicit authorization.

## Expected output

The workspace or Stack configuration; the run-flow and permission design; the variable and credential plan; linked-output contracts; evidence labels that separate local syntax checks from HCP run history or API responses actually retrieved; and a completion report. Follow the `terraform-expert-engineer-contract` instruction.
