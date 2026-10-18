# Skill inventory

Seventeen skills ship in `.apm/skills/`. The primary agent `aws-cloud-architect` starts with `aws-architecture-foundations` and routes only the skills a task needs. Activation text is paraphrased from each SKILL.md.

| Skill | Activation | Workflow prompts | Worked examples |
|---|---|---|---|
| aws-architecture-foundations | Start of any AWS architecture work, or when requirements, current state, ownership or constraints are unclear | design-aws-workload, design-aws-landing-zone, design-aws-hybrid-network, plan-aws-migration-and-dr, review-aws-well-architected, review-aws-cost | greenfield-workload-design, landing-zone-design, migration-and-dr-plan |
| aws-workload-and-service-selection | Service choice, solution architecture, modernization or workload decomposition | design-aws-workload, plan-aws-migration-and-dr, review-aws-cost, review-aws-well-architected | greenfield-workload-design, migration-and-dr-plan |
| aws-data-and-application-patterns | Application topology, event-driven systems, APIs, data platforms, containers or AI workloads | design-aws-workload, review-aws-well-architected | greenfield-workload-design |
| aws-networking-hybrid-and-edge | VPCs, routing, Transit Gateway, Direct Connect, VPN, PrivateLink, DNS, CloudFront and edge | design-aws-hybrid-network, design-aws-landing-zone, troubleshoot-aws-incident, review-aws-cost | landing-zone-design, incident-troubleshooting |
| aws-security-identity-and-compliance | IAM, Identity Center, SCPs, KMS, detection services, compliance or threat-informed design | design-aws-landing-zone, review-deployment-plan, design-aws-workload, troubleshoot-aws-incident | landing-zone-design, deployment-review-blocked |
| aws-caf-landing-zones-and-governance | Multi-account strategy, Control Tower, Organizations, OUs, SCPs, account vending | design-aws-landing-zone | landing-zone-design, deployment-review-blocked |
| aws-well-architected-and-frameworks | Architecture reviews, readiness assessments, trade-off analysis, framework alignment | review-aws-well-architected, design-aws-workload, design-aws-landing-zone | greenfield-workload-design, landing-zone-design |
| aws-resilience-dr-and-migration | HA, DR, backups, multi-Region, migration waves, cutover, rollback, recovery testing | plan-aws-migration-and-dr, review-deployment-plan, design-aws-workload | migration-and-dr-plan, deployment-review-blocked |
| aws-iac-deployment-and-lifecycle | CloudFormation, CDK, Terraform, change sets, plans, drift, import, rollback | review-deployment-plan, design-aws-workload, design-aws-landing-zone, troubleshoot-aws-incident | deployment-review-blocked, landing-zone-design |
| aws-operations-observability-and-troubleshooting | Operational readiness, SLOs, alarms, logs, traces, incidents, production troubleshooting | troubleshoot-aws-incident, plan-aws-migration-and-dr, design-aws-workload | incident-troubleshooting, migration-and-dr-plan |
| aws-cost-sustainability-and-finops | Region or service economics, spend analysis, optimization, commitments, sustainability | review-aws-cost, design-aws-workload, design-aws-landing-zone, design-aws-hybrid-network | greenfield-workload-design, incident-troubleshooting |
| aws-docs-mcp-and-evidence | A recommendation depends on current AWS behavior, limits, pricing, Region availability or live account evidence | verify-aws-evidence, and every other prompt | Evidence tables in every example |
| aws-architecture-handoff-and-adr | An architecture is handed to IaC, platform, security, migration, operations or FinOps engineers | design-aws-workload, design-aws-landing-zone, design-aws-hybrid-network, plan-aws-migration-and-dr | greenfield-workload-design, landing-zone-design, migration-and-dr-plan |
| aws-architecture-visualization | A design needs a Draw.io diagram, visual review, export or architecture-to-diagram traceability | create-aws-architecture-diagram | architecture-diagram |
| drawio-core-generation | Any `.drawio` creation or substantive edit, for AWS alone or with Azure, Google Cloud or on-premises systems | create-aws-architecture-diagram | architecture-diagram |
| drawio-render-export-and-review | PNG, SVG, PDF or JPG export, renderer-based inspection, or an output that looks wrong, for any provider | create-aws-architecture-diagram | architecture-diagram |
| diagram-validation-and-evidence | Final diagram review, regression checks, source-to-diagram audits, or any claim that a diagram is correct; checks AWS, Azure and Google Cloud icons against draw.io's current libraries | create-aws-architecture-diagram | architecture-diagram |

## Templates the skills produce

| Template | Produced by | Notes |
|---|---|---|
| `templates/REQ.md` | aws-architecture-handoff-and-adr | Also carries verification criteria, ownership, open questions and the "not proven" list |
| `templates/TOPOLOGY.json` | aws-architecture-handoff-and-adr | Every entry carries an evidence label. Ids are reused as diagram cell IDs |
| `templates/CONSTRAINTS.json` | aws-architecture-handoff-and-adr | Quotas are recorded as dated evidence; recovery and rollback constraints live here |
| `templates/ADR.md` | aws-architecture-handoff-and-adr | One section per decision, with supersession instead of rewriting |
| `templates/completion-report.md` | aws-cloud-architect-contract instruction | The twelve contract sections in contract order |
| `templates/well-architected-review.md` | aws-well-architected-and-frameworks | Six pillars, prioritized actions, optional CAF perspectives |

The handoff file names match what the optional `hooks/architecture-review.ps1` checks for.

Each SKILL.md is an operational instruction for the model. It does not guarantee that a model always follows it, and the pack's tests check metadata and contracts, not model behavior.
