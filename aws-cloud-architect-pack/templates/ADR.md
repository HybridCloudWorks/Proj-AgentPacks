# ADR log: <workload or program name>

One section per material decision, numbered ADR-001 onward. When a decision changes, add a new ADR and mark the old one superseded. Do not rewrite the old one.

---

## ADR-<nnn>: <decision title, phrased as the choice made>

| Field | Value |
|---|---|
| Status | proposed / accepted / superseded by ADR-<nnn> / rejected |
| Date | <YYYY-MM-DD> |
| Deciders and approver | <names or roles> |
| Scope | <workload, accounts, Regions> |
| Related | <REQ ids, TOPOLOGY ids, other ADRs> |

### Context

<The problem, the forces at play, and the current state. Facts only, each one labelled.>

### Decision drivers

- <REQ id: requirement that drives this decision>

### Alternatives considered

| Option | Fits the drivers because | Trade-offs | Cost dimensions | Operational burden | Why not chosen |
|---|---|---|---|---|---|
| <option A> | | | | | selected |
| <option B> | | | | | |

### Decision

<The selected option and the boundary of what it covers.>

### Consequences

- Positive: <what gets better>
- Negative: <what gets worse or harder, and who carries it>
- Implementation: <CloudFormation, CDK or Terraform implications; stack or module boundaries; deployment order; tests that prove it>
- Operations: <telemetry, alarms, runbooks, on-call impact>
- Rollback: <how to reverse it, and what cannot be reversed>

### Evidence

| Claim | Source URL or tool | Retrieved | Account / Region | Label |
|---|---|---|---|---|
| | | <YYYY-MM-DD> | | observed / inferred / not-verified |

### Assumptions

- <assumption, and the owner who must confirm it>

### Revisit trigger

<The measurable condition that reopens this decision, for example a traffic level, a cost threshold, a new Region requirement or a service capability becoming available.>
