# Python Distinguished Engineer Agent Pack

Version: 2.0.0. Recreated from the Python specification and primary/specialist clarification in this conversation. The independent Microsoft Certified Trainer pack is preserved.

## Four primary downloads

1. dist/python-distinguished-engineer-full-pack.zip — all canonical source, documentation, tests, tooling, hooks, templates, worked examples and generated vendor targets.
2. dist/python-distinguished-engineer-canonical.zip — .apm source with five profiles and eighteen Skills.
3. dist/python-distinguished-engineer-prompt.zip — reusable authoring framework with current reproduction/QA requirements.
4. dist/python-distinguished-engineer-validation.zip — uppercase validation report, tests, provenance/compatibility metadata, templates and validation tooling.

Secondary downloads: four vendor ZIPs, dist/python-distinguished-engineer-skills.zip containing eighteen individual skill.zip packages, and dist/SHA256SUMS.txt. Individual archives are in dist/skills/<skill-name>/skill.zip.

## Architecture and users

Developers, service/platform owners and reviewers work with python-distinguished-engineer. It investigates unfamiliar repositories, frames criteria, compares meaningful architecture options, implements Python changes, verifies behavior and reports evidence. Four optional workers support security, tests, measured performance and agent evaluation. The primary can handle the whole task directly.

Primary and specialist profiles share the same host agents directory. Copilot specialists use user-invocable: false; the primary includes the supported agent tool. Host limits differ and are documented in compatibility/compatibility-matrix.yml. Skills remain separate and load on demand.

## Artifact sequence and full contents

AGENT-PACK-README.md is the transfer-ready catalog. It retains the established 28-section sequence, provides ARTIFACT NAME / PURPOSE / CONTENT for every source and generated file, and ends with AGENT PACK VALIDATION SUMMARY. Files can also be transferred directly from targets/<vendor>. No new persona/domain content is copied from another pack.

## Install and use

Choose a target and follow its INSTALL.md. Merge files into an authorized repository; preserve existing context and policies. Copilot uses .github/agents, .github/skills, five .github/instructions files, ten .github/prompts files and .github/hooks. Contracts/templates remain at the installed root. Claude uses .claude profiles/Skills and CLAUDE.md; Codex uses .codex agent TOML, .agents/skills and AGENTS.md; Gemini uses .gemini profiles, .agents/skills and GEMINI.md.

Example request: "Investigate this Python repository, add a tenant-scoped idempotent job API using its conventions, and report acceptance evidence." For review-only work, specify the exact diff/base/head. For unavailable delegation, the primary uses the same Skills directly.

Host-native hooks are supplied only for Copilot. Other targets carry manual preflight/completion helpers. No SDK, browser, MCP server, cloud credential or paid model is installed or configured. Discover actual versions, integrations and authority at task time.

## Build and verify

Build requires Python 3.11+ and PyYAML as declared in tooling/requirements.txt; the task environment already has these. Installing dependencies is a separate environment decision.

```powershell
python tooling/build_pack.py
python tooling/validate_pack.py
python tooling/validate_python_pack.py .
```

The builder creates only generated targets, catalog, behavior evidence/report and dist archives within this pack. It runs local regression tests, checks sources and target mappings, rebuilds artifacts with the final embedded report, and checks archive parity/freshness/checksums. Use --archives-only only after source/target validation; normal source changes should use a full build. Do not edit generated targets.

## Governance and limits

See docs/MAINTENANCE.md, docs/TOOL_PERMISSION_MATRIX.md, docs/APPROVAL_MATRIX.md and docs/INTEGRATION_CONTRACT.md. Static and local tests establish pack integrity and helper behavior. They do not establish live client invocation, actual SDK protocol integration, production authorization, deployment, cloud availability, browser state or model quality. Future task-specific thresholds/identities/configuration must be supplied or discovered rather than fabricated.
