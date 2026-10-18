# infrastructure-pr-reviewer 1.1.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| infrastructure-pr-reviewer.agent.md | Canonical agent: Review pull requests that change infrastructure-as-code, configuration management, deployment automation, platform manifests, or CI/CD. Use for Terraform or OpenTofu, Bicep or ARM, PowerShell, Ansible, GitHub Actions, Azure Pipelines, Bash or Python deployment wrappers, Kubernetes, Helm, Kustomize, and cross-tool execution chains. Produce evidence-based, line-anchored findings without editing or deploying. | .apm/agents/infrastructure-pr-reviewer.agent.md |
| infrastructure-pr-reviewer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the infrastructure pr reviewer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/infrastructure-pr-reviewer-contract.instructions.md |
| infrastructure-review.instructions.md | Canonical instruction: Apply evidence-driven infrastructure and automation pull-request review rules to relevant files. | .apm/instructions/infrastructure-review.instructions.md |
| openai.yaml | Canonical skill | .apm/skills/review-ansible-automation/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/review-ansible-automation/references/official-sources.md |
| review-checklist.md | Canonical skill | .apm/skills/review-ansible-automation/references/review-checklist.md |
| SKILL.md | Canonical skill: Review Ansible playbooks, roles, collections, inventories, variables, templates, handlers, plugins, vault integration, and execution pipelines for target selection, precedence, idempotency, failure semantics, rollout, privilege, secrets, and dependency integrity. Use when a PR changes Ansible YAML, roles, collections, inventory, ansible.cfg, requirements, or commands that run Ansible. Treat check and diff mode as incomplete evidence. | .apm/skills/review-ansible-automation/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/review-bicep-arm/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/review-bicep-arm/references/official-sources.md |
| review-checklist.md | Canonical skill | .apm/skills/review-bicep-arm/references/review-checklist.md |
| SKILL.md | Canonical skill: Review Bicep, Bicep parameter, ARM JSON, deployment-stack, template-spec, and related pipeline changes for deployment scope, resource identity, deletion behavior, API versions, module contracts, secrets, and what-if integrity. Use when a PR changes .bicep, .bicepparam, ARM templates, deployment stacks, template specs, or commands that build, preview, or deploy them. Do not apply Terraform state rules to these templates. | .apm/skills/review-bicep-arm/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/review-cicd-deployment/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/review-cicd-deployment/references/official-sources.md |
| review-checklist.md | Canonical skill | .apm/skills/review-cicd-deployment/references/review-checklist.md |
| SKILL.md | Canonical skill: Review GitHub Actions, Azure Pipelines, other CI/CD definitions, reusable workflows and templates, Bash, Python deployment wrappers, Makefiles, and task runners for trust boundaries, permissions, target selection, conditions, artifact provenance, concurrency, cancellation, supply chain, and failure propagation. Use when a PR changes pipeline YAML or orchestration scripts that validate, preview, approve, deploy, clean up, or roll back infrastructure. | .apm/skills/review-cicd-deployment/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/review-infrastructure-pr/agents/openai.yaml |
| infrastructure-pull-request-template.md | Canonical skill | .apm/skills/review-infrastructure-pr/assets/infrastructure-pull-request-template.md |
| repository-enforcement-checklist.md | Canonical skill | .apm/skills/review-infrastructure-pr/assets/repository-enforcement-checklist.md |
| review-report-template.md | Canonical skill | .apm/skills/review-infrastructure-pr/assets/review-report-template.md |
| github-copilot-setup.md | Canonical skill | .apm/skills/review-infrastructure-pr/references/github-copilot-setup.md |
| review-protocol.md | Canonical skill | .apm/skills/review-infrastructure-pr/references/review-protocol.md |
| severity-and-output.md | Canonical skill | .apm/skills/review-infrastructure-pr/references/severity-and-output.md |
| universal-gates.md | Canonical skill | .apm/skills/review-infrastructure-pr/references/universal-gates.md |
| change_manifest.py | Canonical skill | .apm/skills/review-infrastructure-pr/scripts/change_manifest.py |
| SKILL.md | Canonical skill: Perform a complete evidence-driven pull request review for infrastructure-as-code, configuration management, deployment automation, platform manifests, and CI/CD. Use when a change affects infrastructure targets, identities, state or ownership, deployment scripts, pipelines, policies, tests, secrets, generated artifacts, or cross-tool handoffs. Audit every changed line internally, invoke only the matching technology Skills, and report concrete defects or material evidence gaps. Do not use for general application-code style review or remediation work. | .apm/skills/review-infrastructure-pr/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/review-kubernetes-packaging/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/review-kubernetes-packaging/references/official-sources.md |
| review-checklist.md | Canonical skill | .apm/skills/review-kubernetes-packaging/references/review-checklist.md |
| SKILL.md | Canonical skill: Review Kubernetes manifests, Custom Resources, Helm charts and values, Kustomize bases and overlays, operators, GitOps configuration, and related deployment pipelines for cluster and namespace targeting, field ownership, rollout, security, resources, storage, rendering, and prune behavior. Use when a PR changes Kubernetes YAML, Chart.yaml, values files, templates, kustomization files, CRDs, or GitOps applications. | .apm/skills/review-kubernetes-packaging/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/review-powershell-automation/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/review-powershell-automation/references/official-sources.md |
| review-checklist.md | Canonical skill | .apm/skills/review-powershell-automation/references/review-checklist.md |
| SKILL.md | Canonical skill: Review PowerShell scripts, modules, manifests, DSC, and PowerShell pipeline steps for runtime compatibility, parameter contracts, native command failures, idempotency, quoting, object flow, concurrency, credentials, retries, and tests. Use when a PR changes .ps1, .psm1, .psd1, PowerShell deployment wrappers, or callers that depend on their output. Do not execute deployment scripts merely to validate them. | .apm/skills/review-powershell-automation/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/review-terraform-opentofu/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/review-terraform-opentofu/references/official-sources.md |
| review-checklist.md | Canonical skill | .apm/skills/review-terraform-opentofu/references/review-checklist.md |
| SKILL.md | Canonical skill: Review Terraform and OpenTofu pull request changes for state identity, provider and module contracts, lifecycle transitions, expressions, sensitive data, and plan/apply integrity. Use when a diff contains .tf, .tfvars, .tftest.hcl, .terraform.lock.hcl, OpenTofu equivalents, state migration declarations, or pipelines that run Terraform or OpenTofu. Do not use for Bicep, ARM, or unrelated application code. | .apm/skills/review-terraform-opentofu/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/verify-infrastructure-evidence/agents/openai.yaml |
| evidence-matrix.md | Canonical skill | .apm/skills/verify-infrastructure-evidence/references/evidence-matrix.md |
| official-sources.md | Canonical skill | .apm/skills/verify-infrastructure-evidence/references/official-sources.md |
| run_review_checks.py | Canonical skill | .apm/skills/verify-infrastructure-evidence/scripts/run_review_checks.py |
| SKILL.md | Canonical skill: Run and interpret safe, non-deploying validation for infrastructure and automation reviews, and assess whether plans, what-if results, rendered output, tests, policies, scans, CI logs, and artifacts are tied to the reviewed commit, target, inputs, identity, and dependency set. Use when a pull request includes or requires executable evidence. Do not run apply, deploy, destroy, target-side Ansible, privileged cluster operations, Terraform tests that can create resources, or untrusted workflows automatically. | .apm/skills/verify-infrastructure-evidence/SKILL.md |
| .gitignore | Pack file | .gitignore |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| copilot-instructions-snippet.md | Pack file | setup/copilot/copilot-instructions-snippet.md |
| infrastructure-pull-request-template.md | Pack file | setup/copilot/infrastructure-pull-request-template.md |
| README.md | Pack file | setup/copilot/README.md |
| repository-enforcement-checklist.md | Pack file | setup/copilot/repository-enforcement-checklist.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| script-cases.yml | Local test or recorded evidence | tests/script-cases.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| generate_targets.py | Pack-specific helper code | tooling/generate_targets.py |
| verify_distributions.py | Pack-specific helper code | tooling/verify_distributions.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-infrastructure-pr-reviewer.zip: 42 files generated by `apm install --target copilot`
- claude-infrastructure-pr-reviewer.zip: 42 files generated by `apm install --target claude`
- codex-infrastructure-pr-reviewer.zip: 40 files generated by `apm install --target codex`
- kiro-infrastructure-pr-reviewer.zip: 42 files generated by `apm install --target kiro`
- gemini-infrastructure-pr-reviewer.zip: 39 files generated by `apm install --target gemini`
- agent-skills-infrastructure-pr-reviewer.zip: 39 files generated by `apm install --target agent-skills`
- infrastructure-pr-reviewer-canonical.zip, infrastructure-pr-reviewer-prompt.zip, infrastructure-pr-reviewer-validation.zip, infrastructure-pr-reviewer-skills.zip, infrastructure-pr-reviewer-full-pack.zip, SHA256SUMS.txt
