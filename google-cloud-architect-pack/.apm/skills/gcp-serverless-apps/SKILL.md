---
name: gcp-serverless-apps
description: "Design serverless application architectures on Google Cloud - Cloud Run services, jobs and worker pools, Cloud Run functions, Firebase App Hosting, event-driven flows with Pub/Sub and Eventarc, private multi-tier designs with load balancer-only ingress and internal-only backends, Direct VPC egress, service identity, IAP, database connectivity and scaling. Use when a web app, API, event handler or background job should run on serverless compute or when reviewing an existing Cloud Run design."
---

# Serverless Applications on Google Cloud

## Purpose and activation

Run application tiers without managing servers while keeping every tier private unless it must be public, every hop authenticated, and costs proportional to traffic. Activate for web apps, APIs, event processors, scheduled jobs, pull consumers, n-tier designs on Cloud Run, or reviews of Cloud Run ingress, egress and identity.

## Scope and exclusions

In scope: choosing the Cloud Run resource type, tier layout, ingress and egress settings, private service-to-service calls, edge integration, identity and secrets, data tier connectivity, eventing, scaling and cold start, regional redundancy, and deployment practices. Container orchestration needs beyond Cloud Run go to gcp-gke-platform. Deploying is Level 2.

## Inputs

Tiers and their exposure (public, internal, partner), protocols (HTTP, gRPC, WebSocket, streaming), request duration and concurrency, background and scheduled work, data stores, residency, latency and cold-start tolerance, traffic shape, existing CI, and identity requirements for users.

## Dependencies and tools

[Is Cloud Run a fit](https://docs.cloud.google.com/run/docs/fit-for-run.md.txt), [Cloud Run networking best practices](https://docs.cloud.google.com/run/docs/configuring/networking-best-practices.md.txt), [secured serverless blueprint](https://docs.cloud.google.com/architecture/blueprints/serverless-blueprint.md.txt), [service identity](https://docs.cloud.google.com/run/docs/securing/service-identity.md.txt), [managing access](https://docs.cloud.google.com/run/docs/securing/managing-access.md.txt). Read-only `gcloud run services describe` for reviews.

## Workflow

1. Resource type: services for request-driven HTTP, gRPC or event-triggered work; jobs for run-to-completion tasks (parallel tasks, retries, timeouts up to days; shorter with GPUs); worker pools for always-on pull consumers such as Kafka or Pub/Sub pull. Cloud Run functions for small event handlers; Firebase App Hosting when a web framework's build and deployment pipeline matters more than container control.
2. Tier layout for a private n-tier design:
   - Tier 1 (presentation or gateway): reachable only through an external Application Load Balancer with Cloud Armor and, for global users, Cloud CDN; set ingress to internal and Cloud Load Balancing so clients cannot bypass the WAF through the default `run.app` URL, or disable the default URL.
   - Tiers 2 to N (internal services): ingress set to internal only; callers reach them through Direct VPC egress, either with all traffic routed through the VPC plus a private Cloud DNS zone that resolves `run.app` to Private Google Access addresses, or through an internal Application Load Balancer.
   - Data tier: Cloud SQL, AlloyDB or Memorystore on private connectivity only (Private Service Connect preferred), with IAM database authentication through the Cloud SQL Auth Proxy or language connectors instead of passwords where supported.
   - Egress firewall rules that allow only tier-to-tier ports and the Google API addresses the connectors need, with rule logging on.
3. Identity: one user-managed service account per service with only the roles it needs; never the Compute Engine default service account. Callers hold `roles/run.invoker` on the exact callee and send an OIDC ID token. Workforce users reach internal apps through IAP enabled on the service or load balancer; customer users authenticate in the application with Identity Platform or Firebase Authentication.
4. Secrets and configuration: Secret Manager secrets mounted as volumes or environment variables by reference; no secrets in images or plain environment values; pinned image digests from Artifact Registry with vulnerability scanning and Binary Authorization for production.
5. Eventing: Pub/Sub push or Eventarc triggers into services with authenticated delivery, dead-letter topics and idempotent handlers; Cloud Tasks for explicit, rate-controlled calls; Cloud Scheduler for cron into jobs or services; Workflows for multi-step orchestration.
6. Scaling and performance: set concurrency from load tests, maximum instances to protect downstream databases and budgets, minimum instances only where cold starts break a latency requirement, CPU allocation and startup CPU boost to taste; pool database connections per instance; containers must listen on `0.0.0.0` on the injected `PORT`.
7. Networking cost and capacity: co-locate services with their data in one region, offload static assets to Cloud CDN, use Direct VPC egress instead of connectors, size the subnet for about two addresses per instance, reuse connections to avoid NAT port exhaustion, and keep the default MTU.
8. Redundancy: Cloud Run is regional and spreads across zones; for region-loss tolerance deploy to several regions behind a global external Application Load Balancer with serverless network endpoint groups, and replicate the data tier to match.
9. Delivery: build with Cloud Build or the existing CI under a federated identity, deploy revisions with traffic splitting for canary and instant rollback, and keep infrastructure in Terraform (`google_cloud_run_v2_service`, `google_cloud_run_v2_job`).
10. Validation plan for the user to run after deployment: direct requests to each `run.app` URL are refused, the custom domain answers through the load balancer, a simulated injection request is blocked by Cloud Armor, the managed certificate is active, and tier-to-tier and database calls succeed over private paths in the logs.

## Output

Tier diagram with ingress and egress settings, service and identity table (service, service account, roles, invokers), data connectivity design, eventing design, scaling parameters with their basis, edge and certificate design, delivery and rollback approach, runtime validation commands and decision records.

## Validation

No service has unrestricted ingress unless a requirement names it; every service has its own service account; every internal call carries an ID token and the callee grants invoker only to that caller; database connections are private; maximum instances protect each downstream. For reviews of a named project: `gcloud run services describe SERVICE --region=REGION --project=PROJECT_ID --format="yaml(spec.template.spec.serviceAccountName,metadata.annotations)"` and `gcloud run services get-iam-policy SERVICE --region=REGION --project=PROJECT_ID`.

## Failure handling and escalation

A requirement that Cloud Run cannot meet (long-lived TCP servers without HTTP, privileged containers, specific kernel features): route to gcp-gke-platform or Compute Engine via gcp-architecture-decisions. Residency that forbids global TLS termination: switch to a regional external Application Load Balancer without CDN and explain the latency trade-off. Container crashes on start: check the listen address and port, then the revision logs.

## Permissions and guardrails

Deploying services, jobs or worker pools, changing ingress, IAM, traffic splits, domain mappings or IAP, and creating load balancers are Level 2. Never make a service public with `allUsers` or by disabling the invoker check unless the requirement says it is a public endpoint, and then only behind Cloud Armor. Without the pack's contract installed, treat every deployment or access change as needing explicit approval.

## Connection to the pack

gcp-solution-architecture uses this skill when serverless compute is selected; gcp-ai-agent-architecture uses it for agents and MCP servers on Cloud Run; gcp-security-reviewer applies its ingress and identity checks. The optional `design-solution.prompt.md` recipe reaches it. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
