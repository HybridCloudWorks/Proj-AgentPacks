---
description: "Model a recognizable AWS architecture pattern honestly in Draw.io"
agent: aws-expert-designer
---

# Model an AWS architecture pattern

## Inputs

The pattern in question: VPC networking, serverless, containers, event-driven, data and analytics, hybrid connectivity, CI/CD, multi-Region, or security and governance layers. Also the user's actual requirements or source evidence, and the routing, failover, replication and consistency expectations that apply. When the user names only a pattern, the result is a designed reference, and the report says so.

## Workflow

1. Apply `aws-architecture-patterns` and run its checks for the named pattern. For example, a public subnet is a route-table property; synchronous invocation is not asynchronous delivery; a pipeline is not a runtime dependency; an edge service does not replicate or move database traffic.
2. Apply `aws-architecture-design` to separate what the user's evidence shows from what the pattern adds. Mark every relationship observed, inferred or designed.
3. Apply `aws-layout-and-composition` so that routing, failover authority, replication direction, active/active versus active/passive, and cross-AZ, cross-Region, hybrid and egress edges are visible and labeled distinctly.
4. Apply `aws-icons-and-visual-language`, then `drawio-core-generation` and `aws-xml-authoring` to write the file. Show governance and security services as a separate layer only when the user asks for them.
5. Apply `diagram-validation-and-evidence`, and `drawio-render-export-and-review` when Draw.io Desktop is available.

## Expected output

A `.drawio` pattern diagram with a legend; a list of deviations from the reference pattern; the unresolved assumptions, such as who decides failover, which way data replicates and which consistency model applies; and a completion report. Do not imply that Route 53, Global Accelerator, CloudFront or any other edge service replicates or moves data.

Follow the `aws-expert-designer-contract` instruction: report every section it lists, label evidence with its labels, and never describe an unexecuted check as passed.
