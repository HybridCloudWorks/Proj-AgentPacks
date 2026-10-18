# Design and De-duplication Decisions

## One Agent, Eight Skills

The Agent stays narrow and owns role, scope, permissions, orchestration, evidence posture, and completion. `review-infrastructure-pr` owns the end-to-end protocol. Six technology Skills load only for stacks present in the diff. `verify-infrastructure-evidence` owns safe checks and evidence integrity. This preserves complete coverage without loading every technology adapter into every review.

## Core Protocol Remains Central

Changed-line coverage, cross-tool tracing, existing-environment reasoning, universal gates, severity, de-duplication, adversarial review, and final output apply to every infrastructure review. They remain references of the orchestration Skill rather than separate always-invoked Skills, avoiding coordination and discovery overhead.

## Technology Adapters Become Skills

Terraform/OpenTofu, Bicep/ARM, PowerShell, Ansible, CI/CD and scripts, and Kubernetes packaging have distinct runtime semantics. Each adapter is an independently triggerable Skill so irrelevant technology guidance does not consume context and one adapter can be versioned or replaced without changing the others.

## Evidence Is a Separate Capability

Static checks and evidence interpretation are deterministic and reusable but do not prove semantic correctness. The evidence Skill runs only safe local checks, records passes/failures/skips, validates provenance, and requests target-specific artifacts. The reviewer remains responsible for judgment.

## GitHub Copilot Is a Target, Not the Canonical Identity

The supplied sources were designed for Copilot code review, but the review method itself is vendor-neutral. The canonical Agent is `infrastructure-pr-reviewer`. Copilot-specific skill paths, instructions, environment setup, PR template, and enforcement guidance live in the Copilot target or conditional setup resources.

## Read-Only by Default

Review requires repository access, search, current documentation, PR metadata, and explicitly safe validation. It does not require edits or deployment privileges. Generated adapters deny or omit write tools, Claude uses plan mode, Codex uses a read-only sandbox, and Gemini receives no write tools.

## Source Ownership

Every rule has one canonical owner listed in `docs/SOURCE_TRACEABILITY.md`. Technology checklists support their Skill but do not redefine the universal gates or final output. Generated targets are build artifacts and must not be edited directly.

## Completeness Boundary

The pack is capability-complete for the supplied infrastructure review contract. Correct conclusions still depend on the actual repository, complete diff, current official documentation, target-specific evidence, installed tools, and host access. Missing evidence is reported rather than converted into unsupported assurance.
