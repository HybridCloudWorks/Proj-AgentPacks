---
description: "Add Terraform tests at the right level, from mocked plan checks to gated apply tests"
agent: terraform-expert-engineer
---

# Add Terraform tests

## Inputs

- The module or configuration under test and the behaviours to prove.
- The Terraform version that runs the tests, which decides whether `mock_provider` is available.
- Whether credentials, an isolated account or subscription, a budget and a cleanup owner are authorized for apply-mode or provider acceptance tests.

## Workflow

1. Apply terraform-testing-and-validation to choose a level for each behaviour: `fmt` and `validate` for consistency, plan-mode `run` blocks for logic in a concrete context, mocked providers for configuration logic without credentials, and apply-mode tests only for behaviour that cannot be proven locally.
2. Name each scenario for its intent, and record its inputs, provider mode, assertions, dependencies and cleanup expectation.
3. Cover defaults, validation errors (`expect_failures`), optional resources, `for_each` keys, provider aliases, sensitive outputs, unknown values and replacement behaviour.
4. Version-gate mocks: check the installed Terraform version and the provider schema first. Give computed values deliberate mock shapes, so a mock cannot hide a missing provider configuration or a wrong attribute.
5. Do not raise a module's `required_version` only to run tests; pin the test CLI where the tests run.
6. Run plan-mode and mocked tests locally. Run apply-mode tests only with explicit authorization, in the isolated account, and record the cleanup result. Wire the tests into CI with terraform-ci-cd-and-quality when asked.

## Expected output

The test files; each command with Terraform and provider versions, test mode, credential scope and result; what the mocks do not prove; cleanup status for any apply test; and a completion report. A test that was written but not run is reported as not run. Follow the `terraform-expert-engineer-contract` instruction.
