---
name: review-infrastructure-pr
description: Perform a complete evidence-driven pull request review for infrastructure-as-code, configuration management, deployment automation, platform manifests, and CI/CD. Use when a change affects infrastructure targets, identities, state or ownership, deployment scripts, pipelines, policies, tests, secrets, generated artifacts, or cross-tool handoffs. Audit every changed line internally, invoke only the matching technology Skills, and report concrete defects or material evidence gaps. Do not use for general application-code style review or remediation work.
---

# Objective

Prove whether the proposed infrastructure or automation transition is correct, safe, repeatable, secure, recoverable, and operable. Review every changed line internally without commenting on every line.

## Inputs and Preconditions

Collect what is available:

- PR title, description, issue, acceptance criteria, base/head revisions, and complete diff.
- Repository instructions, architecture decisions, module or role documentation, and runbooks.
- Entry points, values, variables, parameters, inventories, identities, state, ownership, targets, and execution order.
- Plans, previews, compiled or rendered output, tests, policy results, scans, CI logs, and deployment history.

Treat descriptions and passing checks as claims to verify. Record unavailable evidence instead of inventing behavior.

## Workflow

1. **Inventory the change.** Identify every technology, file type, generated artifact, rename, deletion, mode change, binary change, target, identity, and execution entry point.
2. **Build changed-line coverage.** Run `scripts/change_manifest.py --base <base> --head <head> --format markdown` when a Git repository and refs are available; otherwise build an equivalent internal ledger from the full diff.
3. **Reconstruct the contract.** State what the change must produce, what it must never affect, and whether it creates, updates, replaces, deletes, imports, moves, detaches, adopts, configures, restarts, or changes an interface.
4. **Trace the graph.** Follow inputs, transformations, actions, targets, outputs, and ownership in both directions across tools. Read `references/review-protocol.md` for the full tracing and coverage method.
5. **Apply universal gates.** Read `references/universal-gates.md` and evaluate every relevant target, state, lifecycle, security, reliability, concurrency, supply-chain, cost, observability, and test gate.
6. **Activate only matching adapters.** Use the routing table below. For an unsupported technology, map its semantics to the universal gates and verify version-specific behavior in current official documentation.
7. **Verify evidence.** Activate `verify-infrastructure-evidence` when safe checks or review artifacts are available. Require evidence proportional to blast radius and verify its commit, inputs, target, identity, and artifact provenance.
8. **Write findings.** Follow `references/severity-and-output.md`. Anchor each root cause to the narrowest changed line and include trigger, impact, remediation direction, confidence, and verification evidence.
9. **Run an adversarial pass.** Challenge target selection, ownership, destructive impact, existing-environment behavior, partial failure, retry, cancellation, rollback, concurrency, stale artifacts, and unverified generated output.
10. **De-duplicate and conclude.** Remove duplicates, separate confirmed defects from evidence gaps, state residual risk, and produce the output contract in `assets/review-report-template.md`.

## Technology Routing

| Changed stack | Activate |
|---|---|
| Terraform or OpenTofu | `review-terraform-opentofu` |
| Bicep, ARM JSON, deployment stacks, or template specs | `review-bicep-arm` |
| PowerShell, modules, DSC, or PowerShell pipeline steps | `review-powershell-automation` |
| Ansible playbooks, roles, collections, inventory, or variables | `review-ansible-automation` |
| GitHub Actions, Azure Pipelines, other CI/CD, Bash, Python deployment wrappers, Make, or task runners | `review-cicd-deployment` |
| Kubernetes, Helm, Kustomize, operators, or GitOps configuration | `review-kubernetes-packaging` |
| Static checks, plans, previews, renders, tests, policies, scans, or CI evidence | `verify-infrastructure-evidence` |

Activate every relevant Skill for a cross-tool chain. Do not force one tool's concepts onto another.

## Finding Threshold

Raise a defect only when the PR introduces or exposes a specific execution path with material impact and supported evidence. Use an evidence gap when implementation may be correct but high-risk behavior cannot be cleared without target-specific proof. Do not report pre-existing issues unless the PR makes them reachable or materially worse.

## Re-review

On a new push, rebuild the ledger against the new head, verify prior findings against the code rather than resolved conversations, review all newly changed lines, and do not repeat findings whose root cause is fixed.

## Stop Conditions

Stop and report insufficient evidence when:

- The diff is incomplete or a changed line remains uninspected.
- Target, identity, state, inventory, or ownership cannot be established for a high-risk action.
- Version-specific behavior is decisive but no authoritative source, schema, or reproducible evidence is available.
- Required artifacts are tied to a different commit, target, parameters, identity, or dependency set.
- Safe validation would require deployment, target mutation, production credentials, or execution of untrusted code.

## Resources

- Read `references/review-protocol.md` for exhaustive coverage, tracing, existing-environment reasoning, and false-positive controls.
- Read `references/universal-gates.md` for technology-neutral review gates.
- Read `references/severity-and-output.md` for severity, confidence, inline placement, consolidation, and no-finding language.
- Read `references/github-copilot-setup.md` only when installing or tuning GitHub Copilot code review.
- Use `assets/infrastructure-pull-request-template.md` to request reviewable evidence.
- Use `assets/repository-enforcement-checklist.md` to configure non-AI enforcement.
- Use `assets/review-report-template.md` for the final response.
