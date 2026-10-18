---
name: aws-architecture-visualization
description: Route approved AWS architecture designs into correct editable Draw.io diagrams while preserving source evidence, boundaries, flow semantics, and visual validation limits.
---

# AWS Architecture Visualization

Use this Skill when a design needs a Draw.io diagram, visual review, export, or architecture-to-diagram traceability.

Prefer the separate AWS Expert Designer pack or an installed `aws-architecture-diagram` Skill for native AWS4 XML generation. Use `drawio-core-generation` for generic Draw.io mechanics and `drawio-render-export-and-review` for export. Do not create a diagram that silently adds services or relationships absent from the approved architecture.

The diagram should show the relevant account/Region/AZ/VPC/subnet boundaries, primary data/control flows, identity and security boundaries, failure domains, cost-bearing edges, assumptions, and a legend. Keep editable uncompressed XML as the source artifact. Validate structure and rendering separately; a clean diagram is not proof of a deployed architecture.
