# Worked example: claims intake web app from requirements

Prompt: `design-diagram-from-requirements.prompt.md`. Skills: `azure-architecture-design`, `azure-architecture-patterns`, `drawio-core-generation`, `azure-icons-and-visual-language`, `drawio-layout-and-composition`, `drawio-xml-authoring`, `diagram-validation-and-evidence`, `drawio-render-export-and-review`.

Fictional scenario. Names, paths and tool output are illustrative.

## Request

> Draw the Azure architecture for the new claims intake app. Staff upload scanned forms through a web front end; the app stores the files and writes a claim record. Nothing except the front end should be reachable from the internet. Put it in `docs/architecture/`.

## 1. Brief

| Field | Value |
|---|---|
| Task type | design |
| Purpose | design review before any infrastructure code is written |
| Audience | platform team and the security reviewer |
| Scope | one workload, production, one region |
| Source of truth | the requirements note above; no infrastructure code exists yet |
| Fidelity | logical, with network boundaries |
| Output | `docs/architecture/claims-intake.drawio` and `docs/architecture/claims-intake.md` (companion report) |

## 2. Questions asked

The agent asked three questions, each of which changes the architecture. It did not ask about SKUs or naming, which would not change the diagram.

| Question | Answer | Changes |
|---|---|---|
| Do staff connect from the internet or only from the corporate network? | Internet, signing in with Microsoft Entra ID | Public ingress with a web application firewall is needed; Entra ID sits at tenant scope |
| What availability is required? | One region; zone redundancy is acceptable | No second region; zone redundancy is a note, not drawn zones |
| What data do the forms contain? | Personal data | Data stores get private endpoints and public network access disabled |

The region was not chosen. The agent did not invent one: the region frame reads "Primary region (not yet chosen)".

## 3. Model

`azure-architecture-design` produced this minimal model. Every relationship is `designed`, because no source exists yet. The optional observability layer was offered and accepted; a governance layer was offered and declined for this view.

- Application Gateway with WAF in its own subnet is the only public entry point.
- App Service hosts the app. Inbound traffic reaches it through a private endpoint, with public access disabled. Outbound traffic leaves through VNet integration in an integration subnet.
- Azure SQL Database, a Storage account (blob) and Key Vault each have a private endpoint in a private-endpoint subnet. App Service reaches them with its managed identity.
- A private DNS zone for each of the four private endpoints is linked to the VNet. The links are drawn as configuration for name resolution, not as traffic.
- Application Insights and a Log Analytics workspace receive telemetry.

`azure-architecture-patterns` matched the serverless-web and VNet-with-private-endpoint checks. One deviation is recorded: App Service is not drawn inside a subnet, because only its private endpoint NIC and its integration attachment live in subnets.

## 4. Generation path and icons

`drawio-core-generation` chose native XML, because Azure icons, nested boundaries and exact routing matter. Mermaid was not used.

`azure-icons-and-visual-language` copied each icon's style from draw.io's Azure palette (library ID `azure2`) and checked the path against the `diagram-validation-and-evidence` icon catalog:

| Component | Icon |
|---|---|
| Application Gateway | `img/lib/azure2/networking/Application_Gateways.svg` |
| App Service | `img/lib/azure2/app_services/App_Services.svg` |
| Azure SQL Database | `img/lib/azure2/databases/SQL_Database.svg` |
| Storage account | `img/lib/azure2/storage/Storage_Accounts.svg` |
| Key Vault | `img/lib/azure2/security/Key_Vaults.svg` |
| Private endpoints (four) | `img/lib/azure2/other/Private_Endpoints.svg` |
| Private DNS zones (four) | `img/lib/azure2/networking/DNS_Zones.svg`, each labelled "Private DNS zone" with its zone name, because Microsoft's icon set has no separate private DNS zone icon |
| Application Insights | `img/lib/azure2/devops/Application_Insights.svg` |
| Log Analytics workspace | `img/lib/azure2/analytics/Log_Analytics_Workspaces.svg` |
| Microsoft Entra ID | the file the shared `drawio-core-generation` provider reference names for Entra ID |
| Subscription, resource group, VNet, subnets | `general/Subscriptions.svg`, `general/Resource_Groups.svg`, `networking/Virtual_Networks.svg`, `networking/Subnet.svg`, 24 px in each frame's top-left corner, labelled with the frame's name |

Each style is the palette's own, as `check_drawio.py --find "<product>"` printed it, `image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/...;`, followed only by `fontFamily=Helvetica`; the palette's connection points were not needed, because they do not change how an icon draws. Service icons are 48 px on their longest side with the aspect fixed, so SQL Database is 36 by 48, and the product name sits beneath each icon. Staff are drawn as a neutral actor outside the subscription. Entra ID is drawn above the subscription with the label "Microsoft Entra ID (tenant scope)".

## 5. Layout and XML

`drawio-layout-and-composition` produced:

- Left-to-right flow: staff → Application Gateway → App Service → data services. Telemetry runs in a lower row.
- Ten primary services, so 180 px horizontal and 120 px vertical gaps, with 28 px numbered badges 1 to 10 and a right-side legend.
- Real containers for the subscription, resource group, VNet and three subnets; every resource in this design is in the one resource group, so the resource group frame can parent them. The region is a decorative frame with `container=0` and no child cells. Zone redundancy is a legend note, not zone frames.
- App Service sits outside the VNet. Its inbound private endpoint NIC is in the private-endpoint subnet, and an outbound edge labelled "regional VNet integration" runs from App Service into the delegated integration subnet.
- Solid edges for synchronous calls, dashed edges for telemetry, and dotted gray edges for the DNS zone VNet links. Every edge carries a label.

`drawio-xml-authoring` gave every cell a semantic ID, such as `snet_private_endpoints`, `pe_sql`, `edge_app_sql` and `dnszone_sql_link`.

## 6. Validation and first-render fixes

After each write the agent ran the `diagram-validation-and-evidence` checker from that skill's folder:

```text
> python scripts/check_drawio.py --strict docs\architecture\claims-intake.drawio
file: docs\architecture\claims-intake.drawio
pages: 1 (Runtime view)
cells: 72 vertices, 17 edges
catalog: draw.io 32.6.9, built 2026-11-01
icons Azure: current 22
errors: 0
warnings: 0
result: PASS
```

It checks the page layout, root cells, unique IDs, parents, edge references, geometry, compression and every Azure icon path against the catalog. The agent read the XML for what the checker does not cover: Helvetica throughout, container styles, no cell parented to the decorative region frame, and a label on every edge.

`drawio-render-export-and-review` found no installer copy at `C:\Program Files\draw.io\draw.io.exe` and found the Microsoft Store build through `Get-AppxPackage`. It exported a review copy outside the repository, with `-k` and without `--layout` or `--normalize`:

```text
PS> $drawio = Join-Path (Get-AppxPackage *draw.io*).InstallLocation 'app\draw.io.exe'
PS> & $drawio --version
32.6.1
PS> & $drawio -x -k -f png -s 1 -b 20 -o "$env:TEMP\claims-intake-review.png" docs\architecture\claims-intake.drawio
```

Every Azure icon drew; none showed a broken-image placeholder. The first render showed three defects, all fixed in the source:

1. The label "TDS 1433" on the edge from the integration subnet to the SQL private endpoint sat on the subnet border, because draw.io places an edge label at the midpoint of the whole bent edge. The agent moved it along the edge with the label geometry's relative `x`, so it sits inside the integration subnet.
2. The edge from Application Gateway to the App Service private endpoint entered from the top. The agent set exit and entry points so it enters from the left.
3. The DNS VNet-link edge crossed the Storage label. The agent added a waypoint 20 px below the label.

The second render was clean at 100% and at 1280 px slide width. The agent then ran the checker again on the final file, with the same result.

## Completion report

Pack: azure-expert-designer.

### scope_and_inputs

- Task type and outcome: design; diagram and companion report written. `observed`
- Request: claims intake architecture for design review by the platform team and security reviewer. `observed`
- Inputs: the requirements note and three answers from the requester. There is no infrastructure source. `observed`

### source_facts

- Staff connect from the internet and sign in with Entra ID. `observed`
- Single region; zone redundancy acceptable. `observed`
- Forms contain personal data. `observed`

### assumptions_and_design_decisions

- Application Gateway with WAF is the only public ingress; App Service public access is disabled. `designed`
- SQL, Storage and Key Vault use private endpoints, with private DNS zones linked to the VNet. `designed`
- App Service reaches data services with its managed identity. `designed`
- The region is not chosen and is labeled as such on the diagram. `designed`
- Zone redundancy is recorded in the legend notes but not drawn, because no zone placement exists yet. `designed`

### output_files

- `docs/architecture/claims-intake.drawio`: new, uncompressed, one page.
- `docs/architecture/claims-intake.md`: companion report with the brief, evidence matrix, boundary semantics and open questions.
- `%TEMP%\claims-intake-review.png`: review render outside the repository; not a deliverable.

### structural_checks

- `check_drawio.py --strict` from `diagram-validation-and-evidence`, catalog draw.io 32.6.9: PASS with 0 errors and 0 warnings, after the last edit. Cells `0` and `1` present; 89 cells with unique IDs; every parent, source and target resolves; uncompressed; 22 Azure icons, all current. `structurally-validated`
- Read from the XML: Helvetica throughout, no cell parented to the decorative region frame, and every edge labelled. `structurally-validated`

### visual_checks

- Rendered with Draw.io Desktop 32.6.1 (Microsoft Store build) and inspected at 100% and 1280 px width. Every Azure icon drew. Three defects were fixed, and the second render was clean. `visually-validated`

### live_or_external_checks

- No Azure environment exists for this design. `not-verified`
- Icon paths were checked against the shared catalog (draw.io 32.6.9) and drew in the local 32.6.1 render. They were not compared with Microsoft's current icon download. `not-verified`

### unresolved_risks

- The region choice may change service availability and private DNS zone names for some services.
- Zone redundancy support depends on the SKUs chosen later.

### next_safe_action

- The security reviewer reviews `claims-intake.drawio` with its companion report. Once the region is chosen, update the region frame and recheck service availability.
