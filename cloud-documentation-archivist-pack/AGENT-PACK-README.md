# cloud-documentation-archivist 1.2.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| cloud-documentation-archivist.agent.md | Canonical agent: Repository-neutral documentation expert for cloud architecture, operations, software delivery, research, decisions, templates, knowledge bases, and docs-as-code publishing. | .apm/agents/cloud-documentation-archivist.agent.md |
| cloud-documentation-archivist-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the cloud documentation archivist pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/cloud-documentation-archivist-contract.instructions.md |
| document-reference.prompt.md | Canonical prompt: Create or update reference documentation for an API, CLI, configuration file, schema, resource or error catalogue | .apm/prompts/document-reference.prompt.md |
| document-release.prompt.md | Canonical prompt: Write changelog entries, release notes, deprecation notices or a migration guide from shipped and traceable changes | .apm/prompts/document-release.prompt.md |
| explain-architecture.prompt.md | Canonical prompt: Explain a cloud architecture: rationale, boundaries, data flows and trade-offs, with current, target and proposed state kept apart | .apm/prompts/explain-architecture.prompt.md |
| govern-documentation.prompt.md | Canonical prompt: Set the documentation contract, ownership, templates, taxonomy and lifecycle rules for a documentation repository or knowledge base | .apm/prompts/govern-documentation.prompt.md |
| plan-documentation.prompt.md | Canonical prompt: Plan a document or documentation set: reader, task, content mode, canonical source, location, owner and review cadence | .apm/prompts/plan-documentation.prompt.md |
| prepare-publication.prompt.md | Canonical prompt: Build, preview and package finished documentation for a static site, wiki, portal or Notion, and publish only with explicit authorization | .apm/prompts/prepare-publication.prompt.md |
| record-decision.prompt.md | Canonical prompt: Record a significant architecture or operating decision as an ADR, or supersede an existing one, with options, consequences and evidence | .apm/prompts/record-decision.prompt.md |
| review-documentation.prompt.md | Canonical prompt: Review existing documentation for accuracy, structure, links, freshness, editorial quality and exposure of sensitive data | .apm/prompts/review-documentation.prompt.md |
| synthesize-research.prompt.md | Canonical prompt: Turn cloud research, vendor documentation, incidents and repository evidence into a cited brief or comparison with a source ledger | .apm/prompts/synthesize-research.prompt.md |
| write-runbook.prompt.md | Canonical prompt: Create or review an operational runbook, recovery procedure or incident record from alerts, incidents and operator evidence | .apm/prompts/write-runbook.prompt.md |
| write-tutorial-or-how-to.prompt.md | Canonical prompt: Write a tutorial or how-to guide for a cloud, infrastructure, delivery or operations task with safe verification points | .apm/prompts/write-tutorial-or-how-to.prompt.md |
| SKILL.md | Canonical skill: Author and maintain concise Architecture Decision Records and decision logs with alternatives, consequences, traceability, status, and supersession. | .apm/skills/adr-and-decision-records/SKILL.md |
| SKILL.md | Canonical skill: Record shipped changes, release notes, deprecations, breaking changes, migration paths, and upgrade guidance accurately and traceably. | .apm/skills/changelogs-release-notes-and-migration/SKILL.md |
| SKILL.md | Canonical skill: Classify and design documentation as tutorial, how-to guide, reference, or explanation without mixing reader needs or content modes. | .apm/skills/diataxis-content-design/SKILL.md |
| SKILL.md | Canonical skill: Design and operate repository-based documentation workflows, static-site builds, previews, versioning, publication, redirects, and documentation CI safely. | .apm/skills/docs-as-code-and-publishing/SKILL.md |
| SKILL.md | Canonical skill: Prevent documentation from exposing secrets, personal data, customer information, private infrastructure, unsafe commands, or misleading security claims. | .apm/skills/docs-security-privacy-and-redaction/SKILL.md |
| SKILL.md | Canonical skill: Route documentation requests to the smallest content, governance, template, research, publishing, validation, or knowledge-management Skill. | .apm/skills/documentation-archivist-orchestration/SKILL.md |
| SKILL.md | Canonical skill: Use safe documentation inventory, pre-write checks, post-write validation, template generation, link checks, freshness reports, and publication gates. | .apm/skills/documentation-hooks-and-automation/SKILL.md |
| SKILL.md | Canonical skill: Define why documentation is needed, who it serves, what belongs in it, where it lives, and how it connects to adjacent sources. | .apm/skills/documentation-purpose-and-information-architecture/SKILL.md |
| SKILL.md | Canonical skill: Edit technical documentation for clarity, accuracy, consistency, accessibility, inclusive language, scannability, and maintainable examples. | .apm/skills/documentation-style-and-editorial-quality/SKILL.md |
| SKILL.md | Canonical skill: Validate documentation structure, frontmatter, links, code examples, templates, terminology, freshness, redaction, and report quality. | .apm/skills/documentation-validation-and-link-checking/SKILL.md |
| SKILL.md | Canonical skill: Explain cloud architecture, system behavior, design rationale, trade-offs, boundaries, dependencies, and mental models without turning explanations into procedures. | .apm/skills/explanation-and-architecture-docs/SKILL.md |
| SKILL.md | Canonical skill: Organize durable cloud knowledge with taxonomy, metadata, ownership, lifecycle, search terms, related content, and archive rules. | .apm/skills/knowledge-base-and-taxonomy/SKILL.md |
| SKILL.md | Canonical skill: Govern documentation repositories, ownership, source-of-truth rules, cross-file contracts, lifecycle, review cadence, and documentation change control. | .apm/skills/repository-and-project-doc-governance/SKILL.md |
| SKILL.md | Canonical skill: Synthesize cloud research, product documentation, incidents, conversations, and repository evidence into cited briefs, comparisons, and durable knowledge. | .apm/skills/research-synthesis-and-source-traceability/SKILL.md |
| SKILL.md | Canonical skill: Create and review cloud operational runbooks, troubleshooting guides, recovery procedures, incident records, and support handoffs. | .apm/skills/runbooks-and-operational-docs/SKILL.md |
| SKILL.md | Canonical skill: Create and maintain accurate reference documentation for APIs, CLIs, configuration, schemas, resources, commands, errors, and compatibility. | .apm/skills/technical-reference-and-api-docs/SKILL.md |
| SKILL.md | Canonical skill: Select, adapt, and create reusable documentation templates for blogs, gists, README files, tasks, workflows, ADRs, runbooks, APIs, incidents, migrations, and knowledge pages. | .apm/skills/templates-and-content-models/SKILL.md |
| SKILL.md | Canonical skill: Write practical tutorials and how-to guides for cloud, software, infrastructure, operations, and documentation tasks with safe verification points. | .apm/skills/tutorials-and-how-to-guides/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| architecture-decision-workflow.md | Worked example | examples/architecture-decision-workflow.md |
| configuration-reference-workflow.md | Worked example | examples/configuration-reference-workflow.md |
| documentation-review-workflow.md | Worked example | examples/documentation-review-workflow.md |
| how-to-guide-workflow.md | Worked example | examples/how-to-guide-workflow.md |
| publication-blocked-workflow.md | Worked example | examples/publication-blocked-workflow.md |
| research-brief-workflow.md | Worked example | examples/research-brief-workflow.md |
| runbook-from-incident-workflow.md | Worked example | examples/runbook-from-incident-workflow.md |
| post-documentation.ps1 | Hook helper script | hooks/post-documentation.ps1 |
| post-documentation.sh | Hook helper script | hooks/post-documentation.sh |
| pre-documentation.ps1 | Hook helper script | hooks/pre-documentation.ps1 |
| pre-documentation.sh | Hook helper script | hooks/pre-documentation.sh |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| adr.md | Reusable template | templates/adr.md |
| api-reference.md | Reusable template | templates/api-reference.md |
| architecture.md | Reusable template | templates/architecture.md |
| blog_template.md | Reusable template | templates/blog_template.md |
| changelog.md | Reusable template | templates/changelog.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| documentation-plan.md | Reusable template | templates/documentation-plan.md |
| explanation.md | Reusable template: [Question this explains] | templates/explanation.md |
| gist_template.md | Reusable template | templates/gist_template.md |
| glossary.md | Reusable template | templates/glossary.md |
| handoff.md | Reusable template | templates/handoff.md |
| how-to.md | Reusable template: [Short description] | templates/how-to.md |
| incident-postmortem.md | Reusable template | templates/incident-postmortem.md |
| meeting-notes.md | Reusable template | templates/meeting-notes.md |
| migration.md | Reusable template | templates/migration.md |
| README.md | Reusable template | templates/README.md |
| reference.md | Reusable template: [What this reference defines] | templates/reference.md |
| rfc.md | Reusable template | templates/rfc.md |
| runbook.md | Reusable template | templates/runbook.md |
| security-review.md | Reusable template | templates/security-review.md |
| source-ledger.md | Reusable template | templates/source-ledger.md |
| task.md | Reusable template | templates/task.md |
| tutorial.md | Reusable template: [What the learner will accomplish] | templates/tutorial.md |
| workflow-doc-template.md | Reusable template | templates/workflow-doc-template.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| REVIEW.md | Local test or recorded evidence | tests/fixtures/REVIEW.md |
| valid-document.md | Local test or recorded evidence: A small validation fixture. | tests/fixtures/valid-document.md |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| documentation_inventory.py | Pack-specific helper code | tooling/documentation_inventory.py |
| validate_doc_bundle.py | Pack-specific helper code | tooling/validate_doc_bundle.py |
| validate_documentation.py | Pack-specific helper code | tooling/validate_documentation.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-cloud-documentation-archivist.zip: 31 files generated by `apm install --target copilot`
- claude-cloud-documentation-archivist.zip: 31 files generated by `apm install --target claude`
- codex-cloud-documentation-archivist.zip: 19 files generated by `apm install --target codex`
- kiro-cloud-documentation-archivist.zip: 20 files generated by `apm install --target kiro`
- gemini-cloud-documentation-archivist.zip: 29 files generated by `apm install --target gemini`
- agent-skills-cloud-documentation-archivist.zip: 18 files generated by `apm install --target agent-skills`
- cloud-documentation-archivist-canonical.zip, cloud-documentation-archivist-prompt.zip, cloud-documentation-archivist-validation.zip, cloud-documentation-archivist-skills.zip, cloud-documentation-archivist-full-pack.zip, SHA256SUMS.txt
