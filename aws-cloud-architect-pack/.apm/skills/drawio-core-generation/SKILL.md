---
name: drawio-core-generation
description: Create and edit native Draw.io diagrams from requirements, code, structured data, or Mermaid while preserving editable XML and selecting the right generation path.
---

# Draw.io Core Generation

Use this Skill for any `.drawio` creation or substantive edit. The current upstream Draw.io skill is the generic capability baseline; use its available scripts and references when installed rather than recreating importers or export logic.

## Choose the generation path

- Use native XML when provider icons, custom boundaries, precise edge routing, or reviewable IDs matter.
- Use Mermaid only for standard diagrams when the installed Draw.io version supports conversion and no custom cloud-provider styling is required; inspect and normalize the result.
- Use structured JSON plus autolayout for large or data-driven diagrams, then apply provider-specific containment, spacing, labels, and edge routing.
- Use source importers or snapshots only when their input is actually available. A generated snapshot is evidence of the input at a point in time, not proof of the live environment.

## Required output contract

Produce an uncompressed `.drawio` file with a valid `mxfile`, one or more `diagram` elements, `mxGraphModel`, root cells `0` and `1`, unique stable IDs, explicit parents, and edges with valid source and target references. Keep the file diffable. Add a concise companion report when the task involves design decisions or source inference.

Ask at most a few focused questions when diagram type, audience, scope, output location, or fidelity materially changes the result. Otherwise make a documented assumption and proceed.

Read [references/upstream-routing.md](references/upstream-routing.md) when the task involves Mermaid, importers, autolayout, or Draw.io CLI capabilities.
