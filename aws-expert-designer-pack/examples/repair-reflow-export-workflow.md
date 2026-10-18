# Worked example: repair, reflow and export for the change board

Synthetic scenario. It continues `diagram-review-workflow.md`. Workflow prompts: `repair-aws-drawio-xml`, then `reflow-aws-diagram-layout`, then `export-drawio-diagram`.

## Authority

The user replies: "Fix everything in a new file, `network-overview.v2.drawio`, and keep the original. Export SVG and PNG into `exports/` for the deck. Don't upload anything to the wiki."

That covers one new source file and one export folder. It does not cover changing `network-overview.drawio` or publishing anywhere.

## Repair

This step applies `aws-xml-authoring`, its checklist, and `aws-icons-and-visual-language`.

| Cell | Defect (review ID) | Repair | Meaning changed? |
|---|---|---|---|
| file | Compressed payload (S1) | Written uncompressed with an inline `mxGraphModel` | no |
| `e12` | Dangling target `node_44` (S2) | New neutral cell `cgw_corp` labeled "Customer gateway (corporate data center)" inside an on-premises group; `e12` re-targeted to it | restores what the Terraform declares (observed) |
| `elb`, `rds_primary`, `natgw` | Legacy `mxgraph.aws3` (S3) | AWS4 resource icons and resource shapes. Each name was confirmed in the installed library's AWS4 sidebar before use | no |
| `jenkins` | EC2 icon for an on-premises system (S4) | Neutral server shape in the on-premises group | yes: corrects the hosting claim, based on the user's statement |
| `rds_primary` | In a public subnet (M1) | Re-parented to `subnet_data_a` | yes: Terraform evidence |
| `natgw` | In a private subnet (M2) | Re-parented to `subnet_public_a` | yes: Terraform evidence |
| `sg_app` | Security group used as a real container (M3) | Removed. New `sg_app_a` and `sg_app_b` dashed annotation groups (`container=0`) around the app instances, labeled "sg-app (attached to instance ENIs)". Subnets re-parented to their AZs | yes: removes a false boundary |
| new `rds_standby` | Multi-AZ standby missing (M4) | Standby in `subnet_data_b`; edge `edge_rds_sync` labeled "synchronous replication, cross-AZ, standby not readable" | yes: Terraform evidence |
| `e7` | Edge ends on a container (A1) | Re-targeted to `asg_app_a`, the icon of the target group's Auto Scaling group | no |
| `e3`, `e4` | No arrowheads (A2) | `endArrow=block`, from web to app, labeled "HTTP 8080" | no; the direction comes from security-group evidence |

Every valid original ID is kept, so the diff against the decoded original stays readable; only `sg_app` is removed. New cells get semantic IDs. Each correction that changes meaning appears in the companion report's decision table with its evidence.

## Reflow

This step applies `aws-layout-and-composition`.

- The repairs raised the primary service count to 14, so spacing goes to 220 px by 160 px.
- Internet users sit at the top left below the title block. The on-premises group sits at the bottom left. Its VPN edge is labeled "hybrid: Site-to-Site VPN, two tunnels".
- The Region frame becomes decorative (C2), and the AZs are re-parented to the VPC. Fonts are Helvetica throughout, and edge labels are 11 px (C1). The VPN label is widened (V1).
- A legend is added for solid, dashed and annotation-group styles and for the cost-bearing label prefixes.

The first render at slide size showed that a single page could not hold 14 services with readable 10 px labels: they shrank to about 7 px on the slide. Following the skill, the agent split the views rather than shrinking text:

- Page "Overview": users, VPC, AZs, ALB, app tier, NAT and egress, and the database primary, standby and replication edge. The on-premises side is one labeled cell, "Corporate data center (detail on page Hybrid)", joined by a single VPN edge.
- Page "Hybrid": the customer gateway, both VPN tunnels, the virtual private gateway, and the on-premises group with Jenkins. `cgw_corp`, `e12` and `jenkins` move here with their IDs unchanged, so they still diff against the original.

The agent then re-checked that the reflow changed no meaningful parent. Every cell kept the subnet, AZ and VPC parent it had after the repair. Each page has its own root cells, and IDs are unique within each page.

## Export

This step applies `drawio-render-export-and-review`.

- Draw.io Desktop was found at `C:\Program Files\draw.io\draw.io.exe`, and the version it printed was recorded in the render record.
- Commands, one for each page and format. Both pages ran; page 1 is shown:

```text
"C:\Program Files\draw.io\draw.io.exe" --export --format svg --page-index 1 --border 20 --output exports\network-overview.v2-overview.svg network-overview.v2.drawio
"C:\Program Files\draw.io\draw.io.exe" --export --format png --page-index 1 --scale 2 --border 20 --output exports\network-overview.v2-overview.png network-overview.v2.drawio
```

- All four commands exited with code 0. Exit codes were recorded, but not treated as quality evidence.
- The PNGs were inspected at slide size (1920×1080, image scaled to fit) and the SVGs in a Windows browser at 100%. Two defects appeared. On the overview, the legend overlapped the egress label. In the SVG, labels referencing Helvetica rendered in a substitute font on Windows, slightly wider.
- Fixes: the legend moved 40 px right and that page was re-exported. Under the substitute font every label still fit its geometry, so the font substitution is recorded as a limit rather than changed.
- Nothing was uploaded to the wiki.

## Completion report

Pack: aws-expert-designer.

Outcome: corrected diagram and slide exports delivered; the original file is untouched.

### scope_and_inputs

- Task: repair, reflow and export of `network-overview.drawio` into a new file. The user authorized the new file and `exports/`. No other changes and no publishing.
- Inputs: the original diagram, `infra/network/*.tf`, the review findings and the user's statement about Jenkins — observed.

### source_facts

- Database subnets are private, Multi-AZ is enabled, the NAT gateway is in a public subnet, and the VPN and customer gateway are declared — observed.
- App security-group ingress is from the web security group on 8080 — observed.

### assumptions_and_design_decisions

- The two-page split, overview and hybrid, keeps labels readable at slide size — designed.
- The on-premises side is summarized as one labeled cell on the overview page — designed.
- Security groups shown as annotation groups, not containers — designed.
- Helvetica substitution in the SVG on Windows was accepted after inspection — designed.

### output_files

- `network-overview.v2.drawio`: new, uncompressed, two pages.
- `network-overview.v2.md`: new companion report with the change list and decisions.
- `exports/network-overview.v2-overview.svg`, `exports/network-overview.v2-overview.png`, `exports/network-overview.v2-hybrid.svg` and `exports/network-overview.v2-hybrid.png`: new.
- `network-overview.drawio`: unchanged.

### structural_checks

- Parse, root cells on each page, IDs unique within each page (every valid original ID kept, `sg_app` removed), parents, edges with existing icon endpoints, no compression, AWS4 namespace only, Helvetica — structurally-validated.

### visual_checks

- Both pages were inspected as PNG at slide size and as SVG at 100%. The legend overlap was fixed and re-exported, and the font substitution was inspected and found acceptable — visually-validated.

### live_or_external_checks

- The deployed network was not compared. Evidence is Terraform plus the user's statement — not-verified.

### unresolved_risks

- Changes made outside Terraform would not appear in either file — not-verified.
- On a machine with Helvetica, SVG text may render narrower than reviewed. It will still fit — inferred.

### next_safe_action

- The user inserts the four exports into the deck. Replacing the original file or publishing to the wiki needs a separate go-ahead.
