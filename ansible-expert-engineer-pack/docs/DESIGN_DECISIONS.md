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
