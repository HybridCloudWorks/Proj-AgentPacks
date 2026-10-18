---
name: aws-iac-deployment-and-lifecycle
description: Turn AWS architecture into safe CloudFormation, CDK, or Terraform implementation plans with validation, change review, drift, rollback, and lifecycle controls.
---

# AWS IaC, Deployment, and Lifecycle

Use this Skill for CloudFormation, CDK, Terraform-aware architecture, CI/CD, change sets, synth/diff/plan, deployment gates, drift, import, refactoring, rollback, and deletion protection.

## Implementation contract

Specify ownership, repository boundaries, stack/module/component boundaries, environments, account/Region targets, bootstrap prerequisites, parameter/secret sources, provider/version constraints, tags, state, dependencies, outputs, and policy checks. Prefer small composable units and explicit interfaces.

## Safe change workflow

Validate syntax/schema and policy, synth or plan, review the change set/plan, assess replacement and data-loss risk, approve through protected gates, deploy in an isolated environment, observe stabilization, and record rollback. Preserve lock files, state backups/versioning, CloudFormation termination protection, deletion/update-replace policies, and CDK logical-ID stability for stateful resources.

Drift, import, refactoring, and rollback are separate workflows. Do not use state mutation, force unlock, stack deletion, or broad permissions to solve an unclear deployment failure. Read current product docs for version-sensitive CLI flags and behavior.
