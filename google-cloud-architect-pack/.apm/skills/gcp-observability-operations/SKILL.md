---
name: gcp-observability-operations
description: "Design Google Cloud observability and operations - log routing and retention, metrics scopes, SLO-based and burn-rate alerting, metric selection, Logging Query Language queries, tracing and profiling with OpenTelemetry, operational readiness, incident and change management, and continuous best-practice evaluation. Use when planning monitoring, alerting, logging, dashboards, runbooks, release processes or production readiness for a Google Cloud workload."
---

# Google Cloud Observability and Operations

## Purpose and activation

Make failures visible before users report them, make every alert actionable, and make change routine and reversible. Activate for monitoring and logging design, alert strategy, production readiness reviews, incident process design, release pipeline design, log queries during an investigation, or telemetry cost problems.

## Scope and exclusions

In scope: telemetry architecture, SLO monitoring and alert policies, dashboards, log queries, metric discovery, tracing and profiling, readiness criteria, incident and postmortem process, change automation, continuous evaluation with Workload Manager. SLO targets themselves come from gcp-reliability-dr; GKE-specific telemetry defaults from gcp-gke-platform. Creating alert policies, sinks, dashboards or evaluations in a live project is Level 2.

## Inputs

Services and their critical journeys, SLOs, the on-call model and paging tools, compliance retention requirements, existing logging, monitoring and tracing tools (including third-party APM or SIEM), deployment tooling, and telemetry budget.

## Dependencies and tools

[Well-Architected operational excellence pillar](https://docs.cloud.google.com/architecture/framework/operational-excellence/printable.md.txt), [instrumentation strategy](https://docs.cloud.google.com/stackdriver/docs/instrumentation/choose-approach.md.txt), [Logging Query Language](https://docs.cloud.google.com/logging/docs/view/logging-query-language), [monitored resource types](https://docs.cloud.google.com/logging/docs/api/v2/resource-list), [Google Cloud metrics list](https://cloud.google.com/monitoring/api/metrics_gcp), Managed Service for Prometheus best practices. A Cloud Monitoring or Cloud Logging MCP server only if the client already has one connected; this skill never edits MCP configuration.

## Workflow

1. Telemetry architecture: route logs with the Log Router into log buckets per environment or compliance domain, set retention per requirement, add exclusion filters for noisy, low-value logs, and use Log Analytics or a linked BigQuery dataset for analysis. Create a metrics scope in a central monitoring project per environment group. Prefer OpenTelemetry instrumentation for traces and metrics, Managed Service for Prometheus for Kubernetes and Prometheus-native workloads, Cloud Trace for latency paths, Cloud Profiler for hot code, and Error Reporting for exceptions. Write structured JSON logs to standard output with a correlation identifier.
2. Metric selection: identify the service prefix (for example `run.googleapis.com/`, `cloudsql.googleapis.com/`, `kubernetes.io/`, `agent.googleapis.com/` for guest metrics, `prometheus.googleapis.com/` for managed Prometheus), list the metric descriptors for that prefix from the Monitoring API or documentation, filter by the concepts the user cares about, and present five to fifteen metrics with type, kind, value type and monitored resource. Do not guess metric names.
3. Alerting: alert on symptoms users feel, through SLO burn rates. Use at least a fast-burn policy (short window, high burn rate, pages) and a slow-burn policy (long window, low burn rate, tickets). Add a few cause alerts only where they predict an outage early (quota exhaustion, certificate expiry, backlog age, disk or connection saturation). For signals with strong daily or weekly patterns, such as AI agent latency or quality scores, prefer anomaly or baseline-relative conditions over static thresholds. Each alert names its owner, runbook link and severity; deduplicate policies before adding new ones.
4. Log queries: write Logging Query Language with double-quoted strings, upper-case `AND`, `OR` and `NOT`, and parentheses for precedence; always set `resource.type` from the resource catalog rather than guessing; for "who changed what" use audit logs and `protoPayload.methodName:"service.resource.verb"` (substring match with a colon); if no schema for a field is known, fall back to `SEARCH("term")` within the right resource type and say so in a `--` comment; use placeholders such as `"<PROJECT_ID>"` instead of blocking on missing identifiers.
5. Dashboards: one per service showing SLO status, error-budget burn, traffic, latency percentiles, saturation and dependency health; one per platform (for GKE include API server latency, node readiness and pod restarts).
6. Operational readiness: before production, require defined SLOs, tested alerts, runbooks for the top failure modes, an on-call rotation, capacity and quota headroom, tested backups, a dependency map, and security sign-off. Register the application's resources in App Hub where it helps teams see the topology.
7. Incidents and problems: define incident roles (commander, communications, operations), severity levels, communication channels and status updates, and blameless postmortems with tracked actions and follow-up review.
8. Change management: all infrastructure through IaC in version control with review, CI with Cloud Build or the existing CI using a federated identity, progressive delivery with Cloud Deploy (canary or blue-green) for Cloud Run, GKE and Compute Engine, automated rollback criteria tied to SLOs, and change freeze rules aligned with maintenance windows.
9. Continuous evaluation: Workload Manager evaluations for SAP, SQL Server or general best-practice rules (including custom Rego rules), scoped to the smallest project or label filter that answers the question, with results exported to BigQuery for trend tracking.
10. Telemetry cost: estimate log ingestion, metric time series and Prometheus samples; set retention, sampling and exclusions accordingly.

## Output

Telemetry architecture diagram, log routing and retention table, metric selection tables, alert catalog (name, condition, window, severity, owner, runbook), dashboard list, readiness checklist, incident process outline, release pipeline design and telemetry cost estimate.

## Validation

Every SLO has a burn-rate alert and every paging alert has a runbook; every log query names a valid resource type or states that it uses global search; retention meets compliance; metric names come from descriptors or documentation. Read-only checks on a named project: `gcloud logging sinks list --project=PROJECT_ID` and `gcloud logging buckets list --location=global --project=PROJECT_ID`; list existing alert policies through the Cloud Monitoring API or console, because `gcloud` support for alert policies depends on the installed release track. Validate every command's syntax with `gcloud help` first.

## Failure handling and escalation

No SLOs defined: propose SLIs and SLOs and send them to gcp-reliability-dr for agreement before writing burn-rate alerts. A monitoring tool or MCP server is missing: generate queries and configuration for the user to apply; do not install or configure anything. Conflicting signals from two telemetry sources: report the primary source's answer and the discrepancy once, without an open-ended reconciliation loop.

## Permissions and guardrails

Reading logs and metrics in a named project is Level 1; log reads can expose personal data, so query narrowly and summarize. Creating or changing sinks, buckets, exclusions, alert policies, notification channels, dashboards, uptime checks, Workload Manager evaluations or pipelines is Level 2, as is any BigQuery query over exported logs without a dry run and approval. Without the pack's contract installed, treat each of these changes as needing explicit approval.

## Connection to the pack

The optional `plan-resilience.prompt.md` recipe pairs this skill with gcp-reliability-dr; gcp-solution-architecture and gcp-well-architected-review use it for the operational excellence pillar, and gcp-estate-inspector uses its query rules. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
