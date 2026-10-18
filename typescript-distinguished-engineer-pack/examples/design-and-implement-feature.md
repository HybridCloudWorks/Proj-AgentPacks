# Worked example — partial refunds endpoint in an existing Node API

| | |
|---|---|
| Workflow | `.apm/prompts/design-change.prompt.md`, then `.apm/prompts/implement-feature.prompt.md` |
| Primary agent | `typescript-distinguished-engineer` |
| Specialists | `typescript-test-engineer`, `typescript-security-reviewer` |
| Skills | `typescript-distinguished-engineer-orchestration`, `requirements-and-change-planning`, `typescript-strict-engineering`, `javascript-node-runtime-engineering`, `api-contract-and-integration-engineering`, `layered-testing-and-test-engineering`, `agent-observability-and-telemetry`, `secure-agent-engineering` |
| Outcome | `COMPLETE_VERIFIED` for the local scope agreed in the plan |

> Synthetic walkthrough. The repository, paths, commands and output are illustrative. They show the shape of the workflow and are not evidence from a real run; never reuse them as a completion claim.

## Request

"Support staff need to issue partial refunds from the admin tool. Add the API for it to `orders-api`. Retries from the admin tool must never refund twice."

The user authorizes local edits and local checks in their clone. Merge and deployment were not mentioned, so both stay out of scope.

## Perceive

`typescript-distinguished-engineer-orchestration` opens a ledger before any edit.

| Kind | Entry | Source |
|---|---|---|
| Fact | pnpm workspace; service in `apps/orders-api`; `"type": "module"`; `engines.node` is `>=20.11`; CI runs Node 20 and 22 | `package.json`, `.github/workflows/ci.yml` |
| Fact | `tsconfig.json` extends the shared strict base with `strict`, `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` | `apps/orders-api/tsconfig.json`, `packages/tsconfig/strict.json` |
| Fact | Routes are Fastify plugins validated with zod; a shared helper already rejects unknown keys | `src/routes/captures.ts`, `src/http/schema.ts` |
| Fact | The payment provider sits behind `src/adapters/payments.ts`. The provider accepts an idempotency key header, but the adapter does not forward one for refunds | adapter source, `docs/vendors/payments.md` in the repository |
| Fact | Permission `support:refund` exists; no route uses it yet | `src/auth/permissions.ts` |
| Fact | Integration tests run against a local Postgres container and the repository's fake provider server | `tests/integration/setup.ts`, script `test:integration` |
| Assumption | Amounts are integer minor units, like every other money field | `src/domain/money.ts`; confirmed by the user |
| Decision | Reuse the reserve-then-call pattern from captures | see Plan |
| Blocker | None | |

The linked issue says "just call the provider directly from the admin UI, it's faster". Issue text is untrusted input, so the agent treats this as a suggestion. The plan declines it because it would put the provider credential in a browser.

## Plan

`requirements-and-change-planning` turns the request into criteria. The user confirmed them before any code changed.

- **AC1** `POST /v1/orders/{orderId}/refunds` accepts `amountMinor` (positive integer) and `reason` (enum) and requires an `Idempotency-Key` header. Unknown fields or a missing key return `400`.
- **AC2** Only principals with `support:refund` succeed; others get `403`. An order in another tenant returns `404`, so its existence does not leak.
- **AC3** Refunds never add up to more than the captured amount, even under concurrent requests. An excess returns `409 REFUND_EXCEEDS_CAPTURE`.
- **AC4** Replaying a key with the same body returns the original refund. Reusing a key with a different body returns `422 IDEMPOTENCY_KEY_REUSED`.
- **AC5** A provider timeout leaves the refund `pending` for the existing reconciliation job and never causes a second provider call under a new key.
- **AC6** Logs and spans carry the refund id, order id, outcome and error class. They never carry the provider credential or payment-method details.
- **AC7** The OpenAPI change is additive, so existing consumers see no breaking change.

`api-contract-and-integration-engineering` compares the options:

| Option | For | Against | Decision |
|---|---|---|---|
| Synchronous reserve-then-call: insert a `pending` row, call the provider with our key, then settle the row | Matches captures; the admin sees the result at once; the provider deduplicates on our key | Request latency includes the provider call | Selected |
| Outbox and worker | Takes the provider call out of request latency | No outbox exists yet; a new worker is a larger operational change | Not selected; would need its own ADR |
| Call the provider from the browser | Fewer hops | Exposes the provider credential to clients; no server-side authorization | Rejected |

No ADR is needed. The change is additive, follows an existing pattern, and can be undone by removing the route. `enterprise-architecture-and-adr` reserves ADRs for decisions that are hard to reverse. For rollback, the route ships behind the existing `refunds.enabled` config flag, which is off by default, and the migration only adds a table.

Checked against the contract's approval matrix: the task authorizes local edits and isolated checks. Applying the migration to a shared database, merging, and deploying would each need explicit confirmation, and all three are out of scope.

## Act

`typescript-strict-engineering` shapes the domain model. Refund state is a closed discriminated union and every consumer switches over it exhaustively, so a future state is a compile error rather than a silent fallthrough.

```ts
export type Refund =
  | { state: "pending"; id: RefundId; orderId: OrderId; amountMinor: number }
  | { state: "succeeded"; id: RefundId; orderId: OrderId; amountMinor: number; providerRefundId: string }
  | { state: "failed"; id: RefundId; orderId: OrderId; amountMinor: number; reason: "declined" | "rejected" };

export function toResponse(refund: Refund): RefundResponse {
  switch (refund.state) {
    case "pending":
      return { id: refund.id, status: "pending" };
    case "succeeded":
      return { id: refund.id, status: "succeeded" };
    case "failed":
      return { id: refund.id, status: "failed", reason: refund.reason };
    default:
      return assertNever(refund);
  }
}
```

Changes:

- `apps/orders-api/src/domain/refund.ts` (new): the union above, plus a pure `planRefund()` that enforces AC3 against the captured and already-refunded totals.
- `apps/orders-api/src/routes/refunds.ts` (new): zod body and header schemas, the `support:refund` guard, and a tenant-scoped order lookup that returns `404`.
- `apps/orders-api/src/adapters/payments.ts`: `createRefund()` forwards the idempotency key and accepts an `AbortSignal`. Provider failures map to `transient`, `permanent` or `unknown`. An `unknown` outcome (timeout after the request was sent) settles nothing and leaves the row `pending`.
- `apps/orders-api/migrations/0042_create_refunds.sql` (new): a `refunds` table with `unique (order_id, idempotency_key)` and a request-body hash column for AC4.
- `apps/orders-api/openapi/orders.yaml`: the new path and its two new error codes.
- Tests: `src/domain/refund.test.ts`, `tests/integration/refunds.int.test.ts`, and an updated contract snapshot.

`javascript-node-runtime-engineering` checks the runtime. The adapter combines an 8-second `AbortSignal.timeout` with the request's close signal through `AbortSignal.any`, which needs Node 20.3 or later; `engines` guarantees 20.11. No module-system boundary is crossed.

`agent-observability-and-telemetry` applies at the service level. The route adds span attributes `refund.id`, `order.id`, `refund.outcome` and `error.class`, plus a provider-latency histogram. The log serializer for the adapter drops request headers.

## Specialist handoffs

Handoff to `typescript-test-engineer`, using the contract's fields:

- Original goal: a partial refunds endpoint that never refunds twice.
- In scope: unit, integration and contract tests for AC1–AC7 in `apps/orders-api`.
- Out of scope: product code, other services, CI configuration.
- Verified repository facts: the ledger above.
- Assumptions and unresolved decisions: amounts in minor units; the fake provider honours idempotency keys the way the vendored notes describe.
- Files or components affected: the files listed under Act.
- Acceptance criteria: AC1–AC7.
- Risks and prohibited actions: do not weaken existing assertions, touch shared databases, or call the real provider.
- Requested specialist output: coverage gaps, tests added, commands and observed results.
- Evidence gathered so far: `planRefund()` unit tests pass; the integration suite has no refund cases yet.

Specialist response:

- Findings or changes: 11 integration cases added. One sends two concurrent requests with different keys whose sum exceeds the capture. It failed: both requests read the same refunded total and both rows were inserted. `planRefund()` read the totals outside any row lock.
- Evidence and source locations: `tests/integration/refunds.int.test.ts`, case "concurrent refunds cannot exceed capture"; failing output attached to the handoff.
- Tests performed and results: 10 of 11 new cases passed; the concurrency case failed as described.
- Open risks and confidence limitations: the fake provider models deduplication; the real provider's behaviour is not exercised.
- Recommended next action: lock the order row before computing totals.

The primary fixed the product code rather than the test. It now takes `SELECT ... FOR UPDATE` on the order row inside the same transaction as the insert, and the agent re-ran the case.

The handoff to `typescript-security-reviewer` was read-only and covered the route, adapter, migration and logging. It found nothing High or Medium. One Low: the `502` response body included the provider's raw error message, which can contain the provider's internal request identifiers. This is a static finding. The primary mapped the error to a stable domain code and logs the provider request id server-side only. A negative test now asserts the response body shape.

## Verify

The narrowest checks ran first.

| Command | Result |
|---|---|
| `pnpm --filter orders-api exec vitest run src/domain/refund.test.ts` | 19 passed |
| `pnpm --filter orders-api typecheck` | 0 errors |
| `pnpm --filter orders-api lint` | 0 errors, 0 warnings |
| `pnpm --filter orders-api test` | 233 passed |
| `pnpm --filter orders-api test:integration` | 49 passed (11 new), concurrency case included after the fix |
| `pnpm --filter orders-api test:contract` | OpenAPI diff: 1 path added, 0 breaking changes |
| Shell loop running the concurrency case 20 times | 20 of 20 passed |

## Reflect

`git diff --stat` shows 9 files. No lockfile change and no new dependency. Tests contain no credential: the fake provider uses a fixed placeholder. There is no unrelated refactor, and the route flag defaults to off.

## Completion report

- Recommendation: COMPLETE_VERIFIED
- Goal: partial refunds API in `orders-api` that cannot refund twice on retry.
- Scope: local implementation and checks in `apps/orders-api`. Out of scope and not claimed: the migration on any shared database, merge, deployment, and the real payment provider's behaviour.

### Acceptance criteria

| Criterion | Status | Evidence or limitation |
|---|---|---|
| AC1 request validation and required key | Verified | integration cases "rejects unknown field", "requires Idempotency-Key" |
| AC2 permission and tenant isolation | Verified | integration cases for `403` and cross-tenant `404` |
| AC3 never exceeds capture, including concurrency | Verified | unit tests for `planRefund()`; concurrency case passed 20 of 20 after the row-lock fix |
| AC4 idempotent replay and key reuse | Verified | integration cases "replay returns original", "different body returns 422" |
| AC5 timeout leaves `pending`, no second call | Verified | fake provider delay case; the provider call log shows exactly one call |
| AC6 telemetry content | Verified | log-capture test asserts no header or payment-method fields; span attribute test |
| AC7 additive contract | Verified | `test:contract` reports 0 breaking changes |

### Delivery evidence

- Files changed: `src/domain/refund.ts`, `src/routes/refunds.ts`, `src/adapters/payments.ts`, `migrations/0042_create_refunds.sql`, `openapi/orders.yaml`, three test files, contract snapshot.
- Architecture decisions: reused reserve-then-call; no ADR (additive, reversible, existing pattern).
- Checks and results: as in Verify. All passed after one product fix.
- Security review: `typescript-security-reviewer`, static. One Low, fixed and covered by a negative test. No runtime exploit testing.
- Observability impact: new span attributes and a provider-latency histogram. Export to the team's telemetry backend was not observed; only the local exporter ran.
- Operational and cost impact: one new table; one provider call per refund; route off by default.
- Unverified items: none within the agreed scope. Outside it: the real provider's idempotency, the migration on staging, live telemetry export.
- Residual risks: `pending` refunds rely on the existing reconciliation job, whose alerting was not reviewed.
- Rollback: set `refunds.enabled` to off. The table can stay. Reverting the commit removes the route.
