# Evidence register: workload or review name

The `azure-docs-mcp-and-evidence` Skill requires a record for every drift-prone claim a design depends on: regional and zone availability, service limits and quotas, SKU behaviour, API, provider and module versions, AVM specification requirements, pricing, and deprecations. Keep one register per handoff, and cite its IDs from `TOPOLOGY.json`, `CONSTRAINTS.json`, `ADR.md` and the completion report.

Prefer primary sources: Microsoft Learn, Azure Architecture Center, Cloud Adoption Framework, Well-Architected Framework, service documentation, the ARM and Bicep reference, Azure Verified Modules specifications, and the official Azure MCP documentation.

## Register

| ID | Claim | Source URL or tool | Retrieved (date) | Scope or region | API, provider or module version | Observed fact | Evidence type | Confidence | Label | Used by |
|---|---|---|---|---|---|---|---|---|---|---|
| E-01 | The statement the design relies on | URL, or the MCP tool and query | Date | Region, subscription or "global" | Version, or "n/a" | What the source actually says, quoted or closely paraphrased | documentation | high, medium or low | observed | ADR-001, C-SKU-01 |

Evidence types: documentation, static repository inspection, rendered artifact, live read-only query, live mutation, third-party.

Labels: observed (retrieved documentation or supplied file), live-verified (authorized read-only query against the real scope), not-verified (not retrieved or not checked).

## Rules

- A live query records the tenant or subscription, the identity used, and the authorization that allowed it. Natural-language MCP tools do not widen scope, roles or approvals.
- A claim whose source could not be retrieved stays in the register with source "not retrieved", label not-verified, and the validation task that would close it.
- When a newer source contradicts an older row, add a new row and mark the old one superseded; do not edit history.
- Third-party sources can explain behaviour but cannot be the only evidence for a limit, availability or price.

## Validation tasks

| ID | Claim waiting on evidence | What would verify it | Owner | Blocks |
|---|---|---|---|---|
| E-03 | | | | ADR-001 |
