---
name: azure-deployment-and-lifecycle
description: Plans safe Azure deployment, what-if, validation, deployment-stack, CI/CD, OIDC, drift, rollback, change review, and post-deployment lifecycle workflows.
---

# Azure Deployment and Lifecycle

Use read-only validation first. For Bicep/ARM, use `validate`, preflight, and `what-if` at the correct resource-group, subscription, management-group, or tenant scope. Interpret false positives, unresolved expressions, permissions, and provider validation limits. Do not treat what-if as proof that a deployment will succeed.

Use deployment stacks when managed-resource ownership and explicit detach/delete behavior are required; do not use deletion-capable modes casually. For Terraform, require init/validate/format/lint, plan review, state-lock awareness, policy checks, and approval before apply.

Review pipeline identity, OIDC subject, permissions, action/provider pinning, environment approvals, artifact provenance, secrets, rollback, and post-deployment health. Never apply, force-unlock, import, destroy, or change shared platform scope without explicit authorization.
