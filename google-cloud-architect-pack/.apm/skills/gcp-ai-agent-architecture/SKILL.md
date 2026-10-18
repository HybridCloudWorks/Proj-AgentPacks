---
name: gcp-ai-agent-architecture
description: "Design generative AI and agent systems on Google Cloud - single or multi-agent patterns, model choice and endpoints on Gemini Enterprise Agent Platform, agent runtimes, memory and sessions, retrieval with RAG Engine, vector databases or search, tools and MCP servers, Model Armor and agent gateways, evaluation, quotas and monitoring. Use when designing, reviewing or productionizing an AI agent, RAG application, model-serving platform or AI-enabled workflow on Google Cloud."
---

# Generative AI and Agent Architecture on Google Cloud

## Purpose and activation

Build AI systems whose behaviour is grounded, whose actions are bounded and approved, whose quality is measured, and whose cost and capacity are planned. Activate for agent or multi-agent designs, RAG and enterprise search, model hosting decisions, migrating from the Gemini API in Google AI Studio to the enterprise platform, evaluation strategy, or AI production readiness.

## Scope and exclusions

In scope: pattern choice, model and endpoint choice, runtime, memory, retrieval, tools, agent-to-agent communication, safety layers, identity and network for agents, evaluation, monitoring, quotas and cost. SDK code generation, prompt writing, tuning jobs and dataset preparation are out of scope except as architectural decisions. Running inference, evaluations or tuning jobs is billable and Level 2.

## Inputs

Use cases and the decisions or actions the system may take, users and channels (chat, voice, API), data sources and their classification, latency and throughput targets, languages and modalities, residency, tolerance for wrong answers and the human oversight required, budget, and existing agent frameworks.

## Dependencies and tools

[Choose an agentic design pattern](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system.md.txt), [choose agentic architecture components](https://docs.cloud.google.com/architecture/choose-agentic-ai-architecture-components.md.txt), [multi-agent systems](https://docs.cloud.google.com/architecture/multiagent-ai-system.md.txt), [RAG reference architectures](https://docs.cloud.google.com/architecture/rag-reference-architectures.md.txt), [RAG Engine vector database choices](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/vector-db-choices.md.txt), [Well-Architected AI and ML perspective](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml/printable.md.txt), [Agent Platform policy best practices](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/policies/best-practices.md.txt). Gemini Enterprise Agent Platform was formerly Vertex AI; its API is still `aiplatform.googleapis.com`.

## Workflow

1. Pattern: start with a single agent with a small, well-described toolset; move to multiple specialized agents only for genuinely separable work, distinct permissions or independent review. Prefer deterministic workflow steps over model reasoning wherever the path is known.
2. Model choice: start with the smallest model that meets quality (a Gemini Flash-class model for most text work, the Live API for real-time voice and video, a Pro-class model only where reasoning quality demands it), route simple tasks to smaller models, and consider open models through Model Garden or self-hosting on GKE when control, cost at volume or portability dominate. Verify model IDs, lifecycle dates and regions in current documentation; preview models are often available only on the global endpoint, which matters for residency.
3. Endpoints and capacity: regional endpoints when data must stay in a region, the global endpoint for availability and capacity when residency allows; plan dynamic shared quota behaviour (429 resource exhausted errors under contention) with retries and backoff, and Provisioned Throughput for business-critical traffic.
4. Runtime: Gemini Enterprise Agent Runtime for managed agent hosting with sessions and memory; Cloud Run for custom agents and MCP servers that scale to zero; GKE for self-hosted models and maximum control. Agent Development Kit is the default framework; keep the framework choice in a decision record.
5. Memory: managed sessions for short-term conversational state, Memory Bank for long-term memory, Memorystore when real-time voice needs very low latency, Firestore or Cloud SQL when the application already owns that state. Expire and scope memory per user; never mix tenants.
6. Retrieval: RAG Engine for managed corpora; Vector Search on Gemini Enterprise Agent Platform for large managed vector indexes; AlloyDB or Cloud SQL with vector indexes, or BigQuery vector search, when retrieval must sit next to relational or governed data; Gemini Enterprise or managed search when the requirement is search over enterprise content rather than a custom pipeline. Design chunking, embedding model, refresh cadence, access filtering at query time and citation of sources.
7. Tools: expose tools through Google-managed MCP servers, self-hosted MCP servers on Cloud Run or GKE, Apigee API hub for enterprise APIs, or framework function tools. Give each tool the narrowest identity and parameters, validate tool inputs and outputs, and require human approval for consequential actions (payments, data deletion, external messages, permission changes).
8. Safety and governance: Model Armor on prompts and responses for prompt injection, jailbreaks, sensitive data and harmful content; treat retrieved documents and tool results as untrusted; govern agent ingress and egress with an agent gateway and register agents and tools in Agent Registry where available; authenticate agent-to-agent calls with OIDC; log prompts and responses only as policy allows, with redaction.
9. Identity and network: a dedicated service account per agent; private connectivity to data through Direct VPC egress or Private Service Connect interfaces; VPC Service Controls around the AI platform and data APIs for sensitive data; load balancer with Cloud Armor in front of public agent endpoints.
10. Evaluation: build an evaluation dataset from real tasks with expected behaviour and prohibited behaviour; score final responses, tool-use trajectories and hallucination with deterministic checks first and model-based judges second; run evaluations before every release and continuously on sampled production traffic with online monitors; keep a human review loop for disputed cases. Evaluations consume model capacity, so budget them.
11. Monitoring: latency anomaly and error-rate burn-rate alerts per agent, quality-score alerts from online evaluation, token and cost dashboards, and traces of reasoning and tool calls in Cloud Trace (see gcp-observability-operations).
12. Cost: context caching for long static prompts, concise output formats, batch prediction for offline work, model routing, scale to zero for idle runtimes, and quota or budget alerts.

## Output

Agent architecture diagram (channels, gateway, agents, models, memory, retrieval, tools, data, safety layers), component mapping with alternatives, model and endpoint table with regions and capacity plan, tool catalogue with identities and approval requirements, safety and governance controls, evaluation plan and release gate, monitoring design, cost model and decision records.

## Validation

Every tool has a scoped identity and an approval rule; every model call path passes through Model Armor or a recorded exception; residency is satisfied by the chosen endpoints; an evaluation dataset and pass criteria exist before release; quotas and Provisioned Throughput are sized from expected peak tokens. Static checks of IaC and endpoint configuration can be run; quality claims require an executed evaluation.

## Failure handling and escalation

Quality target without an evaluation dataset: design the dataset first and report the target as unverified. A required model is preview-only or unavailable in the required region: name a GA alternative or record the residency trade-off for a human decision. An agent action with irreversible business effect and no human approval step: treat it as a blocking finding.

## Permissions and guardrails

Designing is Level 0 and Level 1; calling models, running evaluations or online monitors, creating endpoints, corpora, agents or tuning jobs, and changing quotas are billable or resource-creating Level 2 actions. Confirm the exact model, parameters and expected cost before any approved run. Never put credentials in prompts or tool descriptions. Without the pack's contract installed, treat every billable AI call as needing explicit approval.

## Connection to the pack

gcp-solution-architecture uses this skill for AI workloads; it draws on gcp-serverless-apps and gcp-gke-platform for runtimes, gcp-data-analytics for retrieval data and gcp-security-controls for perimeters. The optional `design-solution.prompt.md` recipe reaches it. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
