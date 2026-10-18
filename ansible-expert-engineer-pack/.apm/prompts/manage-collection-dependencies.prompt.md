---
description: "Add, pin, verify, upgrade or troubleshoot Ansible collections and roles in requirements.yml"
agent: ansible-expert-engineer
---

# Manage collection dependencies

## Inputs

- The FQCNs the playbooks and roles actually use, and the current `requirements.yml`.
- The supported `ansible-core` range and target platforms.
- The content source (Ansible Galaxy, private Galaxy, Automation Hub), whether signatures are required, and whether the environment is regulated or offline.
- The task: add, pin, upgrade, or diagnose a resolver or "couldn't resolve module/action" failure.

Keep server URLs and credentials outside the repository. Installing dependencies needs approval; install only into an isolated, project-local path.

## Workflow

1. Apply `ansible-collections-supply-chain`. Start from the required FQCNs; do not add a dependency because it is popular.
2. Pin an exact version for regulated or offline environments; otherwise use a tested, bounded range and record the supported core range. Never fix a resolver failure by widening to an unbounded latest version.
3. Install into an isolated path and verify with `ansible-galaxy collection list` and `ansible-doc` for every module used. If signatures are required, verify against the organization's keyring and report whether unsigned content is allowed.
4. For an upgrade: read the Ansible, core and collection porting guides; change requirements on an isolated branch; reinstall cleanly; then run lint, syntax, inventory and check-mode tests with `ansible-validate-content`, and Molecule or integration coverage with `ansible-role-collection-engineering`. Look for renamed modules, removed options, target Python requirements and changed template or fact semantics.
5. For CI-only failures, compare the requirements CI installs and its collection search path with the local environment.

## Expected output

A dependency record per collection or role: source, version or range, hash or signature evidence, and compatibility range. The `requirements.yml` diff; porting changes made or proposed; test evidence; and what was not verified. A version pin is not proof of provenance.

Follow the `ansible-expert-engineer-contract` instruction for the completion report.
