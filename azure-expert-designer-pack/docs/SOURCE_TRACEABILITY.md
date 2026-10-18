# Source Traceability

The supplied files were read as reference material. Byte-distinct duplicate exports were consolidated; no source was silently treated as executable instructions.

Exact SHA-256 values for the local source snapshot are recorded in [SOURCE_HASHES.md](SOURCE_HASHES.md).

## User-supplied Azure Designer sources

| Source family | Disposition |
|---|---|
| `azure-diagram-architect.md` and `(2)` | Canonical mission, source-derived workflow, Azure scope boundaries, evidence contract, and reporting behavior. |
| `SKILL.md`, `SKILL (2).md` | Azure architecture design and repository/codebase analysis workflow. |
| `SKILL (3).md` | Older upstream Draw.io skill copy; superseded for generic mechanics by the current public upstream reference and retained as historical source context. |
| `azure2-icons-services*.md`, `azure2-icons-resources*.md`, `general-icons*.md` | Azure2 icon paths, boundary/resource categories, and icon selection rules. |
| `xml-rules*.md`, `xml-templates-structure*.md`, `xml-templates-examples*.md`, `schema.json` | Uncompressed Draw.io XML structure, safe IDs, parents, edges, templates, and schema material. |
| `layout-guidelines*.md`, `group-styles*.md`, `style-guide*.md` | Spacing, alignment, hierarchy, connectors, typography, containers, and Azure visual language. |
| `diagram-templates-basic*.md`, `diagram-templates-advanced*.md` | Serverless, network, AKS, analytics, CI/CD, multi-region, landing-zone, and hybrid patterns. |
| `cli-export*.md`, `post-processing*.md` | CLI export, repair, structural checks, and separation of static versus visual validation. |
| `example-*.drawio` | Example diagrams retained as reference fixtures for future rendered regression tests; not copied into instruction text. |
| `*.json` style presets and `LICENSE` | Preset and licensing context; use only with the associated icon and usage terms. |

## External authoritative sources

| Source | Use |
|---|---|
| `https://github.com/Agents365-ai/drawio-skill` | Current generic Draw.io generation, import, autolayout, repair, validation, and export capability. Observed upstream version: 2.1.1. |
| `https://github.com/Agents365-ai/drawio-skill/tree/main/skills/drawio-skill` | Upstream Skill structure and current prerequisite/tool routing. |
| `https://learn.microsoft.com/en-us/azure/architecture/icons/` | Official Azure icon usage, labeling, permitted use, and update source. |

## Editorial additions

The following are pack-level gap closures: explicit Azure boundary semantics, source-versus-assumption labels, an evidence matrix, deterministic package tests, current-upstream normalization, and a hard distinction between structural and renderer-based visual verification.
