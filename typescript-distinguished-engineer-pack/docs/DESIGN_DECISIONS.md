# Design Decisions

## Thin routing agent, focused Skills

The primary agent owns investigation, planning, implementation, integration, validation, and the final evidence report. Conditional expertise is split into 20 Skills so a task loads only what it needs. This follows the supplied Python engineer reference's useful consolidation pattern without copying Python-specific tooling.

## Specialist reviewers are advisory

Security, testing, and evaluation agents have narrow scopes and return evidence contracts. They do not silently approve, merge, deploy, publish, or change unrelated code.

## Evidence is a product feature

The pack uses explicit completion statuses, handoff and report templates, report validation, repository inventory, and pre/post hooks. Static pack validation is intentionally separate from proving a target repository's runtime or production behavior.

## Vendor-native targets with one source

`.apm` is the canonical source. The builder generates host-specific agent locations, Skill locations, instructions, prompts, and Codex TOML while preserving content parity. Targets are reproducible and archives use a fixed ZIP timestamp.

## Repository-neutral cloud and AI coverage

Azure, AWS, and Google Cloud appear as integration boundaries, not hard-coded environments. MCP and agentic guidance emphasizes schemas, least privilege, bounded execution, provenance, approval, and auditability rather than a particular provider implementation.
