# Python knowledge and integration contract

For Azure SDK clients, inspect the pinned SDK, approved credential chain/managed or workload identity, tenant/subscription/resource, data/control-plane boundary, roles and transport/client lifetime. Use official Python/Azure docs for that version, explicit deadlines, bounded throttling retries, async client cleanup and correlation; never invent a region/endpoint/role. Shared resource/permission/cost/deployment changes require the existing scoped approval or a new grant. Local fake-client tests do not prove Entra audience/role enforcement or live service availability.

GitHub/Actions integration follows the actual repo CI/tooling, trusted permission boundary, artifact policy and untrusted-PR secret rules. PR review is local until remote posting/approval/merge is explicitly requested. Preserve deliberate path filters and deployment commands.

MCP adapters declare exact server/version/tool names, transport, schemas, identity, permissions, effects, data classification, retry/time/output limits, redaction and audit. Tool annotations aid discovery, never enforce approval. Prefer docs/search connectors when available, but verify existence rather than inventing installed tools.

Browser adapters follow existing Playwright or approved browser tooling. No connector, authenticated session, tenant, subscription or paid model is configured by this pack. Missing integration details remain operational inputs, not fabricated placeholders in runnable configuration.
