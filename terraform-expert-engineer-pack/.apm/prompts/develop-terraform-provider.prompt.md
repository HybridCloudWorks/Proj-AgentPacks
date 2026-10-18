---
description: "Scaffold, implement and test a Terraform provider with the Plugin Framework in Go"
agent: terraform-expert-engineer
---

# Develop a Terraform provider

## Inputs

- The provider address, the API it wraps, its client library and its authentication model.
- Terraform CLI and plugin protocol targets, the Go version, the framework version pinned in the repository, and any documented SDKv2 requirement.
- The resources, data sources and functions in scope.
- Whether credentials, quotas and an isolated account are authorized for acceptance tests.

## Workflow

1. Apply terraform-provider-development. Use the Terraform Plugin Framework for a new provider unless the repository documents an SDKv2 compatibility requirement.
2. Scaffold only in an intentionally new `terraform-provider-*` workspace. Initialize the Go module and use the pinned framework version.
3. Implement the smallest provider, resource or data source first; pass the API client to resources and data sources through the framework's configured data; remove scaffold placeholders.
4. Run `gofmt`, `go vet` or the repository linter, `go test ./...` and the build. Test locally with developer overrides or an isolated local registry path, never by replacing a shared installation.
5. Test schema and plan behaviour without credentials where possible. Add acceptance tests for create, read, import, update, delete, idempotence, drift, errors and timeouts, and run them only with explicit authorization in the isolated environment.
6. Before any release, review the provider address, versioning, documentation, examples, platform builds, checksums and signing, registry requirements, backward compatibility, state upgrades, importers and sensitive logging.

Do not publish or rotate a provider release without explicit authorization.

## Expected output

The Go diff; a schema summary for each resource or data source; commands and results; acceptance test status (run, with its environment and cleanup, or not run); release-readiness notes; and a completion report. Follow the `terraform-expert-engineer-contract` instruction.
