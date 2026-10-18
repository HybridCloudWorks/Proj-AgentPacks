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
- Private DNS zones for each private endpoint are linked to the VNet. They are drawn as resolution, not traffic.
- Application Insights and a Log Analytics workspace receive telemetry.

`azure-architecture-patterns` matched the serverless-web and VNet-with-private-endpoint checks. One deviation is recorded: App Service is not drawn inside a subnet, because only its private endpoint NIC and its integration attachment live in subnets.

## 4. Generation path and icons

`drawio-core-generation` chose native XML, because Azure2 icons, nested boundaries and exact routing matter. Mermaid was not used.

`azure-icons-and-visual-language` checked each icon against the Azure2 library shipped with the detected Draw.io build:

| Component | Icon |
|---|---|
| Application Gateway | `img/lib/azure2/networking/Application_Gateways.svg` |
| App Service | `img/lib/azure2/app_services/App_Services.svg` |
| Azure SQL Database | `img/lib/azure2/databases/SQL_Database.svg` |
| Storage account | `img/lib/azure2/storage/Storage_Accounts.svg` |
| Key Vault | `img/lib/azure2/security/Key_Vaults.svg` |
| Private DNS zones | neutral labeled shape: no exact icon was found in that build's library, so none was guessed |

Each icon is 48 px with the product name beneath it. Staff are drawn as a neutral actor outside the subscription. Entra ID is drawn above the subscription with the label "Microsoft Entra ID (tenant scope)".

## 5. Layout and XML

`drawio-layout-and-composition` produced:

- Left-to-right flow: staff → Application Gateway → App Service → data services. Telemetry runs in a lower row.
- Ten primary services, so 180 px horizontal and 120 px vertical gaps, with 28 px numbered badges 1 to 10 and a right-side legend.
- Real containers for the subscription, resource group, VNet and three subnets. The region is a decorative frame with `container=0`.
- Solid edges for synchronous calls, dashed edges for telemetry, and dotted gray edges for the DNS zone VNet links.

`drawio-xml-authoring` gave every cell a semantic ID, such as `snet_private_endpoints`, `pe_sql`, `edge_app_sql` and `dnszone_sql_link`.

## 6. Validation and first-render fixes

The agent parsed the file after each write and checked root cells, unique IDs, parents, edge references, Azure2 image paths, Helvetica font, container styles and the absence of compressed content. These are the same checks the pack's `tooling/validate_drawio_xml.py` helper runs.

`drawio-render-export-and-review` detected `C:\Program Files\draw.io\draw.io.exe`, version 24.7.17. The agent exported a review copy outside the repository:

```text
"C:\Program Files\draw.io\draw.io.exe" --export --format png --scale 1 --border 20 --output "%TEMP%\claims-intake-review.png" docs\architecture\claims-intake.drawio
```

The first render showed three defects, all fixed in the source:

1. The label "Private endpoint (SQL)" was clipped in its tile. The agent let it wrap onto two lines and widened the label area.
2. The edge from Application Gateway to the App Service private endpoint entered from the top. The agent set exit and entry points so it enters from the left.
3. The DNS VNet-link edge crossed the Storage label. The agent added a waypoint 20 px below the label.

The second render was clean at 100% and at 1280 px slide width.

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

- XML parses; cells `0` and `1` present; 58 cells with unique IDs; every parent, source and target resolves. `structurally-validated`
- Uncompressed; all image paths are under `img/lib/azure2/`; no legacy `mxgraph.azure` shapes; Helvetica throughout. `structurally-validated`

### visual_checks

- Rendered with Draw.io Desktop 24.7.17 and inspected at 100% and 1280 px width. Three defects were fixed, and the second render was clean. `visually-validated`

### live_or_external_checks

- No Azure environment exists for this design. `not-verified`
- Icon file names were checked against the local Draw.io build's library, not against Microsoft's current icon download. `not-verified`

### unresolved_risks

- The region choice may change service availability and private DNS zone names for some services.
- Zone redundancy support depends on the SKUs chosen later.

### next_safe_action

- The security reviewer reviews `claims-intake.drawio` with its companion report. Once the region is chosen, update the region frame and recheck service availability.
