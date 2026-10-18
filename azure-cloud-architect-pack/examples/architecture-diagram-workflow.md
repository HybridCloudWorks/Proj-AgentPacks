# Worked example: diagram from an approved topology, visual review not run

Synthetic scenario that continues `greenfield-workload-design.md`. Prompt: `create-azure-architecture-diagram.prompt.md`. This example ends **unverified**: the diagram is structurally valid, but it was never rendered.

## Request

"Draw the approved tracking architecture for Thursday's change board, as a Draw.io file plus a PNG."

Inputs: `handoff/tracking/TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`, after the evidence pass confirmed E-03 to E-06 and the lead architect accepted ADR-001 to ADR-003. Audience: the change board and the IaC squad. Output: `docs/architecture/tracking-workload.drawio` in the tracking repository, with a PNG beside it.

## 1. What the diagram must say

From `azure-architecture-visualization`, two pages:

- **Workload and network**: tenant, subscription and resource group containers; the West Europe region with a zone note; the spoke VNet and its subnets; private endpoints; Front Door as the only public entry; hub peering and egress through the firewall; flows FLOW-01 to FLOW-07.
- **Recovery**: the North Europe secondary database, the failover group link, and recovery path REC-01.

The requester also asked for a Redis icon "since we will probably need it". It is not in `TOPOLOGY.json` and no ADR supports it; the design deferred any cache to a load-test result. It stays off the diagram, because a drawn component reads as a decided one.

Routing: the Azure Expert Designer was not installed in this host. The agent used this pack's `drawio-core-generation`, `drawio-render-export-and-review` and `diagram-validation-and-evidence` Skills, and says so in the report.

## 2. Generate

Following `drawio-core-generation`: native XML rather than Mermaid, because the views need custom boundaries and Azure2 icons. Cell IDs reuse topology IDs, so a reviewer can trace and diff them. Excerpt:

```xml
<mxCell id="RG-DATA" value="rg-tracking-data-prod-weu" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;fillColor=none;verticalAlign=top;align=left;" vertex="1" parent="SUB-PROD">
  <mxGeometry x="620" y="80" width="300" height="220" as="geometry"/>
</mxCell>
<mxCell id="SVC-SQL" value="Azure SQL Database&lt;br&gt;zone redundant" style="image;aspect=fixed;html=1;image=img/lib/azure2/databases/SQL_Database.svg;verticalLabelPosition=bottom;verticalAlign=top;align=center;" vertex="1" parent="RG-DATA">
  <mxGeometry x="40" y="60" width="48" height="64" as="geometry"/>
</mxCell>
<mxCell id="FLOW-05" value="TDS 1433 via private endpoint" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;" edge="1" parent="1" source="SVC-CAE" target="PE-SQL">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## 3. Structural check

From `diagram-validation-and-evidence`, using the pack's helper from the pack folder:

```text
> python tooling/validate_drawio_xml.py D:\repos\tracking\docs\architecture\tracking-workload.drawio
PASS: D:\repos\tracking\docs\architecture\tracking-workload.drawio
```

The helper checks the root structure, unique IDs, parent, source and target references, Azure2 image paths, legacy Azure shape syntax, and compression. A pass is [structurally-validated]. It says nothing about how the diagram looks.

## 4. Semantic reconciliation

| Topology element | Diagram cell | Result | Label |
|---|---|---|---|
| SVC-AFD, Front Door Premium | SVC-AFD | Outside every VNet, labelled as the only public entry | designed |
| FLOW-02, Front Door to Container Apps over Private Link | FLOW-02 | Dashed line labelled "Private Link" | designed |
| PE-SQL in snet-pe | PE-SQL | Inside snet-pe | designed |
| Central private DNS zone | DNS-CENTRAL | Inside the connectivity subscription container, not the spoke | designed |
| REC-01, failover group to North Europe | Page 2, REC-01 | Dotted replication line between regions | designed |
| Zone redundancy | Region container label: "3 zones; ZR = zone-redundant service" | No per-zone boxes. These are zone-redundant platform services, and per-zone boxes would imply instances the design does not place | designed |
| Firewall rule set | Not drawn | Out of scope for this view; noted in the legend | designed |

The legend defines line styles (solid for request flow, dashed for Private Link, dotted for replication), the ZR marker, and the boundary styles for subscription, resource group and VNet.

## 5. Render and visual review

From `drawio-render-export-and-review`, the agent looked for Draw.io Desktop at `C:\Program Files\draw.io\draw.io.exe`, in the user installation directory under `%LOCALAPPDATA%\Programs\draw.io\`, and on PATH. It found none. Export and visual review were not run, and no PNG exists. Spacing, clipping, label legibility, icon scale and edge routing are therefore unreviewed.

## Completion report

- Pack: azure-cloud-architect
- Workflow: `create-azure-architecture-diagram.prompt.md`
- Outcome: **unverified**. An editable two-page diagram is written and structurally validated, and it reconciles with the topology. It was never rendered: there is no PNG and no visual review, because Draw.io Desktop is not installed.

### scope_and_inputs

Diagram of the accepted tracking design for the change board. Inputs: the four handoff files. Requested outputs: a `.drawio` file and a PNG. No live tenant snapshot was requested or taken.

### business_outcomes_and_requirements

A change-board view that shows boundaries, the single public entry, private data paths and the recovery path, matching ADR-001 to ADR-003.

### source_facts_and_evidence

Every component and flow comes from `TOPOLOGY.json` [designed]. The Azure2 image path follows the library convention the helper accepts [structurally-validated]. That the icon renders correctly in the installed Draw.io version is [not-verified].

### framework_alignment

Not reassessed. The diagram reflects the accepted design and adds no decisions.

### proposed_architecture

None new. Two views of the existing design.

### assumptions_and_tradeoffs

Two pages rather than one, to keep the recovery path readable. Zone redundancy is shown as a label rather than per-zone boxes. The Redis request was declined because no decision supports it.

### implementation_and_operating_implications

The `.drawio` file lives in the tracking repository and changes with `TOPOLOGY.json`. Cell IDs match topology IDs so drift is visible in review.

### security_resilience_cost_and_sustainability

The diagram shows trust boundaries and the recovery path. It is not evidence that the live topology matches.

### output_files

| File | Purpose | Status and label |
|---|---|---|
| docs/architecture/tracking-workload.drawio | Editable two-page diagram | written [structurally-validated] |
| docs/architecture/tracking-workload.png | Requested export | not produced [not-verified] |
| handoff/tracking/REQ.md, TOPOLOGY.json, CONSTRAINTS.json, ADR.md | Source of the diagram | unchanged |

### live_or_external_checks

| Check | Tool | Result | Label |
|---|---|---|---|
| Draw.io XML structure | `tooling/validate_drawio_xml.py` | PASS | structurally-validated |
| Semantic reconciliation | Table in section 4 | All elements in scope matched | designed |
| Render and export | Draw.io Desktop | Not run: executable not found | not-verified |
| Visual review | Rendered output | Not run: nothing rendered | not-verified |
| Live topology comparison | None | Not requested | not-verified |

### unresolved_risks

Layout defects such as clipped labels or crossing edges may exist and are invisible to the structural check. The change board meets Thursday.

### next_safe_action

Install Draw.io Desktop, or open the file on a machine that has it; export the PNG and review it at presentation size before Thursday. If that cannot happen in time, tell the board the diagram has had no visual review.
