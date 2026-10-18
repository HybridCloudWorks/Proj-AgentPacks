---
name: tests-build-and-dependency-review
description: Verifies that changed code, infrastructure, containers, dependencies, and configuration have appropriate build, test, lint, package, and regression evidence.
---

# Tests, Build, and Dependency Review

Map changed behavior to unit, integration, end-to-end, negative-path, security, migration, and infrastructure tests. Review whether assertions prove behavior rather than implementation detail and whether environment assumptions are explicit.

Check build and package commands, lock files, dependency changes, vulnerability or license gates where present, Docker build context, `npm ci` lock requirements, generated artifacts, Bicep compilation, Terraform formatting/validation, and unresolved AZD template variables such as `{{ .Env.* }}`.

Report skipped checks and the reason. Do not claim "all tests passed" when only static checks ran or when a required tool/environment was unavailable.
