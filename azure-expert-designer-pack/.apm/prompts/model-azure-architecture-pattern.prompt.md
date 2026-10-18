---
description: "Model a recognizable Azure architecture pattern in Draw.io without misleading flows"
agent: azure-expert-designer
---

# Model an Azure architecture pattern

## Inputs

- The pattern requested or implied: serverless web, VNet with private endpoints, AKS, data and analytics, CI/CD, landing zone and governance, hybrid connectivity, or multi-region.
- The services the user has chosen, and the requirements that drive the pattern, such as availability target, failover expectations, regions and connectivity.
- Any source evidence, existing diagram and the output location.

## Workflow

1. Record a brief: purpose, audience, scope, source of truth, fidelity, output format and task type.
2. Apply `azure-architecture-patterns`. Run the pattern check that matches the request: show only what is configured or designed; distinguish private endpoints from service endpoints and inbound routes; separate the AKS control plane, node pools, ingress and workload identity; keep CI/CD out of the runtime path; draw governance as its own layer; and for hybrid or multi-region designs label routing, failover authority, replication direction and whether each tier is active/active or active/passive.
3. Apply `azure-architecture-design` to place subscriptions, resource groups, regions, zones, VNets and subnets as distinct concepts and to label each relationship `observed`, `inferred` or `designed`.
4. When the requested pattern and the chosen services disagree, for example an active/active request with a data tier that has a single writable primary, draw what the services actually do and record the conflict as a design decision or an open question. Do not silently substitute a different service.
5. Apply `drawio-layout-and-composition`: left-to-right data flow, top-to-bottom for governance, deployment or control-plane flows, global ingress outside regional frames, distinct edge styles for synchronous calls, asynchronous messages, replication and control-plane relationships, and a separate view when one page would be crowded.
6. Apply `azure-icons-and-visual-language`, `drawio-core-generation` and `drawio-xml-authoring` for icons, boundaries, generation path and XML structure.
7. Apply `diagram-validation-and-evidence` after every write, and `drawio-render-export-and-review` when Draw.io Desktop is detected.

Write a new file. Ask before changing or overwriting an existing diagram.

## Expected output

- A new uncompressed `.drawio` file with labeled routing, replication direction, failover authority and active/active or active/passive semantics, plus a legend.
- A companion report listing the pattern applied, deviations from it, design decisions, assumptions and open questions.
- A completion report that follows the `azure-expert-designer-contract` instruction.
