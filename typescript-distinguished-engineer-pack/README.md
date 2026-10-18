# TypeScript Distinguished Engineer Agent/Skill Pack

This pack creates a Distinguished Engineer for enterprise TypeScript and JavaScript delivery. It is designed for an existing repository: inspect first, preserve local conventions, make the smallest coherent change, validate it, and report evidence honestly.

## Downloads

After `python tooling/build_pack.py`, use:

- `dist/typescript-distinguished-engineer-canonical.zip` - canonical `.apm` Agent and Skills.
- `dist/typescript-distinguished-engineer-prompt.zip` - reusable authoring prompt.
- `dist/typescript-distinguished-engineer-skills.zip` - Skills bundle.
- `dist/typescript-distinguished-engineer-validation.zip` - uppercase validation report.
- `dist/{github-copilot,claude-code,openai-codex,gemini-cli}/*.zip` - vendor targets.
- `dist/skills/<skill>/skill.zip` - one deterministic archive per Skill.
- `dist/typescript-distinguished-engineer-pack.zip` - complete pack.

## Canonical source

```text
.apm/
├── agents/
│   ├── typescript-distinguished-engineer.agent.md
│   ├── typescript-security-reviewer.agent.md
│   ├── typescript-test-engineer.agent.md
│   └── agent-evaluation-engineer.agent.md
└── skills/
    ├── typescript-distinguished-engineer-orchestration/
    ├── typescript-strict-engineering/
    ├── javascript-node-runtime-engineering/
    ├── api-contract-and-integration-engineering/
    ├── enterprise-architecture-and-adr/
    ├── mcp-typescript-engineering/
    ├── agentic-workflow-design/
    ├── agent-state-and-context-engineering/
    ├── playwright-validation/
    ├── layered-testing-and-test-engineering/
    ├── secure-agent-engineering/
    ├── agent-observability-and-telemetry/
    ├── agent-evaluation/
    ├── pull-request-review-and-delivery/
    ├── frontend-react-engineering/
    ├── dependency-supply-chain-and-reproducibility/
    ├── performance-reliability-and-operability/
    ├── cloud-integration-and-identity/
    ├── agentic-cost-and-budget-controls/
    └── requirements-and-change-planning/
```

The generated Copilot target also contains `.github/agents`, `.github/instructions`, `.github/prompts`, a `.github/skills/README.md` compatibility note, and discoverable `.agents/skills`.

## Operating model

The primary agent uses PERCEIVE, PLAN, ACT, VERIFY, and REFLECT. It asks for a plan before broad, destructive, security-sensitive, or architecturally significant work. It may inspect the approved workspace and run local non-destructive checks without additional approval. Deployment, merge, publishing, production changes, access or secret changes, external communication, material cost, external uploads, and destructive actions require explicit approval showing target, parameters, effect, risks, and rollback.

Specialists are advisory and return findings, evidence, tests, limitations, and next action. They do not silently change scope. See `docs/AGENT_HANDOFF_CONTRACT.md`, `docs/TOOL_PERMISSION_MATRIX.md`, and `docs/APPROVAL_MATRIX.md`.

## Install and use

1. Run `python tooling/build_pack.py`.
2. Copy the target for the chosen host into the repository, or install the canonical `.apm` source through the host's pack workflow.
3. Start with repository discovery and the narrowest applicable Skill.
4. Run `python tooling/validate_pack.py --write-report` and each installed Skill through `quick_validate.py`.
5. Read `VALIDATION_REPORT.md` before treating the pack as deliverable.

Do not treat static pack validation as proof that a user's repository compiles, tests pass, a cloud deployment works, an MCP authorization policy is effective, or production state changed.

## Supporting material

- `.apm/instructions/` - shared repository, TypeScript, testing, security, and evidence rules, plus the always-on `typescript-distinguished-engineer-contract` instruction.
- `.apm/prompts/` - repeatable workflows for design, implementation, review, MCP, web, agent design and evaluation, diagnosis, and release readiness. `docs/PROMPT_INVENTORY.md` maps each prompt to its skills and worked example.
- `examples/` - seven synthetic worked walkthroughs, one per prompt workflow (design and implementation, and agent design and evaluation, are paired). Each ends with a completion report in the contract's format, and between them they use all five completion statuses, including blocked and unverified outcomes.
- `templates/` - handoff, completion, ADR, evaluation, tool contract, workflow, and PR-review templates.
- `tooling/` - pack-specific helpers: repository inventory, command guard, completion-report validator, and evaluation-scenario validator. Shared validation and build tooling lives at the pack repository root.
- `hooks/` - local read-only pre/post review checks; they do not publish or mutate external systems.
- `docs/` - decisions, source traceability, matrices, workflow example, and governance.
