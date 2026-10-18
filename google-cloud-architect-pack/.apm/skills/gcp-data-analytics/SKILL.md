---
name: gcp-data-analytics
description: "Design Google Cloud data and analytics platforms - ingestion and streaming, batch and stream processing, BigQuery warehouse and lakehouse with Apache Iceberg, Spark, governance with Knowledge Catalog, lineage and impact analysis, fine-grained access, data products and in-database AI. Use when designing or reviewing a warehouse, lakehouse, data mesh, streaming pipeline, cross-cloud analytics or data governance on Google Cloud."
---

# Google Cloud Data and Analytics Platforms

## Purpose and activation

Deliver trustworthy, governed data to analysts, applications and AI with predictable cost, and make every data movement and access decision explainable. Activate for warehouses, lakehouses, data meshes, streaming analytics, ETL or ELT design, cross-cloud or on-premises federation, governance and lineage, or BigQuery cost and performance reviews.

## Scope and exclusions

In scope: ingestion, processing engines, storage formats and layout, BigQuery design, governance and catalog, lineage and impact analysis, access control, data quality, sharing, cost and performance, and when to run ML or generative AI in the data platform. Operational OLTP database choice belongs to gcp-architecture-decisions; agent and model serving design to gcp-ai-agent-architecture. Running billable queries or creating datasets is Level 2.

## Inputs

Sources (databases, files, SaaS, events, other clouds), volumes and velocity, latency needs (batch, micro-batch, streaming), consumers and their tools, data classification and residency, domain ownership model, retention, existing pipelines and skills (SQL, Spark, Beam, Python), and cost model preference (on-demand or capacity).

## Dependencies and tools

[Data mesh architecture](https://docs.cloud.google.com/architecture/data-mesh.md.txt), [BigQuery ETL versus ELT](https://docs.cloud.google.com/bigquery/docs/load-transform-export-intro.md.txt), [BigQuery cost best practices](https://docs.cloud.google.com/bigquery/docs/best-practices-costs.md.txt), [BigQuery performance best practices](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview.md.txt), [secured data warehouse blueprint](https://docs.cloud.google.com/architecture/blueprints/confidential-data-warehouse-blueprint.md.txt), [hybrid and borderless analytics pattern](https://docs.cloud.google.com/architecture/hybrid-multicloud-patterns-and-practices/analytics-hybrid-multicloud-pattern.md.txt). Read-only `bq show` and `bq ls`, and `bq query --dry_run` to estimate bytes. A Data Lineage MCP server or the Data Lineage API when the client already has access.

## Workflow

1. Classify the workload: analytical warehouse, open lakehouse shared by several engines, streaming analytics, operational analytics on transactional data, or a data mesh of domain-owned products. Most designs mix these; name the dominant one.
2. Ingestion: Pub/Sub for events (Managed Service for Apache Kafka when Kafka protocol compatibility is required), Datastream for change data capture from operational databases, the BigQuery Data Transfer Service and Storage Transfer Service for scheduled loads, the BigQuery Storage Write API for high-throughput streaming inserts, and federated or external tables when data must stay where it is (including other clouds through BigQuery Omni or open catalogs).
3. Processing: SQL-first ELT inside BigQuery (scheduled queries, Dataform, continuous queries for streaming SQL) for most transformations; Dataflow (Apache Beam) for unified batch and stream pipelines with complex event-time logic; Managed Service for Apache Spark for Spark code and open-format processing; orchestration with Managed Airflow (Cloud Composer) for pipelines with many dependencies, or Workflows for light orchestration.
4. Storage and format: BigQuery managed storage for performance and simplicity; Apache Iceberg tables on Cloud Storage with Lakehouse for Apache Iceberg as the shared catalog when several engines (BigQuery, Spark, others) must read and write the same tables; Parquet for interchange. Partition by date or ingestion time and cluster on frequent filters; set table and partition expiration from retention rules.
5. Governance: register assets in Knowledge Catalog with business metadata and data quality rules; use data profiling and Sensitive Data Protection discovery; apply BigQuery policy tags for column-level security, row access policies, dynamic data masking and authorized views or datasets; keep raw, curated and published zones in separate datasets or projects with separate access; put sensitive projects inside a VPC Service Controls perimeter (see gcp-security-controls).
6. Lineage and impact: enable Data Lineage for BigQuery and supported pipelines. Before changing, pausing or deleting a table, run a downstream impact analysis: resolve the fully qualified name (`bigquery:project.dataset.table`), find the dataset location, search downstream lineage to a sensible depth, separate direct from indirect dependents and identify the processes (views, scheduled queries, pipelines) that propagate the data. Use upstream lineage to debug data quality.
7. Sharing and products: Analytics Hub listings and data clean rooms for cross-team or cross-organization sharing; data products with owners, SLAs, schemas and versioning in a mesh.
8. In-platform AI: BigQuery ML and AI functions for forecasting, anomaly detection, classification and text generation next to the data; BigQuery DataFrames for pandas-style Python at warehouse scale; vector search in BigQuery or AlloyDB when retrieval stays close to governed data. Model calls from SQL incur model charges as well as query charges.
9. Cost and performance: choose on-demand pricing for spiky or small usage and capacity (editions with reservations and autoscaling slots) for steady heavy usage; require partition filters on large tables; avoid `SELECT *`; use materialized views and BI Engine for repeated dashboards; set per-user or per-project custom quotas; dry-run queries to estimate bytes before running them.
10. Residency and locations: keep datasets, buckets, processing and lineage in locations that satisfy residency. A BigQuery query normally runs in one location, so joining data held in different locations needs replication, transfer or a feature that supports cross-location queries; verify current support before designing on it.

## Output

Data platform diagram (sources, ingestion, zones, processing, serving, consumers), ingestion and processing choices with alternatives, storage layout and table design rules, governance and access model, lineage and impact procedure, sharing model, cost model with pricing choice, residency map and decision records.

## Validation

Every source has an ingestion path and an owner; every sensitive column has a policy tag or a recorded reason; every large table has partitioning and expiration settings; impact analysis was run before any proposed destructive change; query cost estimates come from dry runs. Read-only checks on a named project: `bq ls --project_id=PROJECT_ID`, `bq show --format=prettyjson PROJECT_ID:DATASET`, and `bq query --use_legacy_sql=false --dry_run 'SQL'`.

## Failure handling and escalation

Lineage unavailable for a source system: list the dependents found from other evidence (views, scheduled queries, IaC) and mark the impact analysis incomplete. Unknown data rights or classification: stop before designing access and escalate to the data owner. A query whose dry run exceeds the agreed byte budget: return the estimate and wait.

## Permissions and guardrails

`bq show`, `bq ls` and dry runs are Level 1; running queries, loads, exports, copies, deletes, dataset or reservation changes, policy tag or row-policy changes, and Analytics Hub publishing are Level 2. Never read production data only to make an example look realistic; use schemas and synthetic samples. Without the pack's contract installed, treat every billable query or data change as needing explicit approval.

## Connection to the pack

gcp-solution-architecture uses this skill for data-centric workloads, gcp-ai-agent-architecture for retrieval and data agents, and gcp-migration-planning for warehouse and database migrations. The optional `design-solution.prompt.md` recipe reaches it. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
