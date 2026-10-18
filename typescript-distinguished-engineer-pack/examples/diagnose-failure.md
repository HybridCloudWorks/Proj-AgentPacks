# Worked example — dropped requests during rolling deploys

| | |
|---|---|
| Workflow | `.apm/prompts/diagnose-failure.prompt.md` |
| Primary agent | `typescript-distinguished-engineer` |
| Specialists | None. The work stayed inside one service and needed no independent review |
| Skills | `javascript-node-runtime-engineering`, `performance-reliability-and-operability`, `agent-observability-and-telemetry`, `typescript-strict-engineering`, `layered-testing-and-test-engineering` |
| Outcome | `IMPLEMENTATION_PREPARED_NOT_VERIFIED` |

> Synthetic walkthrough. The repository, paths, commands and output are illustrative. They show the shape of the workflow and are not evidence from a real run; never reuse them as a completion claim.

## Request

"Every deploy of `catalog-api` causes a burst of 502s for about 30 seconds, and the old instances take the whole grace period to die. Find out why and fix it."

The user pasted:

- A deploy timeline.
- Termination log lines showing `received SIGTERM` and then, 30 seconds later, the instance killed.
- A trace in which requests to an old instance fail with an upstream connection reset.

They authorized local investigation and a fix. Deploying, and touching the platform configuration, were not authorized.

## Preserve state

The agent restarted and redeployed nothing. The working tree was clean, and it created the local branch `fix/graceful-shutdown`. The pasted evidence was kept as given. It is the user's observation of production, and the agent treats it as input to test, not as proof of a cause.

## Perceive

`javascript-node-runtime-engineering` establishes how the process actually runs:

- `package.json` has `engines.node` set to `20.x`. The Dockerfile uses `node:20-bookworm-slim` with `CMD ["node", "dist/main.js"]` in exec form, so Node receives `SIGTERM` directly with no shell in between. The app installs its own handler, which rules out PID 1 signal semantics as the cause.
- `src/main.ts` runs `process.on("SIGTERM", () => server.close(() => process.exit(0)))`.
- `src/routes/stream.ts` serves `GET /v1/catalog/changes` as a server-sent events stream. Storefront clients hold these connections open for hours.
- `src/health.ts`: `/readyz` returns `200` whenever the process is up, and nothing changes it during shutdown.
- `src/metrics.ts` starts `setInterval(flush, 10_000)` and never clears it. The Redis client is never closed.

In the pasted trace, the errors line up with the moment the instance was killed, not with the `SIGTERM`.

## Hypotheses, tested one at a time

| # | Hypothesis | Test | Result |
|---|---|---|---|
| H1 | `server.close()` never completes, because open event streams are active connections it waits for | Start the built server locally, attach one stream client with `curl -N`, send `kill -TERM <pid>` | Still alive after 60 s; the close callback never fired. **Confirmed locally** |
| H2 | Readiness stays `200` after `SIGTERM`, so the load balancer keeps routing new requests to an instance that is stopping | Same run, polling `/readyz` | `200` throughout. **Confirmed locally** |
| H3 | The interval timer and the Redis socket keep the event loop alive even once the server has closed | Same, with no stream client attached; `process.getActiveResourcesInfo()` logged after close | Server closed, but the process stayed alive; the output listed a `Timeout` and a TCP handle. **Confirmed locally** |
| H4 | The load balancer's deregistration delay and the orchestrator's grace period combine so traffic arrives after the process stops listening | Needs the ingress and deployment configuration, which is not in this repository | **Not tested**; no access |

H1 to H3 are real defects, and together they reproduce the symptoms locally: a 30-second hang, then a forced kill with connections still open. That is not yet proof that they are the whole production cause. Correlation with the pasted trace does not exclude H4.

## Plan

`performance-reliability-and-operability` sets a bounded shutdown sequence:

1. Mark readiness as draining, so `/readyz` returns `503`.
2. Stop accepting new connections.
3. Send each event stream a final `reconnect` event with a `retry` hint, then end the stream so clients reconnect to a healthy instance.
4. Wait for in-flight requests, up to `SHUTDOWN_DRAIN_MS`. The default is 10 s. The value is validated by the existing config schema and must be between 1 and 25 s, below the 30-second grace period the user reported.
5. Force-close any connections that remain.
6. Clear timers and close Redis.
7. Exit with code 0 when drained, or 1 when the drain was forced. A second signal exits 1 immediately.

`agent-observability-and-telemetry`: emit `shutdown.started` and `shutdown.complete` log events with signal, drained flag, duration and in-flight count, plus a gauge `http_inflight_requests`, so a future deploy shows the drain directly.

## Act

```ts
import { setTimeout as delay } from "node:timers/promises";

export async function shutdown(deps: ShutdownDeps, drainMs: number, signal: NodeJS.Signals): Promise<void> {
  const started = performance.now();
  deps.log.info({ signal, inflight: deps.inflight.count() }, "shutdown.started");
  deps.readiness.markDraining();
  const closed = new Promise<void>((resolve) => deps.server.close(() => resolve()));
  deps.streams.endAll({ event: "reconnect", retryMs: 1_000 });
  // ref: false so the drain timer itself never keeps the process alive
  const drained = await Promise.race([
    closed.then(() => true),
    delay(drainMs, false, { ref: false }),
  ]);
  if (!drained) deps.server.closeAllConnections();
  clearInterval(deps.metricsTimer);
  await deps.redis.quit();
  deps.log.info({ signal, drained, ms: Math.round(performance.now() - started) }, "shutdown.complete");
  process.exitCode = drained ? 0 : 1;
}
```

`typescript-strict-engineering`: `ShutdownDeps` is an explicit interface, so every resource that must be released is visible in one type. Tests construct it with fakes.

Changes:

- `src/lifecycle/shutdown.ts` (new): the sequence above, plus `installShutdown()`, which registers `SIGTERM` and `SIGINT` once and exits 1 on a second signal.
- `src/main.ts`: uses `installShutdown()` in place of the inline handler.
- `src/health.ts`: readiness state with `markDraining()`.
- `src/routes/stream.ts`: registers each stream in a registry and removes it on `close`, so the registry cannot leak entries.
- `src/metrics.ts`: returns its timer so shutdown can clear it.
- `src/config.ts`: adds `SHUTDOWN_DRAIN_MS` to the existing zod config schema.
- `test/integration/shutdown.int.test.ts` (new).
- `docs/runbooks/catalog-api.md`: the shutdown behaviour and the platform settings it assumes.

## Verify

| Command | Result |
|---|---|
| `pnpm typecheck` | 0 errors |
| `pnpm test` | 142 passed, including config validation for `SHUTDOWN_DRAIN_MS` |
| `pnpm exec vitest run test/integration/shutdown.int.test.ts` | 5 passed (cases below) |
| Shell loop running the shutdown file 25 times | 25 of 25 passed; slowest exit 1.4 s with the default drain |
| `pgrep -f dist/main.js` after the loop | no output; no orphaned processes |
| Manual H1–H3 reproduction, repeated | exits with code 0 in about 1 s with a stream client attached; `/readyz` returns `503` at once |

The 5 integration cases:

- (a) `/readyz` returns `503` within 100 ms of `SIGTERM`.
- (b) A 2-second in-flight request completes with `200`.
- (c) A stream client receives the `reconnect` event, and the stream ends.
- (d) The process exits with code 0 within the drain budget plus 1 s.
- (e) A request longer than the drain budget is force-closed; the process logs `drained: false` and exits with code 1.

Each case spawns the built server with `child_process.spawn`. `afterEach` kills any surviving child, so a failed assertion cannot leave a process behind (`layered-testing-and-test-engineering`).

## Completion report

- Recommendation: IMPLEMENTATION_PREPARED_NOT_VERIFIED
- Goal: stop the 502 burst and the slow terminations during `catalog-api` deploys.
- Scope: application shutdown behaviour and regression tests. The platform configuration and observing a real deploy were out of reach.

### Acceptance criteria

| Criterion | Status | Evidence or limitation |
|---|---|---|
| The instance exits promptly after `SIGTERM` with long-lived streams open | Verified locally | integration case (d); manual reproduction |
| Readiness fails as soon as `SIGTERM` arrives | Verified locally | integration case (a) |
| In-flight requests complete within the drain budget | Verified locally | integration case (b) |
| Shutdown never exceeds the drain budget | Verified locally | integration case (e) |
| No 502 burst during a real deploy | Not verified | Needs a staging deploy, which requires explicit confirmation, and the ingress settings (H4) |

### Delivery evidence

- Files changed: `src/lifecycle/shutdown.ts`, `src/main.ts`, `src/health.ts`, `src/routes/stream.ts`, `src/metrics.ts`, `src/config.ts`, `test/integration/shutdown.int.test.ts`, `docs/runbooks/catalog-api.md`.
- Architecture decisions: a bounded drain controlled by one validated setting; streams are told to reconnect rather than being held open.
- Checks and results: as in Verify; all passed.
- Security review: no trust boundary changed. The new setting is validated, and no secrets are involved.
- Observability impact: the new shutdown log events and in-flight gauge are present in code. Export from a real deploy was not observed.
- Operational and cost impact: a deploy should take about the drain budget per instance instead of the full grace period. The new runbook section states the assumed platform settings.
- Unverified items: whether H1–H3 fully explain the production 502s; H4; whether storefront clients honour the `retry` hint when they reconnect, since that code is in another repository.
- Residual risks: if the load balancer takes longer to notice the failing readiness check than the drain budget allows, some requests can still reach a closed instance. A pre-stop delay on the platform side may be needed; that is recorded as a recommendation, not done.
- Rollback: revert the commit to return to the previous handler. There is no data or schema change.

Next safe action, which needs explicit confirmation: deploy the branch to staging and watch the 5xx rate and termination time during a rolling restart. Separately, share the ingress and deployment settings so H4 can be checked.
