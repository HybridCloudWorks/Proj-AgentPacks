# azure-cloud-architect 1.4.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| azure-cloud-architect.agent.md | Canonical agent: Senior Azure Cloud Architect for foundations, landing zones, workload design, deployment, operations, migration, security, resilience, cost, AVM, and evidence-aware handoff. | .apm/agents/azure-cloud-architect.agent.md |
| azure-cloud-architect-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the azure cloud architect pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/azure-cloud-architect-contract.instructions.md |
| create-azure-architecture-diagram.prompt.md | Canonical prompt: Produce an editable Draw.io diagram from an approved Azure TOPOLOGY and reconcile it against the handoff | .apm/prompts/create-azure-architecture-diagram.prompt.md |
| design-azure-hybrid-network.prompt.md | Canonical prompt: Design Azure hybrid and edge networking: hub-spoke or Virtual WAN, ExpressRoute or VPN, Private Link, DNS, ingress and egress | .apm/prompts/design-azure-hybrid-network.prompt.md |
| design-azure-landing-zone.prompt.md | Canonical prompt: Design or audit Azure platform and application landing zones: management groups, subscriptions, policy, identity, network hub and governance | .apm/prompts/design-azure-landing-zone.prompt.md |
| design-azure-workload.prompt.md | Canonical prompt: Design an Azure workload from business requirements and produce the REQ, TOPOLOGY, CONSTRAINTS and ADR handoff | .apm/prompts/design-azure-workload.prompt.md |
| estimate-azure-cost.prompt.md | Canonical prompt: Build an assumption-based Azure cost model with drivers, budgets, FinOps controls and sustainability trade-offs | .apm/prompts/estimate-azure-cost.prompt.md |
| plan-azure-migration-and-dr.prompt.md | Canonical prompt: Plan an Azure migration and disaster recovery strategy with RTO/RPO tiers, cutover, rollback and recovery rehearsal | .apm/prompts/plan-azure-migration-and-dr.prompt.md |
| review-azure-well-architected.prompt.md | Canonical prompt: Run an Azure Well-Architected five-pillar and CAF review of an architecture and return prioritized gaps | .apm/prompts/review-azure-well-architected.prompt.md |
| review-iac-and-deployment-plan.prompt.md | Canonical prompt: Review Bicep, ARM or Terraform/AVM changes and their what-if or plan output for replacement risk, identity, state, drift and production gates | .apm/prompts/review-iac-and-deployment-plan.prompt.md |
| troubleshoot-azure-issue.prompt.md | Canonical prompt: Diagnose an Azure deployment, access, network or runtime failure from evidence, separating confirmed cause from hypothesis | .apm/prompts/troubleshoot-azure-issue.prompt.md |
| verify-azure-evidence.prompt.md | Canonical prompt: Verify drift-prone Azure facts against Microsoft Learn and authorized Azure MCP evidence before a design depends on them | .apm/prompts/verify-azure-evidence.prompt.md |
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
| provider-checks.md | Canonical skill | .apm/skills/diagram-validation-and-evidence/references/provider-checks.md |
| check_drawio.py | Canonical skill | .apm/skills/diagram-validation-and-evidence/scripts/check_drawio.py |
| icon_catalog.json | Canonical skill | .apm/skills/diagram-validation-and-evidence/scripts/icon_catalog.json |
| SKILL.md | Canonical skill: Validate Draw.io diagrams for AWS, Azure, Google Cloud, or several providers together: structure, icon currency against draw.io's current libraries, boundary semantics, and source evidence, then report static, rendered, live and unresolved results without overstating what was proven. Use when reviewing, auditing or regression-checking a diagram, or before any claim that a diagram is correct. | .apm/skills/diagram-validation-and-evidence/SKILL.md |
| providers.md | Canonical skill | .apm/skills/drawio-core-generation/references/providers.md |
| upstream-routing.md | Canonical skill | .apm/skills/drawio-core-generation/references/upstream-routing.md |
| SKILL.md | Canonical skill: Create and edit native, editable Draw.io diagrams for AWS, Azure, Google Cloud, or several providers in one diagram: choose the generation path, take each provider's current icon library, and nest boundaries the way each provider scopes its networks. Use when creating or substantially editing a diagram file, choosing provider icons, or drawing account, subscription, project, region, zone, network or subnet boundaries. | .apm/skills/drawio-core-generation/SKILL.md |
| export-cli.md | Canonical skill | .apm/skills/drawio-render-export-and-review/references/export-cli.md |
| SKILL.md | Canonical skill: Export Draw.io diagrams through the installed Draw.io Desktop command line and review the rendered output for AWS, Azure, Google Cloud, or mixed diagrams: icons that failed to draw, labels, edges, boundaries and legibility. Use when exporting a diagram to PNG, SVG, PDF or JPG, inspecting a render, or troubleshooting an output that does not look right. | .apm/skills/drawio-render-export-and-review/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| architecture-diagram-workflow.md | Worked example | examples/architecture-diagram-workflow.md |
| deployment-failure-troubleshooting.md | Worked example | examples/deployment-failure-troubleshooting.md |
| greenfield-workload-design.md | Worked example | examples/greenfield-workload-design.md |
| iac-deployment-review-blocked.md | Worked example | examples/iac-deployment-review-blocked.md |
| landing-zone-design.md | Worked example | examples/landing-zone-design.md |
| migration-and-dr-plan.md | Worked example | examples/migration-and-dr-plan.md |
| architecture-review.ps1 | Hook helper script | hooks/architecture-review.ps1 |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| evidence-register.md | Reusable template | templates/evidence-register.md |
| ADR.md | Reusable template | templates/handoff/ADR.md |
| CONSTRAINTS.json | Reusable template | templates/handoff/CONSTRAINTS.json |
| REQ.md | Reusable template | templates/handoff/REQ.md |
| TOPOLOGY.json | Reusable template | templates/handoff/TOPOLOGY.json |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| minimal.drawio | Local test or recorded evidence | tests/fixtures/minimal.drawio |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| validate_drawio_xml.py | Pack-specific helper code | tooling/validate_drawio_xml.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-azure-cloud-architect.zip: 36 files generated by `apm install --target copilot`
- claude-azure-cloud-architect.zip: 36 files generated by `apm install --target claude`
- codex-azure-cloud-architect.zip: 25 files generated by `apm install --target codex`
- kiro-azure-cloud-architect.zip: 26 files generated by `apm install --target kiro`
- gemini-azure-cloud-architect.zip: 34 files generated by `apm install --target gemini`
- agent-skills-azure-cloud-architect.zip: 24 files generated by `apm install --target agent-skills`
- azure-cloud-architect-canonical.zip, azure-cloud-architect-prompt.zip, azure-cloud-architect-validation.zip, azure-cloud-architect-skills.zip, azure-cloud-architect-full-pack.zip, SHA256SUMS.txt
