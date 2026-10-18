# Worked example: event-ingest service derived from Terraform

Synthetic scenario. Repository, bucket and resource names are fictional. Workflow prompt: `diagram-from-infrastructure-code`.

## Request

"Draw the production architecture of `ingest-service` from its Terraform, and show what is real and what is guessed." Scope: the `prod` environment. Output: a new file, `architecture/ingest-prod.drawio`. The user also allows reading `src/` to confirm calls the Terraform cannot show.

## Inventory before drawing

This is `aws-architecture-design` in source-derived mode.

| File | Contents relevant to the diagram |
|---|---|
| `infra/envs/prod/main.tf` | `provider "aws"` with `region = var.region`; `backend "s3"` (remote state); modules `network` and `api` |
| `infra/envs/prod/terraform.tfvars` | `region = "eu-central-1"`, `azs = ["eu-central-1a", "eu-central-1b"]`, `single_nat_gateway = true` |
| `infra/modules/network/main.tf` | `aws_vpc.this`; `aws_subnet.public` and `aws_subnet.private` with `for_each = toset(var.azs)`; `aws_internet_gateway.this`; `aws_nat_gateway.this` with `count = var.single_nat_gateway ? 1 : length(var.azs)`; per-AZ `aws_route_table.private`; `aws_vpc_endpoint.dynamodb` of type `Gateway` on the private route tables |
| `infra/modules/api/main.tf` | `aws_apigatewayv2_api.http` (HTTP API); `aws_apigatewayv2_integration.ingest` targeting `aws_lambda_function.ingest.invoke_arn`; both functions with `vpc_config` on the private subnets; `aws_sqs_queue.events` with a redrive policy to `aws_sqs_queue.events_dlq`; `aws_lambda_event_source_mapping.worker`; `aws_dynamodb_table.events`; IAM policies |
| `.github/workflows/deploy.yml` | runs Terraform with `-var-file=envs/prod/terraform.tfvars` and sets `TF_VAR_queue_kms_key_arn` from a repository secret |

Nothing was run. `terraform init`, `plan` and `graph` all need the S3 backend, which needs credentials. Reading the source was enough for this scope, so the agent did not ask for credentials. The report notes that a plan would confirm the resource counts.

`drawio-core-generation` routing: the upstream Draw.io skill's Terraform importer is not installed here. That was detected, not assumed. The agent therefore used a controlled extraction: it parsed the HCL into a node and edge list, then wrote native XML. Twelve primary nodes is below the roughly 15 at which structured generation with autolayout becomes the better starting point.

## Evidence matrix (excerpt)

| Element or relationship | Source | Label |
|---|---|---|
| VPC with two public and two private subnets in eu-central-1a and eu-central-1b | `network/main.tf` `for_each`; azs in tfvars; the pipeline uses that tfvars file | observed |
| One NAT gateway, in public subnet eu-central-1a | `count` expression with `single_nat_gateway = true`; `subnet_id = aws_subnet.public[var.azs[0]].id` | observed |
| Both private route tables send 0.0.0.0/0 to that NAT gateway | `aws_route_table.private` routes to `aws_nat_gateway.this[0]` | observed |
| HTTP API → ingest function | `aws_apigatewayv2_integration.ingest` | observed |
| Ingest function → SQS `events` | IAM `sqs:SendMessage` on the queue ARN; `QUEUE_URL` environment variable; `src/ingest/handler.py` calls `send_message` | observed in source; runtime traffic not proven |
| SQS API calls leave through the NAT gateway | VPC-attached function, no SQS interface endpoint declared, private default route to NAT | inferred |
| SQS `events` → worker function | `aws_lambda_event_source_mapping.worker`; Lambda polls the queue | observed |
| SQS `events` → DLQ after 5 receives | `redrive_policy` `maxReceiveCount = 5` | observed |
| Worker → DynamoDB `events` through the gateway endpoint | `src/worker/handler.py` calls `put_item`; the endpoint route is on both private route tables | path inferred from routes |
| KMS key for the queue | `kms_master_key_id = var.queue_kms_key_arn`; value comes from a pipeline secret | unresolved: owning account unknown |

Cell IDs are derived from resource addresses and normalized for stable regeneration. For example, `module.network.aws_subnet.private["eu-central-1a"]` becomes `module_network__aws_subnet_private__eu_central_1a`.

## Drawing decisions

- `aws-architecture-patterns`, serverless and VPC checks:
  - API Gateway invokes Lambda through the Lambda service, not through the VPC. Each function is therefore drawn once, parented to the VPC across the two private subnets, with the label "VPC-attached (ENIs in private subnets a and b)". The API edge ends on the function icon.
  - Queue-to-worker delivery is asynchronous and drawn dashed, labeled "async, polled by Lambda".
- `aws-layout-and-composition`:
  - Left to right: clients → HTTP API → ingest function → SQS → worker → DynamoDB. AZ a and AZ b are stacked rows inside the VPC.
  - Egress from private subnet b to the NAT gateway in AZ a is drawn and labeled "cross-AZ to NAT (single_nat_gateway = true)". It is a cost-bearing path and an AZ dependency.
  - The SQS-through-NAT path is labeled "egress via NAT: SQS API (no interface endpoint)".
- `aws-icons-and-visual-language`: AWS4 resource icons for API Gateway, Lambda, SQS, DynamoDB and KMS. The NAT gateway, internet gateway and gateway endpoint use AWS4 resource shapes from the installed library. Clients use a neutral shape. The KMS key sits in the auxiliary frame with a dashed outline and the label "ARN supplied at deploy; owning account unknown".

## Validation

- Structural checks: the parse, root cells, 38 unique IDs, parents, 13 edges with icon endpoints, no compression and the AWS4 namespace were all checked, and all passed.
- Semantic check: every row of the evidence matrix maps to a cell or an edge. No cell lacks a source row.
- Visual check: `drawio-render-export-and-review` looked for Draw.io Desktop at `C:\Program Files\draw.io\draw.io.exe`, at `%LOCALAPPDATA%\Programs\draw.io\draw.io.exe` and on PATH, and found none. Rendering was not run.

## Completion report

Pack: aws-expert-designer.

Outcome: diagram delivered; visual check not run.

### scope_and_inputs

- Task: reconstruction from Terraform, `prod` environment only; a new file.
- Inputs: `infra/envs/prod/*`, `infra/modules/network`, `infra/modules/api`, `.github/workflows/deploy.yml`, and the handlers in `src/ingest` and `src/worker` — observed.
- Not available: Terraform state and plan output, and the deployed account — not-verified.

### source_facts

- Two AZs, one NAT gateway in eu-central-1a, both private default routes through it — observed.
- API → ingest function, SQS → worker, SQS → DLQ, and a DynamoDB gateway endpoint on the private route tables — observed.
- Ingest sends to SQS and the worker writes to DynamoDB, both seen in code — observed.

### assumptions_and_design_decisions

- SQS API traffic leaves through the NAT gateway because no interface endpoint is declared — inferred.
- Worker traffic to DynamoDB uses the gateway endpoint route — inferred.
- Functions drawn once at VPC level, not once per subnet — designed.
- Controlled extraction used instead of an importer, which is not installed — designed.

### output_files

- `architecture/ingest-prod.drawio`: new, uncompressed, one page.
- `architecture/ingest-prod.md`: new companion report with the full evidence matrix.

### structural_checks

- Parse, root cells, IDs, parents, edge endpoints, compression and namespace — structurally-validated.

### visual_checks

- Draw.io Desktop not found in the three locations checked. No render and no visual inspection — not-verified.

### live_or_external_checks

- No `terraform plan`, state read or AWS API call. Deployed counts and routes may differ from the source if anything changed outside Terraform — not-verified.

### unresolved_risks

- The single NAT gateway makes egress from both AZs depend on eu-central-1a and carries cross-AZ charges for AZ b. This is drawn, but it is a design concern for the owners — observed.
- The account that owns the queue's KMS key is unknown. If it is another account, the diagram is missing an account boundary — not-verified.

### next_safe_action

- Open the file in Draw.io, or install Draw.io Desktop, and run the export review. Ask the platform team which account owns `queue_kms_key_arn`.
