---
name: python-api-engineering
description: Engineer Python REST, webhook, event, streaming and library contracts with validation and reliable failure behavior. Use when a Python endpoint, event consumer or public integration contract is created or changed.
---

# Python Api Engineering

## Activation and scope

A Python endpoint, event consumer or public integration contract is created or changed. Use installed framework conventions; do not assume FastAPI or deploy by default.

## Inputs and dependencies

- Inputs: Framework/version, schemas, identity rules, consumers, compatibility and service objectives.
- Dependencies: Existing routing/validation/client stack; contract and integration test environment.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Map transport, domain and persistence layers, middleware/lifecycle and documented extension points before editing framework code.
2. Define request/response or event schemas, required/optional/null semantics, size limits, error taxonomy, authn/authz, pagination/versioning and user-visible compatibility.
3. Specify deadlines, cancellation, bounded retries, idempotency keys, duplicate/replay behavior, transaction/commit ordering and webhook signature verification as applicable.
4. Keep authorization server-side and independent of supplied identity fields. Parameterize persistence and redact logs; expose safe errors with correlation IDs. Test invalid payloads, unauthenticated/forbidden access, transient failure and duplicate delivery.

## Output and validation

Contract and implementation with unit/contract/integration evidence, telemetry and rollout/rollback implications. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Ambiguous authorization, breaking consumer contract, missing commit semantics, unsatisfied service objective or unsafe response disclosure. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `build-python-api.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. Consult shared instruction, handoff and completion contracts when the full pack is available.
