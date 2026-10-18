---
name: python-database-engineering
description: Engineer Python persistence, transactions, schemas, pooling, migrations and recovery. Use when database access, query performance, consistency, cache behavior or schema migration changes.
---

# Python Database Engineering

## Activation and scope

Database access, query performance, consistency, cache behavior or schema migration changes. SQLite or mocks do not establish production database semantics.

## Inputs and dependencies

- Inputs: Driver/ORM and database versions, schema/migrations, query consumers, consistency and rollout requirements.
- Dependencies: Existing database adapter and isolated representative database or explicitly unavailable integration evidence.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Trace transaction boundaries, commit/rollback and connection/pool ownership; use parameterized queries and explicit timeouts.
2. Evaluate N+1 queries, indexes, pagination/streaming, isolation, optimistic concurrency, deadlocks and retry safety against the actual engine.
3. For migrations prefer expand/migrate/contract when consumers overlap. Separate destructive cleanup, define backward compatibility and recovery, and do not assume a down migration restores deleted data.
4. Specify authoritative data versus cache, TTL/invalidation, backup and restore validation, and test transaction rollback, conflicts, empty/large results and mixed-version rollout in an isolated database.

## Output and validation

Persistence patch or migration plan with query/transaction evidence, compatibility and data recovery limits. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Destructive shared migration without approval, missing backup evidence, pool leak, duplicate writes, unsafe query construction or engine-dependent unknown. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `design-change.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
