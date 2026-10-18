# Portable Agent Skill Pack Authoring Prompt

## Goal and source context

Reconstruct a complete pack for the agent currently established by the conversation. Reuse the approved framework and completeness standard, rebuild the new agent's domain content. Recover mission, problem/users/outcomes, use cases, capabilities, workflows, inputs/outputs, sources/data/integrations, constraints/permissions/responsible AI, examples/tests and acceptance criteria from the current conversation. Do not ask users to repeat established information. If agent identity is inferred, state that assumption.

## Canonical framework

Retain artifact categories and positions: DESCRIPTION.md, README.md, thin .apm/agents profiles, modular .apm/skills, PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md, LICENSE, descriptive apm.yml, uppercase VALIDATION_REPORT.md; docs, compatibility metadata, capability/trigger/report tests and fixtures, safe tooling/hooks, instructions/prompts/examples/templates, four vendor targets, primary archives, individual validated skill.zip archives. Retain genuinely inapplicable artifact purposes with an explicit reason. Do not import another agent's terminology/personas/integrations/business rules just because its framework was consulted.

Four primary downloads are full-pack, canonical, authoring-prompt and validation ZIPs. Secondary output includes GitHub Copilot/Claude Code/OpenAI Codex/Gemini CLI ZIPs, bundled individual Skills and SHA256 checksums. Preserve names, section ordering, source traceability and installation depth.

## Content and operationalization

For each Skill/hook, define purpose/activation/exclusions, inputs, dependencies, behavior, output/validation, failure conditions, guardrails and concrete workflow/instruction connection. Keep shared controls in maintained contracts; avoid redundant tutorials or empty placeholders. Use realistic examples and explain the boundary between illustrative and executed evidence.

One primary technology agent owns the outcome. Optional specialists share the host's agents folder, have clear role/tool boundaries and receive goal/scope/facts/files/interfaces/versions/criteria/evidence/authority. They return located findings/changes/checks/results/risks/limits/next action. Choose tools using current official host schemas; do not invent generic aliases or assume a Markdown approval field enforces access.

Preserve explicit user authorization for its scope and context. Ask only for missing authority at consequential external/shared/destructive/sensitive/cost-bearing steps, after preparing concrete reviewable work. No self-approval, scope expansion, fabricated completion or confidential examples.

## Integrated QA

Every referenced Skill/prompt/contract exists in each installed target. Examples demonstrate the documented behavior; tests cover actual critical helper behavior as well as structure. Parse YAML/TOML/JSON; verify frontmatter, paths/tool names, profile visibility, source parity, exact inventories, executable scripts, bounded hooks, prompt injection/redaction/tenancy/cancellation/budget controls as applicable, ZIP safety/parity/checksums and final embedded report freshness. Do not count static trigger cases as executed model evaluations.

Record official sources with retrieval date, application and relevant version limits. Explain discrepancies between native host features and portable guidance. APM-friendly source layout does not claim unverified APM CLI compatibility. No live integration, credential or quality guarantee follows from a static PASS.

## Artifact presentation

Generate an ordered full-content catalog with executive summary, goals/non-goals, assumptions, design principles, architecture decisions, agent/Skill/prompt/instruction inventories, tools/approval matrices, directory tree, full contents, worked feature/API/MCP/security/browser/evaluation/completion examples, installation/usage/validation, governance/maintenance/versioning, known limits and unresolved assumptions.

For each file provide ARTIFACT NAME, PURPOSE and CONTENT at its exact relative path. Avoid recursive embedding of the catalog itself and show where generated target content comes from. End with AGENT PACK VALIDATION SUMMARY: agent, artifacts, Skills, hooks/triggers, knowledge/integrations, guardrails/tests, true gaps and assumptions.

## Current Python specialization

This pack is Python Distinguished Engineer: five profiles (one primary plus optional security/test/performance/evaluation), eighteen specifically named Skills, five shared instructions, ten prompts and six worked examples. Discover repository runtimes/framework/tooling first; distinguish static typing and runtime validation; address cancellation, packaging, data/migrations, Azure, MCP, browser testing, agent memory/security, observability, cost and responsible AI. Completion requires criterion-level evidence; if unavailable say exactly: "Implementation is prepared, but completion is not verified."
