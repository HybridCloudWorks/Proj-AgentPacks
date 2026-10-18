---
name: aws-docs-mcp-and-evidence
description: Retrieve current AWS documentation, API facts, service limits, Region availability, pricing, and architecture guidance through official sources or authorized MCP tools.
---

# AWS Documentation, MCP, and Evidence

Use this Skill whenever a recommendation depends on current AWS behavior, limits, pricing, Region availability, SDK/CLI syntax, framework questions, or live account evidence.

## Preferred evidence order

1. Official AWS documentation, API references, service quotas, pricing, What's New, Architecture Center, Prescriptive Guidance, and Well-Architected sources.
2. Official AWS Knowledge MCP Server for current documentation, architecture guidance, agent skills, and Region listing when remote MCP is available.
3. AWS MCP Server/Agent Toolkit or specialized official AWS Labs MCP servers for authorized live/read-only evidence or service workflows.
4. Local CLI/SDK output and repository evidence, with command/version/profile/Region recorded.

Do not use an MCP tool merely because its name sounds authoritative. Inspect available tools, verify the target account/profile/Region, understand read versus write permissions, and ask before mutation. The AWS API MCP Server and older core bundles may be superseded; follow current migration guidance rather than copying stale configuration.

## Evidence record

Record source URL or tool, retrieval date, account/Region if applicable, query/command, result summary, uncertainty, and what remains unverified. Never expose credentials, secrets, tokens, or sensitive state in the report.

Read [references/mcp-routing.md](references/mcp-routing.md) for current routing and safety.
