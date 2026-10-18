# Governance, maintenance and versioning

Pack version 1.0.0 follows agent-pack-prompt v2.3. The canonical `.apm/` source is authoritative; vendor files are generated at install time by APM or by the Code Workflow installer and are never edited by hand.

## Changing the pack

1. Change the canonical source in `.apm/`.
2. Update `tests/capability-coverage.yml`, `tests/trigger-cases.yml` and, if the report format changes, `tests/report-contract.yml`, `tooling/completion_contract.py` and the contract instruction together (a unit test keeps the last three in step).
3. When skills change, regenerate `tests/skill-coverage.yml` with the repository's `python tooling/skill_coverage.py docker-senior-engineer-pack`.
4. Run the repository's `python tooling/validate_pack.py docker-senior-engineer-pack --install-check` and fix every failure.
5. Build release archives with the repository's shared build tooling; archives, the artifact catalog and the validation report are build outputs.

Use semantic versioning: major for incompatible changes to agents, the contract, the report format or tool intents; minor for compatible capabilities; patch for corrections.

## Keeping Docker knowledge current

Docker facts in the skills were written from the author's knowledge on 2026-10-18 without browsing. Review them against the official documentation listed in `compatibility/vendor-sources.yml` at least when a new Docker Engine, Buildx, Compose or Dockerfile frontend major release ships, and when a skill fails in real use. Areas most likely to drift: build checks rules, Compose feature minimum versions, default image store, attestation defaults, Docker Content Trust status, licence-dependent features, and example base image versions in `dockerfile-patterns.md`.

The static checker in `tooling/container_lint.py` is heuristic. Add a rule only with a fixture that triggers it and one that does not, and prefer pointing users to `docker build --check`, hadolint and `docker compose config` over growing it into a parser.

## Known limits and unresolved operational inputs

Engine versions, registries, scanners, signing identities, CI systems, base image policy, platforms and approval authority are discovered per task. Live discovery and invocation in Claude Code, Codex, GitHub Copilot, Kiro and Gemini CLI, model behaviour, real Docker builds and runs, registry behaviour and user-scope installs are not established by the local tests. The unit tests exercise only the pack's own tooling.

## Genuinely inapplicable artifacts

The pack is meant for any repository, so it ships no registry settings, deployment files or credentials of its own; INTEGRATION_CONTRACT.md lists what has to be discovered or supplied when a task starts. Every canonical artifact category exists in the pack.
