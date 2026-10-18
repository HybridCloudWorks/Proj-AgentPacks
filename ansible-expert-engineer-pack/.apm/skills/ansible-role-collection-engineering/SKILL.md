---
name: ansible-role-collection-engineering
description: Build or review production-quality Ansible roles and collections, including public variable contracts, argument specifications, metadata, documentation, Molecule scenarios, ansible-test, and supported-version evidence.
---

# Role and Collection Engineering

Choose the content boundary first: a role is a reusable unit inside a project; a collection is a namespaced distribution of roles, modules, plugins, docs, tests, and metadata. Do not create a collection to hide a poorly defined role contract.

## Contract

Document supported platforms, Ansible/core range, required collections, inputs, defaults, outputs, side effects, privilege needs, tags, handlers, and idempotency expectations. Use `meta/argument_specs.yml` to validate role inputs early. Keep defaults overrideable and avoid exposing internal variable names as public API. Do not put secrets in examples or defaults.

## Layout and quality

For roles, keep tasks, handlers, defaults, vars, files, templates, meta, docs, and tests separated. For collections, preserve the standard namespace/name layout and include `galaxy.yml`, runtime requirements, collection docs, sanity tests, unit/integration tests, and changelog discipline. Use FQCNs everywhere.

## Tests

Use Molecule for scenario-based role testing when a real target or container is appropriate. Cover converge, idempotency, check mode where supported, verify assertions, platform variants, and cleanup. Use `ansible-test sanity` for collection quality and `ansible-test units` / integration tests when plugins or modules require them. Tests that cannot run in the current environment must be reported as skipped, not passed.

Run lint and syntax checks independently of Molecule. Pin or constrain test dependencies and avoid a test scenario that silently reaches production infrastructure. For privileged or destructive behavior, use disposable containers/VMs or a mock boundary.

## Release evidence

Before publishing or consuming content, verify namespace ownership, collection version, runtime requirements, dependency ranges, docs, changelog, artifact provenance, and supported Ansible/core matrix. Compare a clean install with the repository's declared requirements. Record failures and unsupported platforms explicitly.

References: https://docs.ansible.com/projects/molecule/ and https://docs.ansible.com/projects/dev-tools/user-guide/testing/
