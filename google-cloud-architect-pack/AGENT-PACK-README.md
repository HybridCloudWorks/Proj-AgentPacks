# google-cloud-architect 1.2.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| gcp-estate-inspector.agent.md | Canonical agent: Read-only discovery of a named Google Cloud organization, folder or project with gcloud, bq and kubectl; returns a compact, cited inventory and evidence without changing anything. | .apm/agents/gcp-estate-inspector.agent.md |
| gcp-security-reviewer.agent.md | Canonical agent: Independent read-only review of Google Cloud designs and infrastructure changes for IAM, network exposure, data protection, perimeter and supply-chain risk; returns located findings. | .apm/agents/gcp-security-reviewer.agent.md |
| google-cloud-architect.agent.md | Canonical agent: Google Cloud architect for requirements-driven solution design, landing zones, decision records, Well-Architected reviews, migration and DR planning, and plan-only infrastructure validation. | .apm/agents/google-cloud-architect.agent.md |
| gcp-cli-scripts.instructions.md | Canonical instruction: Safety rules for scripts and runbooks that call gcloud, bq, gcloud storage, gsutil or kubectl: explicit scope, validated syntax, previews and no hidden mutations. | .apm/instructions/gcp-cli-scripts.instructions.md |
| gcp-terraform.instructions.md | Canonical instruction: Guardrails for Google Cloud Terraform and OpenTofu: identity, exposure, encryption, labels, deletion protection, provider pinning and plan-only validation. | .apm/instructions/gcp-terraform.instructions.md |
| google-cloud-architect-contract.instructions.md | Canonical instruction: Approval levels, specialist handoff rules and the completion report format for the Google Cloud Architect pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/google-cloud-architect-contract.instructions.md |
| create-google-cloud-architecture-diagram.prompt.md | Canonical prompt: Turn an approved Google Cloud architecture into an editable Draw.io diagram with current Google Cloud icons, validate it structurally, semantically and visually, and report what was proven | .apm/prompts/create-google-cloud-architecture-diagram.prompt.md |
| design-google-cloud-landing-zone.prompt.md | Canonical prompt: Design a Google Cloud landing zone and identity foundation | .apm/prompts/design-google-cloud-landing-zone.prompt.md |
| design-network.prompt.md | Canonical prompt: Design Google Cloud VPC, hybrid connectivity and load balancing | .apm/prompts/design-network.prompt.md |
| design-solution.prompt.md | Canonical prompt: Design a Google Cloud solution from requirements | .apm/prompts/design-solution.prompt.md |
| optimize-cost.prompt.md | Canonical prompt: Find and plan Google Cloud cost and sustainability improvements | .apm/prompts/optimize-cost.prompt.md |
| plan-migration.prompt.md | Canonical prompt: Plan a migration to Google Cloud | .apm/prompts/plan-migration.prompt.md |
| plan-resilience.prompt.md | Canonical prompt: Plan reliability, observability and disaster recovery for a Google Cloud workload | .apm/prompts/plan-resilience.prompt.md |
| record-google-cloud-decision.prompt.md | Canonical prompt: Choose between Google Cloud options and record the decision | .apm/prompts/record-google-cloud-decision.prompt.md |
| review-architecture.prompt.md | Canonical prompt: Review a Google Cloud design or estate against the Well-Architected Framework | .apm/prompts/review-architecture.prompt.md |
| validate-iac.prompt.md | Canonical prompt: Validate Google Cloud infrastructure code with static checks and a plan | .apm/prompts/validate-iac.prompt.md |
| provider-checks.md | Canonical skill | .apm/skills/diagram-validation-and-evidence/references/provider-checks.md |
| check_drawio.py | Canonical skill | .apm/skills/diagram-validation-and-evidence/scripts/check_drawio.py |
| icon_catalog.json | Canonical skill | .apm/skills/diagram-validation-and-evidence/scripts/icon_catalog.json |
| SKILL.md | Canonical skill: Validate Draw.io diagrams for AWS, Azure, Google Cloud, or several providers together: structure, icon currency against draw.io's current libraries, boundary semantics, and source evidence, then report static, rendered, live and unresolved results without overstating what was proven. Use when reviewing, auditing or regression-checking a diagram, or before any claim that a diagram is correct. | .apm/skills/diagram-validation-and-evidence/SKILL.md |
| providers.md | Canonical skill | .apm/skills/drawio-core-generation/references/providers.md |
| upstream-routing.md | Canonical skill | .apm/skills/drawio-core-generation/references/upstream-routing.md |
| SKILL.md | Canonical skill: Create and edit native, editable Draw.io diagrams for AWS, Azure, Google Cloud, or several providers in one diagram: choose the generation path, take each provider's current icon library, and nest boundaries the way each provider scopes its networks. Use when creating or substantially editing a diagram file, choosing provider icons, or drawing account, subscription, project, region, zone, network or subnet boundaries. | .apm/skills/drawio-core-generation/SKILL.md |
| export-cli.md | Canonical skill | .apm/skills/drawio-render-export-and-review/references/export-cli.md |
| SKILL.md | Canonical skill: Export Draw.io diagrams through the installed Draw.io Desktop command line and review the rendered output for AWS, Azure, Google Cloud, or mixed diagrams: icons that failed to draw, labels, edges, boundaries and legibility. Use when exporting a diagram to PNG, SVG, PDF or JPG, inspecting a render, or troubleshooting an output that does not look right. | .apm/skills/drawio-render-export-and-review/SKILL.md |
| SKILL.md | Canonical skill: Design generative AI and agent systems on Google Cloud - single or multi-agent patterns, model choice and endpoints on Gemini Enterprise Agent Platform, agent runtimes, memory and sessions, retrieval with RAG Engine, vector databases or search, tools and MCP servers, Model Armor and agent gateways, evaluation, quotas and monitoring. Use when designing, reviewing or productionizing an AI agent, RAG application, model-serving platform or AI-enabled workflow on Google Cloud. | .apm/skills/gcp-ai-agent-architecture/SKILL.md |
| decision-record-template.md | Canonical skill | .apm/skills/gcp-architecture-decisions/decision-record-template.md |
| SKILL.md | Canonical skill: Select Google Cloud services for each component with decision guides for compute, databases, storage, messaging, orchestration, load balancing, connectivity and private access, and record significant choices as decision records. Use when comparing Google Cloud options, mapping components to products, or documenting a Day-0 or hard-to-reverse architecture decision. | .apm/skills/gcp-architecture-decisions/SKILL.md |
| SKILL.md | Canonical skill: Estimate, attribute and optimize Google Cloud cost and carbon - cost drivers per architecture, labels and billing export, budgets and alerts, rightsizing and autoscaling, pricing models such as committed use discounts and Spot VMs, storage lifecycle, network egress, low-carbon regions and Carbon Footprint data. Use when estimating the cost of a design, reviewing spend, planning savings or adding sustainability goals to a Google Cloud workload. | .apm/skills/gcp-cost-sustainability/SKILL.md |
| SKILL.md | Canonical skill: Design Google Cloud data and analytics platforms - ingestion and streaming, batch and stream processing, BigQuery warehouse and lakehouse with Apache Iceberg, Spark, governance with Knowledge Catalog, lineage and impact analysis, fine-grained access, data products and in-database AI. Use when designing or reviewing a warehouse, lakehouse, data mesh, streaming pipeline, cross-cloud analytics or data governance on Google Cloud. | .apm/skills/gcp-data-analytics/SKILL.md |
| command_guard.py | Canonical skill | .apm/skills/gcp-estate-discovery/scripts/command_guard.py |
| SKILL.md | Canonical skill: Gather evidence from a live Google Cloud organization, folder or project safely with gcloud, bq, gcloud storage and kubectl - validated command syntax, explicit scope, data reduction, a read-only identity, Cloud Asset Inventory searches and a command classifier that assigns each command an approval level before it runs. Use when an inventory, current-state assessment, review or diagnosis needs facts from a real Google Cloud environment. | .apm/skills/gcp-estate-discovery/SKILL.md |
| SKILL.md | Canonical skill: Design and review GKE platforms - Autopilot versus Standard, production golden-path defaults, Day-0 networking and identity choices, multi-tenancy, ComputeClasses, workload and cluster scaling, reliability settings, storage, Backup for GKE, upgrades and maintenance, observability and cost. Use when creating, auditing, upgrading or onboarding workloads to Google Kubernetes Engine clusters, or when choosing GKE for AI inference, batch or HPC. | .apm/skills/gcp-gke-platform/SKILL.md |
| plan_summary.py | Canonical skill | .apm/skills/gcp-iac-validation/scripts/plan_summary.py |
| SKILL.md | Canonical skill: Structure, review and validate Google Cloud infrastructure code in Terraform or OpenTofu - module and state layout, provider pinning, Google-specific review rules for IAM, exposure, encryption and deletion, static checks, policy validation, plan-only validation with a risk summary, drift detection and CI design. Use when writing, reviewing or checking Google Cloud Terraform, reading a plan before apply, or designing an infrastructure pipeline. | .apm/skills/gcp-iac-validation/SKILL.md |
| SKILL.md | Canonical skill: Design Google Cloud identity and access - workforce onboarding and federation, group-based IAM, least-privilege role design, conditions, deny policies, just-in-time elevation, workload identity without keys, and end-user access with IAP or Identity Platform. Use when deciding how people, pipelines, workloads or agents authenticate to Google Cloud and what they may do. | .apm/skills/gcp-identity-access/SKILL.md |
| SKILL.md | Canonical skill: Design a Google Cloud landing zone - organization and account planning, folder and project hierarchy, organization policy baseline, billing, centralized logging and monitoring, administrative groups and foundation IaC staging. Use when setting up or reviewing an organization foundation, adding environments or business units, or preparing an enterprise for workload onboarding. | .apm/skills/gcp-landing-zone/SKILL.md |
| SKILL.md | Canonical skill: Plan migrations to Google Cloud from on-premises, other clouds or other Google Cloud regions - assessment and discovery, migration approach per workload, service mapping, foundation readiness, wave planning, data and database migration, cutover and rollback, and post-migration optimization. Use when a user needs a migration strategy, wave plan, data transfer plan or cutover plan for moving workloads to or within Google Cloud. | .apm/skills/gcp-migration-planning/SKILL.md |
| ip_plan.py | Canonical skill | .apm/skills/gcp-network-design/scripts/ip_plan.py |
| SKILL.md | Canonical skill: Design Google Cloud networks - VPC topology and Shared VPC, IP planning for VMs, GKE and Cloud Run, private access to Google and producer services, hybrid and cross-cloud connectivity, DNS, load balancing and edge security, egress control, and read-only path diagnosis. Use when planning or reviewing VPCs, subnets, connectivity, load balancers, firewall models or a network path problem on Google Cloud. | .apm/skills/gcp-network-design/SKILL.md |
| SKILL.md | Canonical skill: Design Google Cloud observability and operations - log routing and retention, metrics scopes, SLO-based and burn-rate alerting, metric selection, Logging Query Language queries, tracing and profiling with OpenTelemetry, operational readiness, incident and change management, and continuous best-practice evaluation. Use when planning monitoring, alerting, logging, dashboards, runbooks, release processes or production readiness for a Google Cloud workload. | .apm/skills/gcp-observability-operations/SKILL.md |
| availability.py | Canonical skill | .apm/skills/gcp-reliability-dr/scripts/availability.py |
| SKILL.md | Canonical skill: Design Google Cloud reliability and disaster recovery - user-centred SLOs and error budgets, composite availability, redundancy across zones and regions, graceful degradation, backup and restore, DR patterns matched to RTO and RPO, and recovery testing. Use when setting availability targets, choosing redundancy or a DR pattern, planning backups, or checking a design against RTO and RPO. | .apm/skills/gcp-reliability-dr/SKILL.md |
| SKILL.md | Canonical skill: Design and assess Google Cloud security controls - security by design, zero trust access, VPC Service Controls perimeters, encryption and key management, secrets, sensitive data protection, threat detection, software supply chain, compliance and residency, and AI workload safety. Use when a design, review or change touches data protection, exposure, perimeters, detection, compliance obligations or deployment provenance. | .apm/skills/gcp-security-controls/SKILL.md |
| SKILL.md | Canonical skill: Design serverless application architectures on Google Cloud - Cloud Run services, jobs and worker pools, Cloud Run functions, Firebase App Hosting, event-driven flows with Pub/Sub and Eventarc, private multi-tier designs with load balancer-only ingress and internal-only backends, Direct VPC egress, service identity, IAP, database connectivity and scaling. Use when a web app, API, event handler or background job should run on serverless compute or when reviewing an existing Cloud Run design. | .apm/skills/gcp-serverless-apps/SKILL.md |
| SKILL.md | Canonical skill: End-to-end Google Cloud solution design workflow, from requirements discovery and technical decomposition through product mapping, diagram, per-pillar recommendations, deployment guidance and a validation plan. Use when a user needs a complete multi-product Google Cloud architecture for a workload or use case rather than a single product answer. | .apm/skills/gcp-solution-architecture/SKILL.md |
| solution-guide-template.md | Canonical skill | .apm/skills/gcp-solution-architecture/solution-guide-template.md |
| SKILL.md | Canonical skill: Review a Google Cloud design, estate or infrastructure change against the six pillars of the Google Cloud Well-Architected Framework - security, reliability, operational excellence, cost, performance and sustainability - with evidence-based findings, severities and a remediation roadmap. Use when asked to assess, audit, review or score an architecture, a production readiness gate, or an existing Google Cloud environment. | .apm/skills/gcp-well-architected-review/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| AGENT_INVENTORY.md | Pack contract or inventory | docs/AGENT_INVENTORY.md |
| APPROVAL_MATRIX.md | Pack contract or inventory | docs/APPROVAL_MATRIX.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| HANDOFF_CONTRACT.md | Pack contract or inventory | docs/HANDOFF_CONTRACT.md |
| INTEGRATION_CONTRACT.md | Pack contract or inventory | docs/INTEGRATION_CONTRACT.md |
| MAINTENANCE.md | Pack contract or inventory | docs/MAINTENANCE.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SKILL_INVENTORY.md | Pack contract or inventory | docs/SKILL_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| TOOL_PERMISSION_MATRIX.md | Pack contract or inventory | docs/TOOL_PERMISSION_MATRIX.md |
| dr-plan.md | Worked example | examples/dr-plan.md |
| final-completion-report.md | Worked example | examples/final-completion-report.md |
| gke-estate-review.md | Worked example | examples/gke-estate-review.md |
| iac-plan-review.md | Worked example | examples/iac-plan-review.md |
| landing-zone-design.md | Worked example | examples/landing-zone-design.md |
| migration-wave-plan.md | Worked example | examples/migration-wave-plan.md |
| copilot-instructions.md | Optional repository-level file | examples/repository/copilot-instructions.md |
| serverless-web-app-design.md | Worked example | examples/serverless-web-app-design.md |
| post-gcp-architecture.ps1 | Hook helper script | hooks/post-gcp-architecture.ps1 |
| post-gcp-architecture.sh | Hook helper script | hooks/post-gcp-architecture.sh |
| pre-gcp-command.ps1 | Hook helper script | hooks/pre-gcp-command.ps1 |
| pre-gcp-command.sh | Hook helper script | hooks/pre-gcp-command.sh |
| README.md | Hook helper script | hooks/README.md |
| google-cloud-architect.copilot-hooks.sample.json | Reviewed hook sample, not installed | hooks/samples/google-cloud-architect.copilot-hooks.sample.json |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| ip-plan.example.json | Reusable template | templates/ip-plan.example.json |
| requirements-questionnaire.md | Reusable template | templates/requirements-questionnaire.md |
| specialist-handoff.md | Reusable template | templates/specialist-handoff.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| invalid-cloud-change.json | Local test or recorded evidence | tests/fixtures/invalid-cloud-change.json |
| invalid-completion.json | Local test or recorded evidence | tests/fixtures/invalid-completion.json |
| valid-completion-report.md | Local test or recorded evidence | tests/fixtures/valid-completion-report.md |
| valid-completion.json | Local test or recorded evidence | tests/fixtures/valid-completion.json |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| test_behavior.py | Local test or recorded evidence | tests/test_behavior.py |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| completion_contract.py | Pack-specific helper code | tooling/completion_contract.py |
| requirements.txt | Pack-specific helper code | tooling/requirements.txt |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-google-cloud-architect.zip: 48 files generated by `apm install --target copilot`
- claude-google-cloud-architect.zip: 48 files generated by `apm install --target claude`
- codex-google-cloud-architect.zip: 35 files generated by `apm install --target codex`
- kiro-google-cloud-architect.zip: 38 files generated by `apm install --target kiro`
- gemini-google-cloud-architect.zip: 42 files generated by `apm install --target gemini`
- agent-skills-google-cloud-architect.zip: 32 files generated by `apm install --target agent-skills`
- google-cloud-architect-canonical.zip, google-cloud-architect-prompt.zip, google-cloud-architect-validation.zip, google-cloud-architect-skills.zip, google-cloud-architect-full-pack.zip, SHA256SUMS.txt
