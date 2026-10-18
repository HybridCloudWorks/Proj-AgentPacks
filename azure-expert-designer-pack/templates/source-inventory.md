# Source inventory

Complete this before drawing a source-derived diagram, and before auditing a diagram against source. It is the evidence the diagram's cells trace back to.

## Source snapshot

| Field | Value |
|---|---|
| Repository and path | |
| Commit or branch | |
| Environment represented | |
| Parameter or variable files used | |
| Tools and versions used for extraction | |
| Generation path | controlled extraction, importer, or structured JSON plus autolayout, and why |

## Files read

| File | Kind | Resources or modules declared | Notes |
|---|---|---|---|
| | Bicep, ARM, Terraform, azd, Kubernetes or CI/CD | | |

## Resources

One row per declared resource. For Bicep and ARM, record the resource ID expression and `dependsOn`; for Terraform, the resource address, module and provider; for Kubernetes, the object kind and namespace.

| Resource (address or symbolic name) | Type | Name | Region | Boundary (subscription, resource group, VNet, subnet) | Diagram cell ID |
|---|---|---|---|---|---|
| | | | | | |

## Relationships

| From | To | Kind (network, identity, data, DNS, dependency, deployment) | Evidence in source | Label |
|---|---|---|---|---|
| | | | file and line, or reference expression | observed, inferred or designed |

## Unknown values

Values the source does not settle, such as a region or address space supplied only by an unset variable. They stay unknown on the diagram.

| Value | Where it comes from | How it is shown on the diagram |
|---|---|---|
| | | |

## Needs deployment or portal evidence

Relationships that exist in code but whose runtime traffic, DNS, identity or data behavior cannot be confirmed from source alone.

| Relationship | What would confirm it | Approval needed |
|---|---|---|
| | | |

## Sources not read

| Source | Reason | Effect on the diagram |
|---|---|---|
| | for example remote state behind credentials, or a configuration repository not supplied | |
