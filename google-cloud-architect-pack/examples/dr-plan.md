# Worked example: checking a design against its SLO, RTO and RPO

Synthetic scenario for the `plan-resilience.prompt.md` workflow, using the calculator in the gcp-reliability-dr skill.

## Targets

SLO 99.95% monthly availability for checkout; RPO 5 minutes and RTO 60 minutes for the orders database; region loss in scope; EU residency allows two EU regions.

## Error budget

`python scripts/availability.py budget --slo 99.95 --days 30` returns 21.6 allowed minutes of unavailability per 30 days.

## Composite availability of the first draft

The first draft ran in one region: load balancer and service tier in series with a regional HA database. With illustrative inputs of 99.95% for each of the two tiers (the real figures must come from each product's SLA page for the exact configuration):

`python scripts/availability.py compose --serial 99.95 99.95` returns a composite of about 99.900025%, below the 99.95% SLO. Arithmetic does not fix this; the design has to change.

## Revised design

Service tier deployed in two EU regions, each behind its own regional external Application Load Balancer, with Cloud DNS failover routing between them so that TLS still terminates inside EU regions (a global external Application Load Balancer would terminate TLS at edge locations, which this residency requirement does not allow). Each region is given an illustrative 99.95%, with the database tier as the remaining serial component:

`python scripts/availability.py compose --parallel 99.95x2 --serial 99.99` returns about 99.989975% when the database is given an illustrative 99.99%. The database therefore needs a configuration whose published SLA supports that figure, or the SLO must be revisited with the owner.

## Recovery check

Database DR pattern: warm standby with a cross-region read replica. Replication lag measured at about 1 minute under load; failure detection 10 minutes; promotion and connection switch 20 minutes.

`python scripts/availability.py dr-check --rpo-minutes 5 --rto-minutes 60 --replication-lag-minutes 1 --detection-minutes 10 --restore-minutes 20` returns a worst-case data loss of 1 minute (RPO margin 4 minutes) and a recovery time of 30 minutes (RTO margin 30 minutes), exit code 0.

## Tests planned

Quarterly restore test from backups into an isolated project, measuring real restore time; semi-annual regional failover game day in non-production; postmortems for any test that misses its objective. No failover or restore was triggered by the agent.

## Result

Status DESIGN_READY_FOR_REVIEW, with SLA inputs marked unverified until replaced by published figures.
