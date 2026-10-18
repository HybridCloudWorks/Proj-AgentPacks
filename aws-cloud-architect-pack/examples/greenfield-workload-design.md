# Worked example: greenfield shipment-tracking platform

Workflow: `design-aws-workload.prompt.md`. Skills applied: `aws-architecture-foundations`, `aws-workload-and-service-selection`, `aws-data-and-application-patterns`, `aws-networking-hybrid-and-edge`, `aws-security-identity-and-compliance`, `aws-resilience-dr-and-migration`, `aws-operations-observability-and-troubleshooting`, `aws-cost-sustainability-and-finops`, `aws-docs-mcp-and-evidence`, `aws-well-architected-and-frameworks`, `aws-iac-deployment-and-lifecycle`, `aws-architecture-handoff-and-adr`.

The company, figures and accounts are fictional.

## Request

> Larkspur Logistics is building a shipment-tracking platform. Design the production AWS architecture and hand it to our platform team, who build with Terraform. Write the handoff to `handoff/tracking-platform/`.

## Inputs and discovery

The user supplied a requirements brief, the landing-zone account list and the Terraform module catalogue. The session had no AWS account access.

| Input | Value | Label |
|---|---|---|
| Carrier status webhooks | 14 carriers. Average 50 events/s, bursts to 1,500 events/s during carrier batch windows | observed (brief) |
| Customer tracking queries | Web and mobile. 300 req/s steady, 900 req/s peak, p95 under 300 ms | observed (brief) |
| Availability | 99.9% monthly for the query API | observed (brief) |
| Recovery | RTO 1 h, RPO 5 min for shipment data | observed (brief) |
| Data | Consignee names and addresses are personal data. EU customers only; data stays in the EU | observed (brief) |
| Region | eu-west-1 chosen by the business | observed (brief) |
| Accounts | `tracking-prod` and `tracking-nonprod` already vended under Workloads OUs; network hub with a shared Transit Gateway | observed (account list) |
| Team | Six engineers. Strong Java and container skills, some Lambda experience | observed (brief) |
| Budget | EUR 18,000 per month for production, excluding support | observed (brief) |

`aws-architecture-foundations` turned up a gap. The brief does not say which failure scenarios the 1 h RTO covers. AZ failure and data corruption fit inside one Region; losing the whole Region does not. The architect did not block on this. It recorded assumption A-01: Region loss is out of scope for phase 1, and backups are copied to a second EU Region. This was raised as open question Q-01 for the business owner.

## Service selection and integration semantics

Each material choice was compared with at least one plausible alternative (`aws-workload-and-service-selection`):

- **ADR-001, webhook ingestion.** Selected: API Gateway REST API with a direct SQS service integration, then a Lambda consumer. Rejected: an ALB in front of an ECS service that writes straight to the database. The queue absorbs carrier bursts without sizing compute for peak, and carriers are decoupled from database writes.
- **ADR-002, query API compute.** Selected: the existing Java Spring Boot service on ECS with Fargate, behind an ALB, at least two tasks per AZ across three AZs. Rejected: Lambda. JVM start-up latency would need tuning against the p95 target, and the team already runs containers. Revisit if traffic becomes highly spiky.
- **ADR-003, data store.** Selected: DynamoDB with on-demand capacity and point-in-time recovery. Rejected: Aurora PostgreSQL. The hot paths are key lookups: shipment by tracking number, events by shipment, and account plus date range through a secondary index. Conditional writes give idempotency, and ad hoc reporting moves to exports in S3. Aurora's SQL flexibility is not needed in the request path, and write bursts would need provisioned headroom.

`aws-data-and-application-patterns` set the semantics for the asynchronous path:

- **Delivery.** SQS standard queues deliver at least once, so the consumer must handle duplicates. The idempotency key is `carrier_code#carrier_event_id`, enforced by a conditional put.
- **Ordering.** Not guaranteed. Each event carries the carrier's timestamp, and a conditional update keeps the latest status per shipment, so out-of-order events cannot regress it. A FIFO queue was considered. Timestamps and conditional writes already give the needed per-shipment ordering, so FIFO's guarantee was not worth its throughput and cost trade-off. Revisit if a carrier cannot supply reliable timestamps.
- **Retry and poison messages.** The consumer reports partial batch failures. After five receives a message moves to a dead-letter queue. Redrive is a runbook action, not automatic.
- **API contract.** Carrier identity is mutual TLS on the custom domain, with throttling per carrier. The query API is reached through CloudFront and AWS WAF and uses customer tokens from the existing identity provider. The target timeout is 3 s. The ingestion API's integration timeout sits below the shortest carrier retry interval; that interval is still to be confirmed, so it is not-verified.

## Network, identity and protection

From `aws-networking-hybrid-and-edge` and `aws-security-identity-and-compliance`:

- **VPC layout.** One VPC in `tracking-prod`, using a range from the hub IPAM pool. Three private application subnets and three endpoint subnets, one of each per AZ ID. No public subnets. The VPC attaches to the hub Transit Gateway only for shared services.
- **Ingress.** CloudFront with AWS WAF, then an internet-facing ALB whose security group admits only the CloudFront origin-facing managed prefix list.
- **Egress.** The query service makes no outbound internet calls. Gateway endpoints for DynamoDB and S3, plus interface endpoints for ECR, CloudWatch Logs, Secrets Manager and SQS, remove the need for NAT.
- **Placement outside the VPC.** The Lambda consumer runs outside the VPC because it only reaches DynamoDB, SQS and CloudWatch through IAM-authorized endpoints.
- **Identities.** A task role with read-only access to the table. A consumer execution role limited to `PutItem` and `UpdateItem` on the table and receive and delete on the queue. No access keys.
- **Encryption.** A customer managed KMS key, owned by the tracking team, for the table, queues and logs.
- **Personal data.** Consignee fields must never be logged. This is a REQ verification criterion, not just an assumption.

## Resilience, operations and cost

- **Resilience** (`aws-resilience-dr-and-migration`).
  - Multi-AZ by design: Fargate tasks across three AZs, and DynamoDB, SQS and Lambda are Regional services.
  - Point-in-time recovery covers the 5 min RPO for corruption.
  - AWS Backup copies to eu-central-1 cover Region loss as backup and restore only. The designed restore estimate for that case is "hours", which does **not** meet the 1 h RTO. This is recorded against A-01 and Q-01.
- **Operations** (`aws-operations-observability-and-troubleshooting`). The SLI is the ratio of non-5xx responses to all requests at CloudFront, measured over 30 days. Alarms:
  - age of the oldest SQS message over 120 s
  - any message in the dead-letter queue
  - Lambda errors and throttles
  - ALB target 5xx
  - DynamoDB throttled requests

  Runbooks cover dead-letter redrive, carrier certificate rotation and point-in-time restore.
- **Cost** (`aws-cost-sustainability-and-finops`). Cost dimensions: CloudFront requests and transfer, WAF requests, API Gateway requests, SQS requests, Lambda GB-seconds, Fargate vCPU and GB-hours, DynamoDB request units, storage and recovery, interface endpoint hours per AZ, and log ingestion.
  - Monthly units were modelled for steady, peak and replay-after-outage scenarios.
  - Prices were **not** retrieved because no pricing tool was available, so the budget fit is not-verified.
  - Required tags: `application`, `environment`, `owner`, `cost-center`, `data-classification`.
- **Sustainability.** Use ARM64 (Graviton) for Fargate and Lambda if the Java base image builds for arm64. This is designed and still has to be confirmed by a build.

## Evidence

`aws-docs-mcp-and-evidence` used the AWS Knowledge MCP Server, which the host provided.

| Claim | Source | Result | Label |
|---|---|---|---|
| REST APIs support mutual TLS on custom domains | API Gateway developer guide, retrieved 2026-10-18 | Supported | observed |
| SQS event source mapping supports partial batch responses | Lambda developer guide, retrieved 2026-10-18 | Supported | observed |
| All selected services are available in eu-west-1 | AWS Knowledge MCP Region listing, retrieved 2026-10-18 | All listed | observed |
| Account-applied quotas for API Gateway throttling and Lambda concurrency in `tracking-prod` | Not checked; no account access | Unknown | not-verified |
| AWS Backup cross-Region copy for this table configuration | Not checked | Unknown | not-verified |

## Framework check

`aws-well-architected-and-frameworks` found these gaps:

- **Reliability.** Region-loss RTO is unmet (Q-01).
- **Security.** Carrier mTLS onboarding is unproven, because 3 of the 14 carriers have not confirmed they can present client certificates (Q-02).
- **Cost Optimization.** Unpriced (not-verified).
- **Operational Excellence.** The SLO and alarms are designed but not yet built.
- **Performance Efficiency.** Fargate and DynamoDB choices fit the traffic shape (designed).
- **Sustainability.** ARM64 build pending.

None of these is a "pass".

## Handoff

`aws-architecture-handoff-and-adr` wrote the four artifacts to `handoff/tracking-platform/`. The `aws-iac-deployment-and-lifecycle` implications were written into the ADR consequences and into CONSTRAINTS:

- Separate Terraform state per environment.
- The table and the KMS key in a module with `prevent_destroy`.
- Plan review before every apply.
- Point-in-time recovery enabled before any data is loaded.

No Terraform was written or applied.

## Completion report

Pack: aws-cloud-architect. Date: 2026-10-18.

Outcome: the architecture and handoff are designed. Nothing is deployed, priced or live-verified, and the Region-loss RTO needs a business decision.

### scope_and_inputs

The tracking-platform production design for `tracking-prod` in eu-west-1. Inputs were the requirements brief, the landing-zone account list and the Terraform module catalogue (observed). Authority covered writing files to `handoff/tracking-platform/` only. No AWS account access.

### business_outcomes_and_requirements

- Carrier events are ingested reliably at bursts of 1,500/s.
- Customers can query tracking at 99.9% availability with p95 under 300 ms.
- RTO 1 h and RPO 5 min.
- Data stays in the EU, and personal data is protected.

These are recorded as FR-01 to FR-04 and NFR-01 to NFR-09 in REQ.md.

### source_facts_and_evidence

- Brief and account-list facts: observed.
- Service capabilities and Region listing: observed through the AWS Knowledge MCP Server on 2026-10-18.
- Account quotas and backup-copy support: not-verified.

### framework_alignment

Six pillars reviewed, with gaps in Reliability (Q-01), Security (Q-02), Cost (unpriced), Operational Excellence (not built) and Sustainability (ARM64 build pending). This is not a formal Well-Architected Tool review.

### proposed_architecture

- CloudFront with WAF in front of the ALB and ECS Fargate across three AZs.
- API Gateway (mTLS) to SQS to a Lambda consumer, with a dead-letter queue.
- DynamoDB on demand with point-in-time recovery, exports to S3, and AWS Backup copies to eu-central-1.
- A private-only VPC with endpoints and no NAT.

All of this is designed. TOPOLOGY ids run from `svc-cdn` to `svc-backup`.

### assumptions_and_tradeoffs

- A-01: Region loss is out of scope for phase 1 (owner: business, Q-01).
- ADR-001: SQS standard over FIFO.
- ADR-002: Fargate over Lambda for the query API.
- ADR-003: DynamoDB over Aurora.

Each ADR records the rejected option and its revisit trigger.

### implementation_and_operating_implications

- Terraform modules per environment, with protected stateful resources and plan review before apply.
- Deploy order: KMS key, then table, then queues, then the ingestion API, then the query service, then the edge.
- Runbooks for redrive, certificate rotation and restore. Alarms as listed above.
- Owners: the tracking team for the workload and the platform team for the network hub.

### security_resilience_cost_and_sustainability

- Security (designed): federated access only, least-privilege roles, a customer managed KMS key, no personal data in logs, WAF at the edge.
- Resilience (designed): multi-AZ, with the Region-loss RTO unmet.
- Cost: dimensions modelled, prices not-verified.
- Sustainability: ARM64, pending a build.

### output_files

| File | Purpose | Check run | Label |
|---|---|---|---|
| `handoff/tracking-platform/REQ.md` | Requirements, verification criteria, Q-01 and Q-02 | Section completeness reviewed by the architect | designed |
| `handoff/tracking-platform/TOPOLOGY.json` | Accounts, VPC, subnets, services, flows, failure domains | Parsed as JSON | structurally-validated |
| `handoff/tracking-platform/CONSTRAINTS.json` | Region, tags, encryption, IAM, budget, recovery | Parsed as JSON | structurally-validated |
| `handoff/tracking-platform/ADR.md` | ADR-001 to ADR-003 | Every ADR has alternatives and a revisit trigger | designed |

The optional pack hook `hooks/architecture-review.ps1` confirmed that all four files are present. It checks presence only, not content quality.

### live_or_external_checks

- AWS Knowledge MCP documentation and Region lookups: executed (observed).
- Account quotas, pricing, deployment, carrier mTLS and the restore test: not executed (not-verified).

### unresolved_risks

- Q-01: Region-loss RTO (owner: business owner).
- Q-02: carrier certificate capability (owner: integrations lead).
- Budget fit is unpriced (owner: FinOps).
- Account quotas are unchecked (owner: platform team).

### next_safe_action

The business owner answers Q-01. In parallel, the platform team checks account quotas through Service Quotas with read-only access. No deployment is authorized.
