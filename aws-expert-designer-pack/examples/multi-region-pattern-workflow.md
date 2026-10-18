# Worked example: active-active multi-Region status API

Synthetic scenario. Domain, names and Regions are illustrative. Workflow prompt: `model-aws-architecture-pattern`.

## Request

"Produce an active-active multi-Region architecture for our shipment-status API, with clear routing, replication and transfer semantics." Requirements supplied:

- S1: Serve each user from the nearest healthy Region (us-east-1 and eu-west-1).
- S2: Either Region accepts writes.
- S3: A Region outage must not stop the service.
- S4: Nightly reports are archived and copied to the other Region.

No source code exists yet. Every service choice is therefore designed, and the report says so.

## Pattern checks

These come from `aws-architecture-patterns` (hybrid and multi-Region, serverless) and `aws-architecture-design`.

| Concern | How it is drawn | Label |
|---|---|---|
| Routing | Route 53 latency-based records for `status.example.com`, one per Region, each tied to a health check. Users resolve DNS first, then connect straight to the Regional API. No request passes through Route 53. | designed |
| Failover authority | Route 53 health checks and record evaluation. Failover speed depends on DNS TTL and client caching, and the legend says so. | designed |
| Per-Region path | API Gateway Regional custom domain → Lambda → local DynamoDB replica. Lambda is not VPC-attached, so no VPC is drawn. Drawing one would invent a network boundary. | designed |
| Write replication | DynamoDB global table with replicas in both Regions: multi-active, asynchronous, with a conflict policy of last writer wins. The edge is bidirectional and labeled "cross-Region async replication, last writer wins". | designed |
| Report replication | Reports are written only in us-east-1. S3 Replication copies them to eu-west-1, one way. The edge is one-directional and labeled "cross-Region S3 Replication, one way". The report path is active/passive, and the legend says so. | designed |
| Edge services | No CloudFront or Global Accelerator. Nothing in the diagram implies that DNS moves or replicates data. | designed |

Deviation from the reference pattern: the API is active/active, but the report pipeline is active/passive. If us-east-1 is down, no new reports are produced. That is recorded as a deviation and not hidden by symmetry.

## Layout

From `aws-layout-and-composition`:

- Two decorative Region frames (`container=0`) side by side, with mirrored service rows.
- Route 53 is centered above both frames as a global service.
- Users sit below the title block on the left.
- An 80 px channel between the frames is reserved for cross-Region edges, so replication never crosses a service.
- Badges: 1 resolve, 2 HTTPS to the Regional API, 3 invoke, 4 write locally, 5 replicate.
- The right-side legend distinguishes:
  - synchronous request: solid
  - health check: dotted, from Route 53 to each API
  - asynchronous replication: dashed and labeled with direction
  - "cross-Region" as the prefix on every cost-bearing transfer label

Region frames are decorative, so services are parented to cell `1` and only positioned inside the frames. Moving a frame does not move its services, and the companion report notes this for editors.

## Validation

- Structural checks: parse, root cells, 34 unique IDs, parents, 11 edges with icon endpoints, no compression, the AWS4 namespace and Helvetica were all checked, and all passed.
- Visual check:
  - `drawio-render-export-and-review` rendered a review PNG to a scratch folder with the detected Draw.io Desktop, which also printed its version.
  - At the 1280 px review width, both arrowheads of the DynamoDB replication edge were hidden under the replica labels, so the edge read as one-directional.
  - Fix: moved the exit and entry points to the icons' vertical midpoints and placed the label in the channel.
  - The re-render was clean.

## Completion report

Pack: aws-expert-designer.

Outcome: pattern diagram delivered as a designed reference.

### scope_and_inputs

- Task: pattern model for active-active multi-Region; a new file.
- Inputs: requirements S1–S4 from the user — observed. No source code or account exists.

### source_facts

- Two Regions, nearest-healthy routing, writes in either Region, survival of a Region outage, and reports copied cross-Region (S1–S4) — observed.

### assumptions_and_design_decisions

- Route 53 latency routing with health checks as the failover authority — designed.
- DynamoDB global table with asynchronous multi-active replication and last-writer-wins conflicts — designed.
- Lambda not VPC-attached, so no VPC is drawn — designed.
- Reports are active/passive through one-way S3 Replication; this is a recorded deviation — designed.

### output_files

- `architecture/status-multi-region.drawio`: new, uncompressed, one page.
- `architecture/status-multi-region.md`: new companion report with the pattern table and the deviation.
- Review PNG in a scratch folder: not a deliverable.

### structural_checks

- Parse, root cells, IDs, parents, edge endpoints, compression, namespace and fonts — structurally-validated.

### visual_checks

- Render inspected at 1280 px. One arrowhead defect was fixed and the re-render was clean — visually-validated.

### live_or_external_checks

- DynamoDB global table consistency options, Route 53 health-check behavior and cross-Region transfer pricing were not checked against current AWS documentation — not-verified.

### unresolved_risks

- Last-writer-wins can silently discard a concurrent update made in the other Region. The business has not confirmed that this is acceptable for shipment status — not-verified.
- Whether a stronger consistency option is required has not been decided. Check the current DynamoDB global tables documentation before the design is approved — not-verified.
- DNS failover time depends on TTL and client caching. Requirement S3 is met only by design, because no Region-outage test has been run — not-verified.

### next_safe_action

- Ask the product owner to accept or reject last-writer-wins for status updates. The diagram changes only if a different replication or consistency model is chosen.
