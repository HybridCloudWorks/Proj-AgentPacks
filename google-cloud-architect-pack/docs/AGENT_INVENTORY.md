# Agent inventory

| Profile | Responsibility | Invocation | Declared intent (see TOOL_PERMISSION_MATRIX.md) |
|---|---|---|---|
| google-cloud-architect | Requirements-driven Google Cloud solution design, landing zones, decision records, Well-Architected reviews, migration and DR planning, and plan-only infrastructure validation. Owns integration and completion. | User-facing primary (`user-invocable: true`) | read, edit, shell, web, delegate |
| gcp-security-reviewer | Independent read-only review of designs, IaC and plan output for IAM, exposure, data protection, perimeters and supply chain. | Optional specialist (`user-invocable: false`) | read |
| gcp-estate-inspector | Read-only discovery of a named organization, folder or project with cloud CLIs; returns a compact, cited inventory. | Optional specialist (`user-invocable: false`) | read, shell |

## Why these specialists exist

The prompt's section 3 allows a specialist only where separate expertise, context, permissions or independent review adds concrete value.

- gcp-security-reviewer adds independence and a genuinely narrower permission set: no shell, no edit and no web, so it cannot touch the systems or files it reviews.
- gcp-estate-inspector adds context isolation and separation of privilege: large CLI inventories stay out of the primary's context, and it is meant to run under a separate impersonated viewer identity. It holds a shell, and a shell can change things; its boundary is the read-only cloud identity and the host's approval settings, which the agent body states openly.

No specialist was created per pillar or per product. The pillar and platform skills give the primary the same depth without an organization-chart hierarchy.

## Placement and behaviour per client

The three profiles are installed side by side in each client's agents location; no client needs a dedicated subagents directory. Because the agent files declare no `tools`, an APM install gives them whatever tools the host allows, and an installer that writes vendor files itself should translate the intents in the table instead. The specialists set `include-custom-instructions: true` so that Copilot passes the pack's instructions to them. After an APM install, Codex keeps only each agent's name, description and body, Kiro keeps description, model and tools, and Gemini CLI gets no agents at all, so Gemini users reach the workflow through skills and commands.

If a client cannot run subagents, the primary does the same work with gcp-security-controls and gcp-estate-discovery and tells the user.
