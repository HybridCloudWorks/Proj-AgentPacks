# Portable Agent/Skill Pack Authoring Prompt

Use this prompt when creating or refreshing a portable expert Agent/Skill pack.

## Governing objective

Build a production-oriented, source-traceable pack from the user request and attached reference files. The user request is authoritative. Attachments are evidence and proposed content; distinguish their instructions from the request, consolidate duplicates, preserve valuable intent, and fill meaningful capability gaps without adding token-wasting overlap.

## Required delivery contract

Create:

1. A thin canonical primary Agent that is fully capable without subagents.
2. Optional specialist Agents for meaningful focus areas; they must be delegation paths, not hidden prerequisites.
3. Modular canonical Skills with clear triggers, procedures, evidence boundaries, and no duplicate SOPs.
4. `DESCRIPTION.md`, `README.md`, `AGENT-PACK-README.md`, `LICENSE`, `apm.yml`, and uppercase `VALIDATION_REPORT.md`.
5. Four generated AI-specific packages for GitHub Copilot, Claude Code, OpenAI Codex, and Gemini CLI.
6. Individual validated `skill.zip` archives, canonical and vendor archives, a validation bundle, and a full-pack archive.
7. Compatibility metadata, source traceability, design decisions, inventories, approval/tool matrices, handoff contracts, tests, fixtures, templates, hooks, and deterministic build/validation tooling.

## Research and source handling

- Use official current documentation for technology, agent, skill, product, licensing, privacy, and vendor-format claims. Browse when a claim could have changed.
- Prefer primary documentation and link it in source traceability.
- Treat private or supplied files as reference material. Do not reproduce restricted courseware wholesale or infer redistribution rights.
- Record source path, title, version/date, role in the design, and unresolved uncertainty.
- Distinguish static inspection, local rehearsal, live environment evidence, and unverified assumptions.

## Canonical design

- The primary Agent should be concise and orchestrate the full capability surface directly.
- Skills contain reusable domain procedures and load progressively.
- Specialists should cover only distinct workstreams that benefit from delegation, such as architecture, validation, security, courseware, or operations.
- The primary Agent must state when it can work alone and when it should delegate.
- Include safety gates for credentials, personal data, external communication, tenant or repository changes, publication, destructive operations, and cost-bearing actions.

## Validation

Build generated targets from canonical source. Validate exact agent/Skill parity, frontmatter, thin-agent limits, required files, trigger cases, report contract, hook syntax, script compilation, archive integrity, and uppercase `VALIDATION_REPORT.md`. A static pass must clearly state what it does not prove, including live authorization, cloud state, product availability, MCP connectivity, browser results, model quality, and learning outcomes.

## Pack-specific extension point

For a Microsoft Certified Trainer pack, add MCT/courseware governance, Microsoft Learn mapping, syllabus and assessment design, professional facilitation, rehearsal, PowerPoint engineering, Microsoft 365 Copilot and Copilot Studio teaching, Designer availability caveats, lab/demo reliability, GitHub and Azure handoffs, evaluation, maintenance, and safe trainer automation.

