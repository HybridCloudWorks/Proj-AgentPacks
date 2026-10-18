---
name: notion-api-integration
description: Build, review and troubleshoot code and connections that use the Notion API or a Notion MCP server - integration types and capabilities, sharing pages with an integration, pinned API versions and data sources, pagination, rate limits, payload limits, webhooks, sync jobs and safe token handling. Use when a user wants to connect an agent or tool to Notion, automate Notion from a script, sync Notion with another system, or debug Notion API errors such as 401, 403, 404, 409, 429 or validation failures.
---

# Notion API Integration

## Purpose and activation

Connect software to Notion with the least access that works, code that survives rate limits and schema edits, and no leaked tokens. Activate for MCP connection setup, API scripts, sync jobs, webhooks, integration reviews and API error diagnosis.

## Scope and exclusions

- In scope: internal (token) and public (OAuth) integrations, capability selection, page sharing to integrations, Notion MCP server connection, API version pinning, pages, blocks, databases and data sources, search, comments, users, pagination, retries, chunking, idempotent sync, webhooks, tests and logging.
- Out of scope: workspace structure and schema design decisions (notion-workspace-architecture, notion-database-design), deploying services to production, and creating or rotating credentials on the user's behalf.

## Inputs

- The goal: what must read or write which pages or databases, how often, and from where.
- The project's language, existing Notion client or SDK, and the pinned `Notion-Version`.
- How the connection authenticates: an internal integration token, OAuth, or a hosted MCP server the host signs into.
- The test workspace or page tree that may be written to.
- For errors: the request, the response status and error code, and the request ID, with tokens removed.

## Dependencies and tools

- The project's repository, tests and runtime, through the host's read, edit and shell tools.
- Notion's official API reference and changelog for the version the project pins; verify limits and field names there rather than relying on memory.
- api-reference-notes.md in this skill folder: endpoint families, error handling table, pagination and retry patterns, chunking, sync design and the MCP connection checklist.

## Workflow

1. Clarify access. List the pages and databases the integration needs and the capabilities it needs (read content, update content, insert content, read or insert comments, user information). Choose the smallest set. An integration sees only pages shared with it and their descendants.
2. Pin the API version. Use the version the project already pins. Newer versions model databases as containers of data sources, so creating and querying entries goes through a data source identifier; plan any version upgrade as its own change.
3. Read the schema at runtime or from configuration, never from hard-coded display names alone. Map external fields to property IDs or names in one place.
4. Implement requests with bounded retries: honour `Retry-After` on 429, retry 409 conflicts and transient 5xx with backoff, and never retry validation errors. Follow pagination cursors to the end or to an explicit bound. Split long text and large block lists to stay inside the documented size limits.
5. For sync jobs, make writes idempotent: store the external ID in a property, look it up before creating, use last-edited timestamps as cursors, and archive rather than delete.
6. For MCP connections, confirm the server's identity and source, the sign-in method, the tools it exposes and whether each is read or write. Connecting a new server is Level 2. Prefer a configuration that limits the agent to read tools for review-only work.
7. Test with recorded or synthetic responses first. Writes to a real workspace use a dedicated test page tree and the user's approval.
8. Review logs and errors for leaked content: log request IDs, status codes and object IDs only.
9. Report changed files, checks run with their results, access granted, and what was not exercised against a live workspace.

## Output

Code or configuration changes with tests, an access and capability list, an error diagnosis with the fix, or a connection checklist completed for the user to act on.

## Validation

- Tests cover pagination past the first page, a 429 with `Retry-After`, a validation error that is not retried, and a renamed property or option.
- No token appears in code, fixtures, logs, URLs or test output.
- Live calls, if any were approved, are reported with their target page tree and results; otherwise the report says live behaviour is not established.

## Failure handling and escalation

- 401: the token is wrong, revoked or for another workspace; ask the user to check it, never print it.
- 403 or restricted resource: the integration lacks a capability; name the capability.
- 404 or object not found: usually the page is not shared with the integration; explain how the user shares it, rather than widening access yourself.
- Repeated 429: lower concurrency and add backoff; report the measured rate.
- Unclear version behaviour: stop and check the official changelog for the pinned version.

## Permissions and guardrails

- Never create, rotate, print or commit tokens. Use the environment or the project's secret store.
- Connecting an MCP server or integration, granting capabilities, sharing pages with an integration, creating webhooks and running writes against a real workspace are Level 2.
- Editing project code and running local tests is Level 1 in the repository the user is working in.

## Workflow connection

The primary `notion-subject-matter-expert` agent uses this skill through the pack's integration prompt; the pack's path-scoped integration-code instruction points here when Notion client code changes. Installed alone, it is self-contained: keep tokens out of everything you write, test offline first, and get approval before touching a live workspace or connecting a server. With the full pack installed, the `notion-subject-matter-expert-contract` instruction supplies the approval levels, handoff rules and completion report.
