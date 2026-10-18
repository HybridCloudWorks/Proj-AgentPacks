# Worked example: CDK reconstruction blocked on credentials and an overwrite

Synthetic scenario. Account, domain and construct names are fictional. Workflow prompt: `diagram-from-infrastructure-code`. This example shows a blocked, unverified outcome.

## Request

"Regenerate our production diagram from the CDK app in `infra/` and update `architecture/prod.drawio`."

Two parts of this request need authority the agent does not have:

- "Update" changes an existing diagram, and the agent asks before changing or overwriting one.
- The CDK app cannot be synthesized without a live, credentialed context lookup. That is explained below.

## What the source shows

`aws-architecture-design` in source-derived mode inventoried the app before drawing.

| Location | Construct | What it tells the diagram | Label |
|---|---|---|---|
| `infra/bin/app.ts` | `new OrdersStack(app, 'OrdersProd', { env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: 'eu-west-1' } })` | One stack, eu-west-1; account taken from the environment | observed (Region); account unresolved |
| `infra/lib/orders-stack.ts` | `ec2.Vpc.fromLookup(this, 'SharedVpc', { vpcName: 'shared-prod' })` | The VPC is not defined here. Subnets, AZs and CIDR come from a lookup | unresolved |
| same | `ecs_patterns.ApplicationLoadBalancedFargateService(this, 'Api', { vpc, publicLoadBalancer: true, desiredCount: 2, ... })` | Public ALB in front of a Fargate service with two tasks | observed for the explicit properties; the subnets, security groups and target group the construct creates are inferred until synthesized |
| same | `rds.DatabaseCluster(this, 'Db', { engine: auroraPostgres(...), writer: ..., readers: [...], vpc, vpcSubnets: { subnetGroupName: 'data' } })` | Aurora PostgreSQL with a writer and one reader, in a subnet group named `data` that must exist in the looked-up VPC | observed (cluster shape); placement unresolved |
| same | No `credentials` property on the cluster | The construct's default credential handling (a generated secret) applies | inferred: confirm in the synthesized template |
| same | `route53.HostedZone.fromLookup(...)` and an `ARecord` aliased to the ALB | DNS name for the API | observed (record); zone details from a lookup |
| `infra/cdk.context.json` | Has a cached hosted-zone entry, but no VPC-provider entry for `shared-prod` in this account and Region | `cdk synth` would perform the VPC lookup with AWS credentials, or fail without them | observed |

CDK logical IDs carry hash suffixes, and physical names are assigned at deployment. Without the synthesized template and the deployed stack, the logical-to-physical mapping is labeled uncertain.

## What the existing diagram adds

`architecture/prod.drawio` shows CloudFront and an AWS WAF web ACL in front of the ALB. Neither appears anywhere in the CDK app. They may live in another stack or repository, may have been created in the console, or may have been removed. The agent cannot tell which. It does not silently delete them, and it does not silently keep them.

## What the agent did, and did not do

- Did not run `cdk synth`. The uncached `Vpc.fromLookup` makes synthesis a live call to the production account with credentials, and nobody authorized that.
- Did not change `architecture/prod.drawio`.
- Wrote a draft to a new path, `architecture/prod.draft.drawio`, using `drawio-core-generation`, `aws-icons-and-visual-language` and `aws-xml-authoring`. The draft contains:
  - a VPC boundary labeled "VPC shared-prod (looked up; subnets, AZs and CIDR unresolved)"
  - the ALB, Fargate service and Aurora cluster inside the VPC, with a note "subnet placement unresolved until synthesis"
  - the Route 53 record → ALB edge, labeled observed
  - no AZ or subnet containers, because drawing guessed boundaries would imply placement the evidence does not support
  - no CloudFront or WAF; the companion report lists both as unresolved
- Ran the `diagram-validation-and-evidence` structural checks on the draft. They passed.
- Looked for Draw.io Desktop at `C:\Program Files\draw.io\draw.io.exe`, in the user installation directory and on PATH, and found none. No render.

## Decisions requested

1. **Synthesis.** Choose one:
   - Approve `cdk synth` against the production account with a named profile. The effect is a read-only context lookup of VPC `shared-prod` and its subnets in eu-west-1, cached into `cdk.context.json`.
   - Supply a `cdk.context.json` that already holds the lookup.
   - Accept the draft with placement unresolved.
2. **Overwrite.** Replace `architecture/prod.drawio` with the result, or keep the draft as a separate file for review.
3. **CloudFront and WAF.** Say where they are defined, so the diagram can show them as observed or remove them on evidence.

## Completion report

Pack: aws-expert-designer.

Outcome: blocked on three decisions. A draft was written to a new file, and nothing was overwritten.

### scope_and_inputs

- Task: reconstruction from a CDK app. The requested update of an existing diagram is pending approval.
- Inputs: `infra/bin/app.ts`, `infra/lib/orders-stack.ts`, `infra/cdk.context.json` and `architecture/prod.drawio` — observed.
- Not available: the synthesized template, deployed stack outputs, and the VPC lookup result — not-verified.

### source_facts

- One stack in eu-west-1; a public ALB with a Fargate service of two tasks; Aurora PostgreSQL with a writer and one reader in subnet group `data`; a Route 53 alias record to the ALB — observed.
- The VPC comes from an uncached lookup — observed.
- The existing diagram shows CloudFront and WAF, which the CDK app does not define — observed.

### assumptions_and_design_decisions

- Construct-created subnets, security groups, target group and generated database secret are expected but unconfirmed — inferred.
- AZ and subnet containers were left out of the draft rather than guessed — designed.

### output_files

- `architecture/prod.draft.drawio`: new draft, uncompressed, one page.
- `architecture/prod.draft.md`: new companion report with the table above and the open questions.
- `architecture/prod.drawio`: unchanged.

### structural_checks

- Draft parse, root cells, unique IDs, parents, edges with icon endpoints, no compression and the AWS4 namespace — structurally-validated.

### visual_checks

- Draw.io Desktop not found, so no render and no visual inspection — not-verified.

### live_or_external_checks

- `cdk synth` and the VPC lookup were not run, pending approval to use production credentials — not-verified.

### unresolved_risks

- Subnet placement, AZ count and CIDR are unknown. The draft must not be presented as the production network — not-verified.
- CloudFront and WAF may exist outside this app. Removing them from the diagram without evidence could hide the real ingress path — not-verified.

### next_safe_action

- The user answers decisions 1 to 3. Until then the only safe step is to review the draft and its companion report. Running synthesis or replacing `architecture/prod.drawio` waits for explicit approval.
