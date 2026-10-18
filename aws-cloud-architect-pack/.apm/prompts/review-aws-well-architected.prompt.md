---
description: "Run a Well-Architected six-pillar review, with CAF perspectives when readiness is in scope, and turn gaps into prioritized, owned actions"
agent: aws-cloud-architect
---

# Run a Well-Architected review

## Inputs

- Workload boundary, review date, reviewers and owners.
- Architecture evidence: diagrams, IaC, account and Region inventory, runbooks, dashboards, incident history, cost data.
- Business priorities and accepted risks, and any lenses the user wants applied.
- Whether an organizational CAF readiness view is also needed.

## Workflow

1. `aws-architecture-foundations`: fix the workload boundary and the requirements that the review judges against.
2. `aws-well-architected-and-frameworks`: for Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization and Sustainability, record the workload-specific questions asked, evidence available, gap, risk, owner, priority and recommended action.
3. Go deeper per pillar where the evidence calls for it:
   - Security: `aws-security-identity-and-compliance`
   - Reliability: `aws-resilience-dr-and-migration`
   - Operational Excellence: `aws-operations-observability-and-troubleshooting`
   - Performance Efficiency: `aws-workload-and-service-selection` and `aws-data-and-application-patterns`
   - Cost Optimization and Sustainability: `aws-cost-sustainability-and-finops`
   - Network paths: `aws-networking-hybrid-and-edge`
4. Add the six CAF perspectives when organizational readiness, a migration program or a platform operating model is in scope.
5. `aws-docs-mcp-and-evidence`: read the current framework and lens content before quoting question IDs or best practices.
6. `aws-architecture-handoff-and-adr`: record an ADR for each decision the owners accept from the review.

## Expected output

- A review record with scope, boundary, date, an evidence inventory, findings per pillar, and actions ranked high-risk first.
- CAF readiness by perspective with workstreams and owners, when requested.
- A "not reviewed" list, and a completion report in the contract's format.

## Guardrails

This is an architecture review, not a formal AWS Well-Architected Tool review, certification or audit, unless the user ran the tool and shared its results. Do not write results into the Well-Architected Tool or any shared system without authorization. Never call a workload "Well-Architected". Follow the `aws-cloud-architect-contract` instruction.
