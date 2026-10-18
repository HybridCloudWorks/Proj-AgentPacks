# cloud-prepress-reviewer 1.1.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| cloud-prepress-reviewer.agent.md | Canonical agent: Expert pre-PR and pre-deployment reviewer for built application and Azure infrastructure changes; verifies evidence, defects, security, IaC, policy, tests, previews, rollback, cost, and handoff without mutating systems. | .apm/agents/cloud-prepress-reviewer.agent.md |
| cloud-prepress-reviewer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the cloud prepress reviewer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/cloud-prepress-reviewer-contract.instructions.md |
| SKILL.md | Canonical skill: Reviews implementation and infrastructure changes against approved architecture, topology, ADRs, service boundaries, ownership, and stated acceptance criteria. | .apm/skills/architecture-and-adr-consistency/SKILL.md |
| SKILL.md | Canonical skill: Grounds Azure review claims in current Microsoft documentation, Azure MCP results, repository evidence, previews, and clearly labeled confidence boundaries. | .apm/skills/azure-evidence-and-mcp-review/SKILL.md |
| SKILL.md | Canonical skill: Determines the exact change boundary, architecture context, resource blast radius, state and dependency impact, and files that must be reviewed before approval. | .apm/skills/change-scope-and-impact/SKILL.md |
| SKILL.md | Canonical skill: Orchestrates the evidence-first review between implementation and pull request or deployment, selecting only the review domains required by the changed artifact. | .apm/skills/cloud-prepress-orchestration/SKILL.md |
| SKILL.md | Canonical skill: Performs evidence-first code review for defects, logic, maintainability, error handling, observability, performance, and safe behavior across changed application code. | .apm/skills/code-defect-and-quality-review/SKILL.md |
| SKILL.md | Canonical skill: Reviews cost, allocation, tags, budgets, quotas, resource sizing, sustainability, policy exceptions, and operational ownership before a change reaches deployment. | .apm/skills/cost-allocation-and-governance-review/SKILL.md |
| SKILL.md | Canonical skill: Reviews deployment readiness, environment configuration, authentication, Bicep what-if, Terraform plan, AZD previews, and mutation gates without executing deployment actions. | .apm/skills/deployment-preview-and-environment-review/SKILL.md |
| SKILL.md | Canonical skill: Reviews whether changed behavior, inputs, secrets references, runbooks, ADRs, review records, checklists, and repository contracts are documented in the correct artifact. | .apm/skills/documentation-inputs-and-repository-contracts/SKILL.md |
| SKILL.md | Canonical skill: Reviews Terraform, Bicep, ARM, Azure Policy, RBAC, managed identity, tags, naming, and infrastructure governance changes for correctness and least privilege. | .apm/skills/iac-policy-and-identity-review/SKILL.md |
| SKILL.md | Canonical skill: Reviews observability, alerting, backup, recovery, rollout, rollback, migration, downtime, and day-two operating readiness before deployment. | .apm/skills/operability-resilience-and-rollback-review/SKILL.md |
| SKILL.md | Canonical skill: Uses the pack's pre-review and post-review hooks plus deterministic inventory and report validators to make recurring review checks consistent and non-mutating. | .apm/skills/review-hooks-and-automation/SKILL.md |
| SKILL.md | Canonical skill: Produces the final pre-press findings report, merge or deployment recommendation, evidence ledger, unresolved risks, and precise engineer handoff without overstating validation. | .apm/skills/review-report-and-pr-gate/SKILL.md |
| SKILL.md | Canonical skill: Verifies agent roles, tool permissions, ownership, reviewer boundaries, handoff contracts, approval gates, and whether the next actor can safely continue the work. | .apm/skills/role-authority-and-handoff-review/SKILL.md |
| SKILL.md | Canonical skill: Reviews changed code and infrastructure for trust-boundary failures, secret exposure, identity misuse, insecure defaults, dependency risk, and supply-chain weaknesses. | .apm/skills/security-secrets-and-supply-chain-review/SKILL.md |
| SKILL.md | Canonical skill: Verifies that changed code, infrastructure, containers, dependencies, and configuration have appropriate build, test, lint, package, and regression evidence. | .apm/skills/tests-build-and-dependency-review/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| post-review.ps1 | Hook helper script | hooks/post-review.ps1 |
| post-review.sh | Hook helper script | hooks/post-review.sh |
| pre-review.ps1 | Hook helper script | hooks/pre-review.ps1 |
| pre-review.sh | Hook helper script | hooks/pre-review.sh |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| REVIEW.md | Local test or recorded evidence | tests/fixtures/REVIEW.md |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| review_inventory.py | Pack-specific helper code | tooling/review_inventory.py |
| validate_review_bundle.py | Pack-specific helper code | tooling/validate_review_bundle.py |
| validate_review_report.py | Pack-specific helper code | tooling/validate_review_report.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-cloud-prepress-reviewer.zip: 17 files generated by `apm install --target copilot`
- claude-cloud-prepress-reviewer.zip: 17 files generated by `apm install --target claude`
- codex-cloud-prepress-reviewer.zip: 16 files generated by `apm install --target codex`
- kiro-cloud-prepress-reviewer.zip: 17 files generated by `apm install --target kiro`
- gemini-cloud-prepress-reviewer.zip: 15 files generated by `apm install --target gemini`
- agent-skills-cloud-prepress-reviewer.zip: 15 files generated by `apm install --target agent-skills`
- cloud-prepress-reviewer-canonical.zip, cloud-prepress-reviewer-prompt.zip, cloud-prepress-reviewer-validation.zip, cloud-prepress-reviewer-skills.zip, cloud-prepress-reviewer-full-pack.zip, SHA256SUMS.txt
