---
name: cloudflare-storage-and-state
description: "Design and implement data and state on Cloudflare with KV, D1, R2, Durable Objects, Queues, Workflows, Hyperdrive, Vectorize and Secrets Store, covering consistency, concurrency, schema migrations, idempotency, backups and limits. Use when choosing or changing a Cloudflare data store, writing Durable Objects, queue consumers or Workflows, or planning a schema or data migration on Cloudflare."
---

# Cloudflare Storage and State

## Purpose and activation

Place each piece of state in the Cloudflare store whose consistency, throughput and durability match it, then implement access, concurrency, migrations and recovery correctly. Activate for store selection, data modeling, Durable Object classes, queue consumers, Workflows, Hyperdrive connections, vector indexes, schema or data migrations, and data-loss or consistency bugs.

## Scope and exclusions

In scope: KV, D1, R2, Durable Objects and their SQLite storage, alarms and WebSockets, Queues, Workflows, Hyperdrive, Vectorize, Secrets Store, Analytics Engine writes, and moving data into these stores.

Not in scope: generic Worker code rules (cloudflare-workers-development), AI retrieval design beyond the index (cloudflare-agents-and-ai), and applying remote migrations or data changes (cloudflare-change-control).

## Required inputs

- The data, its access pattern (reads and writes per second, per key or entity), size per item and in total, consistency needs, retention and residency.
- Existing schema, migrations folder and binding names; the environments and which resource each binding points to.
- Recovery objectives: how much data loss and downtime are acceptable.

## Dependencies and tools

- Current documentation and limits pages for each store; numbers below are deliberately absent and must be retrieved.
- Project Wrangler for local commands: `wrangler d1 migrations create`, `wrangler d1 migrations apply --local`, `wrangler d1 execute --local`, `wrangler dev` with local bindings.
- `@cloudflare/vitest-pool-workers` for tests against simulated bindings, including Durable Object and alarm helpers.

## Workflow

1. Classify each piece of state with the consistency table below and choose the store. Reject a store whose write rate, item size or database size limit the workload approaches without a sharding plan.
2. Model keys and identities. For Durable Objects, pick the coordination atom (room, document, tenant, user) and a deterministic name; for D1, decide between one database and one per tenant; for KV and R2, design key prefixes for listing and lifecycle.
3. Write the access code with the product rules below, including idempotency for every at-least-once path.
4. Write migrations: D1 SQL files through `wrangler d1 migrations create`; Durable Object class changes through new migration tags; schema changes inside Durable Object SQLite through a versioned migrations table run in the constructor.
5. Test locally: concurrent writers, retries and duplicates, alarm re-execution, migration from the previous schema, and oversized items.
6. Plan recovery: backups or point-in-time restore, export procedures, and how to replay or reconcile after partial failure.
7. Hand the remote migration and any data backfill to cloudflare-change-control.

## Consistency guide

| Store | Consistency and shape | Good for | Avoid for |
|---|---|---|---|
| KV | Eventually consistent, cached at the edge, per-key write rate limit, negative lookups cached | Configuration, flags, read-mostly lookups | Counters, locks, read-after-write across locations |
| D1 | SQLite per database; strongly consistent on the primary; replicas need the Sessions API for read-your-writes | Relational data, per-tenant databases | Large blobs, unbounded single databases |
| R2 | Strongly consistent object storage, S3-compatible API | Files, media, exports, large values | Small hot counters, relational queries |
| Durable Objects | Single-threaded per object, transactional SQLite storage | Coordination, per-entity state, WebSockets, schedules | Global singletons, high fan-out stateless work |
| Queues | At-least-once delivery, batched consumers, retries and dead-letter queues | Decoupling, buffering, fan-out | Exactly-once assumptions, request-path work |
| Workflows | Durable steps with persisted results and retries | Multi-step processes, waiting for events | Sub-second hot paths |
| Hyperdrive | Pooled connections and cached reads to an existing database | Existing PostgreSQL or MySQL | Write caching, bypassing database security |
| Vectorize | Vector index with fixed dimensions and metric; writes become visible asynchronously | Semantic search | Primary storage of records |

## Product rules

KV
- Never read back a key you just wrote to confirm it; return the value you wrote. Spread hot writes across keys; batch reads with the multi-key get; handle `null` explicitly; tune `cacheTtl` for cold reads.

D1
- Always use prepared statements with `bind()`; never interpolate input into SQL. Use `batch()` for statements that must commit together. Add indexes and check plans with `EXPLAIN QUERY PLAN`.
- SQLite types apply: store booleans as integers and timestamps as ISO text or epoch integers.
- `--local` and `--remote` are different databases. Every remote migration is forward-only and must keep the running code working during rollout (expand, migrate, then contract).
- Know the point-in-time recovery window for the plan and take an export before destructive changes.

R2
- Validate keys (no `..`, no leading `/`, bounded length) before use. Page lists with `truncated` and `cursor`, not by counting results. Use `httpEtag` in headers. Supply a known length when streaming uploads. Respect multipart rules for part sizes and numbering.
- S3 clients use region `auto` and the account endpoint. Presigned URLs carry an expiry; return it to the client. Prefer a custom domain over the development `r2.dev` hostname for public production access.
- Storage classes with minimum durations bill for that duration even after deletion.

Durable Objects
- One object per coordination atom; route with `getByName()` or `idFromName()`. A single global object is a bottleneck.
- New classes use SQLite storage (`new_sqlite_classes`). Persist to storage before updating in-memory caches; in-memory state is lost on eviction.
- Related writes without an `await` between them commit together; an `await` on external I/O (`fetch`, other bindings) lets other requests interleave, so re-check state or use optimistic versions after it.
- `blockConcurrencyWhile()` only for constructor initialization and migrations, never per request or across external I/O.
- One alarm per object; `setAlarm()` replaces it. Alarm handlers are retried on failure and must be idempotent.
- Use the WebSocket Hibernation API for long-lived sockets. Use RPC methods, not a `fetch()` dispatcher, when the compatibility date supports RPC.
- `PRAGMA user_version` is not available; track schema versions in a table. Never edit an applied migration tag. A `deleted_classes` migration deletes that class's data permanently.

Queues
- Ack or retry each message explicitly. An uncaught exception retries the whole batch. Make consumers idempotent with a processed-message record. Configure a dead-letter queue and alert on it. Use `json` content when a pull consumer or the dashboard must read messages.

Workflows
- Step names are deterministic. State lives in step return values, not variables. Non-deterministic logic (time, randomness) belongs inside a step. Each step is idempotent because steps retry. Large results go to R2 with a reference returned. Instance IDs are unique per run.

Hyperdrive
- Only non-mutating queries without volatile functions are cached. Keep driver pools within the per-invocation connection limit. Consider Smart Placement when one request runs several queries. The origin database must accept Hyperdrive connections over TLS or through private connectivity.

Vectorize and Secrets Store
- Index dimensions and metric must match the embedding model and cannot be changed later. Create metadata indexes before inserting vectors that must be filterable. Enforce tenant filters server-side.
- Secrets Store values are read through an asynchronous binding call; never log the value.

## Expected output

The state placement table for the workload, the code and migrations, test evidence, the recovery plan (backup, export, restore steps and their limits), and the release notes for cloudflare-change-control: remote migrations, backfills, binding IDs per environment.

## Validation

- Tests prove duplicate delivery, concurrent writers, alarm retry and migration from the previous schema do not corrupt data.
- Every limit the design depends on has a retrieved source and date.
- Local Miniflare storage is not proof of production replication, latency or limits.

## Failure handling and escalation

- A limit blocks the design: shard (per-tenant databases, per-entity objects), batch, or move the data to another store; escalate only real limit increases to the account team.
- A migration cannot be made backward compatible: stop and present a maintenance-window plan for approval.
- Data inconsistency in production: stop writes that worsen it if authorized, capture evidence, and plan reconciliation before repair.

## Permissions and guardrails

Local edits, local databases and tests only. `wrangler d1 execute --remote`, `d1 migrations apply --remote`, KV or R2 writes and deletes, queue purges, Vectorize writes, Durable Object class deletions and data backfills change live data and need explicit approval for the exact resource and environment, with a backup or export taken first. Never export production data to the workspace without approval and a stated retention.

## Workflow connection

Within the complete pack, the optional `build-workers-application.prompt.md` recipe connects this skill to the primary `cloudflare-subject-matter-expert` workflow, with remote changes going through `release-cloudflare-change.prompt.md`. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval, handoff and completion rules.
