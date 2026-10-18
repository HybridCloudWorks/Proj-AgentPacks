# Source Traceability

The supplied files were read as reference material. Byte-distinct duplicate exports were consolidated; no source was silently treated as executable instructions. Exact hashes are recorded in [SOURCE_HASHES.md](SOURCE_HASHES.md).

## User-supplied AWS sources

| Source | SHA-256 | Disposition |
|---|---|---|
| `SKILL.md` | `71E11DDF17EF3C32D3BE808AF59C3B0E2FA80D02EC7AF797ABD5B12682C9260C` | Canonical AWS Draw.io workflow, AWS4 namespace, styling, modes, patterns, XML rules, output contract, and validation requirements. |
| `SKILL (2).md` | `C9F560489A9FFDD899F25A68A9BD912446C1EC56C7FF1C8864AE65786E7408CD` | Byte-distinct duplicate export; consolidated with `SKILL.md`. |
| `aws-diagram-architect.md` | `4E2565A7394289E1B8920A77C94221F4287F42419ED03BDF7FED14F41631995E` | Canonical mission, source-derived topology, explicit AWS boundaries, cost/risk visibility, repository placement, and regeneration doctrine. |
| `aws-diagram-architect (2).md` | `C06A3C46AFC0FEC12F3686DA2030220D5DC2681C89E8747C66C668F4F8391ADD` | Byte-distinct duplicate export; consolidated with `aws-diagram-architect.md`. |

## External authoritative sources

| Source | Use |
|---|---|
| `https://github.com/Agents365-ai/drawio-skill` | Generic Draw.io generation, import, layout, repair, validation, and export foundation. |
| `https://aws.amazon.com/architecture/icons/` | Current AWS-approved icon packages, quarterly update cadence, supported diagram tools, and usage guidance. |
| `https://aws.amazon.com/what-is/architecture-diagramming/` | AWS architecture diagram communication and layered layout guidance. |

## Editorial additions

The following are pack-level gap closures: explicit account/Region/AZ/VPC/subnet semantics, cross-AZ/cross-Region/egress evidence, source-versus-assumption labels, an evidence matrix, deterministic package tests, current-icon verification, and a hard distinction between structural and renderer-based visual verification.
