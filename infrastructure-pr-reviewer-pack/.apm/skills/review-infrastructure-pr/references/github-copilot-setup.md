# GitHub Copilot Setup for Infrastructure PR Review

**Last verified:** 2026-08-22

Use this reference only for GitHub Copilot code review. Keep the canonical Agent and Skills vendor-neutral.

## Recommended Layout

```text
.github/
├── agents/
│   └── infrastructure-pr-reviewer.agent.md
├── skills/
│   ├── review-infrastructure-pr/
│   └── <domain skills>/
├── instructions/
│   └── infrastructure-review.instructions.md
└── copilot-instructions.md
```

GitHub Copilot code review discovers review-focused Skills from `.github/skills`. It reads repository custom instructions, agent instructions, and Skills from the pull request head branch, so the same PR can test changes to this pack.

## Installation

1. Copy the Copilot target's `.github/agents`, `.github/skills`, and `.github/instructions` directories to the repository root.
2. Merge `setup/copilot-instructions-snippet.md` into any existing `.github/copilot-instructions.md`; do not overwrite unrelated instructions.
3. Adjust path globs in `.github/instructions/infrastructure-review.instructions.md` to match the repository.
4. Optionally merge `setup/infrastructure-pull-request-template.md` into the repository's PR template.
5. Configure parser, lint, plan, preview, render, test, policy, security, and provenance checks for the actual stack.
6. Enable repository custom instructions for Copilot code review and request manual or automatic review.
7. Configure review of new pushes when re-review is required.

## Runtime and Environment

Copilot code review runs agentic capabilities through GitHub Actions in an ephemeral environment. Use `.github/workflows/copilot-code-review.yml` to configure the review environment independently, or `.github/workflows/copilot-setup-steps.yml` when sharing the Copilot cloud-agent environment. Install only the tools required for safe review; do not add production credentials or deployment privileges.

## Review Effort

Use a higher review effort for production, shared, identity, network, data-bearing, destructive, ownership-transfer, provider-upgrade, and pipeline-permission changes. Effort level does not replace required evidence or human approval.

## Enforcement Limitation

Copilot leaves a `Comment` review, not `Approve` or `Request changes`. Its review does not satisfy required approvals or block merging. Enforce non-negotiable controls with repository rulesets, required checks, CODEOWNERS, protected environments, accountable human approval, policy-as-code, state locking, concurrency, and artifact provenance.

## Official Sources

- [Using GitHub Copilot code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review)
- [Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Agent Skills specification](https://agentskills.io/specification)
