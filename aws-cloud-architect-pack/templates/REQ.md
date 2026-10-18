# REQ: <workload or program name>

| Field | Value |
|---|---|
| Version | <n> |
| Date | <YYYY-MM-DD> |
| Requirements owner | <name or role> |
| Status | draft / reviewed / approved |
| Related | TOPOLOGY.json, CONSTRAINTS.json, ADR.md |

This file has been sanitized. It holds no secrets, credentials, tokens or personal data. Include account IDs only where the downstream engineer needs them.

Evidence labels: observed, inferred, designed, structurally-validated, live-verified, not-verified.

## 1. Business outcome and scope

| Item | Value | Source | Label |
|---|---|---|---|
| Business outcome | <what changes for the business, and how it is measured> | <stakeholder, document> | <label> |
| Users and critical journeys | <who, and which journeys must not fail> | | |
| Engagement type | greenfield / migration / modernization / expansion / incident recovery / optimization / review | | |
| In scope | <workloads, accounts, Regions, environments> | | |
| Out of scope | <explicit non-goals> | | |

## 2. Functional requirements

| ID | Requirement | Priority (must / should / could) | Source | Acceptance criterion |
|---|---|---|---|---|
| FR-01 | | | | |

## 3. Non-functional requirements

Separate a must-have from a preference. Express each target so that it can be measured.

| ID | Category | Target | How it is measured | Must or preference | Source | Label |
|---|---|---|---|---|---|---|
| NFR-01 | Availability / SLO | <e.g. monthly %, measured at which edge> | | | | |
| NFR-02 | RTO | <duration, per failure scenario> | | | | |
| NFR-03 | RPO | <duration, per failure scenario> | | | | |
| NFR-04 | Latency | <percentile and threshold> | | | | |
| NFR-05 | Throughput and concurrency | <steady, peak, burst shape> | | | | |
| NFR-06 | Growth | <horizon and rate> | | | | |
| NFR-07 | Observability | <SLIs, retention, trace context> | | | | |
| NFR-08 | Operability | <on-call model, change windows, skills> | | | | |
| NFR-09 | Sustainability | <utilization or efficiency goal, if any> | | | | |

State which failure scenarios each RTO and RPO covers: process, AZ, Region, account, dependency, data corruption, operator error.

## 4. Data and compliance

| Data set | Classification | Residency / Region | Retention | Encryption and key owner | Deletion | Compliance scope |
|---|---|---|---|---|---|---|
| | | | | | | |

A compliance requirement here gives the exact framework, control scope, partition or Region, and evidence period. It is a requirement, not an attestation.

## 5. Scale, cost and lifecycle

- Demand: <current / expected / peak, with units>
- Budget: <amount, currency, time window, budget owner>
- Environments: <dev / test / prod and their isolation requirement>
- Lifecycle: <release cadence, support window, decommission criteria>

## 6. Ownership and approvals

| Area | Owner | Approves |
|---|---|---|
| Architecture | | Design changes, ADR status |
| Platform and landing zone | | Account vending, guardrails |
| Security | | IAM, SCP, KMS, exceptions |
| Network | | Routes, attachments, CIDR |
| Operations | | Runbooks, alarms, on-call |
| FinOps | | Budgets, commitments |
| Data | | Classification, retention, migration |

## 7. Verification criteria

Say how the downstream engineer proves each requirement, and what that proof shows today.

| Requirement ID | Verification method | Environment | Label today |
|---|---|---|---|
| NFR-02 | <e.g. restore or failover test with timed runbook> | <account / Region> | not-verified |

## 8. Assumptions

| ID | Assumption | Why it was made | Impact if wrong | Owner to confirm |
|---|---|---|---|---|
| A-01 | | | | |

## 9. Open questions

| ID | Question | Blocks | Owner | Needed by |
|---|---|---|---|---|
| Q-01 | | | | |

## 10. Not proven

List what this handoff does not establish, for example: deployed state, account-applied quotas, current pricing, recovery times, compliance status, or anything else left not-verified.
