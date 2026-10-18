---
name: terraform-provider-development
description: Scaffold, implement, test, debug, and publish Terraform providers with the Terraform Plugin Framework and Go when provider development is in scope.
---

# Terraform Provider Development

Use this Skill for new Terraform providers, Plugin Framework provider servers, resources, data sources, functions, provider configuration, Go scaffolding, protocol compatibility, provider tests, and registry publishing.

## Choose the framework

For new providers, prefer the current Terraform Plugin Framework unless the repository has a documented SDKv2 compatibility requirement. Establish Terraform CLI and protocol version targets, provider address, Go version, API client behavior, authentication, and supported platforms before scaffolding.

The provider server is the executable boundary Terraform starts. The provider exposes schemas, configuration, resources, data sources, and optional functions. Keep API clients and provider-level data available to resource and data-source implementations through the framework's configured data flow.

## Development loop

Scaffold a new provider only in an intentionally new terraform-provider-* workspace. Initialize Go modules, use the repository's pinned framework version, implement the smallest provider/resource or data source, remove scaffold placeholders, run gofmt, go vet or repository lint, go test ./..., and build. Use developer overrides or an isolated local registry path for local CLI testing.

Test schema and plan behavior without credentials where possible, then add acceptance tests for real API semantics, import, update, delete, idempotence, drift, errors, and timeouts. Acceptance tests need explicit credentials, cleanup, quotas, and an isolated environment.

## Release review

Check provider address, versioning, documentation, generated examples, platform builds, checksums/signing, registry requirements, backward compatibility, state upgrades, importers, and sensitive logging. Do not publish or rotate a provider release without explicit authorization.
