# Worked example: read-only review before a change board

Synthetic scenario. File names, cell IDs and resources are fictional. Workflow prompt: `review-aws-diagram`.

## Request

"Is `network-overview.drawio` right? We present it to the change advisory board on Thursday. Compare it with `infra/network/`. Don't change anything yet."

The scope is read-only. The audience is the change board, and the diagram will appear on a 1920×1080 slide.

## How the review ran

1. `diagram-validation-and-evidence`, structural pass.
   - The `<diagram>` element held a compressed payload. The agent decoded it in memory to inspect it: base64, then raw inflate, then URL-decode. The source file was not rewritten.
   - The decoded model has 63 cells.
2. `aws-xml-authoring` and its checklist reference: IDs, parents, edge references, escaping and geometry.
3. `aws-icons-and-visual-language`: namespaces, legacy shapes and product icons used for non-AWS components.
4. Semantic comparison with `infra/network/*.tf` under `aws-architecture-patterns`: VPC checks, false containment, Multi-AZ representation.
5. `aws-layout-and-composition` readability review, and a `drawio-render-export-and-review` render to `%TEMP%\cab-review\`, outside the source folder, using the detected Draw.io Desktop. The render was inspected at slide size.

## Findings

| ID | Page / cell | Finding | Evidence | Impact | Recommended correction | Blocks? |
|---|---|---|---|---|---|---|
| M1 | Page 1 / `rds_primary` | The database sits inside the container labeled "Public subnet 1" | `aws_db_subnet_group.main` uses `aws_subnet.private[*].id`; `publicly_accessible = false` (observed) | misleading | Re-parent into a private data subnet in AZ a | yes |
| M2 | Page 1 / `natgw` | The NAT gateway sits inside a private subnet | `aws_nat_gateway.main.subnet_id = aws_subnet.public[0].id` (observed) | misleading | Re-parent into public subnet a | yes |
| M3 | Page 1 / `sg_app` | A security group is drawn as a real container (`container=1`) whose children are both private subnets in both AZs. That implies subnets live inside a security group and that it forms a network boundary | Security groups attach to network interfaces; the Terraform attaches `sg_app` to the launch template (observed) | misleading | Replace with dashed annotation groups (`container=0`) around the app instances in each subnet, labeled with the group name | yes |
| M4 | Page 1 / `rds_primary` | No standby or replication is shown | `multi_az = true` on `aws_db_instance.main` (observed) | misleading | Add the standby in a private subnet in AZ b with a cross-AZ "synchronous replication, standby not readable" edge | yes |
| S1 | file | The payload is compressed, so reviews and diffs cannot see changes | `<diagram>` has no inline `mxGraphModel` | structural | Save uncompressed | no |
| S2 | Page 1 / `e12` | The edge labeled "VPN" references the missing target `node_44` and renders as a loose line | Target ID not present among the 63 cells | structural | Restore the customer-gateway endpoint; `aws_vpn_connection.corp` and `aws_customer_gateway.corp` exist (observed) | yes |
| S3 | Page 1 / `elb`, `rds_primary`, `natgw` | Three cells use the legacy `mxgraph.aws3` namespace | Cell styles | structural | Replace with AWS4 names from the installed library | no |
| S4 | Page 1 / `jenkins` | An Amazon EC2 product icon represents Jenkins, which the user says runs in the corporate data center | Cell style; user statement (observed) | misleading | Use a neutral server shape inside an on-premises group | no |
| A1 | Page 1 / `e7` | The ALB edge ends on the container `subnet_private_a`, not on a target | Edge `target="subnet_private_a"` | ambiguous | Attach to the app instances' icon | no |
| A2 | Page 1 / `e3`, `e4` | Web-to-app edges have `endArrow=none`, so direction is unclear | Cell styles; app security group ingress from web security group on 8080 (observed) | ambiguous | Add arrowheads from web to app, labeled "HTTP 8080" | no |
| C1 | Page 1 / many | Arial and Helvetica are mixed; edge labels are 9 px | Cell styles | cosmetic | Helvetica throughout; edge labels 11 px | no |
| C2 | Page 1 / `region_main` | The Region frame is a real container that parents the AZs | `container=1` | cosmetic | Make the Region decorative (`container=0`) and parent the AZs to the VPC | no |
| V1 | Page 1 / `vpn_label` | "Site-to-Site VPN connection" is clipped at slide size | Scratch render (visually inspected) | cosmetic | Widen the label or wrap it | no |

Not reviewed: page 2 ("DR notes"), which the user did not ask about. IAM and security-group rule details beyond what M3 and A2 needed.

Recommended follow-up:

| Findings | Workflow | Approval needed |
|---|---|---|
| S1, S2, S3, S4, M1–M4, A1, A2 | `repair-aws-drawio-xml` | Write a new file, or change `network-overview.drawio` |
| C1, C2, V1 | `reflow-aws-diagram-layout` | The same file decision |
| Slide images | `export-drawio-diagram` | An output folder |

## Completion report

Pack: aws-expert-designer.

Outcome: review delivered; no files changed.

### scope_and_inputs

- Task: read-only review of page 1 of `network-overview.drawio` against `infra/network/`, for the change board on a 1920×1080 slide.
- Inputs: the diagram, `infra/network/*.tf`, and the user's statement that Jenkins runs on premises — observed.

### source_facts

- The database subnet group uses private subnets; `publicly_accessible = false`; `multi_az = true` — observed.
- The NAT gateway is in `aws_subnet.public[0]` — observed.
- `sg_app` is attached through the launch template; app ingress is from the web security group on 8080 — observed.
- A VPN connection and a customer gateway are declared — observed.

### assumptions_and_design_decisions

- The missing `node_44` was the customer gateway. Inferred from the edge label and the Terraform — inferred.
- The impact scale used is misleading, ambiguous, structural or cosmetic, and "Blocks?" is judged against the change board's purpose — designed.

### output_files

- None written in the repository. Scratch render in `%TEMP%\cab-review\`, not a deliverable.

### structural_checks

- The decoded model was checked for IDs, parents, edge references, namespaces and compression. Findings S1–S3 and A1 resulted — structurally-validated.

### visual_checks

- Scratch render inspected at slide size. Finding V1 resulted — visually-validated. This applies only to the current file, and no corrected version exists yet.

### live_or_external_checks

- No AWS account was consulted. The findings compare the diagram with Terraform, not with the deployed network — not-verified.

### unresolved_risks

- If anything was changed outside Terraform, the deployed network may differ from both the diagram and the source — not-verified.
- Five blocking findings mean the current file should not be presented as accurate — observed.

### next_safe_action

- Decide whether the corrections go into a new file, such as `network-overview.v2.drawio`, or into the original. Then run the repair and reflow workflows.
