# aws-cloud-architect 1.1.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| aws-cloud-architect.agent.md | Canonical agent: Senior AWS Cloud Architect for enterprise foundations, workload design, deployment, operations, migration, security, resilience, cost, and evidence-aware handoff. | .apm/agents/aws-cloud-architect.agent.md |
| aws-cloud-architect-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the aws cloud architect pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/aws-cloud-architect-contract.instructions.md |
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
| SKILL.md | Canonical skill: Validate Draw.io structure and AWS diagram evidence, then report static, rendered, live, and unresolved results without overstating what was proven. | .apm/skills/diagram-validation-and-evidence/SKILL.md |
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

- copilot-aws-cloud-architect.zip: 22 files generated by `apm install --target copilot`
- claude-aws-cloud-architect.zip: 22 files generated by `apm install --target claude`
- codex-aws-cloud-architect.zip: 21 files generated by `apm install --target codex`
- kiro-aws-cloud-architect.zip: 22 files generated by `apm install --target kiro`
- gemini-aws-cloud-architect.zip: 20 files generated by `apm install --target gemini`
- agent-skills-aws-cloud-architect.zip: 20 files generated by `apm install --target agent-skills`
- aws-cloud-architect-canonical.zip, aws-cloud-architect-prompt.zip, aws-cloud-architect-validation.zip, aws-cloud-architect-skills.zip, aws-cloud-architect-full-pack.zip, SHA256SUMS.txt
