---
description: "Run an Azure Well-Architected five-pillar and CAF review of an architecture and return prioritized gaps"
agent: azure-cloud-architect
---

# Review an architecture against Azure Well-Architected and CAF

## Inputs

The architecture under review (a handoff, design document, diagram, IaC repository or description), its workload requirements, the review scope, and any telemetry, incident history, test results or prior review findings. State which of these are missing.

## Workflow

1. Apply `azure-architecture-foundations` to confirm the requirements and boundaries the review measures against.
2. Apply `azure-well-architected-and-frameworks`: work through Reliability, Security, Cost Optimization, Operational Excellence and Performance Efficiency. For each material choice record the desired outcome, evidence, trade-off, residual risk, owner and follow-up. Use the CAF lifecycle concerns (Strategy, Plan, Ready, Migrate, Modernize, Cloud-native, Govern, Secure, Manage) for platform, governance and adoption gaps.
3. Go deeper only where a pillar shows a gap: `azure-resilience-dr-and-migration` for reliability, `azure-security-identity-and-compliance` for security, `azure-cost-sustainability-and-finops` for cost, `azure-operations-observability-and-troubleshooting` for operations, and `azure-workload-and-service-selection` for capacity, scaling and limits.
4. Apply `azure-docs-mcp-and-evidence` to service guidance and limits a finding depends on.

The review is read-only. Do not change resources, settings or policy to close a gap.

## Expected output

- Findings per pillar with evidence labels, keeping architecture evidence, static inspection, live telemetry and human sign-off apart.
- A prioritized gap list with owners and follow-ups. A score alone is not an acceptable result.
- An ADR for any gap whose fix is a significant decision.
- A completion report. Never describe the architecture as Well-Architected approved; the review covers only the evidence in scope.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
