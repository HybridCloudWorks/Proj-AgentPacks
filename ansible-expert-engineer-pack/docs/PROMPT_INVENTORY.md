# Prompt inventory

There is one prompt per primary workflow. Each prompt runs on the `ansible-expert-engineer` agent, names the skills it applies by their exact names, and ends with the completion report defined by the always-on `ansible-expert-engineer-contract` instruction. Prompts reference only installed content: skills, the agent and the contract instruction. They never reference pack docs, tests, examples or templates.

## Prompts

| Prompt | Primary skill | Supporting skills | Expected output |
|---|---|---|---|
| `bootstrap-ansible-project.prompt.md` | `ansible-bootstrap-interactive` | inventory-and-variable-design, collections-supply-chain, vault-secrets, debug-runtime-failures, validate-content | Phase summaries; file tree; connectivity and become evidence per approved host; open assumptions. |
| `author-playbook-or-role.prompt.md` | `ansible-playbook-development` | role-collection-engineering, inventory-and-variable-design, vault-secrets, validate-content | Changed or proposed files, variable contract, validation evidence, check/diff limits, convergence status; located findings for a review. |
| `convert-imperative-automation.prompt.md` | `ansible-convert-imperative-automation` | playbook-development, collections-supply-chain, vault-secrets, validate-content | Layout, variable contract, step-by-step conversion map, handler and recovery behavior, secrets boundary, unconvertible or ambiguous steps. |
| `debug-ansible-failure.prompt.md` | `ansible-debug-runtime-failures` | inventory-and-variable-design, collections-supply-chain, vault-secrets, execution-control, validate-content | Confirmed cause, contributing factors, hypotheses and missing evidence; smallest safe reproduction; fix and regression checks. |
| `validate-ansible-content.prompt.md` | `ansible-validate-content` | role-collection-engineering | Evidence ledger per validation layer; located findings and remediation; remaining check/diff limitations. |
| `secure-ansible-secrets.prompt.md` | `ansible-vault-secrets` | inventory-and-variable-design, validate-content | Located findings without values, rotation list with owners, vault layout, output protection, CI password delivery, residual exposure. |
| `manage-collection-dependencies.prompt.md` | `ansible-collections-supply-chain` | validate-content, role-collection-engineering | Dependency record (source, version, hash or signature, compatibility range), requirements diff, porting changes, test evidence. |
| `plan-rolling-change.prompt.md` | `ansible-execution-control` | inventory-and-variable-design, validate-content | Host-selection proof, batch and strategy rationale, concurrency controls, failure behavior, recovery plan, safe validation command, operator handoff. |
| `engineer-role-or-collection.prompt.md` | `ansible-role-collection-engineering` | playbook-development, collections-supply-chain, validate-content | Content tree, public contract and argument spec, README contract, test results, supported-version matrix, release evidence gaps. |
| `design-inventory-and-variables.prompt.md` | `ansible-inventory-and-variable-design` | execution-control, vault-secrets, validate-content | Inventory layout, variable placement table, precedence analysis, selection proof per environment, fact and caching decisions. |

Supporting skills are abbreviated without the `ansible-` prefix in this table. The prompts themselves use the full names.

The source files live in `.apm/prompts/`.

## Skills to prompts, examples and templates

| Skill | Prompt | Worked example | Template |
|---|---|---|---|
| `ansible-bootstrap-interactive` | `bootstrap-ansible-project.prompt.md` | `examples/bootstrap-lab-estate.md` | `templates/handoff.md` (phase handoff) |
| `ansible-playbook-development` | `author-playbook-or-role.prompt.md` | `examples/convert-shell-bootstrap.md`, `examples/role-with-molecule-skipped.md` | `templates/completion-report.md` |
| `ansible-convert-imperative-automation` | `convert-imperative-automation.prompt.md` | `examples/convert-shell-bootstrap.md` | `templates/conversion-map.md` |
| `ansible-debug-runtime-failures` | `debug-ansible-failure.prompt.md` | `examples/debug-conditional-after-upgrade.md`, `examples/bootstrap-lab-estate.md` | `templates/failure-diagnosis.md` |
| `ansible-validate-content` | `validate-ansible-content.prompt.md` | every example | `templates/completion-report.md` (evidence ledger) |
| `ansible-vault-secrets` | `secure-ansible-secrets.prompt.md` | `examples/secrets-migration-blocked.md` | `templates/completion-report.md` |
| `ansible-collections-supply-chain` | `manage-collection-dependencies.prompt.md` | `examples/convert-shell-bootstrap.md` (adds and pins `ansible.posix`) | `templates/completion-report.md` |
| `ansible-execution-control` | `plan-rolling-change.prompt.md` | `examples/plan-rolling-release.md` | `templates/rollout-plan.md`, `templates/handoff.md` |
| `ansible-role-collection-engineering` | `engineer-role-or-collection.prompt.md` | `examples/role-with-molecule-skipped.md` | `templates/role-contract.md` |
| `ansible-inventory-and-variable-design` | `design-inventory-and-variables.prompt.md` | `examples/debug-conditional-after-upgrade.md`, `examples/plan-rolling-release.md` | `templates/rollout-plan.md` (selection proof) |

## Example outcomes

The examples deliberately cover different completion states, so the contract's distinctions are shown under pressure:

| Example | Outcome |
|---|---|
| `examples/bootstrap-lab-estate.md` | verified on approved target (lab hosts, with a second, convergence run) |
| `examples/debug-conditional-after-upgrade.md` | verified locally; production not re-run |
| `examples/plan-rolling-release.md` | real staging runs; production prepared, unverified, handed to the operator |
| `examples/convert-shell-bootstrap.md` | prepared, unverified; dry run partial because of a check-mode limitation |
| `examples/role-with-molecule-skipped.md` | prepared, unverified; Molecule skipped with no container runtime |
| `examples/secrets-migration-blocked.md` | blocked on a vault password delivered out of band, secret owners, and rotation authority |

## How the prompts install

As recorded in the repository's verified client facts:

- **GitHub Copilot:** installed as prompt files, including at user scope. The `agent` key is honoured.
- **Claude Code:** installed as commands. APM drops the `agent` key with a warning, so the prompt runs in the current session rather than on the named agent.
- **OpenAI Codex:** a user-scope APM install deploys no prompts. Invoke the `ansible-expert-engineer` agent directly.
- **Kiro and Gemini CLI:** prompt deployment is not recorded in the verified facts and is not established here.
