# aws-cloud-architect 1.3.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| aws-cloud-architect.agent.md | Canonical agent: Senior AWS Cloud Architect for enterprise foundations, workload design, deployment, operations, migration, security, resilience, cost, and evidence-aware handoff. | .apm/agents/aws-cloud-architect.agent.md |
| aws-cloud-architect-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the aws cloud architect pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/aws-cloud-architect-contract.instructions.md |
| create-architecture-diagram.prompt.md | Canonical prompt: Turn an approved AWS architecture into an editable Draw.io diagram, validate it structurally, semantically and visually, and report what was proven | .apm/prompts/create-architecture-diagram.prompt.md |
| design-aws-workload.prompt.md | Canonical prompt: Design a production AWS workload from business requirements and hand it off as REQ, TOPOLOGY, CONSTRAINTS and ADR | .apm/prompts/design-aws-workload.prompt.md |
| design-hybrid-network.prompt.md | Canonical prompt: Design or choose AWS network, hybrid and edge connectivity: VPC layout, Transit Gateway, peering, PrivateLink, Direct Connect, VPN, DNS and egress | .apm/prompts/design-hybrid-network.prompt.md |
| design-landing-zone.prompt.md | Canonical prompt: Design a multi-account AWS landing zone: Organizations, Control Tower, OUs, guardrails, identity, logging, network hub and account vending | .apm/prompts/design-landing-zone.prompt.md |
| plan-migration-and-dr.prompt.md | Canonical prompt: Plan an AWS migration or disaster-recovery strategy from explicit RTO and RPO, with waves, cutover, rollback and recovery testing | .apm/prompts/plan-migration-and-dr.prompt.md |
| review-aws-cost.prompt.md | Canonical prompt: Analyze AWS architecture economics or spend and recommend measured cost and sustainability optimizations without weakening security or resilience | .apm/prompts/review-aws-cost.prompt.md |
| review-deployment-plan.prompt.md | Canonical prompt: Review a CloudFormation, CDK or Terraform change for replacement, data loss, drift, policy widening and rollback before anyone applies it | .apm/prompts/review-deployment-plan.prompt.md |
| review-well-architected.prompt.md | Canonical prompt: Run a Well-Architected six-pillar review, with CAF perspectives when readiness is in scope, and turn gaps into prioritized, owned actions | .apm/prompts/review-well-architected.prompt.md |
| troubleshoot-aws-incident.prompt.md | Canonical prompt: Investigate an AWS production incident or performance problem with a read-only, hypothesis-driven loop, keeping mitigation separate from root cause | .apm/prompts/troubleshoot-aws-incident.prompt.md |
| verify-aws-evidence.prompt.md | Canonical prompt: Verify current AWS service behavior, quotas, Region availability, pricing or CLI syntax from official sources or authorized MCP tools, and record the evidence | .apm/prompts/verify-aws-evidence.prompt.md |
| SKILL.md | Canonical skill: Discover AWS workload requirements and turn them into explicit architecture scope, constraints, assumptions, topology, and decision inputs. | .apm/skills/aws-architecture-foundations/SKILL.md |
| SKILL.md | Canonical skill: Produce implementation-ready AWS architecture handoffs with REQ, TOPOLOGY, CONSTRAINTS, ADRs, risks, verification criteria, and downstream ownership. | .apm/skills/aws-architecture-handoff-and-adr/SKILL.md |
| SKILL.md | Canonical skill: Route approved AWS architecture designs into correct editable Draw.io diagrams while preserving source evidence, boundaries, flow semantics, and visual validation limits. | .apm/skills/aws-architecture-visualization/SKILL.md |
| SKILL.md | Canonical skill: Design AWS Organizations, OUs, Control Tower landing zones, account vending, guardrails, shared services, logging, and governance boundaries. | .apm/skills/aws-caf-landing-zones-and-governance/SKILL.md |
| SKILL.md | Canonical skill: Make AWS architecture cost-aware and sustainable through demand modeling, cost drivers, transfer analysis, budgets, ownership, and measured optimization. | .apm/skills/aws-cost-sustainability-and-finops/SKILL.md |
| SKILL.md | Canonical skill: Design AWS serverless, event-driven, container, API, data platform, analytics, and AI application patterns with clear consistency and failure semantics. | .apm/skills/aws-data-and-application-patterns/SKILL.md |
| mcp-routing.md | Canonical skill | .apm/skills/aws-docs-mcp-and-evidence/references/mcp-routing.md |
| SKILL.md | Canonical skill: Retrieve current AWS documentation, API facts, service limits, Region availability, pricing, and architecture guidance through official sources or authorized MCP tools. | .apm/skills/aws-docs-mcp-and-evidence/SKILL.md |
| SKILL.md | Canonical skill: Turn AWS architecture into safe CloudFormation, CDK, or Terraform implementation plans with validation, change review, drift, rollback, and lifecycle controls. | .apm/skills/aws-iac-deployment-and-lifecycle/SKILL.md |
| SKILL.md | Canonical skill: Design and troubleshoot AWS VPC, routing, segmentation, Transit Gateway, Direct Connect, VPN, PrivateLink, DNS, CloudFront, and edge connectivity. | .apm/skills/aws-networking-hybrid-and-edge/SKILL.md |
| SKILL.md | Canonical skill: Design AWS operating models and investigate incidents using CloudWatch, CloudTrail, Config, VPC telemetry, service events, runbooks, and evidence-aware troubleshooting. | .apm/skills/aws-operations-observability-and-troubleshooting/SKILL.md |
| SKILL.md | Canonical skill: Design AWS availability, backup, disaster recovery, migration, modernization, cutover, rollback, and recovery-testing strategies from explicit RTO and RPO. | .apm/skills/aws-resilience-dr-and-migration/SKILL.md |
| SKILL.md | Canonical skill: Design AWS identity, authorization, network and data protection, detection, incident response, and compliance controls using shared-responsibility boundaries. | .apm/skills/aws-security-identity-and-compliance/SKILL.md |
| framework-routing.md | Canonical skill | .apm/skills/aws-well-architected-and-frameworks/references/framework-routing.md |
| SKILL.md | Canonical skill: Evaluate AWS designs with the Well-Architected six pillars and Cloud Adoption Framework perspectives, turning gaps into prioritized actions instead of checklist theater. | .apm/skills/aws-well-architected-and-frameworks/SKILL.md |
| SKILL.md | Canonical skill: Select and compose AWS compute, containers, serverless, storage, databases, messaging, and managed services from workload requirements and operational constraints. | .apm/skills/aws-workload-and-service-selection/SKILL.md |
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
| SKILL_INVENTORY.md | Pack contract or inventory | docs/SKILL_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| architecture-diagram.md | Worked example | examples/architecture-diagram.md |
| deployment-review-blocked.md | Worked example | examples/deployment-review-blocked.md |
| greenfield-workload-design.md | Worked example | examples/greenfield-workload-design.md |
| incident-troubleshooting.md | Worked example | examples/incident-troubleshooting.md |
| landing-zone-design.md | Worked example | examples/landing-zone-design.md |
| migration-and-dr-plan.md | Worked example | examples/migration-and-dr-plan.md |
| architecture-review.ps1 | Hook helper script | hooks/architecture-review.ps1 |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| ADR.md | Reusable template | templates/ADR.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| CONSTRAINTS.json | Reusable template | templates/CONSTRAINTS.json |
| REQ.md | Reusable template | templates/REQ.md |
| TOPOLOGY.json | Reusable template | templates/TOPOLOGY.json |
| well-architected-review.md | Reusable template | templates/well-architected-review.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| minimal.drawio | Local test or recorded evidence | tests/fixtures/minimal.drawio |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| validate_drawio_xml.py | Pack-specific helper code | tooling/validate_drawio_xml.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-aws-cloud-architect.zip: 37 files generated by `apm install --target copilot`
- claude-aws-cloud-architect.zip: 37 files generated by `apm install --target claude`
- codex-aws-cloud-architect.zip: 26 files generated by `apm install --target codex`
- kiro-aws-cloud-architect.zip: 27 files generated by `apm install --target kiro`
- gemini-aws-cloud-architect.zip: 35 files generated by `apm install --target gemini`
- agent-skills-aws-cloud-architect.zip: 25 files generated by `apm install --target agent-skills`
- aws-cloud-architect-canonical.zip, aws-cloud-architect-prompt.zip, aws-cloud-architect-validation.zip, aws-cloud-architect-skills.zip, aws-cloud-architect-full-pack.zip, SHA256SUMS.txt
