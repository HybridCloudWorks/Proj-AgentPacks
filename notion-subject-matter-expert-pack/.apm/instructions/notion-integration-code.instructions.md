---
description: "Rules for code that calls the Notion API or a Notion MCP server: token handling, pinned API version, rate limits, pagination, payload limits and safe logging."
applyTo: "**/*notion*.py,**/*notion*.ts,**/*notion*.js,**/*notion*.mjs,**/notion/**"
---

# Notion integration code

Apply the notion-api-integration skill when this code changes.

- Read the integration token from the environment or the project's secret store. Never hard-code it, print it, put it in a URL or commit it in a fixture. Notion tokens commonly begin with `ntn_` or `secret_`; treat any such string in source as a leaked credential.
- Pin the `Notion-Version` header to the version the project already uses. Changing it is a contract change: newer versions model databases as containers of one or more data sources, which changes how pages are created and queried.
- Handle HTTP 429 by honouring `Retry-After` with bounded retries and backoff. Do not retry validation errors. Keep request rates within the documented per-integration limit.
- Follow pagination cursors until `has_more` is false, or stop at an explicit bound the caller chose. Split long rich text and large block appends into chunks that respect the documented size limits.
- Resolve property names and option values from the fetched schema; do not hard-code display names that workspace users can rename without telling the integration owner.
- Log request IDs, status codes and object IDs, not page content, comments or user emails.
- Tests use recorded or synthetic responses. A test that writes to a real workspace needs a dedicated test workspace or page tree and the user's explicit approval.
