# Worked example: intermittent 504s on the tracking API

Workflow: `troubleshoot-aws-incident.prompt.md`. Skills applied: `aws-operations-observability-and-troubleshooting`, `aws-networking-hybrid-and-edge`, `aws-iac-deployment-and-lifecycle`, `aws-cost-sustainability-and-finops`, `aws-docs-mcp-and-evidence`, `aws-architecture-handoff-and-adr`.

This continues the fictional Larkspur tracking platform from the greenfield example. Since that design, two changes went in:

- Release 2.4 added an ETA-enrichment call to an external geocoding provider. ADR-004 added one NAT gateway per AZ for it.
- On 2026-10-10 a cost-saving pull request consolidated the three NAT gateways into one.

## Request

At 09:40 UTC on 2026-10-18:

> Since yesterday afternoon the tracking API returns intermittent 504s and p99 latency is roughly six times normal. Find the cause. Do not change anything in production. You can use the `larkspur-readonly` profile for `tracking-prod` in eu-west-1.

The incident commander is the on-call lead, who also authorizes any mitigation.

## Evidence gathered (read-only)

All commands ran with profile `larkspur-readonly` against account `tracking-prod`, Region eu-west-1, AWS CLI v2. Log lines were redacted before quoting.

| # | Evidence | How | Label |
|---|---|---|---|
| E1 | ALB `HTTPCode_ELB_504_Count` rises from 0 to peaks of 140 per minute from 16:05 UTC on 2026-10-17. `TargetResponseTime` p99 rises from 180 ms to 1.1 s | `aws cloudwatch get-metric-data` | observed |
| E2 | Healthy host count steady at 6. Task CPU peaks at 41%, memory at 55%, no task restarts | `get-metric-data`, `aws ecs describe-services` | observed |
| E3 | Feature flag `eta-enrichment` raised from 5% to 100% at 15:52 UTC on 2026-10-17 | Flag-service audit log shared by the on-call lead | observed |
| E4 | CloudTrail shows `DeleteNatGateway` for the AZ b and AZ c gateways and `ReplaceRoute` on `rt-private-b` and `rt-private-c` to the AZ a gateway, at 2026-10-10 14:12 UTC, by the pipeline role | `aws cloudtrail lookup-events` | observed |
| E5 | All three private route tables now send 0.0.0.0/0 to `nat-a` | `aws ec2 describe-route-tables` | observed |
| E6 | `ErrorPortAllocation` on `nat-a` is non-zero from 16:04 UTC, and peaks line up with 504 peaks in 38 of 40 one-minute buckets. `ActiveConnectionCount` is at its highest ever | `get-metric-data` on `AWS/NATGateway` | observed |
| E7 | Application logs show `connect timed out` to the geocoder host. Geocoder calls that succeed are as fast as before | CloudWatch Logs Insights query | observed |
| E8 | No AWS Health events for eu-west-1 services in the window | AWS Health Dashboard, checked by the on-call lead | observed |
| E9 | Geocoder provider status page shows no incident | External page, not checked by the architect | not-verified |
| E10 | The 2.4 code diff creates a new HTTP client, and so a new TCP connection, for every enrichment call | Pull request diff shared by the user | observed |

`aws-docs-mcp-and-evidence`: the NAT gateway documentation (retrieved 2026-10-18) says a NAT gateway supports up to 55,000 simultaneous connections to each unique destination and reports `ErrorPortAllocation` when it cannot allocate a source port (observed).

## Hypotheses

The troubleshooting loop from `aws-operations-observability-and-troubleshooting`:

| Hypothesis | Test | Status | Confidence |
|---|---|---|---|
| H1: NAT port allocation fails for connections to the geocoder, and the client timeouts surface as ALB 504s | Correlate E6 with E1. Check the connection pattern (E10) and the routing (E5) | Supported | High |
| H2: The geocoder provider is degraded | E7 latency of successful calls, E9 | Weakened. Timeouts occur only alongside NAT errors | Medium that it is **not** the cause |
| H3: ECS tasks are saturated | E2 | Refuted | High |
| H4: ALB or target health problem | E2 healthy host count | Refuted | High |

**Root cause (inferred, high confidence).** Release 2.4 opens a new connection for every enrichment call (E10). At 100% rollout (E3), connection churn to a single geocoder IP and port went past what one NAT gateway can allocate. All three AZs had shared that gateway since the consolidation (E4, E5). The 5% rollout stayed under the limit, which is why the consolidation looked harmless for a week.

`aws-networking-hybrid-and-edge` found a second problem in the same evidence. Routing AZ b and AZ c through `nat-a` adds cross-AZ data processing, and it makes AZ a a single point of failure for all egress.

`aws-cost-sustainability-and-finops`: the consolidation saved two NAT gateways' hourly charges. It added cross-AZ transfer and removed AZ-independent egress. That trade-off was never recorded, and the pull request had no ADR.

## Mitigation and correction

The architect gave the incident commander these options and changed nothing itself:

| Option | Effect | Risk | Rollback | Approver |
|---|---|---|---|---|
| M1: set `eta-enrichment` to 0% | Removes the connection churn immediately; ETA enrichment is off | Low; the feature is degraded, not broken | Raise the flag again | Incident commander |
| M2: revert the NAT consolidation through the pipeline | Restores per-AZ egress and the per-gateway connection headroom | Medium; it is a network change, so the plan must be reviewed first (`review-deployment-plan.prompt.md`) | Re-apply the consolidation | Network owner and service owner |
| M3: reuse a pooled HTTP client with keep-alive | Fixes the root cause in code | Low after testing | Release revert | Service owner |

The incident commander approved M1, and the on-call engineer set the flag to 0% at 10:22 UTC. The architect re-read E1 and E6 with the read-only profile. 504s were back to baseline by 10:27 UTC and `ErrorPortAllocation` read 0 (observed after the change).

M2 and M3 are proposed root-cause corrections. Neither is done. Proposed follow-ups:

- An alarm on `ErrorPortAllocation > 0` for every NAT gateway.
- A runbook entry for egress saturation.
- ADR-005, which records the NAT topology decision and supersedes the unrecorded consolidation (`aws-architecture-handoff-and-adr`).

## Completion report

Pack: aws-cloud-architect. Date: 2026-10-18.

Outcome: the mitigation is live-verified. The root cause is inferred with high confidence. The root-cause corrections are proposed and not done.

### scope_and_inputs

Intermittent 504s and high p99 on the tracking query API in `tracking-prod`, eu-west-1, from 16:05 UTC on 2026-10-17. Read-only access through `larkspur-readonly` was authorized. The incident commander authorizes mitigation.

### business_outcomes_and_requirements

Restore the 99.9% availability SLO (NFR-01) and the p95 latency target (NFR-04) for customer tracking queries, without unapproved production changes.

### source_facts_and_evidence

- E1 to E8 and E10: observed, with commands, profile, account and Region recorded above.
- E9: not-verified.
- NAT gateway connection limit and metric behavior: observed from documentation retrieved 2026-10-18.

### framework_alignment

- Reliability: one NAT gateway is a single point of failure for egress.
- Operational Excellence: there was no alarm on NAT errors, and a cost change merged without an ADR.
- Cost: an unrecorded trade-off against resilience.
- Performance Efficiency: a connection-per-request client pattern.

### proposed_architecture

- One NAT gateway per AZ, with each private route table pointing to the gateway in its own AZ (M2, designed).
- A pooled HTTP client (M3, designed).
- A NAT error alarm (designed).

### assumptions_and_tradeoffs

- The geocoder resolves to one IP and port for this traffic. E7 hostnames support this; the DNS answers were not captured.
- Restoring per-AZ NAT reverses the cost saving. ADR-005 records the trade-off.

### implementation_and_operating_implications

- M2 goes through a reviewed Terraform plan in the pipeline.
- M3 ships in the next release with a load test that counts connections per destination.
- Add the alarm and the runbook entry.
- The flag stays at 0% until M3 is deployed.

### security_resilience_cost_and_sustainability

- Security: no IAM or exposure change involved. Redacted logs only.
- Resilience: egress depends on AZ a until M2 is done.
- Cost: M2 restores two NAT gateways' hourly charges and removes cross-AZ processing.
- Sustainability: connection reuse cuts per-request network work.

### output_files

| File | Purpose | Check run | Label |
|---|---|---|---|
| None written | Findings returned inline in the incident channel summary, as the user requested | n/a | n/a |

ADR-005 is drafted inline for the service owner to commit.

### live_or_external_checks

- Read-only CloudWatch, CloudTrail, EC2, ECS and Logs queries: executed (observed).
- Mitigation effect after M1: executed (live-verified).
- Geocoder provider status and DNS capture: not executed (not-verified).

### unresolved_risks

- AZ a remains a single point of failure for egress until M2 (owner: network owner).
- Enrichment is disabled until M3 (owner: service owner).
- The unrecorded cost change shows there is no ADR gate for network changes (owner: platform lead).

### next_safe_action

The service owner opens the M2 revert as a pipeline plan for review. Nothing else changes in production until that plan is reviewed and approved.
