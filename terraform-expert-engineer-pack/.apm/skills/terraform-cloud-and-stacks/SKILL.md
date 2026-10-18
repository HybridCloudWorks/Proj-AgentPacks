---
name: terraform-cloud-and-stacks
description: Work with HCP Terraform and Terraform Enterprise workspaces, remote runs, variables, policies, run tasks, registries, Stacks, deployments, and linked outputs.
---

# HCP Terraform, Enterprise, and Stacks

Use this Skill for HCP Terraform, Terraform Enterprise, workspace operations, remote execution, run tasks, Sentinel stages, variable sets, private registry, Stacks, deployment groups, publish_output, upstream_input, or the HCP Terraform API.

## Workspace model

Separate HCP Terraform workspaces from Terraform CLI workspaces. Establish organization, project, workspace, VCS or uploaded configuration, execution mode, Terraform version, variable sources, state ownership, permissions, and auto-apply behavior. HCP workspaces retain state history and run history; do not assume local files or local credentials are present in remote operations.

Prefer workspace-scoped least privilege. Sensitive variables and state access need explicit control. Review whether dynamic provider credentials, agent pools, private networking, or variable sets are available before introducing static secrets.

## Run and policy flow

Trace pending, fetch, plan, policy, cost, run-task, approval, apply, and completion states. Distinguish speculative plans from runs that can apply. Run tasks may be advisory or mandatory; record enforcement level, stage, external payload, timeout, and failure behavior. Treat plan JSON sent to external run tasks as sensitive.

Do not queue, approve, cancel, apply, change variables, modify permissions, attach run tasks, or alter auto-apply without explicit authorization. Static workspace configuration is not proof of a live run.

## Terraform Stacks

Use component files ending in .tfcomponent.hcl for reusable infrastructure components and deployment files ending in .tfdeploy.hcl for repeated environment, region, or account deployments. Keep component inputs, provider configuration, dependencies, deployment groups, auto-approve conditions, and linked outputs explicit. Treat each deployment's isolated state as a boundary.

Before using Stacks, verify CLI and HCP feature availability, current syntax, deployment limits, provider/module sources, and whether ordinary workspaces are a better fit. For linked Stacks, document the upstream output contract, consumer timing, sensitivity, and failure behavior; do not treat a published output as a secret boundary.

## Evidence

Use HCP run history, logs, state versions, plan, policy results, and API responses as live evidence only when actually retrieved. Label local syntax checks and generated examples as structural evidence.
