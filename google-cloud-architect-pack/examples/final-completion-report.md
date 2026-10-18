# Worked completion report

For the serverless web application example in this folder.

- Status: DESIGN_READY_FOR_REVIEW
- Outcome: solution guide, four decision records and a Terraform skeleton for the customer portal are prepared for the lead architect's review.

| Criterion | Status | Evidence |
|---|---|---|
| Every requirement traced to a design element | passed | Traceability matrix in the solution guide |
| Residency: TLS terminates in the EU region | passed | ADR-002 and the load balancer configuration in the skeleton |
| Backends unreachable around the load balancer | unverified | Runtime check written for the user; nothing deployed |
| Composite availability meets 99.9% | passed | Calculator output with cited SLA pages |

- Deliverables: solution-guide.md, adr-001 to adr-004, infra/ skeleton.
- Decisions: ADR-001 to ADR-004, all Proposed, owner the portal's lead architect.
- Assumptions: peak load of 300 requests per second supplied by the user, not measured.
- Security posture: load balancer-only frontend ingress, internal-only api, per-service identities, IAM database authentication, Cloud Armor rules.
- Reliability posture: regional, zone-redundant; backups with point-in-time recovery cover region loss within the RTO.
- Cost estimate: range from the pricing calculator with stated traffic assumptions; low confidence until load-tested.
- Sustainability impact: services scale to zero off-peak.
- Operational impact: burn-rate alerts and runbooks proposed.
- Performance impact: concurrency and maximum instances set from the peak estimate.
- Compliance and residency: all data and TLS termination in one EU region.
- Cloud changes: none.
- Checks: `terraform fmt -check` (local workspace, exit 0, passed); `terraform validate` (local workspace, exit 0, passed).
- Unverified: runtime ingress, WAF and certificate behaviour.
- Remaining risks: peak load is an estimate.
- Rollback: nothing deployed.
- Follow-ups: owner reviews the decision records; user deploys and runs the runtime checks.

The JSON files in `tests/fixtures` are invented inputs for the report checker in `tooling/`; they are not evidence that any real work was done.
