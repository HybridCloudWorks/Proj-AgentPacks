# Design Decisions

## Thin Agent, modular Skills

The supplied Agent was retained as the control plane. Repeated procedures remain in Skills so a task loads only the relevant context.

## Version-sensitive guidance

The source repeatedly named Ansible 13 / ansible-core 2.20. Official release documentation confirms that as the current released baseline at the validation snapshot, with Ansible 14 / core 2.21 in development. Content therefore says “verify the current baseline” before relying on exact behavior and links to the porting guides.

## Gap closures

- `ansible-execution-control` closes rollout, batching, delegation, concurrency, handler, async, and blast-radius gaps.
- `ansible-role-collection-engineering` closes reusable-content contracts, argument specifications, Molecule, ansible-test, and collection-quality gaps.
- `ansible-inventory-and-variable-design` closes dynamic inventory, precedence, fact lifecycle, caching, environment separation, and target-selection gaps.

## Portability

Skills use the shared `SKILL.md` shape. Agents are generated per target because Copilot, Claude Code, Codex, and Gemini CLI use different Agent file schemas and permission models. APM metadata and generated target trees are validated separately.

## Evidence boundaries

Local checks prove structure and command outcomes only. They do not prove a vendor runtime will select the Agent, a remote host will respond, a collection source is trusted, or a rollout is safe.

## Gap fill 2026-10-18

The pack was missing `.apm/prompts/`, `examples/` and `templates/`. They were authored from the existing agent, the ten skills and the contract instruction, which were not changed. Neither were `apm.yml` and `compatibility/tool-permissions.yml`. Decisions and assumptions:

### Prompts

- **One prompt per capability.** The agent's routing and `tests/capability-coverage.yml` both define ten distinct capabilities, each owned by one skill with its own output. So there are ten prompts, mapped one-to-one. Each names its primary and supporting skills by their exact names.
- **No separate review prompt.** The pack has no review skill. The playbook, role/collection and execution-control skills treat review as a mode ("create or review", "build or review", "design or review"), so the corresponding prompts handle a review-only request as read-only and return findings. Adding a review prompt would have implied a capability the skills do not define.
- **Installed content only.** Prompts reference the agent, the skills and the `ansible-expert-engineer-contract` instruction by name. They describe their output structure inline instead of pointing at `templates/`, which is not installed.
- **`agent` field.** Every prompt sets `agent: ansible-expert-engineer`. Per the verified client facts, Copilot honours it and Claude Code drops it with a warning. That limitation is documented in `docs/PROMPT_INVENTORY.md`, not worked around.
- **No status tokens.** Prompts and templates use plain lowercase outcome words (verified locally, prepared, unverified, blocked). `tests/report-contract.yml` defines no status vocabulary, and adding uppercase status names to installed content would require defining them there.

### Templates

- Six templates: `completion-report.md` and `handoff.md`, plus one each for the outputs that four skills explicitly specify: rollout plan (`ansible-execution-control`), conversion map (`ansible-convert-imperative-automation`), failure diagnosis (`ansible-debug-runtime-failures`), and role contract (`ansible-role-collection-engineering`).
- **Handoff meaning.** The pack has a single agent and no specialists, so "handoff" is read as the approval-boundary handoff from the agent to an authorized human operator. That covers production runs, rotations, shared installs and the bootstrap phase ends. The contract instruction's description mentions handoff but defines no handoff rules. The template adds structure only, not rules.
- No separate template for the dependency record (`ansible-collections-supply-chain`) or the secrets migration record (`ansible-vault-secrets`). Their outputs are short lists that fit the completion report's evidence and changed-files sections, which is how the examples record them.

### Examples

- Six synthetic walkthroughs covering bootstrap, conversion, debugging, rollout, role engineering and secrets. Host names, addresses, repositories and version numbers are illustrative, not recommendations. Error excerpts are marked as abridged.
- **Varied outcomes.** One is blocked (`secrets-migration-blocked.md`). Two are prepared but unverified (a partial dry run caused by a check-mode limitation, and Molecule skipped for lack of a container runtime). One has real staging runs but no production run. One is verified locally. One is verified on approved lab hosts. This shows each contract distinction in a realistic setting.
- **Version-specific behavior.** `debug-conditional-after-upgrade.md` relies on the boolean-conditional change crossed when moving from ansible-core 2.18 to 2.20, consistent with the "boolean conditionals" check named in `ansible-debug-runtime-failures` and the Ansible 13 / core 2.20 baseline recorded above. The example deliberately leaves the old controller's behavior unestablished.
- **No collection-upgrade example.** Collection pinning and an approved project-local install appear inside `convert-shell-bootstrap.md`, and dependency evidence appears in `role-with-molecule-skipped.md`. A dedicated upgrade walkthrough is a candidate for a later revision.

### Test metadata and docs

- `tests/capability-coverage.yml` keeps its keys and adds `prompts`, `examples` and `failure_outcomes` mappings. `tests/trigger-cases.yml` keeps its `positive` and `negative` lists unchanged and adds `prompt_routing` (one case per prompt) and `prompt_guardrails`.
- Both files are now written as JSON, which is valid YAML. The shared validator reads them with PyYAML when available and otherwise falls back to JSON. PyYAML's presence could not be confirmed in this environment, so JSON parses either way.
- `docs/PROMPT_INVENTORY.md` was created. `docs/SKILL_INVENTORY.md` does not exist and was not created, because only the prompt inventory was authorized for creation. The skill-to-prompt, example and template mapping lives in the prompt inventory instead.
- `README.md` gained sections for the contract instruction, prompts, examples and templates. Its build and validate instructions were corrected to the shared tooling at the repository root, because the pack has no `tooling/` folder.
- Not changed, though outside the current standard: the lowercase `validation-report.md` and the deliverables list in `DESCRIPTION.md`. Neither file was in scope for this gap fill.
- **Validation.** `python tooling/validate_pack.py <pack> --install-check --no-report` reported PASS: 122 checks, 0 failures, 1 skipped. The per-check detail was not inspected. The single skip is inferred to be the pack-unit-tests check, because the pack has no `tests/test_*.py`. Without the APM CLI, the compile and install checks would have been skipped too. The examples are synthetic: no Ansible command in them was executed as part of this gap fill.
