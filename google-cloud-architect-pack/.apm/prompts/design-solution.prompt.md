---
description: "Design a Google Cloud solution from requirements"
agent: google-cloud-architect
---

# Design a Google Cloud solution

## Inputs

The workload or use case the user describes, any requirements, constraints, existing architecture or files they supply, and the acceptance criteria. Discover missing facts from the supplied material before asking; ask for missing non-functional requirements and explain why each one changes the design. Do not invent organization IDs, regions, compliance regimes or budgets.

## Workflow

Apply gcp-solution-architecture. Resolve contradictions before proposing products, get the technical decomposition confirmed, then use gcp-architecture-decisions for product mapping and decision records and the platform skill that fits (gcp-serverless-apps, gcp-gke-platform, gcp-data-analytics, gcp-ai-agent-architecture). Apply gcp-security-controls, gcp-reliability-dr, gcp-cost-sustainability and gcp-observability-operations for per-pillar recommendations. Present each deliverable for approval before building the next one, unless the user asked for the whole design at once.

## Expected output

A solution guide with requirements, decomposition, product mapping with alternatives, a Mermaid diagram, data and control flows, per-pillar recommendations, decision records, deployment guidance and a validation plan, followed by the completion report. Apply the `google-cloud-architect-contract` instruction; an earlier approval covers only the exact action it named.
