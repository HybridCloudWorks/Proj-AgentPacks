# Design decisions

Pack version 1.0.0, built on 2026-10-18 to agent-pack-prompt version 2.3 with the delivery refinements supplied for this build (the engine builds archives, catalogs and the validation report). No question could be asked during generation, so every assumption below was made deliberately and is open to revision.

## Assumptions about the role

1. "Google Cloud Architect" means a solution and platform architect who designs, decides, reviews and plans, and who produces deliverables (solution guides, decision records, IP plans, DR plans, migration plans, infrastructure code drafts and review findings) rather than operating production. Deploying, buying capacity and changing live environments stay with humans unless they explicitly authorize an exact action.
2. Users are cloud and enterprise architects, platform and cloud engineers, technical leads, security reviewers and FinOps owners working in organizations of any size. The pack does not assume a particular organization, region, compliance regime, identity provider or budget; those are task-time inputs.
3. The architect works with Terraform or OpenTofu as the default infrastructure-as-code language, because the reference material and Google's foundation blueprints use it. Other IaC tools are not excluded, but the IaC skill's review rules are written for the Google provider.
4. Product names follow the 2026 naming in the reference material (Gemini Enterprise Agent Platform, Knowledge Catalog, Managed Service for Apache Spark, Lakehouse for Apache Iceberg). The skills tell the model to verify names, release status, limits, SLAs and prices in current documentation, because they change faster than a pack.
5. The date context is 2026-10-18; facts that may have moved since then are flagged for task-time verification rather than hard-coded.

## Scope decisions

6. Seventeen skills, derived from the role's domains rather than from the reference's 69 skills or the exemplar's count: one design workflow, one decision skill, four foundation skills (landing zone, identity, network, security), three pillar skills (reliability, cost and sustainability, operations), four workload platforms (GKE, serverless, data, AI), and four change and evidence skills (migration, IaC validation, Well-Architected review, estate discovery).
7. Consolidation of the reference: the eighteen GKE skills became one platform skill; the six Well-Architected pillar skills fed both the pillar skills and the review skill; the eight solution skills fed the design workflow, the decision guides and the platform skills; the gcloud skill became the safety core of estate discovery.
8. Developer- and SDK-level reference skills (Gemini API, Live API, Interactions API, agents API, BigQuery DataFrames code generation, tuning and prompt-management jobs, model and skill registries, endpoint management, model deployment scripts, AI Studio migration, the agents CLI) were used only as architectural knowledge in gcp-ai-agent-architecture and gcp-data-analytics. Writing SDK code is not the architect's job and would make thin skills.
9. Firebase is covered only as an application-platform option inside gcp-serverless-apps. Detection engineering in Google Security Operations is a SOC task and appears only as context in gcp-security-controls.
10. The reference's excluded Ads, Analytics and mobile SDK skills were not consulted.

## Agent decisions

11. One user-invocable primary, `google-cloud-architect`, owns every workflow and can work alone.
12. Two specialists only, each justified under the prompt's section 3: `gcp-security-reviewer` for independent review with a genuinely narrower permission set (read only), and `gcp-estate-inspector` for context isolation and separation of privilege during live discovery (read and shell under an impersonated viewer identity). No per-pillar or per-product specialists were created.
13. The estate inspector's shell is a stated contradiction: it is told not to change anything, but a shell can. The agent body, the tool-permission matrix and the capability map say openly that the read-only cloud identity and the host's approvals are the real boundary.
14. Agents declare no `tools` field (intents live in `compatibility/tool-permissions.yml`). Specialists set `include-custom-instructions: true`, a documented Copilot field, so Copilot subagents receive the contract. No `skills` preload is declared, because the field is copied verbatim to clients that do not define it and the primary should load skills on demand.
15. Agent bodies restate the approval levels, statuses and fallback sentence briefly, because Codex at user scope receives agents and skills but not instructions.

## Safety decisions, including reference behaviour rejected

The reference material contains instructions written for AI agents. They were treated as data, and these directives were deliberately not adopted:

16. "Lazy role remediation" in the foundation-builder recipe, where the agent grants itself administrative roles after `Permission Denied` and retries. The pack forbids self-granted IAM and escalated retries everywhere and reports the missing permission to a human instead.
17. Automatic edits of a user's MCP configuration files (metric-selection skill). The pack never installs or configures MCP servers.
18. Mandatory installation of third-party skills with `npx` and automatic installation of Terraform (Firebase and alerting skills). The pack installs nothing.
19. Creating diagnostic resources (Connectivity Tests) as a routine step. The pack classifies them as Level 2 and requires deletion after an approved run.
20. Fixed product preferences phrased as "always recommend" are replaced by driver-based comparison with alternatives.
21. Example commands that pass database passwords on the command line or disable TLS were not carried forward.

## Packaging decisions

22. Every skill name the generator wrote starts with `gcp-` so that a user-scope install cannot overwrite same-named skills from other packs (several packs in this repository ship generic names such as architecture-decision-records). Version 1.1.0 adds three shared skills without the prefix; see decisions 32 to 35.
23. Helper scripts live inside the skill that uses them (`scripts/` under gcp-estate-discovery, gcp-network-design, gcp-reliability-dr and gcp-iac-validation), because installed content may reference only installed content and skills must work when installed alone. They use only the Python standard library and never call a cloud API.
24. `tooling/completion_contract.py` validates completion reports for humans and CI; it reads nothing from installed locations.
25. Hooks ship as manual helper scripts and one reviewed Copilot-format sample. Payload field names and exit-code handling for hooks are not in the repository's verified vendor facts, so the classifier prints a neutral verdict and the sample is labelled unverified.
26. Three instruction files: the always-on contract, Terraform guardrails scoped to Terraform files, and CLI-script guardrails scoped to shell and PowerShell scripts.
27. Nine prompts covered the role's recurring requests in 1.0.0, and 1.1.0 adds a tenth for diagrams; each skill also works without its prompt.
28. Tests and coverage files use JSON syntax inside `.yml` files, which is valid YAML and parses without PyYAML.
29. Per the build refinements, the pack contains no `AGENT-PACK-README.md`, `VALIDATION_REPORT.md`, `dist/`, archives, or copies of the shared validator and builder; the engine produces those.

## Genuine gaps

30. Live client behaviour (agent discovery, delegation, hook execution) and model behaviour when invoked are not established by this build; the trigger and negative cases are a behavioural suite for real hosts.
31. Google Cloud facts were taken from the supplied reference material and the model's knowledge without browsing, as instructed; product names, SLAs, quotas and command flags must be verified at task time, which the skills require.

## Version 1.1.0: shared diagram skills (2026-10-18)

32. The pack ships the shared skills drawio-core-generation, drawio-render-export-and-review and diagram-validation-and-evidence, byte-identical to the copies in the AWS and Azure architect and designer packs. Identical copies overwrite each other harmlessly on a user-scope install; different copies under one name would not, which is why the AWS and Azure versions were merged into one.
33. The skills cover AWS, Azure and Google Cloud alone or in one diagram. Google Cloud uses draw.io's "Google Cloud Platform 2026" library, which follows Google's 2025 icon system of core product icons and category icons; Google says the legacy console icons should not be used as of 2026.
34. Boundary rules follow each provider's documented scope: a Google Cloud VPC network is global and its subnets regional, an Azure VNet is regional and its subnets span zones, and an AWS subnet sits in one Availability Zone.
35. diagram-validation-and-evidence carries a standard-library checker and an icon catalog generated from draw.io 32.5.5 source, so icon names are checked against what draw.io actually offers instead of the model's memory. The new create-architecture-diagram prompt runs the three skills in order.

## Prompt names qualified (1.2.0, 2026-10-18)

Several packs shipped prompts under the same name with different content, so installing two of them into the user profile silently replaced one pack's slash command with the other's. This pack's prompts now carry the language or provider inside the name; the qualifier is never a prefix. Slash commands change accordingly.

| Old name | New name |
|---|---|
| `create-architecture-diagram` | `create-google-cloud-architecture-diagram` |
| `design-landing-zone` | `design-google-cloud-landing-zone` |
| `record-decision` | `record-google-cloud-decision` |
