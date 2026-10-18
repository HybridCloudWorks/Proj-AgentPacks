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
- Generation path: native XML, because the diagram needs AWS4 icons, real VPC, AZ and subnet containment, and a precisely routed egress edge.

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
| AWS Secrets Manager, Amazon CloudWatch Logs | Region, auxiliary frame | designed | database credentials, task logs |
| Region eu-west-1 | decorative frame | observed | R4 |
| Two Availability Zones | real containers | observed | R5 |

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

- `aws-icons-and-visual-language`: AWS4 resource icons for each AWS service, with names taken from the installed Draw.io AWS4 sidebar. Customers and the payment provider use neutral shapes with labels. Each icon is 48×48 inside a 120×120 category container.
- The diagram has eight primary services, so it gets a right-side legend and teal step badges 1 to 5 on the request path. Secrets Manager and CloudWatch Logs sit in a dashed auxiliary frame without step numbers.
- `aws-layout-and-composition`: request flow runs left to right. AZ a and AZ b are stacked rows, so cross-AZ edges are short, vertical and labeled. Spacing is 180 px by 120 px. Customers sit below the title block at y = 160.
- The ALB is drawn once, parented to the VPC and straddling both public subnets, with the label "Application Load Balancer (nodes in public subnets a and b)". Real containment cannot place one icon in two subnets, and drawing two ALBs would be false.

## XML excerpt

Applying `aws-xml-authoring`. IDs are semantic and stable, and geometry is abbreviated.

```xml
<mxCell id="region_euw1" value="AWS Region eu-west-1" style="rounded=0;whiteSpace=wrap;html=1;container=0;fillColor=none;strokeColor=#00A4A6;fontColor=#00A4A6;fontFamily=Helvetica;fontSize=14;fontStyle=1;verticalAlign=top;align=left;spacingLeft=10;" vertex="1" parent="1">
  <mxGeometry x="400" y="140" width="1180" height="900" as="geometry" />
</mxCell>
<mxCell id="vpc_orders" value="VPC orders-prod 10.20.0.0/16" style="rounded=0;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;fillColor=none;strokeColor=#8C4FFF;fontColor=#8C4FFF;fontFamily=Helvetica;fontSize=14;fontStyle=1;verticalAlign=top;align=left;spacingLeft=10;" vertex="1" parent="1">
  <mxGeometry x="440" y="190" width="1000" height="700" as="geometry" />
</mxCell>
<mxCell id="cat_alb" value="Networking" style="rounded=1;whiteSpace=wrap;html=1;container=1;collapsible=0;fillColor=#F3EDFF;strokeColor=#8C4FFF;fontColor=#8C4FFF;fontFamily=Helvetica;fontSize=10;verticalAlign=top;" vertex="1" parent="vpc_orders">
  <mxGeometry x="40" y="260" width="120" height="120" as="geometry" />
</mxCell>
<mxCell id="svc_alb" value="Application Load Balancer (nodes in public subnets a and b)" style="outlineConnect=0;fontColor=#232F3E;fillColor=#8C4FFF;strokeColor=#ffffff;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;whiteSpace=wrap;fontSize=10;fontFamily=Helvetica;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;" vertex="1" parent="cat_alb">
  <mxGeometry x="36" y="28" width="48" height="48" as="geometry" />
</mxCell>
<mxCell id="edge_alb_tasks_b" value="HTTP to targets, cross-AZ" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;fontFamily=Helvetica;fontSize=11;endArrow=block;exitX=0.5;exitY=1;entryX=0;entryY=0.5;" edge="1" parent="1" source="svc_alb" target="svc_tasks_b">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

The Region frame has `container=0`, so the VPC is parented to cell `1`. The edge ends on the task icon `svc_tasks_b`, not on its subnet.

## Validation

`diagram-validation-and-evidence`, structural checks:

- The XML parses with a namespace-aware parser, and `mxfile`, `diagram`, `mxGraphModel`, `root` and cells `0` and `1` are present.
- 41 cells have unique IDs, and every parent resolves.
- 14 edges have existing sources and targets, all of them icons.
- The payload is uncompressed, every AWS shape uses the `mxgraph.aws4` namespace, and Helvetica is used throughout.
- No defects.

Semantic check: every element traces to R1–R6, to one of the two answers, or to a recorded decision.

Visual check under `drawio-render-export-and-review`:

- Draw.io Desktop was found at `C:\Program Files\draw.io\draw.io.exe`, and the version it printed was recorded.
- A review PNG was exported to `%TEMP%\order-portal-review\`, outside the repository, and inspected at 100% and at 1280 px width.
- Two defects were found. The label "Amazon Aurora PostgreSQL-Compatible Edition" ran into the reader icon. The egress label overlapped the VPC border.
- Fixes: the label geometry was widened to 160 px with wrapping, and a waypoint moved the egress label 30 px clear of the border.
- After re-rendering, no defects remained.

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

- XML parse, root cells, unique IDs, parents, edges ending on icons, no compression, AWS4 namespace only, and Helvetica — structurally-validated.
- Icon names come from the installed Draw.io AWS4 sidebar; they were not compared with the current AWS-approved icon package — not-verified.

### visual_checks

- Draw.io Desktop render at scale 1, inspected at 100% and at 1280 px. Two defects were fixed and the re-render was clean — visually-validated.

### live_or_external_checks

- No AWS account, CLI or API was used. Service availability and pricing in eu-west-1 were not checked against current documentation — not-verified.

### unresolved_risks

- How long it takes to promote the Aurora reader, and how connections are handled during an AZ loss, are neither shown nor tested. R5 is satisfied by design, not proven resilient — not-verified.
- NAT data-processing cost grows with image-pull volume. Interface endpoints may be cheaper and tighter; the security review decides — designed.

### next_safe_action

- Send the file and the companion report to the security review. If the review adopts interface endpoints, the diagram needs updating, and changing it needs the user's go-ahead.
