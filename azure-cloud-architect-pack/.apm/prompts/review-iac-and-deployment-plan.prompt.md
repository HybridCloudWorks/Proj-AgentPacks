---
description: "Review Bicep, ARM or Terraform/AVM changes and their what-if or plan output for replacement risk, identity, state, drift and production gates"
agent: azure-cloud-architect
---

# Review Azure IaC and its deployment plan

## Inputs

The repository, branch or diff; the what-if or plan output and the commit it was produced from; the target scope (resource group, subscription, management group or tenant); the pipeline definition; the deployment identity and its federation; the state backend; and module and provider versions. If no plan or what-if output is supplied, say so; do not infer one.

## Workflow

1. Apply `azure-iac-avm-and-repo-standardization`: check the tool choice against ownership and scope, version pinning and lock files, remote and locked state, secrets in code or state, module interfaces, and current AVM specification requirements. Any rename of a live address or resource needs a migration plan, a moved or import strategy, and plan evidence.
2. Apply `azure-deployment-and-lifecycle`: confirm validation and what-if ran at the correct scope, or that a Terraform plan was reviewed with state locking. Interpret replacements, deletions, false positives and unresolved expressions. Review deployment-stack detach and delete behaviour, pipeline approvals, action and provider pinning, artifact provenance, rollback and post-deployment health checks.
3. Apply `azure-security-identity-and-compliance` to the deployment identity: issuer, subject, audience, scopes, owner, token lifetime, and whether pull-request runs can obtain production write access.
4. Apply `azure-resilience-dr-and-migration` to any stateful resource the plan replaces or deletes, and `azure-docs-mcp-and-evidence` to provider, API and module versions the change depends on.

The review is read-only. Run only checks that need no cloud credentials (format, validate, lint) unless the user authorizes more. Never apply, deploy, destroy, import, move state or force-unlock. If the user also asks to apply, review first, and apply only on explicit, scoped authorization with plan evidence for the exact commit, a rollback point and the pipeline's own approval gate.

## Expected output

- Findings ordered by severity, each with location, evidence and its label, impact, remediation, and whether it blocks the change.
- The checks actually run, with exit codes, and the checks not run.
- Additive standardization recommendations, kept separate from blocking findings.
- A completion report that states plainly whether the change is safe to proceed, blocked, or unverified.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
