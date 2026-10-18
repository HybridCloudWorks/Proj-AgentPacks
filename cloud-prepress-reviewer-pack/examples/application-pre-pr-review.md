# Worked example: application change before the pull request

Prompt: `.apm/prompts/review-before-pr.prompt.md`. Outcome: `CHANGES_REQUIRED`.

Skills applied: cloud-prepress-orchestration, change-scope-and-impact, code-defect-and-quality-review, tests-build-and-dependency-review, security-secrets-and-supply-chain-review, documentation-inputs-and-repository-contracts, architecture-and-adr-consistency, review-report-and-pr-gate.

The repository, identities and values are fictional.

## Request

> Review the order-capture feature on `feature/order-capture` before I open the PR. Don't change anything. The acceptance criteria are on the work item.

## 1. Fix scope and boundary (cloud-prepress-orchestration)

The reviewer records the target and authorization before reading code.

- Target: `orders-service`, head `feature/order-capture` at `4e1b9c7`, base `main` at `a02f6d1`.
- Intent, from the work item: consume `orders-placed` Service Bus messages, capture the payment, persist the order to Cosmos DB.
- Acceptance criteria: each order is captured exactly once; failed processing is retried and then dead-lettered; no customer personal data in logs.
- Authorization: read-only. The user allows the local test and lint targets the repository's `Makefile` defines. No live Azure access was asked for, and none is needed for a pre-PR gate.
- Domains selected: scope, code, tests and build, security (logging, identity and a new dependency), documentation, and a light architecture check against ADR-0004, which the work item names. Not selected: IaC, preview, cost. No infrastructure file is in the diff.

## 2. Resolve the diff (change-scope-and-impact)

```text
$ git diff --name-status main...feature/order-capture
A       src/orders/handlers.py
M       function_app.py
M       host.json
A       tests/test_handlers.py
M       requirements.txt
M       README.md
```

Three files outside the diff are read, each for a stated reason: `src/payments/client.py`, because the handler calls `capture()`; `src/orders/models.py`, to learn what the logged message body contains; and `CHECKLIST.md`, the repository's record of required settings. Cosmos DB and Service Bus are provisioned from a separate platform repository, which is out of scope. The function identity's Cosmos DB data-plane role is therefore recorded as not verified, not assumed.

## 3. Trace the code (code-defect-and-quality-review)

```python
29  @bp.service_bus_queue_trigger(arg_name="msg", queue_name="orders-placed",
30                                connection="SERVICEBUS")
31  def process_order(msg: func.ServiceBusMessage) -> None:
32      body = msg.get_body().decode("utf-8")
33      logger.info("processing order message: %s", body)
34      order = Order.model_validate_json(body)
35      try:
36          payments.capture(order.order_id, order.total)
37          container.upsert_item(order.to_document())
38      except Exception:
39          logger.exception("order processing failed for %s", order.order_id)
40          return
```

`host.json` in the diff sets `extensions.serviceBus.autoCompleteMessages` to `true`, and the payment client documents its contract:

```python
def capture(order_id: str, amount: Decimal, idempotency_key: str | None = None) -> CaptureResult:
    """Capture an authorized payment.

    The gateway deduplicates repeated captures only when idempotency_key is supplied.
    """
```

The reviewer traces three paths:

- **Malformed body.** `model_validate_json` raises outside the `try`. The host abandons the message, Service Bus redelivers it, and it is dead-lettered after the maximum delivery count. That is correct poison-message handling, so there is no finding.
- **Downstream failure after capture.** `upsert_item` raises, the broad `except` logs and returns, and the normal return completes the message. The payment is captured, the order is lost, and nothing is retried or dead-lettered. This is proven from the code and configuration, so it is a confirmed defect.
- **Redelivery.** Service Bus delivers at least once. A lost lock or a host restart repeats the message, and so will the retry that fixing the previous defect enables. `capture` is called without an idempotency key, so a repeat charges again. This is also confirmed: the client's own contract says so.

## 4. Tests and build (tests-build-and-dependency-review)

Both checks were run in a scratch virtual environment outside the repository:

```text
$ python -m pytest -q
.........                                                    [100%]
9 passed in 1.42s
$ ruff check .
All checks passed!
```

Of the three tests in `tests/test_handlers.py`, none makes `capture` or `upsert_item` raise, and none delivers a message twice, which is why the suite passes with both defects present. `requirements.txt` adds `azure-cosmos` pinned to an exact version, matching the repository's convention of exact pins. The repository defines no vulnerability scan and no Service Bus emulator, so both are recorded as skipped.

## 5. Security (security-secrets-and-supply-chain-review)

Line 33 logs the full body. `src/orders/models.py` shows that the body carries `customer.email` and `shipping_address`, and `host.json` keeps the default log level at Information, so the data reaches Application Insights. The Cosmos DB client uses `DefaultAzureCredential` with an endpoint setting, and no account key appears anywhere. A search of the diff for key, token, certificate and connection-string patterns finds nothing to redact.

## 6. Documentation and architecture

`README.md` documents the three new settings, but `CHECKLIST.md`, which the deployment operator works from, does not list them. That gap changes whether a deployment starts cleanly, so it is a Low finding rather than a style note. ADR-0004 asks for asynchronous processing with dead-lettering. The trigger and identity-based connection match it, but the swallowed exception contradicts its failure-handling clause.

## 7. Report and gate (review-report-and-pr-gate)

The pack was installed with APM, which does not deploy helper scripts, so the pre-review and post-review helpers are absent on this machine. The reviewer records both as skipped and checks the report against the contract by reading it. Two confirmed High defects break the change's own acceptance criteria, so the gate is `CHANGES_REQUIRED`.

## Completion report

### Scope and inputs

| Item | Value |
|---|---|
| Repository and refs | `orders-service`, base `main` at `a02f6d1`, head `feature/order-capture` at `4e1b9c7` |
| Change intent | Consume `orders-placed` queue messages, capture payment, persist the order to Cosmos DB |
| Change class | application, with configuration and dependency changes |
| Target environment | Not applicable to this gate; no infrastructure in the diff |
| Requirements and design | Work item criteria: exactly-once capture; retry then dead-letter on failure; no customer personal data in logs. ADR-0004. |
| Owner | Change: orders team. Cosmos DB and Service Bus: platform team. |
| Authorization boundary | Read-only review. Local `pytest` and `ruff` authorized. Live read-only queries not authorized and not needed. No source edits, push or pull request comments. |
| Report location | `../reviews/orders-service/order-capture/REVIEW.md` |

### Changed paths and methods

| Path | Change class | Review method |
|---|---|---|
| `src/orders/handlers.py` (added) | application | Read in full; traced success, malformed-input, downstream-failure and redelivery paths |
| `function_app.py` | application | Read diff; confirmed blueprint registration |
| `host.json` | configuration | Read diff; checked message completion and log level |
| `tests/test_handlers.py` (added) | tests | Mapped each test to a behavior; ran the suite |
| `requirements.txt` | dependency | Checked the new pin and its source |
| `README.md` | documentation | Checked new settings and run steps |

Paths inspected outside the diff, and why:

- `src/payments/client.py`: the handler calls `capture()`; its docstring defines the idempotency contract.
- `src/orders/models.py`: to establish which fields the logged body contains.
- `CHECKLIST.md`: the repository's record of required settings.

### Evidence ledger

| Evidence | Label | Source, command or capture | Bound to |
|---|---|---|---|
| Six changed files | observed | `git diff --name-status main...feature/order-capture` | `4e1b9c7` |
| Normal return completes the message | observed | `host.json`, `extensions.serviceBus.autoCompleteMessages` is `true` | `4e1b9c7` |
| Gateway deduplicates only with a key | observed | `src/payments/client.py`, `capture()` docstring | `4e1b9c7` |
| Unit tests pass | observed | `python -m pytest -q`, exit 0, 9 passed | `4e1b9c7` |
| Lint passes | structurally-validated | `ruff check .`, exit 0 | `4e1b9c7` |
| Redelivery and dead-letter behavior | inferred | From trigger configuration and code; not exercised | not bound |
| Cosmos DB data-plane role for the function identity | not-verified | Defined in the platform repository | not bound |

### Findings

#### Downstream failure completes the message and loses the order

| id | severity | status | file | line |
|---|---|---|---|---|
| F1 | High | confirmed | `src/orders/handlers.py` | 40 |

- **scenario:** `payments.capture` succeeds, then `container.upsert_item` raises, for example after the SDK exhausts its retries on throttling. The `except Exception` block logs and returns. With `autoCompleteMessages` enabled a normal return completes the message, so it is neither retried nor dead-lettered. Expected: the message is retried and dead-lettered after the maximum delivery count.
- **impact:** The customer is charged and the order is never stored, with no alert. The retry-then-dead-letter criterion and the failure-handling clause of ADR-0004 are not met.
- **recommendation:** Re-raise after logging, or remove the broad `except`, so the host abandons the message and Service Bus redelivers it. Ship this together with the idempotency fix, because redelivery repeats the capture.
- **verification:** A unit test in which `upsert_item` raises asserts that `process_order` raises. An integration run against a test queue shows the message dead-lettered after the maximum delivery count.

#### Payment capture has no idempotency key on an at-least-once trigger

| id | severity | status | file | line |
|---|---|---|---|---|
| F2 | High | confirmed | `src/orders/handlers.py` | 36 |

- **scenario:** A lost message lock, a host restart, or the retry the failure-handling fix enables delivers the same message again. `capture(order.order_id, order.total)` passes no `idempotency_key`, and the client documents that the gateway deduplicates only when one is supplied.
- **impact:** Duplicate captures charge the customer twice. The exactly-once criterion is not met.
- **recommendation:** Pass a stable key derived from the order, for example `idempotency_key=order.order_id`.
- **verification:** A unit test delivers the same message twice and asserts that both calls carry the same key. The payments owner confirms that the gateway's deduplication window covers redelivery timing.

#### Full message body, including customer contact data, is logged at Information

| id | severity | status | file | line |
|---|---|---|---|---|
| F3 | Medium | confirmed | `src/orders/handlers.py` | 33 |

- **scenario:** Every message is logged whole. The body carries `customer.email` and `shipping_address`, and the default log level sends Information records to Application Insights.
- **impact:** Customer personal data reaches telemetry, with its broader access and retention, against the work item's logging criterion.
- **recommendation:** Log the order ID and message ID only.
- **verification:** A `caplog` test asserts that no record contains the fixture order's email or address.

#### Tests cover only the happy path and malformed input

| id | severity | status | file | line |
|---|---|---|---|---|
| F4 | Medium | confirmed | `tests/test_handlers.py` | 12-44 |

- **scenario:** The three tests cover a valid order, invalid JSON and the capture amount. None makes a downstream call raise and none repeats a delivery, so both High defects pass the suite.
- **impact:** Regressions in failure handling and idempotency would not be caught.
- **recommendation:** Add tests for a failure after capture, a capture failure, and a duplicate delivery.
- **verification:** The new tests fail at `4e1b9c7` and pass after the fixes.

#### New required settings are missing from the input checklist

| id | severity | status | file | line |
|---|---|---|---|---|
| F5 | Low | confirmed | `CHECKLIST.md` | 14 |

- **scenario:** The change reads `COSMOS_ENDPOINT`, `COSMOS_DATABASE` and `SERVICEBUS__fullyQualifiedNamespace`. `README.md` names them; the checklist the deployment operator uses does not.
- **impact:** Without the Service Bus setting, the trigger listener cannot connect at startup; without the Cosmos DB endpoint, the first message fails.
- **recommendation:** Add the three settings, by name and without values, to the checklist's function app section.
- **verification:** The checklist lists every setting that `function_app.py` and `src/orders/handlers.py` read.

### Skipped checks and limits

| Check | Why skipped or limited | Effect on the recommendation |
|---|---|---|
| Pre-review inventory and post-review validation | Helpers not present; APM does not deploy helper scripts | Report shape checked by reading it against the contract |
| Integration run against a Service Bus queue | No emulator or test namespace configured | Redelivery and dead-letter behavior inferred, not exercised |
| Dependency vulnerability scan | The repository defines none | New pin checked by source and version only |
| Cosmos DB data-plane role | Lives in the platform repository | Handed to the platform owner; required before deployment |

### Architecture and ADR status

ADR-0004 (asynchronous order processing through Service Bus, with dead-lettering): the trigger, the queue and the identity-based connection are aligned. The swallowed-exception defect contradicts its failure-handling clause. Nothing in this change needs a new ADR.

### Security, IaC, policy and identity status

- No infrastructure, policy or RBAC file changed.
- The Cosmos DB client authenticates with `DefaultAzureCredential`, and no account key appears in code or configuration. The function identity needs a Cosmos DB data-plane role assignment, which is separate from Azure RBAC and not verified here.
- Customer contact data is logged (the Medium logging finding).
- The new dependency `azure-cosmos` is pinned to an exact version from PyPI.

Secret handling: the diff was searched for key, token, certificate and connection-string patterns. Nothing matched and nothing was redacted, and no secret value appears in this report.

### Tests, build and preview status

| Check | Command or source | Result | Label |
|---|---|---|---|
| Unit tests | `python -m pytest -q` | exit 0, 9 passed | observed |
| Lint | `ruff check .` | exit 0 | structurally-validated |
| Integration | none defined | not run | not-verified |

Preview change counts: no preview; the change contains no infrastructure.

### Operations, rollback, cost and inputs

- Observability: while failures are swallowed, nothing reaches the dead-letter queue and no alert fires on a lost order.
- Rollback boundary: revert the merge and redeploy the previous package. A captured payment cannot be undone by a redeploy; that is the point of no return for each processed message. Label: designed.
- Cost: no new resources in this repository. Cosmos DB request-unit consumption grows with message volume and is not estimated here; the platform team owns it.
- New required inputs: `COSMOS_ENDPOINT`, `COSMOS_DATABASE`, `SERVICEBUS__fullyQualifiedNamespace`. None is a secret.

### Unresolved risks and human blockers

| Item | Type | Owner | Needed to clear |
|---|---|---|---|
| Cosmos DB data-plane role for the function identity | open risk | platform team | The role assignment exists in the target environment before deployment |
| Gateway deduplication window | open risk | payments owner | Confirmation that the window covers redelivery timing |

No human blocker stops the implementer from fixing the findings.

### Recommendation

CHANGES_REQUIRED

Two confirmed High defects break the change's own acceptance criteria. This review does not open, approve or merge the pull request.

### Engineer handoff

- Next actor: the change author.
- Actions, in order: fix the swallowed exception and the missing idempotency key together; reduce the log line to identifiers; add the failure and duplicate-delivery tests; add the three settings to `CHECKLIST.md`.
- Evidence the next actor receives: this report and the test and lint output above.
- Re-review trigger: new commits on `feature/order-capture` that touch `src/orders/` or `tests/`.
- Not done by this review: no code changed, no pull request opened or commented on, no live Azure access.
