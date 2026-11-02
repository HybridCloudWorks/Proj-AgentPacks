# Worked example: Draw.io diagram of the approved tracking-platform design

Workflow: `create-aws-architecture-diagram.prompt.md`. Skills applied: `aws-architecture-visualization`, `drawio-core-generation`, `drawio-render-export-and-review`, `diagram-validation-and-evidence`.

This example ends **unverified**. The diagram is structurally validated, but it was never rendered, so no visual check ran. The workload is the fictional Larkspur tracking platform from the greenfield example.

## Request

> Draw the approved tracking-platform architecture from `handoff/tracking-platform/` for Thursday's design review. I need a runtime view and a network view, and a PNG for the slides.

## Inputs

| Input | Label |
|---|---|
| `handoff/tracking-platform/TOPOLOGY.json`, ADR-001 to ADR-003 marked accepted by the architecture owner | observed |
| Audience: platform and security reviewers | observed (request) |
| Output: `diagrams/tracking-platform.drawio` and `diagrams/export/tracking-platform-*.png` | observed (request) |

## Routing and generation

`aws-architecture-visualization` routed generation to the shared `drawio-core-generation`, then structural checks, rendering and validation to `diagram-validation-and-evidence` and `drawio-render-export-and-review`.

`drawio-core-generation` chose native XML over Mermaid. The diagram needs draw.io's AWS library icons and group styles, boundaries nested account > Region > VPC > Availability Zone > subnet, and reviewable IDs. Every icon and group style was copied whole from the library, with its category `fillColor` and bottom label. Cell IDs reuse the TOPOLOGY ids (`svc-alb`, `svc-ingest-api`, `sn-app-a` and so on), so a reviewer can trace each shape back to the handoff.

Two pages:

1. **Runtime and data flow.** CloudFront with WAF, the ALB, the ECS Fargate service, API Gateway with mTLS, SQS and its dead-letter queue, the Lambda consumer, DynamoDB, the S3 export and AWS Backup copies to eu-central-1. Numbered flows and a legend.
2. **Network and egress.** The VPC, three AZs with application and endpoint subnets, gateway and interface endpoints, the Transit Gateway attachment to the hub, and the CloudFront origin-facing prefix list on the ALB security group.

Cost-bearing edges are labelled: CloudFront-to-ALB transfer, interface endpoint hours per AZ, and the cross-Region backup copy. The legend explains line styles, with a dashed line for "observed in landing-zone inventory, routes not verified".

## Semantic review

`diagram-validation-and-evidence` compared every shape and edge with TOPOLOGY.json and found two problems in the first draft. Both were corrected:

| Issue | Evidence | Correction |
|---|---|---|
| The Lambda consumer was drawn inside the VPC container | TOPOLOGY places `svc-consumer` as "Regional, outside any VPC" (designed, ADR-001) | Moved outside the VPC boundary, inside the Region boundary. Drawing it inside the VPC would have shown network placement that does not exist |
| The Transit Gateway attachment was drawn as a solid line, like the flows that were designed | TOPOLOGY labels the attachment observed, with route propagation not-verified | Changed to the dashed "observed, routes not verified" style |

Nothing in the diagram is missing from the approved design, and nothing in it is extra.

## Structural checks

The architect ran the checker that ships with `diagram-validation-and-evidence`, in strict mode, after every write:

```text
python <installed skills>/diagram-validation-and-evidence/scripts/check_drawio.py --strict diagrams/tracking-platform.drawio
pages: 2 (Runtime and data flow, Network and egress)
cells: 71 vertices, 12 edges
catalog: draw.io 32.5.5, built 2026-10-18
icons AWS: current 38
errors: 0
warnings: 0
result: PASS
```

- Exit code 0. Each page has an inline, uncompressed `mxGraphModel` with root cells `0` and `1`; the 87 cells have unique IDs within each page; every `parent`, `source` and `target` resolves; no cell is hidden or orphaned, and no label carries script.
- All 38 AWS icons and groups are in the catalog's current list, with none legacy, retired or unknown. A namespace check would not have shown this, because draw.io's legacy AWS18 library shares the `mxgraph.aws4` namespace.
- Read from the XML: every subnet sits in one Availability Zone inside the VPC, and nothing is parented to a `container=0` frame.

Structural result: structurally-validated. The checker cannot tell whether each icon is the right product; that was compared by hand with TOPOLOGY.json in the semantic review above.

## Render and export

`drawio-render-export-and-review` looked for Draw.io Desktop in four places:

- `C:\Program Files\draw.io\draw.io.exe`: not found.
- The per-user install directory under `%LOCALAPPDATA%\Programs\draw.io`: not found.
- `PATH`: no `draw.io` or `drawio` on it.
- The Microsoft Store build: `Get-AppxPackage *draw.io*` returned no package.

No renderer was available, so **no PNG was exported and no visual check ran**. The source file was not modified to work around this. Spacing, clipping, label legibility, icon scale and edge crossings have not been inspected.

## Completion report

Pack: aws-cloud-architect. Date: 2026-10-18.

Outcome: the editable diagram is written and structurally validated. Rendering, the PNG export and the visual review are not verified, because Draw.io Desktop was unavailable.

### scope_and_inputs

A runtime view and a network view of the approved tracking-platform design, drawn from `handoff/tracking-platform/` (observed). Authority covered writing files under `diagrams/`.

### business_outcomes_and_requirements

Give the platform and security reviewers diagrams they can review on Thursday, showing boundaries, flows, identities, failure domains and cost-bearing edges, plus a PNG for the slides.

### source_facts_and_evidence

- Every shape traces to a TOPOLOGY id.
- Placement and flow labels come from TOPOLOGY and ADR-001 to ADR-003: designed or observed, as recorded there.
- Two first-draft misrepresentations were corrected (see Semantic review).

### framework_alignment

Not applicable as a review. The diagram shows the existing design's multi-AZ placement, KMS and identity boundaries and cost-bearing edges. It adds no framework findings.

### proposed_architecture

Unchanged from the approved handoff. The diagram adds no services or relationships.

### assumptions_and_tradeoffs

- Native XML was chosen over Mermaid so that AWS4 icons and nested boundaries could be used.
- The work was split into two pages to keep each one readable.
- Interface endpoints are grouped as a single icon per AZ, with a list label.

### implementation_and_operating_implications

- Keep the `.drawio` file next to the handoff in version control. Update it whenever TOPOLOGY changes, and keep the IDs equal to the TOPOLOGY ids.
- Exports are generated outputs, not source files.

### security_resilience_cost_and_sustainability

- Security boundaries shown: the mTLS ingest edge, the WAF edge, the private-only VPC and the KMS key ownership note.
- Failure domains shown: three AZs and the backup Region.
- Cost-bearing edges are labelled.
- None of this is evidence of the deployed environment.

### output_files

| File | Purpose | Check run | Label |
|---|---|---|---|
| `diagrams/tracking-platform.drawio` | Editable source, two pages | `check_drawio.py --strict`, exit 0, 38 AWS icons current (catalog draw.io 32.5.5), plus the nesting read from the XML | structurally-validated |
| `diagrams/tracking-platform.drawio` | Visual quality | Not rendered | not-verified |
| `diagrams/export/tracking-platform-*.png` | Slide images | Not produced: no renderer | not-verified |

### live_or_external_checks

- Draw.io Desktop detection: executed in four places, including the Microsoft Store build; not found.
- Export and visual review: not executed (not-verified).
- AWS account comparison: not in scope and not executed (not-verified).

### unresolved_risks

- Layout problems such as clipping, overlaps or unreadable labels may exist and have not been seen. The design review needs a PNG (owner: requester).

### next_safe_action

The requester either installs Draw.io Desktop or opens the `.drawio` file in an approved Draw.io editor. The architect then re-runs the export and the visual review before Thursday. Do not present the diagram as reviewed until then.
