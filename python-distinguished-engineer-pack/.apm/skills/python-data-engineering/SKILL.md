---
name: python-data-engineering
description: Engineer Python transformations and pipelines with schema, precision, memory, lineage and recovery controls. Use when data ingestion, transformation, batch/stream processing or data-quality repair is requested.
---

# Python Data Engineering

## Activation and scope

Data ingestion, transformation, batch/stream processing or data-quality repair is requested. Do not access production datasets solely to make an example realistic.

## Inputs and dependencies

- Inputs: Source/target schema, volumes, ordering, classification, freshness, precision and retention needs.
- Dependencies: Existing processing libraries, approved representative fixtures, checkpoint/storage contract.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Define input/output schemas, provenance, ownership, partitioning, timezone/encoding and decimal precision. Make schema evolution and malformed-record behavior explicit.
2. Choose generator/chunk/batch/vectorized processing from volume and memory evidence. Bound queues, intermediates and parallelism; do not materialize unbounded input.
3. Design checkpoint, deduplication, ordering, replay, partial-failure quarantine and retention/deletion. Do not discard malformed records silently.
4. Test transformations with deterministic fixtures, invariants and boundary/property tests where justified. Protect sensitive intermediate files and logs; verify recovery and measure representative memory/time before optimizing.

## Output and validation

Pipeline/transform patch, schema/data-quality checks, lineage and recovery notes, memory/throughput evidence where measured. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Schema drift, precision loss, cross-tenant mixing, unbounded memory, unknown data rights or non-recoverable partial writes. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `implement-python-feature.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
