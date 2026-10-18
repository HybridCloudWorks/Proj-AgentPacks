---
name: terraform-modules-and-refactoring
description: Design, review, version, test, publish, and safely refactor Terraform modules without breaking state addresses or consumer contracts.
---

# Terraform Modules and Refactoring

Use this Skill for module boundaries, reusable interfaces, module publication, resource address changes, moved blocks, breaking changes, and module upgrade plans.

## Module design

- Define a small interface around a coherent capability; do not expose whole provider resource objects as outputs.
- Document every input and output, type collections precisely, and keep defaults meaningful and safe.
- Let the root module configure providers. Child modules declare provider requirements and accept passed configurations or aliases.
- Pin registry module versions in consumers and preserve the provider dependency lock file in root configurations.
- Separate stable public interface from implementation details; use examples and tests to define expected behavior.
- Do not add an enabled or module_depends_on switch to disable an entire module. Use narrowly scoped feature controls for optional resources.

## Safe refactoring

Before changing addresses, map current state addresses, dependencies, consumers, and expected plan impact. Prefer configuration moved blocks for published or long-lived modules. Chain historical moved blocks when needed; removing a moved block is a breaking change for users who have not crossed that state transition.

Use terraform plan to confirm moves are recognized as address changes rather than destroy/create. For exceptional state-only work, use terraform state mv or replace-provider only with a backup, exact address map, authorized state lock, and reviewable recovery path. Never use state push, state rm, or force replacement as a shortcut for an unclear refactor.

## Release gate

Check interface compatibility, provider and Terraform constraints, changelog, migration instructions, tests, generated documentation, examples, and downstream plans. Label changes as patch, minor, or breaking based on actual consumer and state behavior rather than file diff size.
