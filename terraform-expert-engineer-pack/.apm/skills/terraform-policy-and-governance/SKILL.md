---
name: terraform-policy-and-governance
description: Author, convert, test, and review Terraform policy controls using Sentinel, tfpolicy, and CI policy checks with explicit enforcement boundaries.
---

# Terraform Policy and Governance

Use this Skill for Sentinel, .policy.hcl, .policytest.hcl, tfpolicy, policy conversion, OPA-adjacent checks, plan governance, allowlists, and enforcement design.

## First classify the policy

Identify the input surface: configuration, plan, state, provider schema, resource attributes, related resources, or external inventory. State whether the requirement is advisory, mandatory, pre-plan, post-plan, pre-apply, or CI-only. Separate a direct attribute rule from a graph/reference rule and from a policy that needs external context.

## Authoring

Translate requirements into a small policy with a clear scope, operation handling, parameterized inputs where appropriate, and remediation-focused failure messages. For Sentinel or tfpolicy conversion, preserve intent but flag non-equivalent constructs, especially configuration-reference metadata, module-aware address reconstruction, unresolved values, and cross-resource lookups. Do not label an approximation as a perfect conversion.

Use the installed product documentation for current policy language, functions, operations, and runner behavior. Policy syntax and tfpolicy availability can change; validate with the installed CLI rather than relying on a copied example.

## Testing

Pair policy code with passing, failing, boundary, operation-aware, and missing-data tests. Design mocks for related resources and prior attributes deliberately. Verify whether the runner evaluates mocks outside the policy operation scope and whether data/module targets support expected failure assertions.

## Enforcement review

Map each rule to the stage that can enforce it and the identity that can override it. Review policy bundles, mocks, run tasks, Sentinel enforcement levels, OPA or CI gates, exception expiry, audit evidence, and remediation ownership. Ask before changing mandatory enforcement, downloading sensitive mocks, approving a blocked run, or weakening a policy.
