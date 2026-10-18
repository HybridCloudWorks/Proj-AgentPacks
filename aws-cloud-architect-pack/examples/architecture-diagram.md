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

`aws-architecture-visualization` checked for a dedicated AWS diagram capability. None was installed in this host, so generation fell to `drawio-core-generation`.

`drawio-core-generation` chose native XML over Mermaid. The diagram needs AWS4 icons, nested account, Region, AZ and subnet boundaries, and reviewable IDs. Cell IDs reuse the TOPOLOGY ids (`svc-alb`, `svc-ingest-api`, `sn-app-a` and so on), so a reviewer can trace each shape back to the handoff.

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

The architect parsed the file with Python's standard XML parser and checked it against the skill's structural list:

- Root `mxfile`, two `diagram` elements, inline uncompressed `mxGraphModel` on each page.
- Root cells `0` and `1` present on each page.
- 87 cells, all IDs unique.
- Every `parent`, `source` and `target` resolves.
- Every AWS shape uses `shape=mxgraph.aws4.*` or `resIcon=mxgraph.aws4.*`. No legacy `mxgraph.aws.` styles.
- No hidden or orphaned cells.
- No HTML labels containing script.

All checks passed: structurally-validated.

## Render and export

`drawio-render-export-and-review` looked for Draw.io Desktop in three places:

- `C:\Program Files\draw.io\draw.io.exe`: not found.
- The per-user install directory under `%LOCALAPPDATA%\Programs\draw.io`: not found.
- `PATH`: no `draw.io` or `drawio` on it.

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
| `diagrams/tracking-platform.drawio` | Editable source, two pages | XML parse plus the structural checks listed above | structurally-validated |
| `diagrams/tracking-platform.drawio` | Visual quality | Not rendered | not-verified |
| `diagrams/export/tracking-platform-*.png` | Slide images | Not produced: no renderer | not-verified |

### live_or_external_checks

- Draw.io Desktop detection: executed, not found.
- Export and visual review: not executed (not-verified).
- AWS account comparison: not in scope and not executed (not-verified).

### unresolved_risks

- Layout problems such as clipping, overlaps or unreadable labels may exist and have not been seen. The design review needs a PNG (owner: requester).

### next_safe_action

The requester either installs Draw.io Desktop or opens the `.drawio` file in an approved Draw.io editor. The architect then re-runs the export and the visual review before Thursday. Do not present the diagram as reviewed until then.
