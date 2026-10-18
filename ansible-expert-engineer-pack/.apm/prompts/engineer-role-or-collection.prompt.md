---
description: "Build or review a reusable Ansible role or collection with a public contract, argument specs and tests"
agent: ansible-expert-engineer
---

# Engineer a reusable role or collection

## Inputs

- What the content does and who consumes it (one project, several repositories, other teams).
- Supported platforms, the `ansible-core` range, and required collections.
- Where it will be distributed, if anywhere (Git tag, private Galaxy, Automation Hub).
- The test infrastructure available here: container runtime, disposable VMs, or neither.

Publishing, and installing test infrastructure, need explicit authorization.

## Workflow

1. Apply `ansible-role-collection-engineering`. Choose the boundary first: a role is a reusable unit inside a project; a collection is a namespaced distribution of roles, plugins, docs and tests. Do not create a collection to hide a poorly defined role contract.
2. Write the contract: supported platforms, core range, required collections, inputs, defaults, outputs, side effects, privilege needs, tags, handlers and idempotency expectations. Validate inputs early with `meta/argument_specs.yml`; keep internal variable names out of the public API and secrets out of defaults and examples.
3. Author the tasks with `ansible-playbook-development`, and bound dependency ranges with `ansible-collections-supply-chain`.
4. Add tests: Molecule scenarios covering converge, idempotence, check mode where supported, verify assertions, platform variants and cleanup; `ansible-test sanity`, units and integration where plugins or modules exist. Run lint and syntax independently of Molecule with `ansible-validate-content`.
5. Before release, verify namespace ownership, version, runtime requirements, dependency ranges, docs, changelog, artifact provenance and the supported core matrix against a clean install.

## Expected output

The role or collection tree; the public variable contract and argument spec; the README contract; test scenarios with their results; the supported-version matrix marked with what was actually exercised; and release evidence gaps. A scenario that cannot run in this environment is reported as skipped, never as passed.

Follow the `ansible-expert-engineer-contract` instruction for the completion report.
