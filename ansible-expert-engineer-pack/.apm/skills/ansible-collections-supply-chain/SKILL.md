---
name: ansible-collections-supply-chain
description: Choose, install, pin, verify, upgrade, and troubleshoot Ansible collections and roles with requirements files, FQCN ownership, Galaxy or Automation Hub sources, signatures, and compatibility evidence.
---

# Collections and Supply Chain

Treat collections, roles, plugins, and their transitive Python/system dependencies as production code. Start from the playbook's required FQCNs and target platforms; do not add a dependency merely because it is popular.

## Requirements

Use `requirements.yml` for collections and roles. Pin an exact version for regulated or offline environments; otherwise use a tested bounded range and record the supported core range. Install into an isolated, reproducible path and verify with `ansible-galaxy collection list`, `ansible-doc`, and CI.

Use FQCNs in content. For private Galaxy/Automation Hub, keep server URLs and credentials outside the repository. Confirm the server API and authentication support the current Ansible release. Do not embed credentials in Git URLs, requirements, `ansible.cfg`, or examples.

## Trust and upgrades

If signatures are required, configure the organization's keyring and verify during install; report whether unsigned content is allowed. A version pin is not proof of provenance. Preserve lockfiles or generated dependency manifests when the project uses them.

For an upgrade: read the Ansible/core and collection porting guides, update requirements in an isolated branch, reinstall cleanly, run lint/syntax/inventory/check-mode tests, execute Molecule or integration coverage, and compare behavior. Investigate renamed modules, removed APIs, option changes, target Python requirements, and template/fact semantics.

## Failure diagnosis

- `couldn't resolve module/action`: wrong FQCN, missing collection, or wrong collection path.
- option not recognized: collection version mismatch or module moved.
- local works, CI fails: CI did not install the same requirements or has a different search path.
- private server fails: authentication/API incompatibility or missing server configuration.

Report the exact dependency source, version, hash/signature evidence, and compatibility range. Never "fix" a resolver failure by broadening to an unbounded latest version.
