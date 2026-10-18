# Upstream Draw.io Routing

The public `Agents365-ai/drawio-skill` repository (MIT) is the generic upstream foundation. Version 3.4.2, observed on 2026-10-18, calls itself "Draw.io Architecture Studio". Its entry point `scripts/diagramctl.py` covers build, sync, multi-view projection, semantic query, policy test, review and what-if. It also ships `validate.py` for structural scoring, `shapesearch.py` for exact styles from an index of about 10,000 draw.io palette shapes, `autolayout.py`, importers for code and infrastructure, and Mermaid conversion. Its frontmatter sets `disable-model-invocation: true`, so a client loads it only when the user or an agent invokes it by name.

Route as follows when it is installed:

- Standard flowcharts, sequences, C4, ERD, UML, or swimlanes: consider Mermaid conversion, which needs draw.io 30 or later, or the upstream preset, then inspect the native result.
- Terraform, Kubernetes, Docker Compose, SQL, OpenAPI, AsyncAPI, CI, or source-code topology: use the upstream importer or a controlled extraction, then apply each provider's semantics from the provider reference.
- More than roughly 15 nodes or dense dependency graphs: use structured generation and autolayout as a starting point, not as the final layout.
- Provider icons: use the upstream shape search to get exact styles. The index includes legacy libraries, so one name can return AWS17, AWS current and AWS 3D variants; pick the current library from the provider reference.
- Custom cloud boundaries, official provider icons, precise network flows, or regulated review: author or normalize native XML directly.

Do not assume the upstream version, script names, Draw.io binary path, or optional Graphviz availability. Detect them and report the installed versions. Version 2.1.1 was current when these packs were first authored; recheck upstream before a future release.
