# Worked example: shipment-tracking workload design

Synthetic scenario. The company, names, address ranges and figures are illustrative. Prompt: `design-azure-workload.prompt.md`. Handoff formats: `templates/handoff/`.

## Request

Contoso Freight asks for a production Azure design for a customer shipment-tracking portal and a partner status API, with implementation handoff artifacts. Supplied inputs:

- Customers and partners are in the EU. Personal data (names, delivery addresses) is classified Confidential and must stay in the EU.
- Peak of 3,000 concurrent portal users and 150 partner API requests per second. Carrier status events arrive in bursts after each depot scan run.
- Monthly SLO of 99.9 % for the portal and API. RTO 4 hours, RPO 15 minutes.
- An existing ALZ-style platform: a connectivity hub in West Europe with Azure Firewall and centrally owned private DNS zones. It was supplied as a hierarchy export and a hub description, with no live access.
- Six .NET developers. The services are already containerized. Nobody has Kubernetes operations experience. CI/CD runs on GitHub Actions.
- Production run-rate ceiling of EUR 9,000 per month.

## 1. Foundations and boundaries

`azure-architecture-foundations` turned the inputs into REQ entries and surfaced three unknowns. They are recorded as open decisions, not filled with defaults:

| ID | Open decision | Why it matters | Owner |
|---|---|---|---|
| OD-01 | Customer identity provider | Changes the sign-in flow, where identity data lives, and the front end | Product owner |
| OD-02 | Partner API authentication: mutual TLS, OAuth client credentials, or keys behind a gateway | Decides whether an API gateway is needed | Integration lead |
| OD-03 | Retention period for proof-of-delivery images | Drives the storage lifecycle and cost | Data protection officer |

Boundary placement:

| Boundary | Placement | What it supplies | Label |
|---|---|---|---|
| Tenant | Contoso Entra tenant (single) | Identity, Conditional Access | observed (supplied) |
| Management group | `mg-landingzones-online` (public-facing workloads) | Inherited policy for internet-exposed workloads | observed (in the supplied export); placement designed |
| Subscriptions | `sub-tracking-prod` and `sub-tracking-nonprod`, vended by the platform team | Billing, quota, RBAC and blast-radius separation between production and non-production | designed |
| Resource groups | `rg-tracking-app-prod-weu`, `rg-tracking-data-prod-weu`, `rg-tracking-net-prod-weu` | Lifecycle: data and network outlive application releases | designed |
| Regions and zones | West Europe primary across three zones; North Europe for recovery | Residency and failure domains | designed; per-service zone support not-verified |
| Network | Spoke `vnet-tracking-prod-weu`, 10.42.0.0/22, peered to the hub | Private access and inspected egress | designed; block not yet confirmed with platform IPAM |

## 2. Evidence

The host exposed Microsoft Learn but no Azure MCP server, and the user authorized no live queries. Under `azure-docs-mcp-and-evidence` the framework pages were retrieved. The four service facts below are tier- and region-specific, so they were left for a focused pass with `verify-azure-evidence.prompt.md`; the ADRs that depend on them stay Proposed until then.

| ID | Claim | Source | Label | Used by |
|---|---|---|---|---|
| E-01 | Five-pillar review lens and trade-off framing | https://learn.microsoft.com/en-us/azure/well-architected/ | observed | Framework alignment |
| E-02 | Separate Online and Corp application landing zones | https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/ | observed | Placement |
| E-03 | Container Apps zone-redundancy prerequisites in West Europe | not retrieved | not-verified | ADR-001 |
| E-04 | Front Door Premium Private Link origin support for Container Apps in West Europe | not retrieved | not-verified | ADR-003 |
| E-05 | Service Bus tier required for private endpoints | not retrieved | not-verified | ADR-002 |
| E-06 | Azure SQL Database geo-replication RPO objective, and zone-redundant tier availability in West Europe | not retrieved | not-verified | ADR-002 |

## 3. Service selection

`azure-workload-and-service-selection` compared three hosting options:

| Criterion | App Service (Premium v3) | Container Apps | AKS |
|---|---|---|---|
| Runs the existing container images | Yes, as custom containers | Yes | Yes |
| Operations load for a team without Kubernetes skills | Low | Low | High: cluster upgrades, node pools, add-ons |
| Scaling the carrier-event worker on queue depth | Autoscale works per plan, not per queue | Scale rules per app, including queue-length triggers | Full control through KEDA, which the team would then operate |
| Private ingress and VNet integration | Private endpoint plus VNet integration | VNet-integrated environment with internal ingress | Full control |
| Zone redundancy | Plan-level setting | Environment-level setting (E-03) | Node pools across zones |

ADR-001 selects Container Apps. It runs the existing images, scales the worker on queue depth, and keeps the operations load within what six developers can own. AKS lost on operations load, since no requirement needs its control. App Service lost on per-queue scaling for the worker. Revisit trigger: a requirement for node-level control or custom networking that Container Apps cannot meet.

## 4. Data and application patterns

`azure-data-and-application-patterns` started from access patterns rather than a product list:

- **Shipments and status history.** Relational, with transactional updates and read-heavy portal queries. Azure SQL Database, zone-redundant in West Europe, with a failover group to North Europe for the recovery target (ADR-002). Geo-replication is asynchronous, so the 15-minute RPO stays not-verified until a failover drill measures data loss.
- **Carrier status events.** Bursty, delivered at least once. A Service Bus queue, `carrier-events`. The worker is idempotent on the carrier event ID, uses a bounded maximum delivery count, and alerts on dead-letter depth. Private access needs a tier that supports private endpoints (E-05).
- **Proof-of-delivery images.** Blob Storage with ZRS. The lifecycle rule's age threshold waits on OD-03.
- **No cache in the first release.** Add one only if the load test misses the p95 read-latency target in REQ; adding it now would be a speculative service.
- **Partner API.** Synchronous and read-only; partner writes arrive only as carrier events. Whether a gateway fronts it is OD-02.

## 5. Security and networking

From `azure-security-identity-and-compliance` and `azure-networking-hybrid-and-edge`:

- Managed identities from each container app to SQL (Entra authentication), Service Bus, Storage and Key Vault. No connection-string secrets.
- Private endpoints for SQL, Service Bus, Storage and Key Vault in `snet-pe`. DNS records go into the platform's central private DNS zones. That is observed in the supplied hub description; the registration mechanism belongs to the platform team and is recorded as dependency DEP-01.
- The only public entry is the Front Door endpoint, with a WAF policy that moves from detection to prevention mode after a tuning period. Public network access is disabled on SQL and Storage.
- Egress goes through the hub Azure Firewall via a route table on the app subnet.
- GitHub Actions authenticates with OIDC: a federated credential with subject `repo:contoso/tracking:environment:prod`, holding Contributor on the three production resource groups only. The platform team creates the role assignments; this design does not.

## 6. Framework alignment

`azure-well-architected-and-frameworks`:

| Pillar | Decision | Trade-off | Residual risk |
|---|---|---|---|
| Reliability | Zone-redundant app, SQL and storage; failover group to North Europe | Secondary database capacity costs money while idle | RTO and RPO unmeasured until a drill |
| Security | Managed identities, private endpoints, one public entry with WAF | More DNS and endpoint dependencies to operate | Depends on platform DNS registration (DEP-01) |
| Cost Optimization | Worker scales on demand; no speculative cache | Scale-from-zero adds latency to the first events after a quiet period | The Service Bus tier needed for private access may raise fixed cost |
| Operational Excellence | Application Insights per environment, platform diagnostics to the central workspace, alerts tied to SLOs, changes through IaC only | The team must own failover and dead-letter runbooks | Runbooks not yet written |
| Performance Efficiency | Queue-based load levelling for carrier bursts | Status updates become eventually consistent, within seconds | Load test not run |

## 7. Cost

Azure Pricing was not retrieved, so the design ranks cost drivers rather than quoting a figure. `CONSTRAINTS.json` records the EUR 9,000 ceiling with budget alerts at 80 % and 100 %. The largest expected drivers are SQL compute plus the geo-secondary, Front Door Premium, the Service Bus tier needed for private endpoints, Log Analytics ingestion, private endpoint hours, and the platform's chargeback for the firewall and hub. A priced estimate is the next step, with `estimate-azure-cost.prompt.md`.

## 8. Handoff

`azure-architecture-handoff-and-adr` wrote the four files to `handoff/tracking/` in the tracking repository. Excerpts:

`TOPOLOGY.json`:

```json
{
  "services": [
    {"id": "SVC-CAE", "type": "Microsoft.App/managedEnvironments", "resource_group": "RG-APP", "region": "REG-PRI", "zone_redundant": true, "public_access": false, "label": "designed", "evidence": ["E-03"]},
    {"id": "SVC-AFD", "type": "Microsoft.Cdn/profiles", "sku": "Premium_AzureFrontDoor", "label": "designed", "evidence": ["E-04"]}
  ],
  "flows": [
    {"id": "FLOW-01", "from": "EXT-CUSTOMERS", "to": "SVC-AFD", "protocol": "HTTPS", "port": 443, "label": "designed"},
    {"id": "FLOW-02", "from": "SVC-AFD", "to": "SVC-CAE", "protocol": "HTTPS", "port": 443, "via": "private-link", "label": "designed", "evidence": ["E-04"]}
  ]
}
```

`CONSTRAINTS.json`:

```json
{
  "regions": {"allowed": ["westeurope", "northeurope"], "data_residency": "EU", "label": "observed"},
  "budget": {"monthly_ceiling": 9000, "currency": "EUR", "alerts_percent": [80, 100], "owner": "Head of Digital", "label": "observed"},
  "approval_gates": [
    {"id": "GATE-01", "action": "first deployment to sub-tracking-prod", "approver": "platform change board", "evidence_required": ["what-if output for the exact commit", "role assignments in place"], "label": "designed"}
  ]
}
```

`ADR.md`:

```text
## ADR-001: Host the application services on Azure Container Apps

Status: Proposed. Decision owner: Contoso Freight lead architect. Implementation owner: tracking squad.
Context: REQ-NFR-03 (carrier event bursts), REQ-ORG-01 (no Kubernetes operations skills).
Alternatives: App Service Premium v3, AKS (comparison in section 3 of the design note).
Decision: one VNet-integrated, zone-redundant Container Apps environment with internal ingress,
hosting the portal, the partner API and the carrier-event worker.
Consequences: platform upgrades are Microsoft's; node-level tuning is not available.
Evidence: E-03 not-verified; acceptance waits on it.
Rollback and revisit: before go-live, swap to App Service with the same images; revisit if a
requirement needs node-level control.
```

Acceptance criteria in `REQ.md`:

| ID | Criterion | Verified by |
|---|---|---|
| AC-REL-01 | Portal and API meet 99.9 % monthly availability | SLO alert history after 30 days in production |
| AC-REL-02 | Region failover completes within 4 hours and loses at most 15 minutes of data | A recorded failover drill in non-production with production-sized data |
| AC-SEC-01 | No data service accepts public network traffic | Policy compliance state, plus a failed connection test from outside the VNet |
| AC-COST-01 | Production run rate stays below EUR 9,000 per month | Cost Management after the first full month |
| AC-PERF-01 | Portal p95 read latency under 400 ms at 3,000 concurrent users | Load test in non-production |
| AC-OPS-01 | Every alert links to a runbook | Alert rule review |
| AC-DEP-01 | Every change deploys through the pipeline with what-if output attached to the PR | Pipeline history |

The pack's handoff presence check, run from the pack folder:

```text
> pwsh -File hooks/architecture-review.ps1 -HandoffPath D:\repos\tracking\handoff\tracking
Architecture handoff contract present: D:\repos\tracking\handoff\tracking
This hook performs no Azure calls and makes no file changes.
```

That proves the four files exist. It says nothing about their content.

## Completion report

- Pack: azure-cloud-architect
- Workflow: `design-azure-workload.prompt.md`
- Outcome: design and handoff delivered with ADR-001 to ADR-003 Proposed; four service facts and every live check are not-verified; no Azure resource was created or changed.

### scope_and_inputs

Production design for the shipment-tracking portal and partner API in Contoso's EU estate, from the supplied requirements, hierarchy export and hub description. No live tenant access was granted and no deployment was requested.

### business_outcomes_and_requirements

Customer self-service tracking and a partner status API; 99.9 % SLO; RTO 4 h and RPO 15 min; EU residency; EUR 9,000 monthly ceiling [observed: supplied]. Open decisions OD-01 to OD-03 are in `REQ.md`.

### source_facts_and_evidence

E-01 and E-02 retrieved from Microsoft Learn [observed]. E-03 to E-06 not retrieved [not-verified]; each is attached to the ADR it gates. Hub and DNS facts come from the supplied description, not the live tenant [observed: supplied document only].

### framework_alignment

Five-pillar table in section 6. The main open trade-off is idle secondary SQL capacity against the RPO target. CAF placement: an application landing zone under the Online management group.

### proposed_architecture

Front Door Premium with WAF, over Private Link, to one Container Apps environment (portal, partner API, carrier-event worker) in a spoke peered to the West Europe hub; Azure SQL Database with a failover group to North Europe; a Service Bus queue; Blob Storage with ZRS; Key Vault; managed identities throughout [designed]. Details in `TOPOLOGY.json`.

### assumptions_and_tradeoffs

Assumed the platform team vends both subscriptions and registers private endpoint DNS records centrally (DEP-01). Container Apps over AKS for operations fit (ADR-001). SQL with a failover group over Cosmos DB because access is relational and transactional (ADR-002). A Private Link origin over a public origin with IP restrictions (ADR-003), falling back to Application Gateway in the spoke if E-04 fails.

### implementation_and_operating_implications

The IaC team implements from `TOPOLOGY.json` and `CONSTRAINTS.json`. The GitHub OIDC identity is scoped to three resource groups. What-if output is attached to every PR. Failover and dead-letter runbooks must exist before go-live (AC-OPS-01). GATE-01 governs the first production deployment.

### security_resilience_cost_and_sustainability

One public entry point and no secrets in configuration. Zone redundancy plus cross-region failover, with RTO and RPO unmeasured. Cost drivers ranked but not priced; this is not an estimate. Sustainability: the worker scales on demand, non-production SQL uses serverless with auto-pause, and non-production apps scale to zero outside working hours.

### output_files

| File | Purpose | Status and label |
|---|---|---|
| handoff/tracking/REQ.md | Requirements, acceptance criteria, open decisions | written [designed] |
| handoff/tracking/TOPOLOGY.json | Typed topology | written [designed] |
| handoff/tracking/CONSTRAINTS.json | Constraints and approval gates | written [designed] |
| handoff/tracking/ADR.md | ADR-001 to ADR-003, all Proposed | written [designed] |

Handoff presence check passed [structurally-validated]. Content was not machine-validated beyond JSON parsing.

### live_or_external_checks

None run. Zone support, Private Link origin support, the Service Bus tier, the SQL geo-replication objective, quota in both regions, and address-space availability are all [not-verified]: no live access was authorized and the service documentation was not retrieved in this session.

### unresolved_risks

ADR-003 may need the Application Gateway fallback (E-04). The RPO target is unproven. OD-01 could change the front end. The design depends on platform DNS registration (DEP-01).

### next_safe_action

Run the evidence pass for E-03 to E-06 and a priced estimate, then ask the lead architect to accept or amend ADR-001 to ADR-003. No deployment until GATE-01 is satisfied.
