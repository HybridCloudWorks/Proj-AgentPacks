# Cloud Documentation Archivist Pack

This pack consolidates the supplied Docs & Knowledge Curator, ADR Authoring, Diátaxis guidance, and blog/gist/README/task/workflow templates into a portable documentation expert.

## What is in the pack

- `apm.yml` and `.apm/`: the canonical source. It holds one agent (`cloud-documentation-archivist`), 18 Skills, the always-on `cloud-documentation-archivist-contract` instruction and 11 workflow prompts. Every vendor file is generated from here at install time.
- `docs/`: design decisions, source traceability and the prompt inventory.
- `compatibility/`: capability map, optional Skills, vendor sources and `tool-permissions.yml`.
- `hooks/`: the pre- and post-documentation helper scripts. Nothing here is installed as a native hook.
- `tooling/`: pack-specific helpers for documentation inventory and validation.
- `templates/`: the writing template library, plus the completion report, handoff, documentation plan and source ledger the workflows produce.
- `examples/`: worked walkthroughs of the main workflows.
- `tests/`: Skill coverage, capability coverage, trigger cases, the report contract and fixtures.

## Prompts

| Prompt | Use it to |
| --- | --- |
| `plan-documentation` | Decide reader, mode, canonical source, location and owner, or plan a reorganization |
| `write-tutorial-or-how-to` | Write a tutorial or how-to guide |
| `document-reference` | Document an API, CLI, configuration file, schema or error catalogue |
| `explain-architecture` | Explain architecture, rationale and trade-offs |
| `record-decision` | Record or supersede an ADR |
| `write-runbook` | Create or review a runbook or incident record |
| `synthesize-research` | Turn sources into a cited brief with a source ledger |
| `document-release` | Write changelog entries, release notes or a migration guide |
| `review-documentation` | Review documents for accuracy, links, freshness and exposed data |
| `govern-documentation` | Set the documentation contract, ownership, taxonomy and templates |
| `prepare-publication` | Build, preview and package for publication, behind the authorization gate |

See `docs/PROMPT_INVENTORY.md` for each prompt's Skills and expected output.

## Worked examples

| Example | Workflow | Outcome |
| --- | --- | --- |
| `examples/how-to-guide-workflow.md` | Plan, then write a deployment how-to | REVIEW_REQUIRED |
| `examples/architecture-decision-workflow.md` | Proposed ADR that will supersede an Accepted one | REVIEW_REQUIRED |
| `examples/runbook-from-incident-workflow.md` | Runbook from an incident, with a credential found in the evidence | NOT_VERIFIED |
| `examples/documentation-review-workflow.md` | Read-only review of a documentation pull request | CHANGES_REQUIRED |
| `examples/publication-blocked-workflow.md` | Notion publication with no destination or connector | BLOCKED_ON_SOURCE_OR_OWNER |
| `examples/configuration-reference-workflow.md` | Schema-generated configuration reference | DOCUMENTATION_READY |
| `examples/research-brief-workflow.md` | Cited brief from supplied sources without web access | NOT_VERIFIED |

All examples are synthetic.

## Primary downloads

- `dist/cloud-documentation-archivist-pack.zip` - complete pack
- `dist/cloud-documentation-archivist-canonical.zip` - canonical Agent and Skills
- `dist/cloud-documentation-archivist-prompt.zip` - reusable authoring prompt
- `dist/cloud-documentation-archivist-skills.zip` - individual Skill bundle
- `dist/cloud-documentation-archivist-validation.zip` - uppercase validation report

Vendor packages are under `dist/github-copilot/`, `dist/claude-code/`, `dist/openai-codex/`, and `dist/gemini-cli/`.

## Build and validate

Validation and build tooling is shared at the repository root. Run these commands from the pack folder:

```text
python ../tooling/validate_pack.py . --install-check   # shared validator; writes VALIDATION_REPORT.md
python ../tooling/build_pack.py .                      # shared builder; writes dist/
python tooling/validate_doc_bundle.py templates        # pack helper; template placeholders allowed
python tooling/validate_documentation.py examples/*.md # pack helper; placeholders not allowed
```

After any Skill changes, regenerate `tests/skill-coverage.yml` with `python ../tooling/skill_coverage.py .`. Validation is static and performs no external publication or connector write.

## Operating model

Use `hooks/pre-documentation.*` before authoring and `hooks/post-documentation.*` after writing. The default behavior is local and read-only. Publishing, PR creation, wiki changes, Notion writes, shared links, and other external mutations require explicit authorization.
