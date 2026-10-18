# Prompt inventory

There is one prompt per primary workflow. All of them live in `.apm/prompts/` and set `agent: aws-cloud-architect`. Each prompt states its inputs, names the skills it applies, describes its expected output, and defers to the always-on `aws-cloud-architect-contract` instruction for the completion report, evidence labels and the REQ, TOPOLOGY, CONSTRAINTS and ADR handoff.

| Prompt | Workflow | Skills applied | Expected output | Worked example |
|---|---|---|---|---|
| design-aws-workload.prompt.md | Greenfield or modernized workload design | foundations, workload-and-service-selection, data-and-application-patterns, networking, security, resilience, operations, cost, docs-mcp, well-architected, iac, handoff | Placed architecture, four handoff artifacts, labelled completion report | `examples/greenfield-workload-design.md` |
| design-aws-landing-zone.prompt.md | Multi-account foundations | foundations, caf-landing-zones, security, networking, cost, well-architected (CAF), docs-mcp, iac, handoff | OU and account map, guardrail catalogue, identity, logging, network hub, vending, phased rollout | `examples/landing-zone-design.md` |
| design-aws-hybrid-network.prompt.md | Network, hybrid and edge connectivity | foundations, networking, security, resilience, cost, docs-mcp, handoff | Routes per segment, DNS paths, option comparison, failure behavior, cost-bearing paths | (none) |
| plan-aws-migration-and-dr.prompt.md | Migration and disaster recovery | foundations, resilience, workload-and-service-selection, networking, security, operations, cost, docs-mcp, handoff | Strategy per application, waves and gates, cutover and rollback, recovery-test plan | `examples/migration-and-dr-plan.md` |
| review-deployment-plan.prompt.md | Pre-apply IaC change review | iac, security, resilience, operations, docs-mcp, handoff | Severity-ordered findings, go or no-go with conditions, one approval per mutation | `examples/deployment-review-blocked.md` |
| review-aws-well-architected.prompt.md | Six-pillar and CAF review | foundations, well-architected, plus the pillar skills | Per-pillar findings, prioritized actions, CAF readiness, not-reviewed list | (none; uses `templates/well-architected-review.md`) |
| review-aws-cost.prompt.md | Cost and sustainability review | foundations, cost, networking, workload-and-service-selection, resilience, security, docs-mcp, handoff | Cost-driver breakdown, ranked recommendations with trade-offs, measurement plan | (none) |
| troubleshoot-aws-incident.prompt.md | Production incident investigation | operations, networking, security, iac, docs-mcp, resilience | Timeline, evidence table, hypotheses with confidence, mitigation options, root-cause correction | `examples/incident-troubleshooting.md` |
| verify-aws-evidence.prompt.md | Verify AWS facts | docs-mcp, then the skill that owns the affected decision | Evidence record per claim with source, date, label and decision impact | Evidence tables in every example |
| create-aws-architecture-diagram.prompt.md | Draw.io diagram of an approved design | aws-architecture-visualization, drawio-core-generation, drawio-render-export-and-review, diagram-validation-and-evidence | Editable `.drawio`, exports when a renderer exists, structural, semantic and visual results | `examples/architecture-diagram.md` |

Skill names are shortened in this table. Each prompt uses the full names: `aws-architecture-foundations`, `aws-workload-and-service-selection`, `aws-data-and-application-patterns`, `aws-networking-hybrid-and-edge`, `aws-security-identity-and-compliance`, `aws-resilience-dr-and-migration`, `aws-operations-observability-and-troubleshooting`, `aws-cost-sustainability-and-finops`, `aws-docs-mcp-and-evidence`, `aws-well-architected-and-frameworks`, `aws-caf-landing-zones-and-governance`, `aws-iac-deployment-and-lifecycle`, `aws-architecture-handoff-and-adr`.

`tests/trigger-cases.yml` maps each trigger case to its prompt through `prompt_file`. `tests/capability-coverage.yml` maps each required capability to its prompts through `prompt_map`.

## How the prompts are installed

APM deploys prompts as Copilot prompt files and as Claude Code commands. For Claude it drops the `agent` key and prints a warning. A user-scope APM install gives Codex no prompts. The validator's install check runs `apm install` for every target. Nobody has inspected which prompt files it generates for Kiro and Gemini CLI. On any host that does not receive the prompts, invoke the `aws-cloud-architect` agent directly with the same inputs; the contract instruction still applies.
