---
name: verify-infrastructure-evidence
description: Run and interpret safe, non-deploying validation for infrastructure and automation reviews, and assess whether plans, what-if results, rendered output, tests, policies, scans, CI logs, and artifacts are tied to the reviewed commit, target, inputs, identity, and dependency set. Use when a pull request includes or requires executable evidence. Do not run apply, deploy, destroy, target-side Ansible, privileged cluster operations, Terraform tests that can create resources, or untrusted workflows automatically.
---

# Objective

Collect trustworthy evidence without mutating infrastructure or confusing static validation with proof of target correctness.

## Inputs

- Repository root and changed technologies.
- Available toolchain and host permissions.
- Base/head revision, target, identity, variables, parameters, inventory, state, dependency versions, and artifacts when available.
- Existing plans, what-if results, compiled or rendered output, tests, policy results, scans, CI logs, approvals, and deployment records.

## Workflow

1. Classify each proposed check as local static, dependency-resolving, remote read, target simulation, or mutating execution.
2. Run only local, non-deploying checks allowed by the host. Use `python scripts/run_review_checks.py <repository-root>` for supported automatic checks.
3. Do not pass `--allow-downloads` unless dependency retrieval is explicitly permitted and the trust boundary is understood.
4. Record every check as pass, fail, skip, or not applicable; preserve command, version, scope, and relevant output.
5. Read `references/evidence-matrix.md` and request risk-proportional evidence that cannot be generated safely in the review environment.
6. Verify evidence integrity: reviewed commit, exact inputs, target, identity, state or inventory, dependency lock, tool version, and artifact ultimately deployed.
7. Interpret a pass narrowly. Syntax, lint, compile, render, or an empty-state plan does not establish lifecycle, authorization, target, or existing-environment safety.
8. Return results and limitations to `review-infrastructure-pr` without duplicating domain findings.

## Safety Rules

- Never run apply, deploy, destroy, import, state mutation, force unlock, target-side configuration, cluster mutation, or production smoke tests automatically.
- Do not execute scripts or workflow definitions from an untrusted pull request solely to validate them.
- Avoid network downloads by default. Do not expose secrets through command lines, environment dumps, plans, diffs, logs, or artifacts.
- Treat Terraform/OpenTofu tests, Ansible check mode, Pester, server-side dry-run, and similar commands as potentially side-effecting until their exact configuration and target are verified.

## Output Contract

Return:

- Checks executed, command and version, result, and relevant evidence.
- Checks skipped and the exact reason.
- Evidence integrity assessment.
- Material gaps with the precise artifact needed.
- Environment limitations and residual uncertainty.

Do not convert a skipped check or absent artifact into a confirmed implementation defect.

## Stop Conditions

Stop when a command would require privileged credentials, contact an unintended target, resolve untrusted executable content, mutate state, or exceed the user's authorized review scope.

## Resources

- Run `scripts/run_review_checks.py --help` before first use.
- Read `references/evidence-matrix.md` for safe and target-specific evidence by technology.
- Read `references/official-sources.md` when command behavior or side effects are uncertain.
