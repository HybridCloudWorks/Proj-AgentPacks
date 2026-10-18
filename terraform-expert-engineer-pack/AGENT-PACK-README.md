# terraform-expert-engineer 1.2.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| terraform-expert-engineer.agent.md | Canonical agent: Expert Terraform and HCL engineer for Terraform configuration, modules, providers, remote state, HCP Terraform, Stacks, policy, testing, CI/CD, imports, and Azure Verified Modules. Use whenever Terraform or Terraform-based IaC is in scope. | .apm/agents/terraform-expert-engineer.agent.md |
| terraform-expert-engineer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the terraform expert engineer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/terraform-expert-engineer-contract.instructions.md |
| add-terraform-tests.prompt.md | Canonical prompt: Add Terraform tests at the right level, from mocked plan checks to gated apply tests | .apm/prompts/add-terraform-tests.prompt.md |
| author-terraform-policy.prompt.md | Canonical prompt: Author, convert or test a Terraform policy and map where it is enforced | .apm/prompts/author-terraform-policy.prompt.md |
| build-terraform-pipeline.prompt.md | Canonical prompt: Build or review a Terraform CI/CD pipeline with ordered quality gates and a protected apply | .apm/prompts/build-terraform-pipeline.prompt.md |
| design-hcp-terraform-workflow.prompt.md | Canonical prompt: Design HCP Terraform or Terraform Enterprise workspaces, run flow and Stacks | .apm/prompts/design-hcp-terraform-workflow.prompt.md |
| develop-terraform-provider.prompt.md | Canonical prompt: Scaffold, implement and test a Terraform provider with the Plugin Framework in Go | .apm/prompts/develop-terraform-provider.prompt.md |
| implement-terraform-change.prompt.md | Canonical prompt: Implement or fix a Terraform configuration change, validate it and review its plan | .apm/prompts/implement-terraform-change.prompt.md |
| import-terraform-resources.prompt.md | Canonical prompt: Bring existing cloud resources under Terraform with reviewed import blocks and a clean plan | .apm/prompts/import-terraform-resources.prompt.md |
| migrate-terraform-state.prompt.md | Canonical prompt: Design a Terraform backend and prepare a gated state migration to S3, Azure Storage or HCP Terraform | .apm/prompts/migrate-terraform-state.prompt.md |
| refactor-terraform-module.prompt.md | Canonical prompt: Refactor or restructure a Terraform module without recreating resources or breaking consumers | .apm/prompts/refactor-terraform-module.prompt.md |
| review-terraform-avm-module.prompt.md | Canonical prompt: Develop or review an Azure Terraform module against current Azure Verified Modules requirements | .apm/prompts/review-terraform-avm-module.prompt.md |
| review-terraform-change.prompt.md | Canonical prompt: Review a Terraform change and its plan without modifying code, state or remote systems | .apm/prompts/review-terraform-change.prompt.md |
| SKILL.md | Canonical skill: Develop or review Azure Terraform modules against current Azure Verified Modules requirements, with focused checks for registry references, providers, interfaces, tests, documentation, and upgrade safety. | .apm/skills/azure-verified-modules/SKILL.md |
| SKILL.md | Canonical skill: Build and review Terraform CI/CD pipelines with formatting, validation, tests, lint, security, plan artifacts, approval gates, and controlled apply. | .apm/skills/terraform-ci-cd-and-quality/SKILL.md |
| SKILL.md | Canonical skill: Work with HCP Terraform and Terraform Enterprise workspaces, remote runs, variables, policies, run tasks, registries, Stacks, deployments, and linked outputs. | .apm/skills/terraform-cloud-and-stacks/SKILL.md |
| SKILL.md | Canonical skill: Author, review, and validate ordinary Terraform and HCL configuration, provider requirements, dependency locks, variables, outputs, expressions, and secure style. | .apm/skills/terraform-core-and-style/SKILL.md |
| SKILL.md | Canonical skill: Design, review, version, test, publish, and safely refactor Terraform modules without breaking state addresses or consumer contracts. | .apm/skills/terraform-modules-and-refactoring/SKILL.md |
| SKILL.md | Canonical skill: Author, convert, test, and review Terraform policy controls using Sentinel, tfpolicy, and CI policy checks with explicit enforcement boundaries. | .apm/skills/terraform-policy-and-governance/SKILL.md |
| SKILL.md | Canonical skill: Scaffold, implement, test, debug, and publish Terraform providers with the Terraform Plugin Framework and Go when provider development is in scope. | .apm/skills/terraform-provider-development/SKILL.md |
| SKILL.md | Canonical skill: Design and operate Terraform remote state, S3 and Azure Storage backends, locking, migrations, state recovery, Terraform Search, and safe imports. | .apm/skills/terraform-state-backends-and-imports/SKILL.md |
| SKILL.md | Canonical skill: Create and run Terraform validation, unit, plan, mock, integration, and provider acceptance tests while controlling credentials, cost, and cleanup risk. | .apm/skills/terraform-testing-and-validation/SKILL.md |
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
| avm-module-review-workflow.md | Worked example | examples/avm-module-review-workflow.md |
| ci-pipeline-workflow.md | Worked example | examples/ci-pipeline-workflow.md |
| import-resources-workflow.md | Worked example | examples/import-resources-workflow.md |
| module-refactor-workflow.md | Worked example | examples/module-refactor-workflow.md |
| policy-conversion-workflow.md | Worked example | examples/policy-conversion-workflow.md |
| state-migration-blocked.md | Worked example | examples/state-migration-blocked.md |
| terraform-test-workflow.md | Worked example | examples/terraform-test-workflow.md |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| approval-handoff.md | Reusable template | templates/approval-handoff.md |
| avm-requirement-review.md | Reusable template | templates/avm-requirement-review.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| plan-review.md | Reusable template | templates/plan-review.md |
| state-address-map.md | Reusable template | templates/state-address-map.md |
| state-migration-record.md | Reusable template | templates/state-migration-record.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| version-sensitivity.yml | Local test or recorded evidence | tests/version-sensitivity.yml |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-terraform-expert-engineer.zip: 22 files generated by `apm install --target copilot`
- claude-terraform-expert-engineer.zip: 22 files generated by `apm install --target claude`
- codex-terraform-expert-engineer.zip: 10 files generated by `apm install --target codex`
- kiro-terraform-expert-engineer.zip: 11 files generated by `apm install --target kiro`
- gemini-terraform-expert-engineer.zip: 20 files generated by `apm install --target gemini`
- agent-skills-terraform-expert-engineer.zip: 9 files generated by `apm install --target agent-skills`
- terraform-expert-engineer-canonical.zip, terraform-expert-engineer-prompt.zip, terraform-expert-engineer-validation.zip, terraform-expert-engineer-skills.zip, terraform-expert-engineer-full-pack.zip, SHA256SUMS.txt
