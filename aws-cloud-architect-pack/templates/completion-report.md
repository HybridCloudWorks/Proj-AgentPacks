# Completion report: <task>

Pack: aws-cloud-architect. Date: <YYYY-MM-DD>.

Outcome: <one sentence saying what is designed, what is verified, and what is blocked or not verified>

Evidence labels: observed, inferred, designed, structurally-validated, live-verified, not-verified. Label every fact, recommendation and check. A check that was not executed is not-verified. It is never passed.

Keep the twelve sections below in this order and use these exact names. If a section does not apply, write "Not applicable" and say why.

## scope_and_inputs

<The request, workload boundary, accounts and Regions, inputs supplied, and the authority granted (read-only, files, nothing live).>

## business_outcomes_and_requirements

<Outcome, must-have requirements, preferences, and the REQ ids they map to.>

## source_facts_and_evidence

| Fact | Source or tool | Retrieved | Account / Region | Query or command | Label |
|---|---|---|---|---|---|
| | | | | | |

## framework_alignment

| Pillar or perspective | Finding | Gap or risk | Label |
|---|---|---|---|
| Operational Excellence | | | |
| Security | | | |
| Reliability | | | |
| Performance Efficiency | | | |
| Cost Optimization | | | |
| Sustainability | | | |

Add CAF perspectives (Business, People, Governance, Platform, Security, Operations) when organizational readiness is in scope. A framework review is not a formal AWS Well-Architected Tool result or an audit.

## proposed_architecture

<The design: accounts, Regions, AZs, networks, services, identities, data flows and failure domains. Point to TOPOLOGY ids.>

## assumptions_and_tradeoffs

<Each assumption with its impact if wrong, and each trade-off with the ADR that records it.>

## implementation_and_operating_implications

<IaC boundaries, deployment order, validation and change-review gates, rollback, owners, telemetry, runbooks.>

## security_resilience_cost_and_sustainability

<Identity and data protection, recovery against RTO and RPO, cost dimensions and ownership, and sustainability actions, each labelled.>

## output_files

| File | Purpose | Check run | Label |
|---|---|---|---|
| REQ.md | Requirements | | |
| TOPOLOGY.json | Structured topology | | |
| CONSTRAINTS.json | Guardrails | | |
| ADR.md | Decisions | | |

## live_or_external_checks

| Check | Executed | Result | Label |
|---|---|---|---|
| <AWS Knowledge MCP lookup, CLI read, renderer, recovery test> | yes / no | | |

## unresolved_risks

<Open risks, each with owner and the decision or evidence that would close it.>

## next_safe_action

<The single next step that is safe to take, and who must authorize it.>
