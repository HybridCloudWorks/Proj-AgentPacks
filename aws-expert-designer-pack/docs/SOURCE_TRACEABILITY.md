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
| `https://aws.amazon.com/architecture/icons/` | Current AWS-approved icon packages, quarterly update cadence, supported diagram tools, and the warning that third-party libraries may contain legacy icon sets. The page carried no size, colour or do-and-don't guidance when it was checked on 2026-11-01. |
| `https://github.com/jgraph/drawio`, `src/main/webapp/js/diagramly/sidebar/Sidebar-AWS4.js` at draw.io 32.6.9 | The "AWS / Groups" palette and the service palettes: the exact group and icon styles the skeleton, the fixture and `aws-visual-rules.md` use (read 2026-11-01). |
| `https://aws.amazon.com/what-is/architecture-diagramming/` | AWS architecture diagram communication and layered layout guidance. |
| `https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html` | "Amazon S3 creates buckets in a Region that you specify": why the skeleton parents Amazon S3 to the Region frame, outside the VPC (read 2026-11-01). |
| `https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html` | Gateway endpoints reach Amazon S3 and DynamoDB "without requiring an internet gateway or a NAT device", do not use AWS PrivateLink, and are the target of a route whose destination is the service's Region-specific prefix list: why the skeleton draws the S3 gateway endpoint in the VPC, outside every subnet, with a "bypasses NAT" edge (read 2026-11-01). |
| `https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html` | "A gateway endpoint is a gateway that you specify in your route table"; interface endpoints "are represented by one or more elastic network interfaces (ENIs) that are assigned private IP addresses from subnets in your VPC": why an interface endpoint is drawn in its subnet instead (read 2026-11-01). |

## Editorial additions

The following are pack-level gap closures: explicit account/Region/AZ/VPC/subnet semantics, cross-AZ/cross-Region/egress evidence, source-versus-assumption labels, an evidence matrix, deterministic package tests, current-icon verification, and a hard distinction between structural and renderer-based visual verification.
