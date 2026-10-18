# Prompt inventory

One prompt per primary workflow of the `cloud-prepress-reviewer` agent. The prompts live in `.apm/prompts/`, set `agent: cloud-prepress-reviewer`, name the skills they apply, and follow the always-on `cloud-prepress-reviewer-contract` instruction. They reference only installed content: skills, the agent, and the contract instruction. They never reference pack docs, templates or helper-script paths.

| Prompt | Workflow | Skills applied | Expected output | Worked example |
|---|---|---|---|---|
| `review-before-pr.prompt.md` | Built application or mixed change, before the pull request | cloud-prepress-orchestration, change-scope-and-impact, code-defect-and-quality-review, tests-build-and-dependency-review, security-secrets-and-supply-chain-review, documentation-inputs-and-repository-contracts, review-report-and-pr-gate; iac-policy-and-identity-review and review-hooks-and-automation when relevant | Full pre-press report; located defects, test and build evidence, skipped checks; a clean result ends at `READY_FOR_PR` | `examples/application-pre-pr-review.md` |
| `review-before-deployment.prompt.md` | Terraform, Bicep, ARM, AZD, Azure Policy or RBAC change, before deployment review | cloud-prepress-orchestration, change-scope-and-impact, iac-policy-and-identity-review, deployment-preview-and-environment-review, azure-evidence-and-mcp-review, architecture-and-adr-consistency, operability-resilience-and-rollback-review, cost-allocation-and-governance-review, tests-build-and-dependency-review, review-report-and-pr-gate | Report with preview counts bound to commit and scope, policy and RBAC status, rollback boundary, cost position; hard stop on any mutation | `examples/terraform-pre-deployment-review.md` |
| `review-deployment-preview.prompt.md` | Interpreting a captured plan, what-if or azd preview | deployment-preview-and-environment-review, change-scope-and-impact, iac-policy-and-identity-review, azure-evidence-and-mcp-review, review-report-and-pr-gate | Change counts, unexplained changes, policy denials and permission errors; preview evidence labelled for what it proves | `examples/bicep-keyvault-not-verified.md` |
| `review-security-and-supply-chain.prompt.md` | Security gate for secrets, identity, trust boundaries, dependencies and CI | cloud-prepress-orchestration, change-scope-and-impact, security-secrets-and-supply-chain-review, iac-policy-and-identity-review, role-authority-and-handoff-review, tests-build-and-dependency-review, review-report-and-pr-gate | Findings with exploit path, boundary, impact, mitigation and residual validation; secret-handling statement; rotation left to the credential owner | `examples/ci-supply-chain-security-review.md` |
| `check-architecture-alignment.prompt.md` | Built change against approved topology, constraints and ADRs | change-scope-and-impact, architecture-and-adr-consistency, documentation-inputs-and-repository-contracts, role-authority-and-handoff-review, review-report-and-pr-gate | Proven contradictions, missing design evidence and decisions needing a new ADR, each with its owner | `examples/architecture-drift-blocked.md` |
| `assess-operability-rollback-and-cost.prompt.md` | Day-two readiness: observability, recovery, rollback, cost, allocation, policy exceptions | change-scope-and-impact, operability-resilience-and-rollback-review, cost-allocation-and-governance-review, azure-evidence-and-mcp-review, review-report-and-pr-gate | Rollback boundary and point of no return, labelled recovery evidence, cost against ceiling with sources, exception expiry, new inputs by name | `examples/terraform-pre-deployment-review.md` |
| `verify-handoff-readiness.prompt.md` | Whether the next actor can safely continue | role-authority-and-handoff-review, documentation-inputs-and-repository-contracts, review-report-and-pr-gate | Next actor, gate, explicit next action, evidence passed on, human blockers with owners, engineering work items | `examples/architecture-drift-blocked.md` |
| `validate-review-report.prompt.md` | Pre-review inventory and post-review report validation | review-hooks-and-automation, review-report-and-pr-gate | Validator result line quoted exactly, corrections made to the report, helpers skipped and why | `examples/hooks-and-report-validation.md` |

## Skill to prompt

Every skill is reached by at least one prompt. The prompt named here is the one that depends on the skill most.

| Skill | Primary workflow prompt |
|---|---|
| cloud-prepress-orchestration | `review-before-pr.prompt.md` |
| change-scope-and-impact | `review-before-pr.prompt.md` |
| code-defect-and-quality-review | `review-before-pr.prompt.md` |
| tests-build-and-dependency-review | `review-before-pr.prompt.md` |
| iac-policy-and-identity-review | `review-before-deployment.prompt.md` |
| deployment-preview-and-environment-review | `review-deployment-preview.prompt.md` |
| azure-evidence-and-mcp-review | `review-deployment-preview.prompt.md` |
| security-secrets-and-supply-chain-review | `review-security-and-supply-chain.prompt.md` |
| architecture-and-adr-consistency | `check-architecture-alignment.prompt.md` |
| operability-resilience-and-rollback-review | `assess-operability-rollback-and-cost.prompt.md` |
| cost-allocation-and-governance-review | `assess-operability-rollback-and-cost.prompt.md` |
| role-authority-and-handoff-review | `verify-handoff-readiness.prompt.md` |
| documentation-inputs-and-repository-contracts | `verify-handoff-readiness.prompt.md` |
| review-report-and-pr-gate | `validate-review-report.prompt.md` |
| review-hooks-and-automation | `validate-review-report.prompt.md` |

## How the prompts install

APM ships prompts as commands. Facts recorded for APM 0.33.0 in the pack repository's `standard/client-locations.md`:

- APM drops the `agent` key, with a warning, for Claude Code commands, which accept only description, input, allowed-tools, model and argument-hint. GitHub Copilot honours it.
- At user scope (`apm install -g`), Copilot receives prompts and instructions, and Codex receives no prompts.

Where a client receives no prompt files, invoke the `cloud-prepress-reviewer` agent directly and state the workflow you want. The agent and its skills carry the same procedure. Whether each client lists and runs these prompts is live behavior and has not been established.
