# Worked example: order intake on Workers with D1 and Queues

Request: "Add `POST /orders` to our Worker. Store the order in D1 and send a confirmation email asynchronously." Acceptance criteria: invalid payloads get 400; a retried request with the same idempotency key creates one order; the email job runs off the request path.

1. Scope and inspect (Level 0). The primary reads `wrangler.jsonc`, `package.json` and the lock file: Wrangler and workers-types are pinned, one `env.staging`, an existing `DB` D1 binding, no queue. It runs the configuration checker from cloudflare-workers-development: one `warn` (`observability-off`) and one `info` (`bindings-not-inherited` for staging).
2. Retrieve. It fetches the current Queues and D1 documentation for the consumer API, retry options, batch limits and the D1 statement limits it will approach, and notes the source and date of each.
3. Design with cloudflare-storage-and-state. The order row and an idempotency key live in D1 under a unique constraint; the email job goes to a queue whose consumer acks or retries each message and records processed message IDs. A dead-letter queue is configured.
4. Implement (Level 1). Prepared statements with `bind()`; the body is size-checked before parsing; the producer `send()` is awaited; the consumer catches errors per message. The queue producer and consumer are added to both the top level and `env.staging`, `observability` is enabled, and `wrangler types` regenerates `Env`. A new migration file adds the table and the unique index.
5. Verify locally. Vitest with the Workers pool: invalid payload, oversized body, duplicate idempotency key (one row), consumer retry on a transient failure, duplicate message delivery (one email). Type check and `wrangler deploy --dry-run` pass. The checker now reports no warnings.
6. Stop before Level 2. Remote migration, queue creation and deployment are listed in release notes for cloudflare-change-control: create the queue and dead-letter queue, apply the D1 migration to staging then production with an export taken first, deploy as a new version with gradual rollout.

Report: status CHANGE_PREPARED_NOT_APPLIED. Checks are labeled `local`. Unverified: production D1 performance under load, queue throughput, and email delivery. Rollback before release is reverting the commit; after release, the plan in the release notes.
