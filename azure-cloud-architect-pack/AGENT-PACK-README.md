# azure-cloud-architect 1.1.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| azure-cloud-architect.agent.md | Canonical agent: Senior Azure Cloud Architect for foundations, landing zones, workload design, deployment, operations, migration, security, resilience, cost, AVM, and evidence-aware handoff. | .apm/agents/azure-cloud-architect.agent.md |
| azure-cloud-architect-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the azure cloud architect pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/azure-cloud-architect-contract.instructions.md |
| SKILL.md | Canonical skill: Establishes Azure architecture scope, requirements, boundaries, assumptions, service vocabulary, and a structured REQ/TOPOLOGY/CONSTRAINTS/ADR handoff before specialist design. | .apm/skills/azure-architecture-foundations/SKILL.md |
| SKILL.md | Canonical skill: Produces implementation-ready Azure architecture handoffs, ADRs, topology contracts, acceptance criteria, risks, ownership, and safe next actions. | .apm/skills/azure-architecture-handoff-and-adr/SKILL.md |
| SKILL.md | Canonical skill: Routes Azure topology diagrams to the Azure Expert Designer while preserving architecture evidence, boundaries, legend, views, and handoff consistency. | .apm/skills/azure-architecture-visualization/SKILL.md |
| SKILL.md | Canonical skill: Designs and audits Azure platform and application landing zones, management groups, subscriptions, policy, shared services, naming, tags, and governance inheritance. | .apm/skills/azure-caf-landing-zones-and-governance/SKILL.md |
| SKILL.md | Canonical skill: Embeds Azure cost, unit economics, budgets, tagging, reservations, savings, egress, quota, sustainability, and FinOps controls into architecture decisions. | .apm/skills/azure-cost-sustainability-and-finops/SKILL.md |
| SKILL.md | Canonical skill: Designs Azure data platforms and application architectures with explicit consistency, partitioning, integration, privacy, lifecycle, and operational trade-offs. | .apm/skills/azure-data-and-application-patterns/SKILL.md |
| SKILL.md | Canonical skill: Plans safe Azure deployment, what-if, validation, deployment-stack, CI/CD, OIDC, drift, rollback, change review, and post-deployment lifecycle workflows. | .apm/skills/azure-deployment-and-lifecycle/SKILL.md |
| SKILL.md | Canonical skill: Retrieves and records current official Azure documentation, Azure MCP evidence, API/version facts, limits, availability, pricing context, and confidence boundaries. | .apm/skills/azure-docs-mcp-and-evidence/SKILL.md |
| SKILL.md | Canonical skill: Designs and reviews Azure IaC with Bicep, ARM, Terraform, AzAPI, AzureRM, AVM, module interfaces, repository standards, policy gates, and safe remote state. | .apm/skills/azure-iac-avm-and-repo-standardization/SKILL.md |
| SKILL.md | Canonical skill: Designs Azure VNets, hub-spoke or Virtual WAN, routing, NSGs, Azure Firewall, Private Link, DNS, ExpressRoute, VPN, edge, ingress, and hybrid connectivity. | .apm/skills/azure-networking-hybrid-and-edge/SKILL.md |
| SKILL.md | Canonical skill: Designs and diagnoses Azure operations using Azure Monitor, Log Analytics, Activity Log, Resource Graph, health signals, alerts, runbooks, and evidence-aware incident analysis. | .apm/skills/azure-operations-observability-and-troubleshooting/SKILL.md |
| SKILL.md | Canonical skill: Designs Azure high availability, backup, disaster recovery, migration, modernization, rollback, and cutover strategies with tested RTO/RPO evidence. | .apm/skills/azure-resilience-dr-and-migration/SKILL.md |
| SKILL.md | Canonical skill: Designs Azure identity, Zero Trust, Entra, RBAC, PIM, managed identities, secrets, network protection, policy, Defender, Sentinel, and compliance evidence. | .apm/skills/azure-security-identity-and-compliance/SKILL.md |
| SKILL.md | Canonical skill: Applies Azure Well-Architected five-pillar reviews and Cloud Adoption Framework guidance to architecture decisions, trade-offs, maturity, and production readiness. | .apm/skills/azure-well-architected-and-frameworks/SKILL.md |
| SKILL.md | Canonical skill: Selects Azure compute, containers, serverless, integration, AI, and platform services from workload requirements, operational fit, limits, and Well-Architected trade-offs. | .apm/skills/azure-workload-and-service-selection/SKILL.md |
| SKILL.md | Canonical skill: Validate Draw.io structure and Azure diagram evidence, then report static, rendered, live, and unresolved results without overstating what was proven. | .apm/skills/diagram-validation-and-evidence/SKILL.md |
| upstream-routing.md | Canonical skill | .apm/skills/drawio-core-generation/references/upstream-routing.md |
| SKILL.md | Canonical skill: Create and edit native Draw.io diagrams from requirements, code, structured data, or Mermaid while preserving editable XML and selecting the right generation path. | .apm/skills/drawio-core-generation/SKILL.md |
| SKILL.md | Canonical skill: Export Draw.io diagrams through the installed desktop CLI and perform a renderer-based review of labels, icons, edges, boundaries, and output legibility. | .apm/skills/drawio-render-export-and-review/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| architecture-review.ps1 | Hook helper script | hooks/architecture-review.ps1 |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| minimal.drawio | Local test or recorded evidence | tests/fixtures/minimal.drawio |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| validate_drawio_xml.py | Pack-specific helper code | tooling/validate_drawio_xml.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-azure-cloud-architect.zip: 21 files generated by `apm install --target copilot`
- claude-azure-cloud-architect.zip: 21 files generated by `apm install --target claude`
- codex-azure-cloud-architect.zip: 20 files generated by `apm install --target codex`
- kiro-azure-cloud-architect.zip: 21 files generated by `apm install --target kiro`
- gemini-azure-cloud-architect.zip: 19 files generated by `apm install --target gemini`
- agent-skills-azure-cloud-architect.zip: 19 files generated by `apm install --target agent-skills`
- azure-cloud-architect-canonical.zip, azure-cloud-architect-prompt.zip, azure-cloud-architect-validation.zip, azure-cloud-architect-skills.zip, azure-cloud-architect-full-pack.zip, SHA256SUMS.txt
