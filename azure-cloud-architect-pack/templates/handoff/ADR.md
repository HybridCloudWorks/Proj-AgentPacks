# ADR: workload name

One file holds every decision for this handoff, one section per decision, numbered ADR-001, ADR-002 and so on. A decision is never renumbered; a replaced decision becomes Superseded and names its successor.

Status values: Proposed (the default; the architect cannot accept their own decision), Accepted (by the named decision owner, with date), Superseded, Rejected.

---

## ADR-001: decision title in plain words

| Field | Value |
|---|---|
| Status | Proposed |
| Date | Date proposed; date accepted when it is |
| Decision owner | The role that accepts or rejects it |
| Implementation owner | The team that builds it |
| Related | REQ IDs, TOPOLOGY IDs, CONSTRAINTS IDs, evidence IDs |

### Context

The requirement or problem that forces a decision, the constraints that bound it, and the facts it rests on, with evidence labels. Keep it short enough that a reader who skips the rest still knows why this decision exists.

### Alternatives

| Option | Reliability | Security | Cost | Operations | Performance | Why it was or was not chosen |
|---|---|---|---|---|---|---|
| Option A | | | | | | |
| Option B | | | | | | |

At least two real options. Doing nothing counts when it is genuinely viable. Name the evidence that eliminated each rejected option; "not familiar" is not a reason.

### Decision

The selected option, stated so an implementer can act on it without guessing: service, tier, scope, region, and configuration that matters.

### Consequences

What becomes easier, what becomes harder, the cost and operating load it adds, and the residual risk accepted. Include implementation, testing and rollback implications for Bicep, ARM, Terraform or AVM where they differ.

### Evidence

| Claim | Evidence ID or source | Label |
|---|---|---|
| A drift-prone fact the decision depends on | E-01 | not-verified |

A decision that depends on a not-verified fact can be Proposed but should not be Accepted until the fact is checked or the owner accepts the risk in writing.

### Rollback and revisit trigger

How to reverse the decision and what that costs, or a plain statement that a step is irreversible and who signed it off. Name the observable condition that should reopen the decision.
