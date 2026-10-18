# Workload requirements questionnaire

Fill this in before a design session; every unanswered item becomes an open question or a labelled assumption in the design.

## Business and function

- What the workload does, for whom, and the business outcome it supports.
- Critical user journeys, in order of importance.
- Expected users, traffic pattern (steady, seasonal, bursty) and growth over three years.

## Non-functional requirements

| Area | Question | Answer |
|---|---|---|
| Security | Data classification per store; who may access what; threat concerns | |
| Compliance and residency | Regimes that apply; countries or regions where data may live and be processed | |
| Reliability | Availability target or SLA; acceptable degraded modes | |
| Recovery | RTO and RPO per data store; region-loss in scope or not | |
| Cost | Monthly budget range; existing commitments or discounts; chargeback model | |
| Operations | Who operates it; on-call model; deployment frequency; tools already in use | |
| Performance | Latency targets per journey; peak throughput; batch windows | |
| Sustainability | Carbon goals or reporting obligations; flexibility on region and timing | |

## Current state and dependencies

- Where it runs today and its architecture.
- Pain points and reasons to change.
- Identity provider; upstream and downstream systems; on-premises or other-cloud dependencies; licences.

## Constraints

- Approved regions and services; organization policies already in force; naming and labelling standards.
- Team skills and preferences (for example Kubernetes experience, SQL versus Spark).
- Deadlines and change freezes.
