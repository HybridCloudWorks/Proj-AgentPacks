# ansible-expert-engineer 1.2.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| ansible-expert-engineer.agent.md | Canonical agent: Expert Ansible engineer for creating, converting, validating, debugging, securing, and operating playbooks, roles, inventories, and collections. Use when Ansible is named or when configuration-management automation is being designed. Do not use it to provision cloud resources that belong in Terraform or to execute against real hosts without explicit approval. | .apm/agents/ansible-expert-engineer.agent.md |
| ansible-expert-engineer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the ansible expert engineer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/ansible-expert-engineer-contract.instructions.md |
| author-playbook-or-role.prompt.md | Canonical prompt: Create, change or review an Ansible playbook or role as idempotent, validated desired state | .apm/prompts/author-playbook-or-role.prompt.md |
| bootstrap-ansible-project.prompt.md | Canonical prompt: Bootstrap an Ansible project connection-first, validating one boundary at a time | .apm/prompts/bootstrap-ansible-project.prompt.md |
| convert-imperative-automation.prompt.md | Canonical prompt: Convert a shell script, runbook, Dockerfile or cloud-init into idempotent Ansible | .apm/prompts/convert-imperative-automation.prompt.md |
| debug-ansible-failure.prompt.md | Canonical prompt: Diagnose an Ansible connection, become, module, templating, version or performance failure | .apm/prompts/debug-ansible-failure.prompt.md |
| design-inventory-and-variables.prompt.md | Canonical prompt: Design or troubleshoot Ansible inventories, variable precedence, facts and environment separation | .apm/prompts/design-inventory-and-variables.prompt.md |
| engineer-role-or-collection.prompt.md | Canonical prompt: Build or review a reusable Ansible role or collection with a public contract, argument specs and tests | .apm/prompts/engineer-role-or-collection.prompt.md |
| manage-collection-dependencies.prompt.md | Canonical prompt: Add, pin, verify, upgrade or troubleshoot Ansible collections and roles in requirements.yml | .apm/prompts/manage-collection-dependencies.prompt.md |
| plan-rolling-change.prompt.md | Canonical prompt: Plan or review a rolling Ansible change with host-selection proof, batching, failure policy and recovery | .apm/prompts/plan-rolling-change.prompt.md |
| secure-ansible-secrets.prompt.md | Canonical prompt: Find plaintext secrets in Ansible content and move them to Vault with output protection | .apm/prompts/secure-ansible-secrets.prompt.md |
| validate-ansible-content.prompt.md | Canonical prompt: Validate Ansible content with layered lint, syntax, inventory, check/diff and test evidence | .apm/prompts/validate-ansible-content.prompt.md |
| SKILL.md | Canonical skill: Guide a connection-first Ansible project bootstrap or hands-on build by gathering hosts, OS, SSH, become, environment, collections, and secrets constraints before writing automation. | .apm/skills/ansible-bootstrap-interactive/SKILL.md |
| SKILL.md | Canonical skill: Choose, install, pin, verify, upgrade, and troubleshoot Ansible collections and roles with requirements files, FQCN ownership, Galaxy or Automation Hub sources, signatures, and compatibility evidence. | .apm/skills/ansible-collections-supply-chain/SKILL.md |
| SKILL.md | Canonical skill: Convert shell scripts, manual runbooks, Dockerfile RUN steps, cloud-init, or imperative host setup into idempotent Ansible playbooks and roles. Use when replacing repeated command sequences with declarative configuration management. | .apm/skills/ansible-convert-imperative-automation/SKILL.md |
| SKILL.md | Canonical skill: Diagnose Ansible UNREACHABLE, SSH, authentication, become, module, templating, variable, version, idempotency, or performance failures from commands and evidence. Use when a playbook or inventory fails or behaves unexpectedly. | .apm/skills/ansible-debug-runtime-failures/SKILL.md |
| SKILL.md | Canonical skill: Design or review Ansible rollout safety, host selection, serial batches, strategies, delegation, run_once, throttle, async work, handlers, failure policy, and blast-radius controls. | .apm/skills/ansible-execution-control/SKILL.md |
| SKILL.md | Canonical skill: Design or troubleshoot Ansible inventories, inventory plugins, host/group variables, precedence, facts, caching, environment separation, and target selection without accidental cross-environment or cross-host changes. | .apm/skills/ansible-inventory-and-variable-design/SKILL.md |
| SKILL.md | Canonical skill: Create or review Ansible playbooks, roles, tasks, handlers, templates, inventories, and variables using FQCN modules, explicit contracts, idempotency, and current Ansible validation. Use when the task is authoring or changing reusable Ansible automation. | .apm/skills/ansible-playbook-development/SKILL.md |
| SKILL.md | Canonical skill: Build or review production-quality Ansible roles and collections, including public variable contracts, argument specifications, metadata, documentation, Molecule scenarios, ansible-test, and supported-version evidence. | .apm/skills/ansible-role-collection-engineering/SKILL.md |
| SKILL.md | Canonical skill: Validate Ansible playbooks, roles, collections, inventories, and CI with ansible-lint, syntax checks, inventory inspection, check/diff mode, idempotency evidence, and targeted tests. Use before execution or when remediating validation failures. | .apm/skills/ansible-validate-content/SKILL.md |
| SKILL.md | Canonical skill: Manage Ansible Vault, vault IDs, secret-manager integration, plaintext-secret migration, no_log, diff suppression, and CI-safe password delivery. Use whenever Ansible variables, templates, inventory, output, or dependencies contain credentials or sensitive data. | .apm/skills/ansible-vault-secrets/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| OFFICIAL_SOURCES.md | Pack contract or inventory | docs/OFFICIAL_SOURCES.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| bootstrap-lab-estate.md | Worked example | examples/bootstrap-lab-estate.md |
| convert-shell-bootstrap.md | Worked example | examples/convert-shell-bootstrap.md |
| debug-conditional-after-upgrade.md | Worked example | examples/debug-conditional-after-upgrade.md |
| plan-rolling-release.md | Worked example | examples/plan-rolling-release.md |
| role-with-molecule-skipped.md | Worked example | examples/role-with-molecule-skipped.md |
| secrets-migration-blocked.md | Worked example | examples/secrets-migration-blocked.md |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| conversion-map.md | Reusable template | templates/conversion-map.md |
| failure-diagnosis.md | Reusable template | templates/failure-diagnosis.md |
| handoff.md | Reusable template | templates/handoff.md |
| role-contract.md | Reusable template | templates/role-contract.md |
| rollout-plan.md | Reusable template | templates/rollout-plan.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| validation-report.md | Pack file | validation-report.md |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-ansible-expert-engineer.zip: 22 files generated by `apm install --target copilot`
- claude-ansible-expert-engineer.zip: 22 files generated by `apm install --target claude`
- codex-ansible-expert-engineer.zip: 11 files generated by `apm install --target codex`
- kiro-ansible-expert-engineer.zip: 12 files generated by `apm install --target kiro`
- gemini-ansible-expert-engineer.zip: 20 files generated by `apm install --target gemini`
- agent-skills-ansible-expert-engineer.zip: 10 files generated by `apm install --target agent-skills`
- ansible-expert-engineer-canonical.zip, ansible-expert-engineer-prompt.zip, ansible-expert-engineer-validation.zip, ansible-expert-engineer-skills.zip, ansible-expert-engineer-full-pack.zip, SHA256SUMS.txt
