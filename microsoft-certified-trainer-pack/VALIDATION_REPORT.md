# VALIDATION_REPORT

Pack: microsoft-certified-trainer 1.1.0
Standard: agent-pack-prompt v2.2
Validated: 2026-10-18
Status: PASS

Checks: 192  Passed: 191  Failed: 0  Skipped: 1

## Scope

5 agents, 18 skills, 7 instruction files, 12 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

## Failed checks

- None

## Not established

- Agents appear and run in the VS Code agent pane for Claude Code, Codex, and GitHub Copilot.
- A user-profile install (Code Workflow installer, or `apm install -g`) behaves identically on Windows and macOS.
- Kiro and Antigravity IDE behaviour, and Gemini CLI behaviour, on a live install.
- Model behaviour of the agents when actually invoked; tests cover helper code and contracts only.
- Hook behaviour: hooks ship as helper scripts and samples; no native hook was installed or exercised.

## Check inventory

| Kind | Check | Result | Detail |
|---|---|---|---|
| structural | required artifact apm.yml | pass |  |
| structural | required artifact DESCRIPTION.md | pass |  |
| structural | required artifact README.md | pass |  |
| structural | required artifact LICENSE | pass |  |
| structural | required artifact PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | pass |  |
| structural | required artifact docs | pass |  |
| structural | required artifact compatibility | pass |  |
| structural | required artifact examples | pass |  |
| structural | required artifact templates | pass |  |
| structural | required artifact hooks/README.md | pass |  |
| structural | required artifact tests | pass |  |
| structural | required artifact .apm/agents | pass |  |
| structural | required artifact .apm/skills | pass |  |
| structural | required artifact .apm/instructions | pass |  |
| structural | required artifact .apm/prompts | pass |  |
| structural | no stale folder targets/ | pass |  |
| structural | no stale folder claude-code/ | pass |  |
| structural | no stale folder gemini-cli/ | pass |  |
| structural | no stale folder github-copilot/ | pass |  |
| structural | no stale folder openai-codex/ | pass |  |
| structural | no stale folder instructions/ | pass |  |
| structural | no stale folder prompts/ | pass |  |
| structural | no __pycache__ or .pyc outside tests/ and tooling/ | pass |  |
| structural | no archives at pack root | pass |  |
| structural | no native hook JSON for APM to deploy | pass | native hooks would carry repository-relative commands; hooks ship as helper scripts and samples |
| structural | no per-pack copy of tooling/validate_pack.py (shared tooling lives at the repository root) | pass |  |
| structural | no per-pack copy of tooling/build_pack.py (shared tooling lives at the repository root) | pass |  |
| structural | apm.yml uses only APM-defined fields | pass |  |
| structural | apm.yml has name and version | pass |  |
| structural | apm.yml version is semantic | pass |  |
| structural | apm.yml name equals the pack folder name without -pack | pass | microsoft-certified-trainer vs microsoft-certified-trainer-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent microsoft-certified-trainer: name and description present | pass |  |
| structural | agent microsoft-certified-trainer: file name equals name | pass |  |
| structural | agent microsoft-certified-trainer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent microsoft-certified-trainer: description within 1024 characters | pass |  |
| structural | agent microsoft-certified-trainer: body within 300 lines | pass |  |
| structural | agent microsoft-copilot-learning-reviewer: name and description present | pass |  |
| structural | agent microsoft-copilot-learning-reviewer: file name equals name | pass |  |
| structural | agent microsoft-copilot-learning-reviewer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent microsoft-copilot-learning-reviewer: description within 1024 characters | pass |  |
| structural | agent microsoft-copilot-learning-reviewer: body within 300 lines | pass |  |
| structural | agent microsoft-course-architect: name and description present | pass |  |
| structural | agent microsoft-course-architect: file name equals name | pass |  |
| structural | agent microsoft-course-architect: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent microsoft-course-architect: description within 1024 characters | pass |  |
| structural | agent microsoft-course-architect: body within 300 lines | pass |  |
| structural | agent microsoft-courseware-engineer: name and description present | pass |  |
| structural | agent microsoft-courseware-engineer: file name equals name | pass |  |
| structural | agent microsoft-courseware-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent microsoft-courseware-engineer: description within 1024 characters | pass |  |
| structural | agent microsoft-courseware-engineer: body within 300 lines | pass |  |
| structural | agent microsoft-lab-demo-engineer: name and description present | pass |  |
| structural | agent microsoft-lab-demo-engineer: file name equals name | pass |  |
| structural | agent microsoft-lab-demo-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent microsoft-lab-demo-engineer: description within 1024 characters | pass |  |
| structural | agent microsoft-lab-demo-engineer: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill azure-and-cloud-lab-handoff: SKILL.md with name equal to folder | pass |  |
| structural | skill azure-and-cloud-lab-handoff: description within 1024 characters | pass |  |
| structural | skill copilot-prompting-and-knowledge-checks: SKILL.md with name equal to folder | pass |  |
| structural | skill copilot-prompting-and-knowledge-checks: description within 1024 characters | pass |  |
| structural | skill copilot-studio-course-labs: SKILL.md with name equal to folder | pass |  |
| structural | skill copilot-studio-course-labs: description within 1024 characters | pass |  |
| structural | skill course-architecture-and-syllabus: SKILL.md with name equal to folder | pass |  |
| structural | skill course-architecture-and-syllabus: description within 1024 characters | pass |  |
| structural | skill course-evaluation-and-feedback: SKILL.md with name equal to folder | pass |  |
| structural | skill course-evaluation-and-feedback: description within 1024 characters | pass |  |
| structural | skill git-and-github-course-delivery: SKILL.md with name equal to folder | pass |  |
| structural | skill git-and-github-course-delivery: description within 1024 characters | pass |  |
| structural | skill instructor-led-facilitation: SKILL.md with name equal to folder | pass |  |
| structural | skill instructor-led-facilitation: description within 1024 characters | pass |  |
| structural | skill lab-and-demo-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill lab-and-demo-engineering: description within 1024 characters | pass |  |
| structural | skill learning-objectives-and-assessment: SKILL.md with name equal to folder | pass |  |
| structural | skill learning-objectives-and-assessment: description within 1024 characters | pass |  |
| structural | skill mct-courseware-governance: SKILL.md with name equal to folder | pass |  |
| structural | skill mct-courseware-governance: description within 1024 characters | pass |  |
| structural | skill microsoft-365-apps-workflows: SKILL.md with name equal to folder | pass |  |
| structural | skill microsoft-365-apps-workflows: description within 1024 characters | pass |  |
| structural | skill microsoft-365-copilot-instruction: SKILL.md with name equal to folder | pass |  |
| structural | skill microsoft-365-copilot-instruction: description within 1024 characters | pass |  |
| structural | skill microsoft-designer-and-visual-content: SKILL.md with name equal to folder | pass |  |
| structural | skill microsoft-designer-and-visual-content: description within 1024 characters | pass |  |
| structural | skill microsoft-learn-curriculum-mapping: SKILL.md with name equal to folder | pass |  |
| structural | skill microsoft-learn-curriculum-mapping: description within 1024 characters | pass |  |
| structural | skill powerpoint-courseware-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill powerpoint-courseware-engineering: description within 1024 characters | pass |  |
| structural | skill trainer-automation-and-tools: SKILL.md with name equal to folder | pass |  |
| structural | skill trainer-automation-and-tools: description within 1024 characters | pass |  |
| structural | skill trainer-preparation-and-rehearsal: SKILL.md with name equal to folder | pass |  |
| structural | skill trainer-preparation-and-rehearsal: description within 1024 characters | pass |  |
| structural | skill training-content-maintenance: SKILL.md with name equal to folder | pass |  |
| structural | skill training-content-maintenance: description within 1024 characters | pass |  |
| structural | instruction copilot.instructions.md: description and applyTo | pass |  |
| structural | instruction courseware.instructions.md: description and applyTo | pass |  |
| structural | instruction curriculum.instructions.md: description and applyTo | pass |  |
| structural | instruction delivery.instructions.md: description and applyTo | pass |  |
| structural | instruction mct.instructions.md: description and applyTo | pass |  |
| structural | instruction microsoft-certified-trainer-contract.instructions.md: description and applyTo | pass |  |
| structural | instruction security-and-privacy.instructions.md: description and applyTo | pass |  |
| structural | prompt build-one-day-agenda.prompt.md: description | pass |  |
| structural | prompt create-copilot-studio-workshop.prompt.md: description | pass |  |
| structural | prompt create-interactive-lab.prompt.md: description | pass |  |
| structural | prompt create-knowledge-checks.prompt.md: description | pass |  |
| structural | prompt design-course.prompt.md: description | pass |  |
| structural | prompt engineer-powerpoint-deck.prompt.md: description | pass |  |
| structural | prompt evaluate-session.prompt.md: description | pass |  |
| structural | prompt ingest-mct-courseware.prompt.md: description | pass |  |
| structural | prompt map-learn-content.prompt.md: description | pass |  |
| structural | prompt prepare-instructor-guide.prompt.md: description | pass |  |
| structural | prompt refresh-from-change-log.prompt.md: description | pass |  |
| structural | prompt rehearse-demo.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/microsoft-certified-trainer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/microsoft-copilot-learning-reviewer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/microsoft-course-architect.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/microsoft-courseware-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/microsoft-lab-demo-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/copilot.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/courseware.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/curriculum.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/delivery.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/mct.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/microsoft-certified-trainer-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/security-and-privacy.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/build-one-day-agenda.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/create-copilot-studio-workshop.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/create-interactive-lab.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/create-knowledge-checks.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-course.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/engineer-powerpoint-deck.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/evaluate-session.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/ingest-mct-courseware.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/map-learn-content.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/prepare-instructor-guide.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/refresh-from-change-log.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/rehearse-demo.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/azure-and-cloud-lab-handoff/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/copilot-prompting-and-knowledge-checks/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/copilot-studio-course-labs/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/course-architecture-and-syllabus/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/course-evaluation-and-feedback/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/git-and-github-course-delivery/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/instructor-led-facilitation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/lab-and-demo-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/learning-objectives-and-assessment/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/mct-courseware-governance/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/microsoft-365-apps-workflows/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/microsoft-365-copilot-instruction/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/microsoft-designer-and-visual-content/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/microsoft-learn-curriculum-mapping/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/powerpoint-courseware-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/trainer-automation-and-tools/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/trainer-preparation-and-rehearsal/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/training-content-maintenance/SKILL.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
| structural | pack doc docs/AGENT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/APPROVAL_MATRIX.md: describes the current layout | pass |  |
| structural | pack doc docs/DELIVERABLE_CONTRACT.md: describes the current layout | pass |  |
| structural | pack doc docs/HANDOFF_CONTRACT.md: describes the current layout | pass |  |
| structural | pack doc docs/MS-4018_SOURCE_NOTES.md: describes the current layout | pass |  |
| structural | pack doc docs/PROMPT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/SKILL_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/SOURCE_TRACEABILITY.md: describes the current layout | pass |  |
| structural | pack doc docs/TOOL_PERMISSION_MATRIX.md: describes the current layout | pass |  |
| structural | pack doc compatibility/capability-map.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/compatibility-matrix.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/optional-skills.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/tool-permissions.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/vendor-sources.yml: describes the current layout | pass |  |
| structural | tests/skill-coverage.yml lists exactly the shipped skills | pass | missing: [] extra: [] |
| structural | tests/skill-coverage.yml has an activation statement for every skill | pass |  |
| structural | tests/capability-coverage.yml prompt files exist | pass |  |
| structural | tests/trigger-cases.yml prompt files exist | pass |  |
| structural | an always-on contract instruction exists (.apm/instructions/*contract*.instructions.md) | pass |  |
| structural | contract instruction states every short value listed in report-contract.yml | pass |  |
| executable | pack unit tests | skipped | no test_*.py in tests/ |
| executable | apm compile --validate | pass | [*] All primitives validated successfully! |
| executable | apm install --target copilot,claude,codex,kiro,gemini,agent-skills succeeds | pass |  |
| executable | copilot: 5 agents generated | pass | found 5 |
| executable | claude: 5 agents generated | pass | found 5 |
| executable | codex: 5 agents generated | pass | found 5 |
| executable | kiro: 5 agents generated | pass | found 5 |
| executable | no hook files generated | pass |  |
| executable | claude: instructions generated as rules | pass | found 7 |
| executable | generated vendor files reference only installed things | pass |  |
