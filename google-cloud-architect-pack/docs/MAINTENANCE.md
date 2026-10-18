# Governance, maintenance and versioning

Pack version 1.1.0 follows agent-pack-prompt version 2.3. Edit only the files under `.apm/`; the client-specific files are produced from them when APM or the Code Workflow installer runs, so a hand edit to a generated file is lost at the next install.

## Changing the pack

1. Change the source under `.apm/` first.
2. Update `tests/capability-coverage.yml`, `tests/trigger-cases.yml` and, if the report format changes, `tests/report-contract.yml` together with `tooling/completion_contract.py` and the contract instruction.
3. Regenerate `tests/skill-coverage.yml` with the repository's shared `tooling/skill_coverage.py`.
4. Run the repository's shared `tooling/validate_pack.py <pack> --install-check`, which also runs `tests/test_behavior.py`.
5. Build release archives with the shared builder; archives are build outputs and are not committed.

## Shared diagram skills

The skills drawio-core-generation, drawio-render-export-and-review and diagram-validation-and-evidence are shared with the AWS and Azure packs. Do not edit them here: change the canonical copy in the repository's `shared-skills/` folder and run `tooling/sync_shared_skills.py`, which updates every pack that ships them. Their icon catalog is generated from draw.io's source by `tooling/build_icon_catalog.py`, and a weekly workflow reports when draw.io or a provider changes its icons.

## Versioning

Semantic versioning: major for incompatible changes to agents, skill names, the contract or report fields; minor for new compatible capabilities; patch for corrections. Skill names are part of the public contract because users and other agents load them by name.

## Keeping Google Cloud facts current

Product names, release status, SLAs, quotas, prices and command flags change often. Review the skills when Google announces renames, deprecations or new GA services, and prefer telling the model to verify a fact at task time over hard-coding it. Re-check the decision guides' links when Google reorganizes its documentation. Retire guidance with a note in DESIGN_DECISIONS.md instead of silently deleting it.

## Ownership

The pack owner approves changes to approval levels, specialist permissions and the report contract. Changes to a skill's guardrails need the same review as changes to the contract, because each skill must stay safe when installed alone.

## Known limits

The local tests cannot show whether each client discovers the agents, whether delegation works, how a wired hook behaves, or how a model actually responds; those need trials in the real clients. Marking an agent as a specialist does not by itself isolate its access in every client. Installing into the user profile for every client relies on the Code Workflow installer, since an APM global install keeps Copilot agents at project level.

## Artifact categories with nothing environment-specific in them

Every canonical category is present. What the pack deliberately does not contain is anything tied to a real environment: no credentials, MCP registrations, deployment manifests or project identifiers, because an architecture pack is reused across organizations. The integration contract lists the inputs a user supplies for each task instead.
