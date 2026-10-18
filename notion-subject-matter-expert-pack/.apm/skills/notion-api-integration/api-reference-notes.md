# API reference notes

These notes summarize the Notion API's shape as an orientation. Endpoint paths, limits and error codes are versioned; confirm them in Notion's official API reference for the `Notion-Version` the project pins before relying on them.

## Integration types

- Internal integration: belongs to one workspace, authenticates with a token, and sees only pages and databases explicitly shared with it (and their descendants).
- Public integration: installed by users through OAuth; each installation yields an access token scoped to what that user shared during installation.
- Hosted MCP server: the host signs in on the user's behalf and exposes Notion operations as tools. Tool names and capabilities depend on the server and the host's prefixing; read them from the session.
- Capabilities are chosen per integration: read content, update content, insert content, read comments, insert comments, and user information with or without email addresses.

## Endpoint families

| Family | Typical operations |
|---|---|
| Search | Find pages and databases shared with the integration, matched mainly by title |
| Pages | Retrieve, create, update properties, archive or move to trash |
| Blocks | Retrieve children, append children, update, delete |
| Databases and data sources | Retrieve schema, query entries with filters and sorts, create, update schema |
| Comments | List and create comments on pages or discussions |
| Users | List users, retrieve a user, retrieve the integration's own bot user |
| File uploads | Upload files for use in file properties and blocks, where the version supports it |

Every request carries `Authorization: Bearer <token>` (from the environment, never inline) and the pinned `Notion-Version` header.

## Data sources

Recent API versions separate a database (the container) from its data sources (the tables of entries with their own schemas). Creating an entry targets a data source, and queries run against a data source. Code written for older versions that targets a database identifier directly needs a deliberate migration when the version is raised.

## Errors

| Status | Common code | Meaning | Action |
|---|---|---|---|
| 400 | validation_error, invalid_request, invalid_json | Request does not match the schema or limits | Fix the request; do not retry |
| 401 | unauthorized | Token missing, wrong or revoked | Ask the user to check the token |
| 403 | restricted_resource | Capability missing | Name the capability needed |
| 404 | object_not_found | Not shared with the integration, or wrong ID | Ask the user to share the page with the integration |
| 409 | conflict_error | Concurrent update conflict | Retry with backoff |
| 429 | rate_limited | Too many requests | Wait for `Retry-After`, then retry with backoff |
| 5xx | internal_server_error, service_unavailable | Transient server problem | Retry a bounded number of times |

## Pagination

```
cursor = none
loop:
    response = query(start_cursor=cursor, page_size=100)
    handle(response.results)
    if not response.has_more or reached_caller_bound: stop
    cursor = response.next_cursor
```

## Rate limits and retries

- The documented limit is an average of a few requests per second per integration, with short bursts tolerated. Keep concurrency low and queue work.
- Retry budget: a small fixed number of attempts with exponential backoff and jitter, capped in total time, then fail with the request ID.

## Size limits

Rich text objects, block arrays per append request and total request payloads all have documented maximums. Chunk long text into several rich text objects and append large documents in batches, preserving order.

## Sync design

- Store the external system's ID in a dedicated property and look it up before creating, so retries do not duplicate entries.
- Use last-edited timestamps or webhook events as change cursors; re-read before writing to avoid overwriting newer edits.
- Archive instead of deleting, and log the mapping of external IDs to Notion page IDs.
- Treat property renames as expected events: resolve names to IDs from the fetched schema at startup.

## Webhooks

Where the integration supports webhooks, verify the subscription with the verification token Notion sends, validate signatures on every event, treat events as hints (re-fetch the object before acting), and make handlers idempotent.

## MCP connection checklist

1. Which server: Notion's hosted server or a self-run one; the publisher and the source of the package.
2. Sign-in: OAuth through the host, or a token in the host's secret configuration.
3. Tool list: names, which are read-only, which write, which notify.
4. Scope: the pages and teamspaces the signed-in identity can reach.
5. Host permissions: whether write tools require confirmation in this host, and whether specialists can be limited to read tools.
6. A test: one search and one fetch on a known page, then stop until the user approves writes.
