# Companion report for a diagram

This report sits beside the `.drawio` file whenever a task involves design decisions or source inference. It carries what the drawing cannot: where each element came from, how strongly the evidence supports it, which choices were made and why, and what is still open. Keep it short. If a row explains nothing a reviewer would ask about, leave it out.

The evidence matrices use the four labels the diagram skills define for semantic evidence: `observed`, `inferred`, `designed` and `unresolved`. The completion report then uses the contract's labels for checks.

## Diagram

- File and pages:
- Date and sources, with the commit if known:
- Purpose and audience, one line each:

## Evidence matrix: components

| Cell ID | Element | Placement (account / Region / AZ / VPC / subnet) | Source location | Label |
|---|---|---|---|---|
|  |  |  | file:line, requirement ID, or the user's answer | observed / inferred / designed / unresolved |

## Evidence matrix: relationships

| Edge ID | From → To | Kind | Crosses | Source location | Label |
|---|---|---|---|---|---|
|  |  | synchronous request / asynchronous message / replication / control plane / hybrid / egress | AZ / Region / account / internet / none |  |  |

A declared resource does not prove runtime traffic, DNS, IAM authorization, routing or data flow. Label a relationship `observed` only for what the source states.

## Design decisions

| Decision | Alternatives considered | Reason | Label |
|---|---|---|---|
|  |  |  | designed / inferred |

## Icon mappings

| Element | Shape used | Exact AWS4 name, or neutral shape | Why approximate |
|---|---|---|---|
|  |  |  |  |

Use AWS icons only for AWS services. Non-AWS systems, custom applications and teams get neutral or general icons with labels.

## Legend notes

Explain each non-obvious item: routing, replication direction, IAM, account boundaries, decorative frames (`container=0`), and cross-AZ, cross-Region, hybrid and egress paths.

## Needs evidence beyond the source

| Relationship or claim | Evidence that would settle it |
|---|---|
|  | deployment output / CloudTrail / AWS Config / runtime telemetry / current AWS documentation |

## Unresolved questions

- Question, who can answer it, and what changes in the diagram for each answer.
