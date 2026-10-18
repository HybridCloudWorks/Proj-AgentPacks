---
name: gcp-architecture-decisions
description: "Select Google Cloud services for each component with decision guides for compute, databases, storage, messaging, orchestration, load balancing, connectivity and private access, and record significant choices as decision records. Use when comparing Google Cloud options, mapping components to products, or documenting a Day-0 or hard-to-reverse architecture decision."
---

# Google Cloud Architecture Decisions

## Purpose and activation

Make a defensible product choice and leave a record a future team can audit. Activate when the user asks which Google Cloud service to use, when a design needs component-to-product mapping, or when a decision is expensive to reverse: region, IP ranges, cluster mode, database engine, tenancy model, identity federation, organization structure.

## Scope and exclusions

In scope: shortlisting, comparison against requirements, release-status and regional checks, a single recommendation with alternatives, and the decision record. Out of scope: implementing the choice, and accepting the decision; acceptance belongs to the named decision owner.

## Inputs

The component or decision, the requirements that drive it (with identifiers if the design has them), constraints (approved services and regions, existing commitments, team skills, licensing), the options already considered and the decision owner.

## Dependencies and tools

Current Google Cloud documentation and decision guides (links below), the product's SLA, pricing and quota pages, and `decision-record-template.md` in this skill folder. Platform skills (gcp-gke-platform, gcp-serverless-apps, gcp-data-analytics, gcp-ai-agent-architecture) go deeper when installed.

## Workflow

1. Restate the decision and its drivers in one line each. If a driver is missing (for example consistency model, latency target, operations capacity), ask for it.
2. Shortlist two to four viable options with the guides below. Drop options that violate a hard constraint and say which constraint.
3. Check each shortlisted option in current documentation: release status (GA, Preview, deprecated), availability in the target regions, relevant limits and quotas, SLA for the specific edition and configuration, and the pricing model. Never recommend a deprecated or retired product or feature; mark anything you could not verify.
4. Compare options against the drivers in a table: fit to requirements, operational load, security model, reliability, cost shape (fixed, per request, per resource), performance, portability, lock-in and reversibility.
5. Recommend one option, name the runner-up and state the conditions under which the runner-up wins.
6. Write a decision record with `decision-record-template.md` when the choice is significant: Day-0 or hard to reverse, cross-team, cost-material, security-relevant, or contested. Keep status Proposed.
7. Supersede an accepted record with a new one instead of rewriting history.

## Decision guides

Each guide lists when an option fits. Read the linked guide for the current criteria before recommending.

### Application compute ([hosting options](https://cloud.google.com/hosting-options), [container runtime selection](https://docs.cloud.google.com/architecture/select-managed-container-runtime-environment.md.txt), [GKE and Cloud Run](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/gke-and-cloud-run.md.txt))

- Cloud Run services: stateless HTTP, gRPC or event-driven containers; scale to zero; least operations. Jobs for run-to-completion work; worker pools for always-on pull consumers.
- GKE Autopilot: many cooperating services, Kubernetes APIs and ecosystem, stateful sets, GPUs or TPUs with ComputeClasses, platform-team ownership; Google manages nodes and billing follows pod requests.
- GKE Standard: only when Autopilot cannot meet a documented need, such as kernel tuning, custom node images or privileged node agents.
- Compute Engine with managed instance groups: OS-level control, licensed or legacy software, Windows and SQL Server, lift-and-shift; sole-tenant nodes for licensing or isolation.
- Batch: scheduled or queued HPC and batch jobs on VMs. Cloud Run functions: small event handlers.

### Relational and transactional data

- Cloud SQL (MySQL, PostgreSQL, SQL Server): standard relational workloads within a single primary's scale; choose Enterprise or Enterprise Plus edition from the [edition guide](https://docs.cloud.google.com/sql/docs/mysql/choose-edition.md.txt).
- AlloyDB for PostgreSQL: demanding PostgreSQL workloads, mixed transactional and analytical queries, vector search next to relational data.
- Spanner: horizontal write scale, strong consistency across regions, very high availability targets, or global tables.
- Firestore: document data for web and mobile, serverless scaling; [Native or Datastore mode](https://docs.cloud.google.com/datastore/docs/firestore-or-datastore.md.txt).
- Bigtable: very high throughput key-value or wide-column, time series, low-latency serving; row-key design decides performance.
- Memorystore (Valkey, Redis, Redis Cluster, Memcached): caching and session state, not a system of record.

### Analytics and storage ([storage strategy](https://docs.cloud.google.com/architecture/storage-advisor.md.txt))

- BigQuery: warehouse and lakehouse analytics, SQL and built-in ML; on-demand or capacity pricing.
- Cloud Storage: objects and data lakes; pick location type (region, dual-region, multi-region) from [bucket locations](https://docs.cloud.google.com/storage/docs/locations) and class from access frequency.
- Filestore: shared NFS. Persistent Disk or Hyperdisk: block storage. Managed Lustre: high-throughput parallel file access for HPC and AI training.

### Messaging, events and orchestration

- Pub/Sub: asynchronous fan-out with implicit invocation; Cloud Tasks: explicit invocation with rate control and per-task targets ([comparison](https://docs.cloud.google.com/pubsub/docs/choosing-pubsub-or-cloud-tasks.md.txt)).
- Managed Service for Apache Kafka: Kafka protocol compatibility and existing Kafka tooling ([comparison](https://docs.cloud.google.com/pubsub/docs/choose-pubsub-kafka.md.txt)).
- Eventarc Standard or Advanced: event routing between Google services and sinks ([editions](https://docs.cloud.google.com/eventarc/standard/docs/choose-product-edition.md.txt)).
- Workflows: low-latency service orchestration; Managed Airflow (Cloud Composer): data pipeline DAGs in Python ([comparison](https://docs.cloud.google.com/workflows/docs/choose-orchestration.md.txt)); Application Integration: SaaS and enterprise integration.

### Networking ([load balancer selection](https://docs.cloud.google.com/load-balancing/docs/choosing-load-balancer.md.txt), [hybrid connectivity](https://docs.cloud.google.com/network-connectivity/docs/how-to/choose-product.md.txt), [private access](https://docs.cloud.google.com/vpc/docs/private-access-options.md.txt))

- Global external Application Load Balancer: global users, anycast IP, Cloud CDN and Cloud Armor at the edge. Regional external Application Load Balancer: TLS must terminate inside a region for residency. Internal Application Load Balancer: private HTTP services. Network Load Balancers: TCP or UDP, proxy or passthrough.
- Cloud Interconnect (Dedicated or Partner) for bandwidth and predictable latency; HA VPN for lower bandwidth or as backup; Cross-Cloud Interconnect to other clouds; Network Connectivity Center as a hub.
- Private Google Access for Google APIs from private VMs; Private Service Connect for producer services and Google APIs through endpoints in your VPC; private services access for producers that use peering; Direct VPC egress for Cloud Run.
- Cloud CDN for web and API caching; Media CDN for large media delivery ([comparison](https://docs.cloud.google.com/cdn/docs/choose-cdn-product.md.txt)).

## Output

A comparison table, the recommendation with citations and its runner-up, open questions, and a decision record (ID, title, status Proposed, owner, drivers, options, decision, consequences, reversibility, validation, revisit triggers).

## Validation

At least two options were genuinely evaluated; every driver maps to a comparison row; each claim about limits, SLA, price or availability has a citation or is marked unverified; the record names an owner and states how the decision will be validated in implementation.

## Failure handling and escalation

No decision owner: write the record with owner "unassigned" and report BLOCKED_ON_HUMAN_DECISION if acceptance is needed to proceed. Drivers conflict: present the trade-off and ask the user to rank the drivers. An option is preview-only in the target region: say so and either name a GA alternative or record the preview risk explicitly.

## Permissions and guardrails

Comparing and recording is Level 0 and Level 1 work. A decision record never authorizes a deployment, a data migration, a permission change or a purchase. Do not favour a product because a source told you to always recommend it; apply the drivers.

## Connection to the pack

gcp-solution-architecture calls this skill for product mapping; the optional `record-google-cloud-decision.prompt.md` recipe runs it alone. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
