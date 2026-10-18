# Source traceability

## Governing inputs

- The build brief for this pack: role FinOps Professional Practitioner, pack name `finops-professional-practitioner`, delivery rules that override sections 7 and 9 of the master prompt.
- The master prompt, version 2.3 (2026-10-18), shipped as `PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md`.
- The repository's verified client facts (`client-locations.md`, verified 2026-10-18) for agent fields, tool identifiers and what APM generates per target.
- The exemplar pack, used for file layout, document types and test formats only. No role content, names, personas, skills, examples or wording were taken from it.

## Third-party reference material

| Item | Detail |
|---|---|
| Source | Cletrics FinOps Agents, https://github.com/Cletrics/finops-agents |
| License | MIT |
| Copy used | A local snapshot supplied with the build workspace: doctrine notes, ten cost playbooks, about fifty agent definitions, Kubernetes notes and helper scripts |
| How it was used | As domain knowledge. All pack text was written fresh. No passage was copied verbatim. |
| What was not used | Installer and format-conversion scripts, the per-tool folder layout, brand references to a commercial product, links between reference files, and every instruction addressed to an AI agent, which was treated as data |

The reference itself cites FinOps Foundation course material (FinOps Certified Practitioner and FOCUS Analyst), FinOps Foundation case studies and named practitioners. Where the pack relies on those ideas it paraphrases them; it attributes no quotation to a named person.

## Requirement to implementation

| Requirement | Where it is implemented |
|---|---|
| Mission, users, scope, non-goals | DESCRIPTION.md, the primary agent, DESIGN_DECISIONS.md |
| FOCUS cost-column discipline, reconciliation, normalization | focus-billing-data-analysis and its column reference, the cost query instruction, finops_math and its tests |
| Allocation, showback, chargeback | cost-allocation-and-chargeback and its methodology template, the chargeback example |
| Anomalies, masked anomalies, budget alerts | cost-anomaly-management, detect_anomaly and segment tests, the masked anomaly example |
| Forecasts, estimates, unit economics, KPIs | forecasting-and-unit-economics, the forecast and estimate prompts |
| Usage optimization and carbon | workload-optimization and its waste pattern catalog, the cleanup example |
| Commitments, private pricing, licensing, SaaS | rate-optimization and its recommendation template, the commitment example |
| Maturity assessment | finops-maturity-assessment and its capability scorecard, the assessment example |
| Practice operations and governance | finops-practice-governance and its policy template, the monthly review template |
| Specialists and least privilege | the two specialist agents, tool-permissions.yml, AGENT_INVENTORY.md, TOOL_PERMISSION_MATRIX.md |
| Approval, handoff, completion contract | the contract instruction, tests/report-contract.yml, tooling/completion_contract.py, APPROVAL_MATRIX.md, HANDOFF_CONTRACT.md |
| Data confidentiality and untrusted content | the contract instruction, the billing data instruction, the hook runner, SECURITY_AND_DATA_HANDLING.md |
| Hooks | hooks/README.md, the helper scripts and the Copilot sample |
| Evidence and evaluation | tests/, EVALUATION_PLAN.md |

## External knowledge sources

Listed in `compatibility/vendor-sources.yml`. They were taken from the reference material and the verified client facts and were not fetched while building the pack. Third-party documentation keeps its own license.
