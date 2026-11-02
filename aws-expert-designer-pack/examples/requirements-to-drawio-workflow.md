# Worked example: order portal from written requirements

Synthetic scenario. Names, paths, CIDRs and counts are fictional. Workflow prompt: `design-aws-diagram`.

## Request and framing

The user supplies `requirements/order-portal.md` with six statements and asks for a diagram for next week's security design review.

- R1: Customers place orders through a web front end.
- R2: Static assets are served from a CDN.
- R3: The application runs in containers, with no servers to patch.
- R4: Order data includes personal data and stays in eu-west-1.
- R5: The service survives the loss of one Availability Zone.
- R6: The payment provider allowlists our outbound IP addresses.

Framing under `drawio-core-generation`:

- Purpose: a security design review.
- Audience: architects and security reviewers.
- Fidelity: logical, with network boundaries, but not every security-group rule.
- Output: a new file, `architecture/order-portal.drawio`, plus a companion report.
- Generation path: native XML, because the diagram needs draw.io's AWS library icons and group styles, real account, Region, VPC, AZ and subnet containment, and a precisely routed egress edge.

## Questions asked

`aws-architecture-design` in interactive design mode asks only questions that change the architecture.

1. "Is this one AWS account, or separate accounts per environment?" Answer: one production workload account. The Organization is not drawn.
2. "How many source addresses will the payment provider allowlist?" Answer: at most two. That fits one NAT gateway with an Elastic IP in each of two AZs.

The agent asked nothing about compute or database products. Those became recorded design decisions, offered as a minimal architecture with optional layers.

## Architecture model

| Element | Placement | Label | Basis |
|---|---|---|---|
| Amazon CloudFront | edge, outside the Region frame | designed | R2 |
| Amazon S3 bucket for static assets | Region, no VPC | designed | R2; origin access limited to CloudFront |
| Application Load Balancer | VPC, with nodes in public subnets a and b | designed | R1, R5 |
| Amazon ECS service on AWS Fargate | private app subnets a and b, no public IPs | designed | R3, R5 |
| Amazon Aurora PostgreSQL cluster: writer in AZ a, reader in AZ b | private data subnets | designed | R4, R5 |
| NAT gateway with Elastic IP, one per AZ | public subnets a and b | designed | R6, answer 2 |
| AWS Secrets Manager, Amazon CloudWatch Logs | Region, drawn over a decorative auxiliary frame | designed | database credentials, task logs |
| Production workload account | outermost frame, a real container | observed | answer 1 |
| Region eu-west-1 | real container inside the account frame | observed | R4 |
| Two Availability Zones | real containers inside the VPC, one subnet of each tier in each | observed | R5 |

| Relationship | Kind | Label |
|---|---|---|
| Customers → CloudFront | synchronous HTTPS | designed |
| CloudFront → S3 (static paths) and → ALB (`/api/*`) | origin requests | designed |
| ALB → tasks in both AZs | synchronous HTTP; cross-zone load balancing | designed |
| Tasks in AZ b → Aurora writer in AZ a | synchronous SQL; cross-AZ | designed |
| Tasks → NAT gateway in the same AZ → payment provider | egress; NAT data processing is billed | designed |
| Aurora storage replication across AZs | managed by Aurora; drawn as a note on the cluster, not as an edge between instances | designed |

The `aws-architecture-patterns` VPC check: a subnet is public because its route table sends 0.0.0.0/0 to the internet gateway, and the label says so. The ALB and the NAT gateways sit in public subnets. Tasks get no public IPs. Each private route table points at the NAT gateway in its own AZ, so egress does not cross AZs.

Image pulls and the calls to Secrets Manager and CloudWatch Logs leave through the NAT gateways in this version. Interface VPC endpoints are listed as an optional security layer and are not drawn.

## Visual and layout decisions

- `aws-icons-and-visual-language`: every AWS icon and boundary style was copied whole from the installed draw.io AWS library through its shape search, including each icon's category `fillColor` and bottom label. Only the typography was changed to the house style. The ALB uses the `application_load_balancer` resource icon, not the Elastic Load Balancing service icon. Customers use the AWS General Resources `users` icon. The payment provider is a third-party system, so it gets a labelled neutral shape. Every icon is 48×48 and is parented directly to its subnet, VPC, Region or account. No category tiles are used.
- Boundaries use the library's AWS group styles, nested account > Region > VPC > Availability Zone > subnet. Each subnet sits in exactly one Availability Zone.
- The diagram has eight primary services, so it gets a right-side legend and teal step badges 1 to 5 on the request path. Secrets Manager and CloudWatch Logs are parented to the Region and drawn over a dashed auxiliary frame without step numbers. The frame is decorative: `container=0` and no children.
- `aws-layout-and-composition`: request flow runs left to right. AZ a and AZ b are stacked rows, so cross-AZ edges are short, vertical and labeled. Spacing is 180 px by 120 px. Customers sit below the title block at y = 160.
- The ALB is drawn once, parented to the VPC and straddling both public subnets, with the label "Application Load Balancer (nodes in public subnets a and b)". Real containment cannot place one icon in two subnets, and drawing two ALBs would be false.

## XML excerpt

Applying `aws-xml-authoring`. IDs are semantic and stable, and geometry is abbreviated. Each style is the library's palette style with only `fontFamily`, `fontSize` and `fontStyle` changed.

```xml
<mxCell id="region_euw1" value="AWS Region eu-west-1" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor=#00A4A6;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=1;fontFamily=Helvetica;fontSize=14;fontStyle=1;" vertex="1" parent="account_prod">
  <mxGeometry x="20" y="40" width="1180" height="900" as="geometry" />
</mxCell>
<mxCell id="vpc_orders" value="VPC orders-prod 10.20.0.0/16" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc2;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#AAB7B8;dashed=0;fontFamily=Helvetica;fontSize=14;fontStyle=1;" vertex="1" parent="region_euw1">
  <mxGeometry x="40" y="50" width="1000" height="700" as="geometry" />
</mxCell>
<mxCell id="az_a" value="Availability Zone a" style="fillColor=none;strokeColor=#147EBA;dashed=1;verticalAlign=top;fontColor=#147EBA;whiteSpace=wrap;html=1;fontFamily=Helvetica;fontSize=12;fontStyle=1;container=1;collapsible=0;recursiveResize=0;" vertex="1" parent="vpc_orders">
  <mxGeometry x="160" y="40" width="820" height="300" as="geometry" />
</mxCell>
<mxCell id="subnet_public_a" value="Public subnet a (route table sends 0.0.0.0/0 to the internet gateway)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#7AA116;fillColor=#F2F6E8;verticalAlign=top;align=left;spacingLeft=30;fontColor=#248814;dashed=0;fontFamily=Helvetica;fontSize=12;fontStyle=1;" vertex="1" parent="az_a">
  <mxGeometry x="20" y="40" width="240" height="240" as="geometry" />
</mxCell>
<mxCell id="svc_alb" value="Application Load Balancer&lt;br&gt;(nodes in public subnets a and b)" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#8C4FFF;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.application_load_balancer;fontFamily=Helvetica;fontSize=10;fontStyle=0;" vertex="1" parent="vpc_orders">
  <mxGeometry x="276" y="326" width="48" height="48" as="geometry" />
</mxCell>
<mxCell id="edge_alb_tasks_b" value="HTTP to targets, cross-AZ" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontFamily=Helvetica;fontSize=11;labelBackgroundColor=default;endArrow=block;endFill=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="svc_alb" target="svc_tasks_b">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

Every boundary is a real container copied from the library's "AWS / Groups" palette, so the VPC is parented to the Region and the Region to the account frame `account_prod`. The library's Availability Zone rectangle has no `container=1`, so it was added. The ALB icon is parented to the VPC, not to a category tile, and sits in the gap between the two Availability Zone rows, across the public-subnet column. The edge ends on the task icon `svc_tasks_b`, not on its subnet.

## Validation

`diagram-validation-and-evidence`, structural checks, run after every write:

```text
python <installed skills>/diagram-validation-and-evidence/scripts/check_drawio.py --strict architecture/order-portal.drawio
file: architecture/order-portal.drawio
pages: 1 (Overview)
cells: 35 vertices, 14 edges
catalog: draw.io 32.6.9, built 2026-11-01
icons AWS: current 22
errors: 0
warnings: 0
result: PASS
```

- Exit code 0. The checker parsed the file, found root cells `0` and `1`, unique IDs, resolvable parents and edge endpoints and no compression, and matched all 22 AWS names, 13 icons and 9 groups, against the catalog's current list. The `mxgraph.aws4` namespace alone was not taken as proof, because the legacy AWS18 library shares it.
- Read from the XML: all 14 edges end on icons; account > Region > VPC > Availability Zone > subnet nesting holds, with each subnet in one Availability Zone; nothing is parented to the `container=0` auxiliary frame; Helvetica is used throughout.
- The checker cannot judge whether each icon is the right product. That was compared by hand with the model table.

Semantic check: every element traces to R1–R6, to one of the two answers, or to a recorded decision.

Visual check under `drawio-render-export-and-review`:

- Draw.io Desktop was not at `C:\Program Files\draw.io\draw.io.exe` or on PATH. `Get-AppxPackage *draw.io*` reported the Microsoft Store build, and its `app\draw.io.exe` printed its version with `--version`, which was recorded.
- `draw.io.exe -x -k -f png -o %TEMP%\order-portal-review\order-portal.png architecture\order-portal.drawio` wrote a review PNG outside the repository. It was inspected at 100% and at 1280 px width. Every icon and group drew its symbol.
- Two defects were found. The label "Amazon Aurora PostgreSQL-Compatible Edition" ran into the reader icon. The egress label overlapped the VPC border.
- Fixes: the label was split over two lines with `<br>`, and a waypoint moved the egress label 30 px clear of the border. The checker ran again and passed.
- The first review PNG was deleted, because `-k` refuses to overwrite it, and the diagram was re-rendered. No defects remained, and `diagram-validation-and-evidence` was completed on that render.

## Completion report

Pack: aws-expert-designer.

Outcome: diagram delivered as a new file.

### scope_and_inputs

- Task: design from requirements. A new diagram; no existing file was changed.
- Purpose and audience: security design review; architects and security reviewers.
- Inputs: `requirements/order-portal.md` (R1–R6) and the user's two answers — observed.

### source_facts

- Order data stays in eu-west-1 (R4) — observed.
- The service survives the loss of one AZ (R5) — observed.
- The payment provider allowlists at most two source addresses (R6, answer 2) — observed.
- One production workload account (answer 1) — observed.

### assumptions_and_design_decisions

- ECS on Fargate for R3; Aurora PostgreSQL with the writer in AZ a and the reader in AZ b — designed.
- One NAT gateway with an Elastic IP per AZ, with each private route table pointing at its own AZ's NAT gateway — designed.
- ALB drawn once, parented to the VPC across both public subnets — designed.
- Aurora storage replication shown as a cluster note, not as an instance-to-instance edge — designed.
- Interface endpoints offered as an optional layer and not drawn — designed.
- The Organization and other accounts are out of scope — inferred from answer 1.

### output_files

- `architecture/order-portal.drawio`: new, uncompressed, one page.
- `architecture/order-portal.md`: new companion report holding the model tables above.
- `%TEMP%\order-portal-review\order-portal.png`: scratch render, not a deliverable.

### structural_checks

- `check_drawio.py --strict`: exit 0; 22 AWS icons and groups current, none legacy, retired or unknown; catalog draw.io 32.6.9 — structurally-validated.
- Edges ending on icons, account > Region > VPC > Availability Zone > subnet nesting, no children under the decorative frame, and Helvetica, checked by reading the XML — structurally-validated.
- Each icon is the right product for its component, compared by hand with the model — observed.
- Icon styles come from the installed draw.io AWS library; they were not compared with the current AWS-approved icon package — not-verified.

### visual_checks

- Draw.io Desktop (Microsoft Store build) render at scale 1, inspected at 100% and at 1280 px. Every icon drew. Two defects were fixed and the re-render was clean — visually-validated.

### live_or_external_checks

- No AWS account, CLI or API was used. Service availability and pricing in eu-west-1 were not checked against current documentation — not-verified.

### unresolved_risks

- How long it takes to promote the Aurora reader, and how connections are handled during an AZ loss, are neither shown nor tested. R5 is satisfied by design, not proven resilient — not-verified.
- NAT data-processing cost grows with image-pull volume. Interface endpoints may be cheaper and tighter; the security review decides — designed.

### next_safe_action

- Send the file and the companion report to the security review. If the review adopts interface endpoints, the diagram needs updating, and changing it needs the user's go-ahead.
