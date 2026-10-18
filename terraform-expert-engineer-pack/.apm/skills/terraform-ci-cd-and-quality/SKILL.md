---
name: terraform-ci-cd-and-quality
description: Build and review Terraform CI/CD pipelines with formatting, validation, tests, lint, security, plan artifacts, approval gates, and controlled apply.
---

# Terraform CI/CD and Quality

Use this Skill for GitHub Actions, GitLab CI, Terraform pipeline design, plan artifacts, quality gates, drift checks, release automation, and apply approvals.

## Pipeline shape

Use a predictable sequence: identify changed roots, install the pinned Terraform version, authenticate with short-lived identity, initialize the intended backend or use backend-disabled initialization for module-only checks, format check, validate, lint/security checks, unit or mock tests, plan, policy checks, review, then apply only through an authorized protected gate.

Keep state and plan files out of public logs and ordinary artifacts. A saved plan can contain sensitive values. Restrict artifact access and retention, or use the platform's secure plan/apply mechanism. Preserve .terraform.lock.hcl and review dependency changes.

## Quality boundaries

Use changed-path filtering carefully so backend, module, provider, policy, workflow, and lock-file changes cannot bypass required checks. Pin action and tool versions according to repository policy. Use concurrency and environment protection to prevent competing writers to one state.

Run lint and security scanners as complementary evidence, not as replacements for Terraform validation, plan review, policy, or provider tests. Record tool versions and findings. A green pipeline proves only the checks that actually ran.

## Apply gate

Require an approved plan tied to the same commit, backend, workspace or state key, variables, provider lock, and policy result. Re-plan when those inputs change. Do not auto-apply production unless the repository owner has explicitly designed, protected, and approved that policy.
