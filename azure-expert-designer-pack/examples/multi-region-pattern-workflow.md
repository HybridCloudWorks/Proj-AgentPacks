# Worked example: active/active booking API across two regions

Prompt: `model-azure-architecture-pattern.prompt.md`. Skills: `azure-architecture-patterns`, `azure-architecture-design`, `drawio-layout-and-composition`, `azure-icons-and-visual-language`, `drawio-core-generation`, `drawio-xml-authoring`, `diagram-validation-and-evidence`, `drawio-render-export-and-review`.

Fictional scenario. Names, paths and tool output are illustrative.

## Request

> Produce an active-active multi-region architecture for the booking API: Front Door, App Service in two regions, Azure SQL. Make routing and replication clear. Regions are Sweden Central and North Europe.

## 1. Brief

| Field | Value |
|---|---|
| Task type | design |
| Pattern | multi-region |
| Audience | architecture board |
| Source of truth | the request; no infrastructure code |
| Output | `docs/architecture/booking-multi-region.drawio` with two pages, and a companion report |

## 2. The conflict the pattern check found

`azure-architecture-patterns` requires each tier to be labeled active/active or active/passive. The services chosen do not support one label for the whole design:

- **Web tier.** Front Door can send traffic to App Service in both regions at once, so this tier is active/active.
- **Data tier.** Azure SQL Database with geo-replication and a failover group has one writable primary. The secondary can serve reads only. This tier is active/passive for writes.

The agent did not draw the database as active/active, and did not swap in a different database. It drew what the chosen services do and recorded the conflict:

| Option | Effect |
|---|---|
| Keep Azure SQL; the web tier is active/active and the data tier is a single writer with a readable secondary | Writes from North Europe cross regions to the primary. Shown on the diagram. |
| Move to a database that supports multi-region writes | A different data model and consistency trade-off. Recorded as an open question for the board, not drawn. |

## 3. Model

All relationships are `designed`.

- Azure Front Door, with a WAF policy, is drawn outside both region frames. Both origins have priority 1. Health probes go to `/health`.
- Each region has its own resource group with an App Service plan, the App Service, a Key Vault and Application Insights. All of them send telemetry to one Log Analytics workspace in Sweden Central.
- Azure SQL logical servers exist in both regions. The failover group's read-write listener points to the primary in Sweden Central; the read-only listener points to the secondary in North Europe.
- Asynchronous geo-replication runs from Sweden Central to North Europe, one way only.
- Failover authority is two separate mechanisms. Front Door health probes decide web routing. The SQL failover group policy decides the database primary; whether that failover is automatic or manual is still undecided and is labeled so.

The diagram states in the legend: "Front Door routes HTTP only. It does not replicate data or move database traffic."

## 4. Layout and views

`drawio-layout-and-composition` and `azure-icons-and-visual-language`:

- Page "Runtime": Front Door at the top center, outside the regions. Two decorative region frames (`container=0`) side by side, each holding a resource group container. Data flows left to right within each region. Twelve primary services: 180 px and 120 px gaps, numbered badges 1 to 12, and a right-side legend.
- Edge styles: solid for synchronous HTTP and SQL calls; thick dashed blue for geo-replication, with the arrow pointing from Sweden Central to North Europe; dotted gray for health probes. The cross-region write path from the North Europe App Service to the read-write listener is labeled "cross-region write".
- Page "After database failover": the same layout, with the roles swapped and the replication arrow reversed. Splitting the failover state into its own page kept the runtime page readable, instead of shrinking it.
- Icons: `img/lib/azure2/networking/Front_Doors.svg`, `img/lib/azure2/app_services/App_Services.svg`, `img/lib/azure2/databases/SQL_Database.svg` and `img/lib/azure2/security/Key_Vaults.svg`, each 48 px with its product label.

## 5. Validation

The agent parsed the file after every write. Draw.io Desktop 24.7.17 rendered both pages:

```text
"C:\Program Files\draw.io\draw.io.exe" --export --all-pages --format pdf --output "%TEMP%\booking-review.pdf" docs\architecture\booking-multi-region.drawio
```

The first render showed the replication arrow overlapping the health-probe edge between the regions. The agent moved the probe edges above the region frames with waypoints. The second render was clean on both pages.

## Completion report

Pack: azure-expert-designer.

### scope_and_inputs

- Task type and outcome: pattern design. Two-page diagram and companion report written; the data tier conflict is recorded. `observed`
- Inputs: the request (Front Door, App Service in two regions, Azure SQL, Sweden Central and North Europe). `observed`

### source_facts

- The requester asked for active/active and named Front Door, App Service, Azure SQL and two regions. `observed`

### assumptions_and_design_decisions

- Web tier active/active behind Front Door, with both origins at priority 1 and probes on `/health`. `designed`
- Data tier drawn as a single writer with a readable geo-secondary, because that is how a failover group behaves. `designed`
- Sweden Central holds the initial primary. `designed`
- Failover policy (automatic or manual) is left undecided and labeled as such. `designed`
- Multi-region writes are an open question, not drawn. `designed`

### output_files

- `docs/architecture/booking-multi-region.drawio`: new, uncompressed, pages "Runtime" and "After database failover".
- `docs/architecture/booking-multi-region.md`: companion report with the pattern deviations and the open question.
- `%TEMP%\booking-review.pdf`: review render outside the repository.

### structural_checks

- XML parses; both pages have root cells; IDs are unique across pages; all references resolve; uncompressed; Azure2 image paths only. `structurally-validated`

### visual_checks

- Both pages rendered with Draw.io Desktop 24.7.17 and inspected. The overlap was fixed and the second render was clean. `visually-validated`

### live_or_external_checks

- No deployed environment exists. Service availability in both regions was not checked against current Azure documentation. `not-verified`

### unresolved_risks

- The requester expects active/active, but writes are single-region. The board must accept this or choose a different data tier.
- Cross-region write latency from North Europe has not been measured.
- The failover policy is undecided.

### next_safe_action

- The architecture board decides between a single-writer SQL data tier and a multi-region-write data tier. Update the data tier and the "After database failover" page to match.
