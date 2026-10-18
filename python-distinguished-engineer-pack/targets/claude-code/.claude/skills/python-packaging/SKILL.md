---
name: python-packaging
description: Maintain Python build metadata, dependency resolution, lockfiles, distributions and supply-chain compatibility. Use when dependencies, packaging, distribution, entry points, runtime versions or reproducibility change.
---

# Python Packaging

## Activation and scope

Dependencies, packaging, distribution, entry points, runtime versions or reproducibility change. Do not impose a preferred manager or publish packages as part of a review.

## Inputs and dependencies

- Inputs: pyproject/requirements, locks, backend, index policy, CI installation/build steps, consumers.
- Dependencies: Repository package manager/build backend and available approved index metadata.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Discover backend, package layout, requires-python, extras/groups, entry points, constraints, editable installs and native-extension/platform needs; preserve the existing manager.
2. Verify package identity and compatibility before suggesting installation. Separate runtime/test/development groups, inspect transitive/version/license implications and dependency-confusion exposure.
3. Generate lock changes with the declared resolver; explain migrations and major upgrades. Prefer existing dependencies or standard-library capability when adequate.
4. Build wheel/sdist in an isolated approved environment, inspect included files and metadata, test clean installation/import where available, and record reproducibility and supported-platform limits. Publishing is a separate approved action.

## Output and validation

Minimal metadata/lock patch, dependency rationale, artifact manifest and build/install evidence. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Unverified package, unsupported interpreter, private-index access gap, divergent lock, leaked source/secrets in artifacts or incompatible major upgrade. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `modernize-python-code.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. Consult shared instruction, handoff and completion contracts when the full pack is available.
