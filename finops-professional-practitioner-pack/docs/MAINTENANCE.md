# Maintenance, versioning and governance

Pack version 1.0.0 follows agent-pack-prompt v2.3. The `.apm/` folder is the only source for installed content; vendor files are generated at install time and never edited by hand.

## Changing the pack

1. Edit `.apm/` first.
2. Update `tests/capability-coverage.yml`, `tests/trigger-cases.yml` and, if the report format changed, `tests/report-contract.yml` together with the contract instruction and `tooling/completion_contract.py`.
3. Regenerate `tests/skill-coverage.yml` with the repository's `tooling/skill_coverage.py <pack>` whenever a skill is added, renamed or its description changes.
4. Run the repository's `tooling/validate_pack.py <pack> --install-check` and fix every failure.
5. Build release archives with the repository's shared build tooling; archives are build outputs, not source.

Semantic versioning: major for incompatible changes to the contract, statuses, agent names or skill names; minor for new capabilities; patch for corrections.

## What goes stale and how often to check

| Area | Why it changes | Review |
|---|---|---|
| FOCUS versions and columns | New releases add and deprecate columns | At each FOCUS release |
| FinOps Framework capability names | The Foundation revises domains and capabilities | Yearly, and when the framework announces changes |
| Provider exports, commitment types, carbon tools | Providers rename and add offerings | Quarterly |
| Client agent fields and install locations | Vendors moved several paths in 2026 | When the repository's client facts are re-verified |
| Example thresholds | Organizations set their own | Never presented as policy |

## Ownership

The pack owner approves changes to the contract, the approval levels and the agent roster. Skills are revised from observed failures in real use, not from isolated anecdotes.

## Known limits and task-time inputs

Billing data access, FOCUS version, currency, organizational thresholds, approvers and business drivers must be discovered for each task. No live tenant, connector, MCP registration or deployment manifest ships with the pack because a reusable pack has no concrete environment; INTEGRATION_CONTRACT.md describes what is discovered instead. Live client discovery, user-scope installs and hook wiring are not established by local tests.
