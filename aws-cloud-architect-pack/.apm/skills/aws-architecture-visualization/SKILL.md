---
name: aws-architecture-visualization
description: Route approved AWS architecture designs into correct editable Draw.io diagrams while preserving source evidence, boundaries, flow semantics, and visual validation limits.
---

# AWS Architecture Visualization

Use this Skill when a design needs a Draw.io diagram, visual review, export, or architecture-to-diagram traceability.

## Route

Diagram work goes through the three shared draw.io skills that ship with this pack, in this order:

1. `drawio-core-generation` writes the diagram. It is the authority on which AWS icon library is current, how to copy each icon and group style whole from draw.io's AWS library, and how AWS boundaries nest: account > Region > VPC > Availability Zone > subnet, with each subnet in exactly one Availability Zone. It also draws Azure, Google Cloud and on-premises parts with their own providers' current icons.
2. `diagram-validation-and-evidence` runs its `check_drawio.py --strict` after every write, so that legacy, retired and unknown icons fail before anything is rendered.
3. `drawio-render-export-and-review` detects Draw.io Desktop, including the Microsoft Store build, exports with `-k` and inspects the render.
4. `diagram-validation-and-evidence` then completes the validation: it compares every component and relationship with the approved architecture and runs its visual checks on the render.

When the AWS Expert Designer pack is also installed, its AWS skills may add house style (sizes, typography, badges and the legend). They never override the shared skills on icon currency or boundary nesting. Do not prefer an unvetted third-party diagram skill over these shared skills.

## What the diagram shows

Show the relevant account, Region, VPC, Availability Zone and subnet boundaries, primary data and control flows, identity and security boundaries, failure domains, cost-bearing edges, assumptions, and a legend. Do not create a diagram that silently adds services or relationships absent from the approved architecture. Keep editable uncompressed XML as the source artifact. Validate structure and rendering separately; a clean diagram is not proof of a deployed architecture.
