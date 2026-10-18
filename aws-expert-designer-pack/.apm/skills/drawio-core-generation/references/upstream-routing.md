# Upstream Draw.io Routing

The public `Agents365-ai/drawio-skill` repository is the generic upstream foundation. Its current Skill describes native `.drawio` XML, PNG/SVG/PDF/JPG export, Mermaid conversion, importers for code and IaC, autolayout, repair, validation, diff, and iterative review.

Route as follows:

- Standard flowcharts, sequences, C4, ERD, UML, or swimlanes: consider Mermaid or the upstream preset, then inspect the native result.
- Terraform, Kubernetes, Docker Compose, SQL, OpenAPI, CI, or source-code topology: use the upstream importer or a controlled extraction, then apply the target cloud provider's semantics when the diagram is provider-specific.
- More than roughly 15 nodes or dense dependency graphs: use structured generation and autolayout as a starting point, not as the final layout.
- Custom cloud boundaries, official provider icons, precise network flows, or regulated review: author or normalize native XML directly.

Do not assume the upstream version, script names, Draw.io binary path, or optional Graphviz availability. Detect them and report the installed versions. The repository was observed at version 2.1.1 during pack authoring; recheck current upstream before a future release.
