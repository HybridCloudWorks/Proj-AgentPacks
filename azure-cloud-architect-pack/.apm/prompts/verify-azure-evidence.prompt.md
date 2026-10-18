---
description: "Verify drift-prone Azure facts against Microsoft Learn and authorized Azure MCP evidence before a design depends on them"
agent: azure-cloud-architect
---

# Verify Azure facts before relying on them

## Inputs

The claims to check, such as a service limit, API version, provider or module requirement, region or zone availability, SKU behaviour, or price; the region, scope and versions they apply to; the decision or ADR that depends on each one; which documentation and Azure MCP tools the host exposes; and whether live read-only queries are authorized, at which scope.

## Workflow

1. Apply `azure-docs-mcp-and-evidence`. Prefer primary sources: Microsoft Learn, Azure Architecture Center, CAF, WAF, service documentation, the ARM and Bicep reference, the Azure Verified Modules specifications, and the official Azure MCP documentation. For each claim record the source URL, retrieval date, scope or region, API, provider or module version, the observed fact, its confidence, and the evidence type (documentation, static repository inspection, rendered artifact, live read-only query, live mutation, or third-party).
2. Use Azure MCP or CLI read queries only when the host exposes them and the user has authorized that tenant or subscription scope. A natural-language tool does not widen the scope, roles or approvals.
3. When a source cannot be retrieved, say so and downgrade the claim to an assumption or a validation task.
4. Apply `azure-architecture-handoff-and-adr` to update each dependent ADR or constraint, and say which recommendations changed.

Never run a mutating command to test a claim.

## Expected output

- An evidence register with one row per claim and its label (observed, live-verified or not-verified).
- The decisions and constraints that changed, and those still waiting on evidence.
- A completion report.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
