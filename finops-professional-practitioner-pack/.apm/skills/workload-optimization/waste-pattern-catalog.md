# Waste pattern catalog

Named patterns give teams a shared shorthand. Each pattern lists two independent signals; one signal alone is not enough to act. Prices change by region and over time, so check current pricing before quoting amounts.

| Pattern | Signal one | Signal two | Safe fix | Trap |
|---|---|---|---|---|
| Idle gateway | Hourly gateway charges with very little data processed | Route tables show few or no active subnets using it | Replace object-storage traffic with a gateway endpoint, consolidate or remove after route review | Removing it cuts management traffic you could not see in application metrics |
| Snapshot sprawl | Snapshot storage rising while volume storage is flat | Snapshots whose source volume no longer exists | Lifecycle policy for new snapshots; holdback tag, then delete orphans | Image-backing snapshots and legal holds cannot simply be deleted |
| Idle load balancer | No request traffic over the window | No healthy targets | Remove listeners first, then the balancer, after a DNS reference check | It may be a failover target with no traffic by design |
| Unattached volume | Volume not attached for the whole window | No owner activity or tag update | Snapshot, notify, delete after the notice period | The snapshot step is what makes the action reversible |
| Oversized database | Low average and peak CPU over a window that includes month-end | Large and steady free memory, connections far below the limit | Downsize one step in a maintenance window, monitor, keep a rollback | A commitment may pin the size; exchange first |
| Cross-zone chatter | Data transfer charges between zones growing | Flow logs show heavy pairs of services in different zones | Same-zone routing, caching, connection reuse | Some replication across zones is the availability design |
| Forgotten environment | Non-production spend steady around the clock | No deployments or logins for weeks | Schedule or decommission with owner sign-off | Shared test environments may serve other teams |
| Untuned function memory | Function duration high at the configured memory | Measured tuning shows a cheaper setting at equal latency | Apply the measured setting | Downstream services may dominate the real cost |
| Over-requested pods | Requests far above p95 usage | Node utilization low while pods stay pending elsewhere | Right-size requests with headroom, then tune consolidation | Removing memory limits trades cost for outages |
| Archive mismatch | Objects in a frequent-access tier never read after the first weeks | Access logs or storage analytics confirm cold access | Lifecycle transition to an infrequent or intelligent tier | Small objects and early deletion fees can erase the saving |
