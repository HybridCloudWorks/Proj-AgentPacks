# Diagram brief

Fill this in before drawing. It records what the AWS Expert Designer agent settles first: purpose, audience, scope, source of truth, expected fidelity, output format and task type. It also records the answers to the few questions that change the architecture or the visual scope. A question nobody answered becomes a recorded assumption, never a silent default.

## Task

- Task type: design from requirements / reconstruction from source / pattern model / review / repair / layout reflow / export
- Requested by and date:
- Existing diagram affected (path), and whether changing it is approved:

## Purpose and audience

- Decision or conversation the diagram supports:
- Audience, and how familiar they are with AWS:
- Consumption size: slide / document page / screen / print

## Scope

- Organization, OUs and accounts shown:
- Partition, Regions and Availability Zones:
- Environments:
- Layers requested: core flow / security / reliability / observability / governance
- Explicitly out of scope:

## Source of truth

| Source | Path or reference | Format | Standing |
|---|---|---|---|
|  |  | CloudFormation / CDK / Terraform / application code / requirement text / existing diagram | authoritative / reference / unknown |

Steps that would need AWS credentials, such as an uncached CDK context lookup, a Terraform plan against remote state or a live account snapshot, and their approval state:

## Fidelity and output

- Fidelity: conceptual / logical / network-level / source-exact
- Output `.drawio` path:
- Exports, only if required: format, pages, scale, background, output folder
- Generation path: native XML / Mermaid, then normalize / structured data with autolayout, then normalize / importer, then normalize
- Draw.io Desktop path and version, or "not available":

## Questions that change the design

Ask only what changes the architecture or the visual scope: workload flow, account and Region model, data sensitivity, availability target, traffic pattern, connectivity, identity, scale and required output.

| Question | Answer | Assumption recorded if unanswered |
|---|---|---|
|  |  |  |

## Approvals

| Action | Needed for this task? | Granted by, and scope |
|---|---|---|
| Change or delete an existing diagram |  |  |
| Overwrite a source file |  |  |
| Use live AWS or CLI snapshots that require credentials |  |  |
| Publish externally |  |  |
