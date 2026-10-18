# REQ: workload name

Handoff ID, version, date, author and decision owner on one line.

Copy this folder as the handoff for one workload or platform scope. `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md` share one ID scheme so every requirement, element, constraint and decision can point at the others. `hooks/architecture-review.ps1` checks that all four files are present; it does not check what they say.

Rules for this file:

- Keep it sanitized: no secrets, credentials, personal data, or internal host names that the handoff audience should not see.
- Label every entry with one evidence label: observed, inferred, designed, structurally-validated, live-verified, not-verified. "observed" means seen in supplied files, command output or retrieved documentation; a requester's statement is observed only as a statement.
- Write "unknown" where a value is unknown. Never fill a gap with a default.

## 1. Business outcomes

| ID | Outcome | How success is measured | Source | Label |
|---|---|---|---|---|
| REQ-BO-01 | The outcome in business terms | The measure and its target | Who stated it, or the document | observed |

## 2. Scope and non-goals

List what is in scope (workloads, environments, regions, interfaces) and what is explicitly out of scope, including adjacent systems the handoff audience might otherwise assume are covered.

## 3. Workload profile

Users and their locations, upstream and downstream dependencies, main data flows, delivery model (team, CI/CD, release cadence) and the current state: greenfield, existing Azure estate, or migration source.

## 4. Nonfunctional requirements

| ID | Category | Requirement | Target | Priority | Source | Label |
|---|---|---|---|---|---|---|
| REQ-NFR-01 | Availability | Monthly SLO for the user-facing path | 99.9 % | Must | Service owner | observed |
| REQ-NFR-02 | Recovery | RTO and RPO for the tier | RTO and RPO values | Must | Continuity plan | observed |

Cover availability, recovery, throughput, latency, growth, security, compliance, residency, operability and cost. Delete a category only with a sentence saying why it does not apply.

## 5. Data classification, residency and compliance

Each data set with its classification, residency constraint, retention, deletion obligation and owner. Name compliance obligations as scoped assessments with an assessor, never as properties of the design.

## 6. Boundaries

| Boundary | Placement | What it supplies | Label |
|---|---|---|---|
| Microsoft Entra tenant | Tenant name | Identity, Conditional Access | observed |
| Management group | Management group | Inherited policy and RBAC | designed |
| Subscription | Subscriptions per environment | Billing, quota, RBAC, blast radius | designed |
| Resource group | Groups by lifecycle | Lifecycle and delegated access | designed |
| Region and zones | Primary and recovery regions | Residency and failure domains | designed |
| Network | VNets, subnets, peering | Private access and inspection | designed |

## 7. Ownership

| Area | Owner | Escalation route |
|---|---|---|
| Workload | Team or role | How to reach them |
| Platform (subscriptions, hub, DNS, policy) | Team or role | How to reach them |
| Security sign-off | Team or role | How to reach them |
| Cost | Budget holder | How to reach them |

## 8. Acceptance criteria

| ID | Area | Criterion | Verified by | Status |
|---|---|---|---|---|
| AC-SEC-01 | Security | A testable statement | The check, test or record that proves it | not-verified |
| AC-REL-01 | Reliability | | | |
| AC-COST-01 | Cost | | | |
| AC-PERF-01 | Performance | | | |
| AC-OPS-01 | Operations | | | |
| AC-DEP-01 | Deployment | | | |

Every criterion names the evidence that would prove it. A criterion stays not-verified until that evidence exists.

## 9. Assumptions

| ID | Assumption | Impact if wrong | How it will be validated | Owner |
|---|---|---|---|---|
| AS-01 | | | | |

## 10. Open decisions and unknowns

| ID | Decision or unknown | Options | Why it matters | Owner | Needed by |
|---|---|---|---|---|---|
| OD-01 | | | | | |

The handoff is not complete while a required input is unknown; say which open decision blocks which ADR or acceptance criterion.

## 11. Dependencies

External teams, platform capabilities, approvals and evidence this design waits on, each with an owner and the ID of what it blocks.
