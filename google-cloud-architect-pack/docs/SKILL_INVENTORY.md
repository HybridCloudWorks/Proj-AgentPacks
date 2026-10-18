# Skill inventory

| Skill | Activation | Bundled files | Workflow prompt |
|---|---|---|---|
| gcp-solution-architecture | A complete multi-product Google Cloud architecture is needed for a workload or use case. | solution-guide-template.md | design-solution.prompt.md |
| gcp-architecture-decisions | Comparing Google Cloud options, mapping components to products, or recording a Day-0 or hard-to-reverse decision. | decision-record-template.md | record-decision.prompt.md |
| gcp-landing-zone | Setting up or reviewing an organization foundation, adding environments or business units. | none | design-landing-zone.prompt.md |
| gcp-identity-access | Deciding how people, pipelines, workloads or agents authenticate and what they may do. | none | design-landing-zone.prompt.md |
| gcp-network-design | Planning or reviewing VPCs, subnets, connectivity, load balancers, firewall models or a path problem. | scripts/ip_plan.py | design-network.prompt.md |
| gcp-security-controls | Data protection, exposure, perimeters, detection, compliance or deployment provenance are in scope. | none | review-architecture.prompt.md |
| gcp-reliability-dr | Availability targets, redundancy, DR patterns, backups or RTO and RPO checks. | scripts/availability.py | plan-resilience.prompt.md |
| gcp-cost-sustainability | Cost estimates, spend reviews, savings plans or sustainability goals. | none | optimize-cost.prompt.md |
| gcp-observability-operations | Monitoring, alerting, logging, dashboards, runbooks, releases or production readiness. | none | plan-resilience.prompt.md |
| gcp-gke-platform | Creating, auditing, upgrading or onboarding to GKE, or GKE for inference, batch or HPC. | none | design-solution.prompt.md |
| gcp-serverless-apps | Web apps, APIs, event handlers or jobs on Cloud Run and related serverless services. | none | design-solution.prompt.md |
| gcp-data-analytics | Warehouses, lakehouses, data meshes, streaming, cross-cloud analytics or governance. | none | design-solution.prompt.md |
| gcp-ai-agent-architecture | AI agents, RAG, model serving or AI-enabled workflows. | none | design-solution.prompt.md |
| gcp-migration-planning | Migration strategy, waves, data transfer or cutover to or within Google Cloud. | none | plan-migration.prompt.md |
| gcp-iac-validation | Writing, reviewing or planning Google Cloud Terraform, or designing an infrastructure pipeline. | scripts/plan_summary.py | validate-iac.prompt.md |
| gcp-well-architected-review | Assessing a design, estate or readiness gate against the six pillars. | none | review-architecture.prompt.md |
| gcp-estate-discovery | Facts are needed from a live Google Cloud environment. | scripts/command_guard.py | review-architecture.prompt.md |
| drawio-core-generation | Creating or substantially editing a Draw.io diagram, choosing provider icons, or drawing scope and network boundaries, for Google Cloud alone or with AWS, Azure or on-premises systems. | references/providers.md, references/upstream-routing.md | create-architecture-diagram.prompt.md |
| drawio-render-export-and-review | Exporting a diagram to PNG, SVG, PDF or JPG, inspecting a render, or troubleshooting an output. | references/export-cli.md | create-architecture-diagram.prompt.md |
| diagram-validation-and-evidence | Reviewing, auditing or regression-checking a diagram, or before claiming it is correct. | scripts/check_drawio.py, scripts/icon_catalog.json, references/provider-checks.md | create-architecture-diagram.prompt.md |

Each SKILL.md states purpose and activation, scope and exclusions, inputs, dependencies and tools, workflow, output, validation, failure handling and escalation, permissions and guardrails, and its connection to the pack. Every skill also carries its own approval guardrail so it stays safe when installed alone, and its scripts depend only on the Python standard library. The skills describe how the model should work; whether a given model run follows them is a behavioural question that only testing in a real client answers.

The three draw.io skills are shared skills: the AWS and Azure architect and designer packs ship byte-identical copies, so a user-scope install of several packs leaves one consistent version. They are maintained in one canonical copy in the source repository, and CI fails if a pack's copy drifts. The other seventeen skill names start with `gcp-`.
