# Ansible Expert Engineer Pack

Portable Agent/Skill package for expert Ansible engineering. The canonical source is under `.apm/`; vendor directories are generated artifacts. The pack is intentionally repository-neutral and does not assume that Ansible is the right configuration-management layer for every estate.

## Deliverables

- `PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md` — reusable authoring standard.
- `ansible-expert-engineer-pack.zip` — complete source, generated vendor files, tests, tooling, and individual Skill archives.
- `ansible-expert-engineer-canonical.zip` — APM-friendly canonical source only.
- `ansible-expert-engineer-prompt.zip` — reusable pack-authoring prompt.
- `ansible-expert-engineer-validation.zip` — generated validation report.
- `validation-report.md` — validation evidence and known environment limits.
- `dist/` — vendor packages generated at build time and one validated `skill.zip` per Skill.

## Canonical design

The Agent routes work and owns boundaries. Skills own procedures. References hold change-prone source links. Scripts are reserved for deterministic validation and packaging. The Agent does not repeat the Skills.

### Skills

1. `ansible-playbook-development`
2. `ansible-convert-imperative-automation`
3. `ansible-debug-runtime-failures`
4. `ansible-validate-content`
5. `ansible-vault-secrets`
6. `ansible-collections-supply-chain`
7. `ansible-bootstrap-interactive`
8. `ansible-execution-control`
9. `ansible-role-collection-engineering`
10. `ansible-inventory-and-variable-design`

The final three close gaps in the supplied material: rollout/concurrency safety, role/collection quality gates, and inventory/fact/variable architecture.

### Contract instruction

`.apm/instructions/ansible-expert-engineer-contract.instructions.md` is always on (`applyTo: "**"`). It defines the completion report that every prompt and example ends with: result, evidence, changed files or proposal, unresolved risks, and next safe action. It also requires four distinctions: observed fact vs inference, skipped vs passed check, local validation vs remote proof, and dry run vs real execution.

### Prompts

One prompt per primary workflow, in `.apm/prompts/`, each run on the `ansible-expert-engineer` agent:

| Prompt | Workflow |
|---|---|
| `bootstrap-ansible-project.prompt.md` | Connection-first project bootstrap |
| `author-playbook-or-role.prompt.md` | Create, change or review playbooks and roles |
| `convert-imperative-automation.prompt.md` | Shell, runbook, Dockerfile or cloud-init conversion |
| `debug-ansible-failure.prompt.md` | Runtime failure diagnosis |
| `validate-ansible-content.prompt.md` | Layered validation evidence |
| `secure-ansible-secrets.prompt.md` | Vault migration and output protection |
| `manage-collection-dependencies.prompt.md` | Collection pinning, verification and upgrades |
| `plan-rolling-change.prompt.md` | Rollout safety and operator handoff |
| `engineer-role-or-collection.prompt.md` | Reusable role or collection with tests |
| `design-inventory-and-variables.prompt.md` | Inventory, precedence and environment separation |

`docs/PROMPT_INVENTORY.md` maps each prompt to its skills, examples and templates, and records how each client installs prompts.

## Examples

Worked walkthroughs in `examples/`. Each one ends with a completion report in the contract's format, and their outcomes differ on purpose:

- `bootstrap-lab-estate.md`: phased bootstrap that hits a host-key failure and a sudo-password failure; verified on approved lab hosts.
- `convert-shell-bootstrap.md`: install script converted to a role; dry run partial because of a check-mode limitation.
- `debug-conditional-after-upgrade.md`: string-valued conditional rejected after a core upgrade; verified locally, production not re-run.
- `plan-rolling-release.md`: `serial` rollout behind HAProxy; real staging runs, production handed to the operator.
- `role-with-molecule-skipped.md`: reusable role with an argument spec; Molecule skipped because no container runtime is available.
- `secrets-migration-blocked.md`: plaintext secrets migration blocked on a vault password delivered out of band and on rotation owners.

## Templates

Reusable documents in `templates/` for the outputs the skills ask for:

- `completion-report.md`: the contract's five sections and four distinctions, with an evidence ledger.
- `handoff.md`: approval-boundary handoff to an authorized operator, or between bootstrap phases.
- `rollout-plan.md`: the output of `ansible-execution-control`, with selection proof.
- `conversion-map.md`: the output of `ansible-convert-imperative-automation`.
- `failure-diagnosis.md`: the output of `ansible-debug-runtime-failures`.
- `role-contract.md`: role README and argument spec skeleton for `ansible-role-collection-engineering`.

Templates, examples and docs are for people. They are not installed, and installed content never refers to them.

## Safety boundary

The Agent may inspect and edit repository automation when authorized by the user. It must not run a playbook against real hosts, rotate credentials, install remote content, or make production changes without explicit authorization. Check mode, diff mode, syntax checks, lint, Molecule, and safe-target tests are evidence—not proof that a live rollout is safe.

## Build and validate

Validation and build tooling is shared at the root of the pack repository; this pack carries no copy of it. From the repository root:

```text
python tooling/skill_coverage.py <path-to>/ansible-expert-engineer-pack
python tooling/validate_pack.py <path-to>/ansible-expert-engineer-pack --install-check
```

`skill_coverage.py` regenerates `tests/skill-coverage.yml` from the skills. The validator checks required artifacts, manifest fields, agent, skill, instruction and prompt frontmatter, and that installed content references only installed content. It also checks that the test metadata names real skills and prompts, and, when the APM CLI is present, `apm compile --validate` and a scratch `apm install`. It does not claim live Ansible, remote-host, or vendor-runtime execution.

## Current baseline

At the 2026-08-22 validation snapshot, the official Ansible release table identifies Ansible 13.x / `ansible-core` 2.20 as current and Ansible 14 / core 2.21 as in development. The Skills therefore require a version check against the official release and porting guides before relying on version-specific behavior.
