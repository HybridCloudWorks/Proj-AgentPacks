---
name: azure-docs-mcp-and-evidence
description: Retrieves and records current official Azure documentation, Azure MCP evidence, API/version facts, limits, availability, pricing context, and confidence boundaries.
---

# Azure Documentation, MCP, and Evidence

Prefer primary sources: Microsoft Learn, Azure Architecture Center, CAF, WAF, Azure service documentation, ARM/Bicep reference, Azure Verified Modules specifications, and official Azure MCP documentation. Use Azure MCP only when the host exposes it and the requested action is authorized.

For every drift-prone claim record source URL, retrieval date, scope/region, API/provider/module version, observed fact, and confidence. Distinguish documentation, static repository inspection, rendered artifact, live read-only query, live mutation, and third-party evidence.

Never let MCP natural-language convenience bypass tenant/subscription scope, RBAC, least privilege, approval gates, secret handling, or user authorization. If a source cannot be retrieved, say so and downgrade the claim to an assumption or validation task.
