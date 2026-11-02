# Worked example: diagram from an approved topology, visual review not run

Synthetic scenario that continues `greenfield-workload-design.md`. Prompt: `create-azure-architecture-diagram.prompt.md`. This example ends **unverified**: the diagram passes the shared checker, but it was never rendered.

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

Following `drawio-core-generation`: native XML rather than Mermaid, because the views need custom boundaries and Azure icons from draw.io's library (ID `azure2`). Cell IDs reuse topology IDs, so a reviewer can trace and diff them. Each icon style is copied from the draw.io palette unchanged, 48 px on its longest side with the aspect fixed, so SQL Database is 36 by 48. Excerpt:

```xml
<mxCell id="RG-DATA" value="" style="rounded=0;html=1;container=1;collapsible=0;recursiveResize=0;fillColor=#F5F5F5;strokeColor=#7A7A7A;fontFamily=Helvetica;" vertex="1" parent="SUB-PROD">
  <mxGeometry x="620" y="80" width="300" height="220" as="geometry"/>
</mxCell>
<mxCell id="RG-DATA-ICON" value="Resource group: rg-tracking-data-prod-weu" style="image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/general/Resource_Groups.svg;points=[[0.5,0,0],[0.5,1,0],[0,0.5,0],[1,0.5,0],[0.995,0.109,0],[0.997,0.888,0],[0.003,0.888,0],[0.003,0.112,0]];fontFamily=Helvetica;labelPosition=right;verticalLabelPosition=middle;align=left;verticalAlign=middle;spacingLeft=6;fontStyle=1;" vertex="1" parent="RG-DATA">
  <mxGeometry x="12" y="10" width="24" height="22.59" as="geometry"/>
</mxCell>
<mxCell id="SVC-SQL" value="Azure SQL Database&lt;br&gt;zone redundant: zones 1, 2, 3" style="image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/databases/SQL_Database.svg;points=[[0.5,0.003,0],[0.502,0.998,0],[0,0.499,0],[1,0.499,0],[0.976,0.093,0],[0.983,0.9,0],[0.017,0.9,0],[0.014,0.103,0]];fontFamily=Helvetica;" vertex="1" parent="RG-DATA">
  <mxGeometry x="40" y="60" width="36" height="48" as="geometry"/>
</mxCell>
<mxCell id="FLOW-05" value="TDS 1433 via private endpoint" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="SVC-CAE" target="PE-SQL">
  <mxGeometry x="-0.4" relative="1" as="geometry"/>
</mxCell>
```

## 3. Structural check

From `diagram-validation-and-evidence`, using that skill's checker from the skill's folder:

```text
> python scripts/check_drawio.py --strict D:\repos\tracking\docs\architecture\tracking-workload.drawio
file: D:\repos\tracking\docs\architecture\tracking-workload.drawio
pages: 2 (Workload and network, Recovery)
cells: 96 vertices, 19 edges
catalog: draw.io 32.5.5, built 2026-10-18
icons Azure: current 23
errors: 0
warnings: 0
result: PASS
```

The checker validates each page on its own (both pages repeat root cells `0` and `1`), the parent, source and target references, geometry and compression, and looks up every Azure icon path in its catalog of draw.io's libraries: all 23 are current, and `--strict` would have failed any legacy `mxgraph.azure.*` or `mxgraph.mscae.*` shape. A pass is [structurally-validated]. It says nothing about how the diagram looks, and a current path is not proof that the icon draws.

## 4. Semantic reconciliation

| Topology element | Diagram cell | Result | Label |
|---|---|---|---|
| SVC-AFD, Front Door Premium | SVC-AFD | Outside every VNet, labelled as the only public entry | designed |
| FLOW-02, Front Door to Container Apps over Private Link | FLOW-02 | Dashed line labelled "Private Link" | designed |
| PE-SQL in snet-pe | PE-SQL | Inside snet-pe | designed |
| Central private DNS zone | DNS-CENTRAL | Inside the connectivity subscription container, not the spoke | designed |
| REC-01, failover group to North Europe | Page 2, REC-01 | Dotted replication line between regions | designed |
| Zone redundancy | Region frame label "3 zones; ZR = zone-redundant service", and each zone-redundant service labelled with its zones | No zone frames. These are zone-redundant platform services, subnets span all zones, and zone frames would imply instances the design does not place | designed |
| Firewall rule set | Not drawn | Out of scope for this view; noted in the legend | designed |

The legend defines line styles (solid for request flow, dashed for Private Link, dotted for replication), the ZR marker, and the boundary styles for subscription, resource group and VNet.

## 5. Render and visual review

From `drawio-render-export-and-review`, the agent looked for Draw.io Desktop on PATH, at `C:\Program Files\draw.io\draw.io.exe`, in the user installation directory under `%LOCALAPPDATA%\Programs\draw.io\`, and for the Microsoft Store build with `Get-AppxPackage *draw.io*` (whose executable would be `app\draw.io.exe` inside the reported InstallLocation). All four came back empty. Export and visual review were not run, and no PNG exists. Spacing, clipping, label legibility, icon scale, edge routing and whether every icon draws are therefore unreviewed.

## Completion report

- Pack: azure-cloud-architect
- Workflow: `create-azure-architecture-diagram.prompt.md`
- Outcome: **unverified**. An editable two-page diagram is written and structurally validated, and it reconciles with the topology. It was never rendered: there is no PNG and no visual review, because Draw.io Desktop is not installed.

### scope_and_inputs

Diagram of the accepted tracking design for the change board. Inputs: the four handoff files. Requested outputs: a `.drawio` file and a PNG. No live tenant snapshot was requested or taken.

### business_outcomes_and_requirements

A change-board view that shows boundaries, the single public entry, private data paths and the recovery path, matching ADR-001 to ADR-003.

### source_facts_and_evidence

Every component and flow comes from `TOPOLOGY.json` [designed]. Every Azure icon path is current in the shared checker's catalog, draw.io 32.5.5 [structurally-validated]. That each icon renders correctly in a Draw.io build is [not-verified].

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
| Draw.io XML structure and icon currency | `diagram-validation-and-evidence` `scripts/check_drawio.py --strict`, catalog draw.io 32.5.5 | PASS: 0 errors, 0 warnings, 23 Azure icons current | structurally-validated |
| Semantic reconciliation | Table in section 4 | All elements in scope matched | designed |
| Render and export | Draw.io Desktop | Not run: not found on PATH, at the installer or per-user location, or as a Microsoft Store build | not-verified |
| Visual review | Rendered output | Not run: nothing rendered | not-verified |
| Live topology comparison | None | Not requested | not-verified |

### unresolved_risks

Layout defects such as clipped labels or crossing edges may exist and are invisible to the structural check. The change board meets Thursday.

### next_safe_action

Install Draw.io Desktop, or open the file on a machine that has it; export the PNG with `-x -k -f png` and without `--layout` or `--normalize`, review it at presentation size before Thursday, confirm every Azure icon drew, and run `check_drawio.py --strict` again after any fix. If that cannot happen in time, tell the board the diagram has had no visual review.
