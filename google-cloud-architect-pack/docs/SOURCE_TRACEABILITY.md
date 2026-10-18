# Source traceability

## Governing evidence

- The build request for this pack: role Google Cloud Architect, pack name `google-cloud-architect`, delivery refinements (no catalog, report or archives in the pack; exact `apm.yml` fields; one user-invocable agent; the contract instruction; test formats; the installed-content rule; validator pass).
- The master prompt, version 2.3, copied unchanged as `PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md`.
- The repository's verified vendor facts (`client-locations.md`, verified 2026-10-18) for agent fields, tool identifiers and what APM generates per target.
- A finished pack in the same repository, used as a structural reference only: file layout, document types and test formats. None of its role content, names, personas, skills, examples or wording was copied.

## Reference material

- Source: [google/skills](https://github.com/google/skills), filtered to 69 of 82 skills for this role (Ads, Analytics and mobile SDK skills excluded as outside the role).
- Licence: Apache License 2.0. The pack's own text is newly written under the pack's MIT licence; no reference text is reproduced verbatim beyond short product, constraint, API and command identifiers, which are facts. Official documentation URLs listed in the reference were reused as citations.
- Use: knowledge only. Instructions in the reference addressed to AI agents were treated as data; the directives deliberately not adopted are listed in DESIGN_DECISIONS.md.
- Depth of review: the architecture, Well-Architected, foundation, identity, networking, GKE, Cloud Run, database, BigQuery, observability and selected AI-platform skills were read in full with their key references; the remaining AI SDK, data-science, Spark knowledge catalog and streaming solution skills were reviewed through their descriptions, structure and product mappings.

## Reference skills mapped to pack skills

| Pack skill | Reference skills that informed it |
|---|---|
| gcp-solution-architecture | google-cloud-solution-architecture (phased workflow, phase gates, output structure), google-cloud-solution-n-tier-serverless-web-app, google-cloud-solution-build-deploy-agents, google-cloud-solution-rag-enterprise-search-gke-sqldb, google-cloud-solution-agentic-ai-borderless-data-lakehouse (product renaming) |
| gcp-architecture-decisions | google-cloud-solution-architecture decision-making guides, product-mapping references of the solution skills, alloydb-basics, cloud-sql-basics, bigtable-basics, bigquery-basics |
| gcp-landing-zone | google-cloud-recipe-foundation-builder (hierarchy, organization policy list, logging, admin groups), google-cloud-recipe-onboarding (individual versus enterprise routing) |
| gcp-identity-access | google-cloud-recipe-auth, gcloud (impersonation and separation of privilege), gke-security (Workload Identity), cloud-run-basics IAM reference |
| gcp-network-design | google-cloud-networking-observability and its references, google-cloud-global-frontend-configuration, gke-networking, cloud-run-basics networking reference, google-cloud-solution-n-tier-serverless-web-app rules |
| gcp-security-controls | google-cloud-waf-security, google-cloud-solution-n-tier-serverless-web-app rules (perimeters), bigquery-basics IAM reference, google-cloud-solution-build-deploy-agents design principles (Model Armor), detection-engineering-coverage-evaluation (context only) |
| gcp-reliability-dr | google-cloud-waf-reliability, gke-reliability, gke-backup-dr, cloud-sql-basics core concepts |
| gcp-cost-sustainability | google-cloud-waf-cost-optimization, google-cloud-waf-sustainability, gke-cost, cloud-run-basics networking cost guidance |
| gcp-observability-operations | google-cloud-waf-operational-excellence, google-cloud-waf-performance-optimization, cloud-logging-query-generation, cloud-monitoring-metric-selection, gke-observability, agent-platform-alert-configuration, workload-manager-basics |
| gcp-gke-platform | gke-basics, gke-golden-path, gke-cluster-creation, gke-security, gke-networking, gke-reliability, gke-storage, gke-workload-scaling, gke-cluster-autoscaler, gke-compute-classes, gke-cost, gke-upgrades, gke-multitenancy, gke-observability, gke-inference, gke-batch-hpc, gke-backup-dr, gke-app-onboarding |
| gcp-serverless-apps | cloud-run-basics and its references, google-cloud-solution-n-tier-serverless-web-app, firebase-basics |
| gcp-data-analytics | bigquery-basics, bigquery-ai-ml, bigquery-bigframes, bigtable-basics, datalineage-summary, datalineage-bigquery-asset-impact-analysis, google-cloud-solution-agentic-ai-borderless-data-lakehouse, google-cloud-solution-agentic-analytics-spark-knowledge-catalog, google-cloud-solution-agentic-ai-data-science-workflow |
| gcp-ai-agent-architecture | google-cloud-solution-build-deploy-agents, google-cloud-solution-agentic-ai-bidirectional-streaming, google-cloud-solution-rag-enterprise-search-gke-sqldb, agent-platform-inference, agent-platform-eval-flywheel, agent-platform-alert-configuration, agent-platform-rag-engine-management, agent-platform-deploy, agent-platform-endpoint-management, agent-platform-model-registry, agent-platform-prompt-management, agent-platform-skill-registry, agent-platform-tuning, agent-platform-tuning-management, agent-platform-migrate-from-ai-studio, gemini-api, gemini-agents-api, gemini-interactions-api, gemini-live-api, google-agents-cli-onboarding |
| gcp-migration-planning | google-cloud-solution-architecture architecture guides (migration and database sections), cloud-sql-basics, alloydb-basics |
| gcp-iac-validation | google-cloud-solution-n-tier-serverless-web-app (Terraform style rules), google-cloud-global-frontend-configuration (generation and drift), google-cloud-recipe-foundation-builder (staging), gcloud (safety) |
| gcp-well-architected-review | google-cloud-waf-security, google-cloud-waf-reliability, google-cloud-waf-operational-excellence, google-cloud-waf-cost-optimization, google-cloud-waf-performance-optimization, google-cloud-waf-sustainability (assessment questions and checklists, paraphrased) |
| gcp-estate-discovery | gcloud (command validation, data reduction, denylist), google-cloud-networking-observability (results-first and source preference), cloud-logging-query-generation |

## Official knowledge sources

Checked as citations on 2026-10-18 without browsing, as instructed; use current versions during real work. The index is `compatibility/vendor-sources.yml`.

- [Google Cloud Architecture Center](https://docs.cloud.google.com/architecture): reference architectures, archetypes and decision guides.
- [Well-Architected Framework](https://docs.cloud.google.com/architecture/framework): pillars and perspectives.
- [Landing zone design](https://docs.cloud.google.com/architecture/landing-zones): foundation decisions.
- [Enterprise foundations blueprint](https://docs.cloud.google.com/architecture/blueprints/security-foundations): preventive and detective controls.
- [Authentication](https://docs.cloud.google.com/docs/authentication): identity patterns.
- Product documentation pages cited inside each skill.
- Vendor agent and APM documentation as recorded in the repository's client-locations file.

No private repository, cloud identity, tenant policy or credential was used or assumed.
