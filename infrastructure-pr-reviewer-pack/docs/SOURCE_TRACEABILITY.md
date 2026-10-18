# Source Traceability

## Inputs

| Source | SHA-256 |
|---|---|
| `SKILL.md` | `b667e8f1469980fab44b9e17e55384f70c72d3cac11ae587488d579193980c89` |
| `run_review_checks.py` | `f25d8b1b07b3e1ee5df952adc2fdb75d92c44ffae32c0f3f911d8c960af2b5b3` |
| `standalone-SKILL.md` | `720674fca79eb1370f640e1aa868a79caacec7eadcdfd17bc8ec9912d8a85c41` |
| `review-protocol.md` | `4b263575735a48fa6591227b3b92c6e98c8f19d8a23bf26d683a1a100fd6672a` |
| `change_manifest.py` | `65593d2c77030afbdc1f3daa8e43a5ab13e17118d861040e2c577ab9a3dca19f` |
| `universal-gates.md` | `a52169402ae13eb2f00fc47be672ef3a2890cfed9e10639fe30fd2375df205d4` |
| `pipelines-and-scripts.md` | `67c54317085a5636892b50aae7cd44f0109043a27ece4a17d7ebd1215b944c24` |
| `terraform-opentofu.md` | `70c91dcbfd151a81c0f42219cabe8795cd6e6dc8ded7d539877e62c8b50d4f42` |
| `bicep-arm.md` | `d83b3b28bc5c707883aed0b0690a64709d4db4355d07b7d0037d1c8676bfc92e` |
| `ansible.md` | `f3d37ce002a3394c36c596e6e4a7096288216cf6ca5fce2124ad052cc22f6d35` |
| `powershell.md` | `60daf78ccc439a71a81253c02c10559dc841dff6dc5d3cbe9654e1755c45ff02` |
| `severity-and-output.md` | `14b56bab39d1efbd11611eeb081358ad3f56fc1fcb542860d3293587d10b9a3f` |
| `github-copilot-setup.md` | `ca05028f3f40ec6a7a0f0b97bdba2ebce9ca08ce1873a32e6a718fbce8bac0d1` |
| `kubernetes-packaging.md` | `cdb42fca821eddf93f5295bdd74fce2914e68c27e7a670d41e165a4327b7000e` |
| `infrastructure.md` | `55e1563dc4575ef9c3620c04517c5ed47486febdf978f41a28a14df9df0be2b8` |
| `infrastructure-pull-request-template.md` | `55e1563dc4575ef9c3620c04517c5ed47486febdf978f41a28a14df9df0be2b8` |
| `infrastructure-review.instructions.md` | `529d1060225e5a4e5bb254b3a58e154661a1ed776b53fae1b9e67c7b35cc9a4c` |
| `README.md` | `69995bf00d3a9261c94773439cc2300bd6c11da42bc266e0ec15b7e1c173e3c1` |
| `repository-enforcement-checklist.md` | `d631411fc316ce6650264f426b5c39e08fe4fcaec4ca2edd116a933d295ca0ad` |

`infrastructure.md` and `infrastructure-pull-request-template.md` are byte-for-byte identical. The pack retains one canonical template and records both source hashes.

## De-duplication Decisions

- `SKILL.md` is the richest source and supplies the main workflow, quick gates, script routing, re-review behavior, and resource inventory.
- `standalone-SKILL.md` confirms the same intended behavior in a condensed form; only unique wording or safeguards were retained.
- The universal quick gates embedded in both Skill drafts were not repeated in runtime instructions because their full definitions already exist in `universal-gates.md` and the technology adapters.
- `change_manifest.py` retains the supplied behavior except that an explicitly requested missing `--base` now fails closed instead of silently falling back to another revision.
- GitHub Copilot installation and enforcement content is isolated from the portable Agent and domain Skills.
- The prior Apple reviewer and Terraform Agent files present elsewhere in the conversation are not part of this intake and were not used.

## Requirement Mapping

| Source requirement | Canonical owner | Supporting material or adapter |
|---|---|---|
| Principal infrastructure, platform, and deployment reviewer role | `.apm/agents/infrastructure-pr-reviewer.agent.md` | Native target adapters |
| Review-only posture and advisory enforcement limit | `.apm/agents/infrastructure-pr-reviewer.agent.md` | Copilot setup and compatibility matrix |
| Complete PR context and technology inventory | `.apm/skills/review-infrastructure-pr/SKILL.md` | `references/review-protocol.md` |
| Every changed line, deletion, rename, generated, mode, and binary change | `.apm/skills/review-infrastructure-pr/references/review-protocol.md` | `scripts/change_manifest.py` inventories the diff |
| Change contract, execution graph, ownership graph, and cross-tool handoffs | `.apm/skills/review-infrastructure-pr/references/review-protocol.md` | Orchestration Skill requires the method |
| Existing-environment reasoning, evidence hierarchy, finding threshold, and false-positive controls | `.apm/skills/review-infrastructure-pr/references/review-protocol.md` | None |
| Universal target, state, lifecycle, security, reliability, concurrency, supply-chain, cost, and operations gates | `.apm/skills/review-infrastructure-pr/references/universal-gates.md` | Domain Skills apply tool semantics |
| Terraform and OpenTofu review | `.apm/skills/review-terraform-opentofu/` | Original adapter retained as `references/review-checklist.md` |
| Bicep and ARM review | `.apm/skills/review-bicep-arm/` | Original adapter retained as `references/review-checklist.md` |
| PowerShell review | `.apm/skills/review-powershell-automation/` | Original adapter retained as `references/review-checklist.md` |
| Ansible review | `.apm/skills/review-ansible-automation/` | Original adapter retained as `references/review-checklist.md` |
| Pipeline, Bash, and Python deployment review | `.apm/skills/review-cicd-deployment/` | Original adapter retained as `references/review-checklist.md` |
| Kubernetes, Helm, and Kustomize review | `.apm/skills/review-kubernetes-packaging/` | Original adapter retained as `references/review-checklist.md` |
| Safe multi-tool static validation | `.apm/skills/verify-infrastructure-evidence/scripts/run_review_checks.py` | Evidence matrix constrains interpretation |
| Severity, confidence, inline placement, consolidation, evidence gaps, and no-finding output | `.apm/skills/review-infrastructure-pr/references/severity-and-output.md` | `assets/review-report-template.md` |
| Adversarial second pass and re-review on new pushes | `.apm/skills/review-infrastructure-pr/SKILL.md` | Agent completion contract |
| GitHub Copilot Skill and custom-instruction installation | `.apm/skills/review-infrastructure-pr/references/github-copilot-setup.md` | Copilot target and `setup/copilot/` |
| Path-specific infrastructure instructions | `.apm/instructions/infrastructure-review.instructions.md` | Generated Copilot instruction |
| Evidence-oriented infrastructure PR template | `.apm/skills/review-infrastructure-pr/assets/infrastructure-pull-request-template.md` | Copilot setup copy |
| Repository enforcement checklist | `.apm/skills/review-infrastructure-pr/assets/repository-enforcement-checklist.md` | Copilot setup copy |
| Repository-ready installation summary | `README.md` | generated vendor files |

## Official-Spec Additions

The following were added to make the source portable, maintainable, and independently testable:

- Canonical APM package, vendor-neutral Agent, generated native adapters, compatibility matrix, and official-source registry.
- Eight progressively disclosed Skills instead of one monolithic infrastructure review prompt.
- `agents/openai.yaml` UI metadata for every Skill.
- Current GitHub Copilot code-review paths, head-branch behavior, review-environment guidance, review effort, and enforcement limitation.
- Native Claude, Codex, and Gemini Agent and Skill layouts with read-only permission controls.
- Trigger, capability, report-contract, script, source-ownership, archive, hidden-Unicode, possible-secret, and target-drift validation.
- Focused official-source files so version-specific behavior can be refreshed without rewriting the workflow.
