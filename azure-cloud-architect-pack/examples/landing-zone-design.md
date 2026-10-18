# Worked example: landing-zone audit and target design

Synthetic scenario. The organization, counts and names are illustrative. Prompt: `design-azure-landing-zone.prompt.md`.

## Request

Fabrikam Health, a regional healthcare provider in the United States, asks for an audit of its Azure estate and a CAF-aligned target landing-zone design. Its own operator produced read-only exports on 2026-10-14 and supplied them:

- `mg.json` from `az account management-group show --name "$TENANT_ID" --expand --recurse`
- `subs.json` from `az account list --all`
- `policy-assignments.csv`: policy assignments per subscription
- `vnets.csv`: a Resource Graph export of VNets, address spaces and peerings

Other inputs: HIPAA obligations; allowed regions East US 2 and Central US; three hospitals connected today by site-to-site VPN; an ExpressRoute circuit being procured. No live access was granted.

## 1. Current state

`azure-architecture-foundations` kept the observed state apart from the target. Findings, all as of the export date:

| ID | Finding | Evidence | Label |
|---|---|---|---|
| CS-01 | All 41 subscriptions sit directly under the tenant root group | `mg.json` | observed |
| CS-02 | 27 policy assignments, all at subscription scope, with five different allowed-locations lists | `policy-assignments.csv` | observed |
| CS-03 | Three subscriptions appear to host domain controllers next to clinical workloads | Subscription names and VNet DNS settings point at in-VNet DNS servers; no resource inventory supplied | inferred |
| CS-04 | Six VNets use 10.0.0.0/16, so they cannot all peer to one hub without re-addressing | `vnets.csv` | observed |
| CS-05 | Standing Owner assignments and PIM usage are unknown | No role-assignment export supplied | not-verified |

## 2. Target hierarchy

`azure-caf-landing-zones-and-governance` produced a deliberately flat hierarchy that separates the platform from application landing zones:

```text
Tenant root group
└── mg-fabrikam               intermediate root: tenant-wide policy and RBAC
    ├── mg-platform
    │   ├── mg-identity       sub-identity-prod
    │   ├── mg-management     sub-management-prod
    │   └── mg-connectivity   sub-connectivity-prod
    ├── mg-landingzones
    │   ├── mg-corp           internal clinical and business workloads
    │   └── mg-online         patient-facing workloads
    ├── mg-sandbox            time-boxed experiments, no hybrid connectivity
    └── mg-decommissioned     subscriptions awaiting closure
```

There are no per-department or per-environment management groups. Environments differ by subscription and policy parameters, not by hierarchy depth (ADR-LZ-001). Revisit trigger: a regulatory boundary that needs a different policy set from every existing group.

## 3. Placement matrix

The placement questions answered for representative components:

| Component | Management group | Subscription | Resource group | Region | Owner | Boundary reason |
|---|---|---|---|---|---|---|
| Hub VNet, Azure Firewall, VPN and ExpressRoute gateways | mg-connectivity | sub-connectivity-prod | rg-hub-eus2, rg-hub-cus | Both | Network team | Shared, inspected routing; RBAC kept apart from workloads |
| Private DNS zones for private endpoints | mg-connectivity | sub-connectivity-prod | rg-dns-global | Global resource | Network team | One resolution authority for private endpoints |
| Domain controllers | mg-identity | sub-identity-prod | rg-adds-eus2, rg-adds-cus | Both | Identity team | Tier-0 isolation from workloads (CS-03) |
| Central Log Analytics workspace | mg-management | sub-management-prod | rg-monitor-eus2 | East US 2 | Cloud operations | Retention and access control in one place |
| EHR integration engine | mg-corp | sub-ehr-int-prod | rg-ehr-int-app-eus2 | East US 2 | Clinical applications | Workload lifecycle; its spoke stays with it |
| Patient portal | mg-online | sub-portal-prod | rg-portal-app-eus2 | East US 2 | Digital team | Public exposure governed apart from Corp |

## 4. Governance

Policy, assigned at the shallowest group where it applies:

| ID | Scope | Intent | Effect and rollout |
|---|---|---|---|
| POL-01 | mg-fabrikam | Allowed locations: eastus2, centralus, with global resources excepted | Audit for 30 days, then Deny |
| POL-02 | mg-fabrikam | Required tags: owner, cost-center, environment, data-classification | Audit, then Deny on resource groups; Modify to inherit tags on resources |
| POL-03 | mg-landingzones | Diagnostic settings to the central workspace | DeployIfNotExists; the platform team runs remediation tasks |
| POL-04 | mg-corp | No public IP addresses and no public network access on PaaS | Audit first; each exemption has an owner and an expiry |
| POL-05 | mg-landingzones | Workloads may not create private DNS zones; endpoint records go to the central zones | Deny, paired with DeployIfNotExists for record registration |
| POL-06 | mg-fabrikam | Regulatory compliance initiative for HIPAA reporting | Audit only. Compliance state is input to an assessment, not a compliance claim |

Identity and access, from `azure-security-identity-and-compliance`:

- No standing Owner for people at mg-fabrikam or below. Platform roles are eligible through PIM, with approval and quarterly access reviews.
- Two break-glass accounts, excluded from the Conditional Access policies that could lock them out, with an alert on any sign-in.
- Workload deployments use one federated identity per subscription, not shared service principals with secrets.
- Defender for Cloud plans enabled by policy at mg-landingzones. Sentinel connects to the central workspace; its sizing is open decision OD-LZ-02.

Networking, from `azure-networking-hybrid-and-edge`: ADR-LZ-002 selects hub-spoke in East US 2 and Central US over Virtual WAN. There are three sites, one planned ExpressRoute circuit, and a firewall team that wants direct route-table control. Revisit trigger: site count growth or SD-WAN integration that makes route tables the bottleneck. CS-04 forces a re-addressing plan before the six overlapping VNets can join a hub; per-region address supernets are recorded in `CONSTRAINTS.json`.

Naming: the new convention applies to new resources only. Existing storage accounts, Key Vaults and web apps keep their names, with exceptions recorded in `CONSTRAINTS.json`; renaming them would mean recreation and data migration for no governance gain.

Subscription lifecycle: requests are approved, then automation creates the subscription under mg-corp or mg-online with budget, tags, spoke and deployment identity. Decommissioning moves a subscription to mg-decommissioned for a 60-day hold before cancellation. The platform IaC team owns the automation; this design specifies the process.

Cost, from `azure-cost-sustainability-and-finops`: a budget per subscription, with alerts to the owner tag. Shared platform cost is shown back to workloads; the allocation key (spoke count, firewall data processed, or a flat share) is open decision OD-LZ-01 for finance.

## 5. Migration sequence

Designed, not executed. Every step changes governance and passes GATE-02 in `CONSTRAINTS.json`.

1. Create mg-fabrikam and its children, and assign POL-01 to POL-06 in audit mode.
2. Move sandbox and decommissioned subscriptions first, and compare compliance before and after.
3. Re-address the six overlapping VNets as part of each workload's own change plan.
4. Move landing-zone subscriptions in waves. Each wave lists the policy and role assignments its subscriptions gain and lose, because inheritance changes with the parent.
5. Switch each policy from audit to deny once its non-compliant resources are remediated or exempted.

## Completion report

- Pack: azure-cloud-architect
- Workflow: `design-azure-landing-zone.prompt.md`
- Outcome: audit findings and a target landing-zone design delivered; nothing in the tenant was changed; standing access, PIM usage and the HIPAA control mapping are not-verified.

### scope_and_inputs

Audit and target design for Fabrikam Health's single tenant and 41 subscriptions, from four read-only exports dated 2026-10-14. No live access. Workload-level designs are out of scope.

### business_outcomes_and_requirements

Consistent governance across the estate, HIPAA reporting support, two allowed regions, hybrid connectivity for three hospitals, and cost ownership per workload [observed: supplied].

### source_facts_and_evidence

CS-01, CS-02 and CS-04 from the exports [observed]. CS-03 [inferred]. CS-05 [not-verified]. Hierarchy and landing-zone guidance from https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/ and https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups [observed]. The exact built-in HIPAA initiative name and its control coverage were not retrieved [not-verified].

### framework_alignment

CAF Ready: hierarchy, subscription vending and hub. Govern: POL-01 to POL-06 with staged enforcement. Secure: PIM, break-glass, Defender. Manage: central workspace and diagnostics. Biggest gap: CS-04 blocks hub connectivity until re-addressing.

### proposed_architecture

The flat ALZ-style hierarchy in section 2, the placement matrix in section 3, hub-spoke in two regions (ADR-LZ-002), central private DNS, and per-subscription federated deployment identities [designed].

### assumptions_and_tradeoffs

Assumed one tenant is enough, as no tenant-level separation requirement was stated. A flat hierarchy trades fine-grained policy targeting for simplicity (ADR-LZ-001). Hub-spoke trades Virtual WAN's managed routing for route-table control (ADR-LZ-002).

### implementation_and_operating_implications

The platform IaC team builds the hierarchy, policy assignments and vending automation. Each subscription move is a governed change. Policy enforcement is staged from audit to deny. Remediation tasks are run by the platform team, not by this agent.

### security_resilience_cost_and_sustainability

Tier-0 identity isolated in its own subscription; no standing human Owner. Connectivity in two regions, with ExpressRoute plus VPN as a backup path once the circuit lands. Budgets per subscription and showback of shared cost. Sustainability: the sandbox gets a budget and an expiry, so idle experiments end.

### output_files

| File | Purpose | Status and label |
|---|---|---|
| handoff/landing-zone/REQ.md | Requirements, findings CS-01 to CS-05, acceptance criteria | written [designed] |
| handoff/landing-zone/TOPOLOGY.json | Hierarchy, subscriptions, hubs, DNS | written [designed] |
| handoff/landing-zone/CONSTRAINTS.json | Policy set, naming exceptions, address supernets, GATE-02 | written [designed] |
| handoff/landing-zone/ADR.md | ADR-LZ-001 and ADR-LZ-002, Proposed | written [designed] |

### live_or_external_checks

None run; no live access. The exports are a point-in-time snapshot. Role assignments, PIM configuration and current Defender plans [not-verified].

### unresolved_risks

CS-03 may mean domain controllers share a blast radius with clinical workloads. CS-05 may hide standing Owner access. Re-addressing (CS-04) touches six production workloads. OD-LZ-01 and OD-LZ-02 are open.

### next_safe_action

Ask Fabrikam's operator for a role-assignment export and a resource inventory of the three suspected identity subscriptions, then take the hierarchy and policy set to the platform change board for step 1 of section 5.
