---
name: azure-evidence-and-mcp-review
description: Grounds Azure review claims in current Microsoft documentation, Azure MCP results, repository evidence, previews, and clearly labeled confidence boundaries.
---

# Azure Evidence and MCP Review

Prefer Microsoft Learn, Azure Architecture Center, Azure Policy documentation, Bicep/ARM references, Terraform/AVM specifications, and official Azure MCP documentation. Record source, retrieval date, scope, version/API, observed fact, and confidence for drift-prone claims.

Use Azure MCP or CLI read-only queries only when the host exposes the tool and the user authorizes the scope. Never use natural-language convenience to bypass RBAC, tenant/subscription boundaries, approval gates, secret handling, or mutation controls.

Separate `observed`, `inferred`, `designed`, `structurally-validated`, `preview-verified`, `live-read-verified`, and `not-verified`. A source document does not prove the repository follows it, and a static review does not prove live policy compliance.
