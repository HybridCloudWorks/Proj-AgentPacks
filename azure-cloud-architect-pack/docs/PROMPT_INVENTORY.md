# Prompt inventory

Ten workflow prompts live in `.apm/prompts/`. Each targets the `azure-cloud-architect` agent, states its inputs, names the Skills it applies, states its expected output, and closes with the completion report that the always-on `azure-cloud-architect-contract` instruction defines.

| Prompt | Workflow | Skills applied | Expected output |
|---|---|---|---|
| design-azure-workload.prompt.md | Greenfield or changed workload design | azure-architecture-foundations, azure-workload-and-service-selection, azure-data-and-application-patterns, azure-docs-mcp-and-evidence, azure-well-architected-and-frameworks, azure-architecture-handoff-and-adr; security, networking, resilience, operations and cost Skills as the workload needs | REQ, TOPOLOGY, CONSTRAINTS and ADR handoff, service comparison, completion report |
| design-landing-zone.prompt.md | Platform and application landing-zone design or audit | azure-architecture-foundations, azure-caf-landing-zones-and-governance, azure-security-identity-and-compliance, azure-networking-hybrid-and-edge, azure-cost-sustainability-and-finops, azure-well-architected-and-frameworks, azure-docs-mcp-and-evidence, azure-architecture-handoff-and-adr | Current-state findings, target hierarchy, placement matrix, staged policy and RBAC design, migration sequence, handoff |
| design-hybrid-network.prompt.md | Hybrid, edge and private connectivity design | azure-architecture-foundations, azure-networking-hybrid-and-edge, azure-security-identity-and-compliance, azure-resilience-dr-and-migration, azure-cost-sustainability-and-finops, azure-docs-mcp-and-evidence, azure-architecture-handoff-and-adr | Address and routing plan, DNS path, ingress and egress, connectivity ADR, handoff |
| plan-migration-and-dr.prompt.md | Migration and disaster recovery planning | azure-architecture-foundations, azure-resilience-dr-and-migration, azure-workload-and-service-selection, azure-data-and-application-patterns, plus networking, security, operations and cost Skills; azure-docs-mcp-and-evidence, azure-architecture-handoff-and-adr | Inventory, strategy per workload, DR per tier, cutover and rollback windows, rehearsal plan, handoff |
| review-iac-and-deployment-plan.prompt.md | Bicep, ARM or Terraform/AVM review with what-if or plan | azure-iac-avm-and-repo-standardization, azure-deployment-and-lifecycle, azure-security-identity-and-compliance, azure-resilience-dr-and-migration, azure-docs-mcp-and-evidence | Located findings by severity with blocking status, checks run and not run, standardization notes |
| review-well-architected.prompt.md | Five-pillar and CAF review | azure-architecture-foundations, azure-well-architected-and-frameworks, then pillar Skills where a gap appears, azure-docs-mcp-and-evidence | Findings per pillar, prioritized gaps with owners, ADRs for significant fixes |
| estimate-azure-cost.prompt.md | Cost model and FinOps controls | azure-cost-sustainability-and-finops, azure-docs-mcp-and-evidence, azure-workload-and-service-selection, azure-well-architected-and-frameworks | Assumption-based cost model, budget and tag design, optimization options with trade-offs |
| verify-azure-evidence.prompt.md | Evidence check of drift-prone facts | azure-docs-mcp-and-evidence, azure-architecture-handoff-and-adr | Evidence register, changed decisions and constraints |
| troubleshoot-azure-issue.prompt.md | Deployment, access, network or runtime diagnosis | azure-operations-observability-and-troubleshooting, azure-deployment-and-lifecycle, azure-security-identity-and-compliance, azure-networking-hybrid-and-edge, azure-docs-mcp-and-evidence, azure-architecture-handoff-and-adr | Confirmed cause or open hypotheses, partial-change assessment, proposed fix with approvals, prevention |
| create-architecture-diagram.prompt.md | Draw.io diagram from an approved topology | azure-architecture-visualization, drawio-core-generation, drawio-render-export-and-review, diagram-validation-and-evidence | `.drawio` file, export if rendered, reconciliation table, separate structural, semantic and visual results |

## Skill coverage

Every shipped Skill is applied by at least one prompt.

| Skill | Primary prompt | Also applied by |
|---|---|---|
| azure-architecture-foundations | design-azure-workload.prompt.md | design-landing-zone, design-hybrid-network, plan-migration-and-dr, review-well-architected |
| azure-architecture-handoff-and-adr | design-azure-workload.prompt.md | every design and planning prompt, verify-azure-evidence, troubleshoot-azure-issue |
| azure-architecture-visualization | create-architecture-diagram.prompt.md | none |
| azure-caf-landing-zones-and-governance | design-landing-zone.prompt.md | none |
| azure-cost-sustainability-and-finops | estimate-azure-cost.prompt.md | design-azure-workload, design-landing-zone, design-hybrid-network, plan-migration-and-dr, review-well-architected |
| azure-data-and-application-patterns | design-azure-workload.prompt.md | plan-migration-and-dr |
| azure-deployment-and-lifecycle | review-iac-and-deployment-plan.prompt.md | troubleshoot-azure-issue |
| azure-docs-mcp-and-evidence | verify-azure-evidence.prompt.md | every other prompt except create-architecture-diagram |
| azure-iac-avm-and-repo-standardization | review-iac-and-deployment-plan.prompt.md | none |
| azure-networking-hybrid-and-edge | design-hybrid-network.prompt.md | design-landing-zone, design-azure-workload, plan-migration-and-dr, troubleshoot-azure-issue |
| azure-operations-observability-and-troubleshooting | troubleshoot-azure-issue.prompt.md | design-azure-workload, plan-migration-and-dr, review-well-architected |
| azure-resilience-dr-and-migration | plan-migration-and-dr.prompt.md | design-azure-workload, design-hybrid-network, review-iac-and-deployment-plan, review-well-architected |
| azure-security-identity-and-compliance | design-landing-zone.prompt.md | design-azure-workload, design-hybrid-network, plan-migration-and-dr, review-iac-and-deployment-plan, review-well-architected, troubleshoot-azure-issue |
| azure-well-architected-and-frameworks | review-well-architected.prompt.md | design-azure-workload, design-landing-zone, estimate-azure-cost |
| azure-workload-and-service-selection | design-azure-workload.prompt.md | plan-migration-and-dr, review-well-architected, estimate-azure-cost |
| diagram-validation-and-evidence | create-architecture-diagram.prompt.md | none |
| drawio-core-generation | create-architecture-diagram.prompt.md | none |
| drawio-render-export-and-review | create-architecture-diagram.prompt.md | none |

## Worked examples

| Prompt | Example | Outcome shown |
|---|---|---|
| design-azure-workload.prompt.md | examples/greenfield-workload-design.md | Handoff delivered, ADRs Proposed, service facts not-verified |
| design-landing-zone.prompt.md | examples/landing-zone-design.md | Audit and target design, nothing changed |
| plan-migration-and-dr.prompt.md | examples/migration-and-dr-plan.md | Plan delivered, RTO and RPO unmeasured, irreversible step recorded |
| review-iac-and-deployment-plan.prompt.md | examples/iac-deployment-review-blocked.md | Blocked: the plan would destroy a production database |
| troubleshoot-azure-issue.prompt.md | examples/deployment-failure-troubleshooting.md | Cause confirmed by read-only queries, fix proposed but not applied |
| create-architecture-diagram.prompt.md | examples/architecture-diagram-workflow.md | Unverified: structurally valid, never rendered |

design-hybrid-network, review-well-architected, estimate-azure-cost and verify-azure-evidence have no dedicated example; the greenfield example shows the evidence and cost steps inside a design.

## Delivery

APM ships prompts as commands. Claude Code receives them as commands, and APM drops the `agent` key with a warning. GitHub Copilot receives them as prompt files and honours `agent`. A user-scope `apm install -g` delivers no prompts to Codex. Where a host has no prompt primitive, invoke `azure-cloud-architect` directly and give it the prompt's body.

Prompts are installed content, so they name only installed things: the agent, the Skills, and the contract instruction. They never point at `templates/`, `examples/` or these docs; the handoff file names they use (`REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json`, `ADR.md`) are files the agent writes in the user's repository.
