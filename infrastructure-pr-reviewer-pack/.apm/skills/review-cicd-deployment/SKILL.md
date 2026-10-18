---
name: review-cicd-deployment
description: Review GitHub Actions, Azure Pipelines, other CI/CD definitions, reusable workflows and templates, Bash, Python deployment wrappers, Makefiles, and task runners for trust boundaries, permissions, target selection, conditions, artifact provenance, concurrency, cancellation, supply chain, and failure propagation. Use when a PR changes pipeline YAML or orchestration scripts that validate, preview, approve, deploy, clean up, or roll back infrastructure.
---

# Objective

Prove that only trusted code and identities can reach the intended target and that the exact artifact validated, previewed, scanned, and approved is the artifact deployed.

## Inputs

- Events, branch/tag/path filters, manual inputs, matrices, environments, approvals, runner trust, permissions, identities, service connections, secrets, and targets.
- Reusable workflows/templates, artifacts, caches, dependency references, conditions, concurrency groups, timeouts, retries, and deployment commands.
- Bash or Python wrappers, tests, workflow validation, logs, provenance, and environment-approval evidence.

## Workflow

1. Map validation, preview, plan, approval, deployment, cleanup, and rollback events and establish the trust boundary for forks, pull requests, branches, tags, schedules, and manual dispatch.
2. Review least-privilege permissions, OIDC or workload-identity claims, service connections, self-hosted runner trust, secret reachability, and separation of validation and deployment identities.
3. Trace every condition through boolean/string/null/empty/skipped/cancelled/failure semantics, dependency outputs, matrices, templates, and continue-on-error behavior.
4. Prove artifact and plan integrity across commit, dependency resolution, build, scan, preview, approval, promotion, download, and deployment. Reject stale or cross-environment selection.
5. Verify explicit environment and target selection before credentials are acquired and ensure matrix parameters cannot cross-wire identity and target.
6. Review concurrency, cancellation, delayed or stale runs, locks, reruns, timeouts, retries, cleanup, manual approval binding, and shared workspaces or caches.
7. Review reusable contracts, immutable pinning, downloaded tools, images, marketplace tasks, Bash quoting/status/traps, Python subprocess/exception/retry behavior, and bypass flags.
8. Return confirmed findings and evidence gaps to `review-infrastructure-pr`.

## Decision Rules

- Pull-request code must not gain privileged secrets, trusted self-hosted runners, or production reach.
- A deployment that rebuilds or re-resolves mutable dependencies after approval requires equivalent revalidation and approval.
- Bypass or force flags are high-scrutiny signals, not automatic defects.
- Do not execute an untrusted pipeline or deployment wrapper merely to validate syntax.

## Output Contract

Return technology-specific findings and evidence gaps to `review-infrastructure-pr` with an anchor, trigger, affected target, impact, remediation, and verification evidence. Do not repeat universal gates or create another final report.

## Validation and Stop Conditions

Use `references/review-checklist.md`; verify uncertain semantics through `references/official-sources.md`. Stop when decisive target state, identity, versions, generated output, or safe access is unavailable. Never mutate targets or expose sensitive values.

## Resources

- Read `references/review-checklist.md` for the complete technology adapter.
- Read `references/official-sources.md` when behavior is version-specific, uncertain, or current verification is required.
