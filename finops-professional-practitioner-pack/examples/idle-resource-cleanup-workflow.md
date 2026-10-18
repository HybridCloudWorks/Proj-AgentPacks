# Worked example: idle resource hunt with safe execution

All figures are synthetic.

**Request.** "Find idle stuff in our non-production accounts and clean it up." Recipe: `find-optimization-opportunities.prompt.md`. Skill: workload-optimization.

**Authority.** The user authorizes analysis and a cleanup plan. Deletion is not authorized; it stays Level 2 for each owner.

**Inventory.** Billing data at ResourceId level for 45 days joined with monitoring exports supplied by the user.

| Resource | Pattern | Signal one | Signal two | Class | Monthly cost | Owner |
|---|---|---|---|---|---|---|
| lb-web-edge-test | Idle load balancer | No requests for 45 days | No healthy targets | Obvious | 24 | web team |
| nat-qa-az2 | Idle gateway | 0.4 GB processed in 45 days | Route table: one subnet, no running instances | Likely | 36 | QA |
| vol-ci-cache (12 volumes) | Unattached volume | Unattached for 45 days | No tag updates | Obvious | 310 | CI platform |
| vm-perf-01 to 04 | Forgotten environment | CPU under 2% | Network near zero, no logins for 6 weeks | Likely | 1,180 | performance team |
| lb-dr-standby | Idle load balancer | No requests | DNS failover record points to it | Exempt (DR) | 24 | web team |

The disaster-recovery balancer is excluded and labelled so the next hunt does not flag it.

**Plan.** For each owner: a notice tag with a scheduled date 14 days out, snapshots of the volumes and machine disks before any deletion, deletion of the load balancer's listeners before the balancer, a route-table check before the gateway is removed, and the rollback steps. Estimated impact 1,550 to 1,600 per month, savings type estimated. Trade-off: negligible for the obvious tier; the performance environment needs a rebuild of about two hours if wanted again.

**Execution.** Not performed by the agent. The owners approve and execute in their change window.

**Measurement.** Thirty days after the change the primary compares cost per day for the changed resources: baseline 51.80 per day, after 0.90 per day (snapshot storage). Realized saving 1,527 per month, recorded in the savings tracker.

**Completion.** First report: PREPARED_NOT_VERIFIED, with the saving labelled estimated. After measurement: VERIFIED_COMPLETE for the realized-savings criterion, with the measurement query recorded as a passed check.
