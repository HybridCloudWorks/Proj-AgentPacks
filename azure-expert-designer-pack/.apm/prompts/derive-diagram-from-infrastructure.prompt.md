---
description: "Derive an Azure diagram from Bicep, ARM, Terraform, Azure Developer CLI or Kubernetes source"
agent: azure-expert-designer
---

# Derive an Azure diagram from infrastructure source

## Inputs

- The repository or folders that hold Bicep, ARM, Terraform, Azure Developer CLI, Kubernetes manifests or CI/CD definitions, and the commit or branch to represent.
- The environment to show, and the parameter or variable files that define it.
- Diagram purpose, audience, fidelity and output location.

Do not run commands that need Azure credentials, a remote state backend or network access to registries (for example `az`, `azd`, or `terraform init` with a backend) unless the user approves that specific use.

## Workflow

1. Record a brief: purpose, audience, scope, source of truth (paths and commit), fidelity, output format, and that the task is reconstruction.
2. Apply `azure-architecture-design` in source-derived mode. Inventory files before drawing. Parse declared resources, modules, variables, outputs, dependencies, names, regions, providers and network references. For Bicep and ARM use resource IDs and `dependsOn`; for Terraform use resource addresses, references, modules, providers and backend context; treat Kubernetes objects as workload evidence, not a complete Azure network model.
3. Preserve unknown values, such as a region or address space supplied only by an unset variable, and label them as unknown on the diagram. Flag every relationship that needs deployment or portal evidence. A resource existing in code does not prove its runtime traffic, DNS, identity or data relationship is configured correctly.
4. Apply `drawio-core-generation` and its upstream routing reference: use an importer or a controlled extraction only when its input is actually available, then author or normalize native XML for Azure2 icons, boundaries and precise network flows.
5. Apply `azure-icons-and-visual-language`, `drawio-layout-and-composition` and `drawio-xml-authoring`. Derive stable cell IDs from resource addresses or names so later regenerations diff cleanly.
6. Apply `azure-architecture-patterns` when the source implements a recognizable pattern, such as hub-spoke private networking or AKS, so the pattern is drawn honestly.
7. Apply `diagram-validation-and-evidence`: trace every component and relationship back to a file and resource, run structural checks after the write, and apply `drawio-render-export-and-review` when Draw.io Desktop is detected.

Write a new file. Ask before changing or overwriting an existing diagram.

## Expected output

- A new uncompressed `.drawio` file whose cells trace to source resources.
- A source inventory: files read, resources and modules found, references used, unknown values, and sources not read (such as remote state).
- An evidence matrix labeling each component and relationship `observed`, `inferred` or `designed`, with the relationships that still need deployment evidence.
- A completion report that follows the `azure-expert-designer-contract` instruction. Source code is intent, so live state stays `not-verified` unless an approved live check was run.
