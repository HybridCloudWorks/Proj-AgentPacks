---
description: "Author, convert or test a Terraform policy and map where it is enforced"
agent: terraform-expert-engineer
---

# Author or convert a Terraform policy

## Inputs

- The requirement in plain words and the resources it governs.
- The policy framework and runner available (Sentinel, tfpolicy, or a CI policy check) and their installed versions.
- An existing policy to convert, if any, and the current and wanted enforcement level.

## Workflow

1. Apply terraform-policy-and-governance. Classify the input surface (configuration, plan, state, provider schema, resource attributes, related resources or external inventory) and the stage (advisory or mandatory; pre-plan, post-plan, pre-apply or CI-only). Separate direct attribute rules from graph or reference rules, and from rules that need external context.
2. Write a small policy with a clear scope, operation handling, parameters where useful, and failure messages that tell the author how to fix the resource.
3. When converting, preserve intent and flag every construct that does not translate exactly: configuration-reference metadata, module-aware address reconstruction, unresolved values and cross-resource lookups. Label an approximation as an approximation.
4. Pair the policy with passing, failing, boundary, operation-aware and missing-data tests. Design mocks for related resources and prior attributes deliberately.
5. Check current syntax and runner behaviour with the installed CLI, not a copied example. If the runner is not installed, say the tests were not run.
6. Map each rule to the stage that enforces it and the identity that can override it. Use terraform-cloud-and-stacks for HCP Terraform policy sets and run tasks, and terraform-ci-cd-and-quality for CI gates.

Ask before changing mandatory enforcement, downloading sensitive mocks, approving a blocked run or weakening a policy.

## Expected output

The policy and its tests; conversion notes that list every non-equivalent construct; test results from the installed runner, or a statement that it was unavailable; the enforcement map; and a completion report. Follow the `terraform-expert-engineer-contract` instruction.
