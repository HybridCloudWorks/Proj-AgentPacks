---
name: terraform-testing-and-validation
description: Create and run Terraform validation, unit, plan, mock, integration, and provider acceptance tests while controlling credentials, cost, and cleanup risk.
---

# Terraform Testing and Validation

Use this Skill for .tftest.hcl files, run blocks, assertions, mock providers, test failures, unit or integration scenarios, acceptance tests, and validation evidence.

## Test level

- terraform fmt and terraform validate catch formatting and configuration consistency, not remote API behavior.
- terraform plan checks a concrete variable, provider, and state context but is still not an apply result.
- terraform test can run plan or apply tests. Apply tests can create real infrastructure, cost money, and require reliable cleanup.
- Provider mocks are available only in Terraform versions that support the mock_provider language and should be version-gated. They validate configuration logic, not provider API behavior.
- Provider acceptance tests exercise real APIs and require explicit credentials, quotas, cleanup, and an isolated account or subscription.

## Test design

Make each test scenario name its intent, inputs, provider mode, assertions, dependencies, and cleanup expectations. Test defaults, validation errors, optional resources, for_each keys, provider aliases, sensitive outputs, unknown values, and replacement behavior. Use plan-mode or mocked scenarios for cheap logic checks and reserve apply or acceptance scenarios for behavior that cannot be proven locally.

Use the supplied examples and mock patterns only after checking the installed Terraform version and provider schema. Mock computed values intentionally and do not let a mock hide missing provider configuration or a wrong attribute shape.

## CI and evidence

Run fmt, init with backend disabled when appropriate, validate, tests, lint, and security checks in a deterministic order. Cache providers safely and preserve lock-file checksums. Record exact commands, Terraform/provider versions, test mode, credentials scope, cleanup result, and failures. Never claim full remote coverage from mocks or syntax validation.
