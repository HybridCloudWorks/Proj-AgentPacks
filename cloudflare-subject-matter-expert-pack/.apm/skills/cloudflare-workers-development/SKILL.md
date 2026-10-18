---
name: cloudflare-workers-development
description: "Build, review and test Cloudflare Workers code and Wrangler configuration, including bindings, static assets, service bindings, Hyperdrive, cron and queue handlers, Containers and Sandbox, local development with Miniflare and tests with the Workers Vitest pool. Use when writing or reviewing Worker code, editing Wrangler configuration, or diagnosing Worker build and runtime errors in a repository."
---

# Cloudflare Workers Development

## Purpose and activation

Produce Worker code and configuration that are correct for the project's pinned toolchain, safe with secrets, observable, and tested before anything reaches an account. Activate when a repository contains or will contain a Wrangler configuration, when Worker code is written or reviewed, or when a Worker fails to build, type-check, start or behave as expected.

## Scope and exclusions

In scope: `wrangler.jsonc`, `wrangler.json` or `wrangler.toml`; handlers (`fetch`, `scheduled`, `queue`, `email`, `tail`); `WorkerEntrypoint` and service bindings; static assets; Hyperdrive clients; Containers and Sandbox wiring; generated types; local development; unit and integration tests; code review.

Not in scope: storage semantics and Durable Object design (cloudflare-storage-and-state), Agents SDK and AI (cloudflare-agents-and-ai), deploying or writing secrets to an account (cloudflare-change-control), and zone rules in front of the Worker (cloudflare-edge-delivery-and-performance).

## Required inputs

- The repository, its package manager and lock file, the pinned `wrangler` and `@cloudflare/workers-types` versions, TypeScript configuration and test setup.
- The intended behavior and acceptance criteria; which environments exist (`env.staging`, `env.production`).
- For reviews: the exact diff or files, and whether findings should be fixed or only reported.

## Dependencies and tools

- Node.js and the project's own Wrangler for credential-free local commands (`wrangler types`, `wrangler dev` with local bindings, `wrangler deploy --dry-run`, `wrangler check startup`). If Wrangler is not installed, ask before adding it; installing packages is a consequential change.
- Sources to retrieve before writing or flagging code: the Workers best-practices page, the runtime API reference, `node_modules/wrangler/config-schema.json`, the installed workers types, and the compatibility-dates and flags pages.
- `scripts/wrangler_check.py` in this skill folder: a read-only Python 3 checker for Wrangler configuration. It parses JSONC, JSON or TOML (TOML needs Python 3.11 or later) without executing project code and never prints values of secret-like keys.

## Workflow

1. Discover. Read the configuration, entry point, framework (for example Hono), test runner and CI. Note compatibility date and flags, every binding, routes and custom domains, and whether `workers_dev` is on.
2. Check configuration. Run `python3 scripts/wrangler_check.py <project-dir>` from this skill folder (`python` on Windows). Treat `error` findings as blocking, `warn` as needing a decision, and `info` as context. The script exits 1 when any error is found.
3. Retrieve the current documentation for every API, binding shape and configuration key you will use. Installed types and schema outrank memory; current documentation outranks an older installed version only when the upgrade is part of the task.
4. Implement with the rules below. Keep changes to the requested scope and match the project's style.
5. Regenerate types with `wrangler types` after binding changes and import the generated `Env`; never hand-write binding interfaces.
6. Test. Use `@cloudflare/vitest-pool-workers` (bindings simulated by Miniflare, with the `cloudflare:test` helpers documented for the installed version) for integration tests and plain unit tests for pure logic. Exercise scheduled handlers with `wrangler dev --test-scheduled` locally. Cover error paths, oversized input, missing bindings and timeouts.
7. Verify. Run the type check, linter (enable a no-floating-promises rule where the project's linter supports it), tests, `wrangler types --check`, and `wrangler deploy --dry-run` to confirm the bundle builds within size limits.
8. Hand off releases to cloudflare-change-control. Do not deploy from this skill.

## Code rules

- Handlers use module syntax. Classes extend `DurableObject`, `WorkerEntrypoint` or `WorkflowEntrypoint` and read `this.env` and `this.ctx`; do not use `implements` on these base classes.
- Use bindings for Cloudflare resources, not the Cloudflare REST API from inside a Worker. Use service bindings for Worker-to-Worker calls.
- Stream request and response bodies of unknown size. Never `await request.text()` or `response.json()` on unbounded input; enforce size limits first.
- Every promise is awaited, returned, or passed to `ctx.waitUntil()`. Do not destructure `ctx`; calling `waitUntil` unbound throws at runtime.
- No request-scoped data in module-level variables, and no I/O during module initialization.
- Use Web Crypto (`crypto.randomUUID()`, `crypto.getRandomValues()`) for identifiers and tokens, and `crypto.subtle.timingSafeEqual` for secret comparison. Never `Math.random()` for security.
- Catch errors explicitly and return structured responses; do not rely on `passThroughOnException()` as error handling.
- Validate external input with a schema at the boundary; validate object keys and paths before using them with R2 or KV.
- Use Hyperdrive for external PostgreSQL or MySQL and respect the per-invocation connection limit in current documentation; close or reuse connections.
- Distinguish CPU time from wall time. Move heavy or slow work to Queues or Workflows; raise `limits.cpu_ms` only on plans that allow it and with a reason.
- Static assets: configure through the `assets` block and its documented options for SPA fallback and running the Worker first; confirm option names in current documentation.
- Containers and Sandbox: confirm the npm package line and the container image line match (stable with stable, preview with preview) before applying any API; keep live credentials in the Worker, not in the container environment.
- Log structured JSON without secrets or personal data, and enable `observability` with an explicit sampling rate.

## Review checklist

| Pattern | Consequence | Fix |
|---|---|---|
| Unbounded `text()`, `json()` or `arrayBuffer()` | Memory limit exceeded, crash | Check size, stream, or reject |
| Floating promise or destructured `ctx` | Lost work, swallowed errors, "Illegal invocation" | `await` or `ctx.waitUntil()` |
| Module-level mutable request state | Cross-request data leak | Keep state per request or in storage |
| Secret in `vars`, source or logs | Credential exposure | Secret binding or Secrets Store, rotate if leaked |
| String comparison of secrets | Timing side channel | `timingSafeEqual` on equal-length buffers |
| `any` on `Env` or handler parameters, double casts | Binding mistakes hidden | Generated types |
| REST API calls to own account from the Worker | Latency, token sprawl, rate limits | Binding |
| Public `fetch` to another own Worker | Extra hop, exposure | Service binding |
| Compatibility date far behind, or in the future | Old semantics, or deploy failure | Reviewed bump with tests |

## Expected output

For implementation: the scoped diff, regenerated types, tests, the checker result, commands run with exit codes, and the release notes needed by cloudflare-change-control (new bindings, secrets to set, migrations, routes). For review: located findings with severity, evidence, impact, recommended change and blocking flag.

## Validation

- `wrangler_check.py` shows no errors, or each remaining error is explained.
- Type check, tests and `wrangler deploy --dry-run` pass locally; anything not run is reported as unverified.
- Local Miniflare behavior is not proof of production behavior for limits, remote bindings, routing or zone rules; say so when it matters.

## Failure handling and escalation

- Wrangler or types missing or out of date: report it, propose the version change as its own decision, and continue with what can be verified.
- Configuration key or API not found in the installed schema: do not invent it; retrieve documentation or ask.
- Tests need remote resources or paid inference: use fakes locally and request approval for any remote test.
- Checker parse failure: report the line or reason and review the file manually; do not guess its content.

## Permissions and guardrails

Local edits and local commands only. `wrangler deploy`, `wrangler versions upload` or `deploy`, `wrangler secret put` or `delete`, `wrangler dev --remote` or `remote: true` bindings, and any command needing account credentials are consequential and need explicit approval for the exact Worker and environment. Never print secret values, never pass them as command arguments, and never read `.dev.vars` contents into chat.

## Workflow connection

Within the complete pack, the optional `build-workers-application.prompt.md` and `review-cloudflare-change.prompt.md` recipes connect this skill to the primary `cloudflare-subject-matter-expert` workflow; the security reviewer uses its checklist for Worker code. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval, handoff and completion rules.
