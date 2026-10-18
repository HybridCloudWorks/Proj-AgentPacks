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

## Safety boundary

The Agent may inspect and edit repository automation when authorized by the user. It must not run a playbook against real hosts, rotate credentials, install remote content, or make production changes without explicit authorization. Check mode, diff mode, syntax checks, lint, Molecule, and safe-target tests are evidence—not proof that a live rollout is safe.

## Build and validate

From this directory:

```text
python tooling/build_pack.py
python tooling/validate_pack.py
```

The build is deterministic and recreates `dist/`. The validator checks the canonical tree, generated target parity, Skill metadata, archives, source traceability, and high-risk content patterns. It does not claim live Ansible, remote-host, APM-runtime, or vendor-runtime execution.

## Current baseline

At the 2026-08-22 validation snapshot, the official Ansible release table identifies Ansible 13.x / `ansible-core` 2.20 as current and Ansible 14 / core 2.21 as in development. The Skills therefore require a version check against the official release and porting guides before relying on version-specific behavior.
