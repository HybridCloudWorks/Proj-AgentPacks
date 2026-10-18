# Worked example — idempotent job-submission API

## Investigation and framing

Synthetic fixture: pyproject declares Python >=3.11; CI tests 3.11/3.12; existing HTTP framework and package manager are discovered from the target repo, not selected by this example. Inspect route/middleware, task store, callers, auth dependencies, tests and deployment. A mismatch in declared/runtime versions becomes a located conflict.

Goal: accept an authorized tenant's bounded job request exactly once per idempotency key. Criteria: invalid/oversized/unknown fields rejected, tenant derived from authenticated principal, duplicate request returns the original job, reused key with different content conflicts, unauthorized tenant cannot read it, and errors expose no secrets. Existing clients keep their response contract.

## Design and implementation

Compare inline execution (simple but ties latency to workload) with an existing worker queue (bounded async processing and durable handoff). Use existing infrastructure if available; a new queue/cloud deployment needs its own ADR/authority. Transactionally reserve idempotency key and job before enqueue using the repository's outbox pattern. Never claim the in-memory fixture solves distributed enqueue consistency.

The executable local domain seam is templates/api_contract.py. It demonstrates typed models, explicit runtime validation, tenant-scoped authorization and idempotency conflict handling with no framework dependency. Adapt it into the repository's installed route layer and transaction/store implementation. Unit/adapter checks in tests/test_behavior.py exercise boundary behavior, not a deployed endpoint.

## Specialist handoff

Send security the request/store/identity boundary and negative cases; security returns located risks without edits. Send tests the criteria, supported versions and fixture adapter; tests can add tests without changing product behavior. Ask performance only if the submission SLO has a measured problem. Primary remains able to do all work directly.

## Validation and completion

Run domain unit tests and route/storage integration tests in the target repository, type/lint/build commands as configured, cancellation/timeout and transaction/outbox failure cases, then sanitized trace/correlation checks. Review final diff and public/dependency/data impacts. Deployment/role enforcement and database uniqueness remain unverified until tested in an authorized environment. A local PASS cannot imply a production release.

Recovery: stop new submissions through an approved feature flag, preserve existing jobs/idempotency records, and revert the compatible route; do not delete persisted jobs as rollback. Report each criterion, exact commands and unverified evidence with templates/completion-report.md.
