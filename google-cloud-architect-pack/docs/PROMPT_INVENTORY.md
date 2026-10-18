# Prompt inventory

| Prompt | Main skills | Expected output |
|---|---|---|
| design-solution.prompt.md | gcp-solution-architecture, gcp-architecture-decisions, platform and pillar skills | Solution guide with requirements, decomposition, product mapping, diagram, recommendations, decision records, deployment guidance, validation plan and completion report. |
| record-google-cloud-decision.prompt.md | gcp-architecture-decisions | Comparison table, cited recommendation, Proposed decision record, open questions and reversal conditions. |
| design-google-cloud-landing-zone.prompt.md | gcp-landing-zone, gcp-identity-access, gcp-network-design, gcp-security-controls | Hierarchy, policy baseline with rollout order, admin group and role model, logging design, decision records and rollout plan. |
| design-network.prompt.md | gcp-network-design, gcp-security-controls | Topology, checked IP plan, connectivity and DNS design, edge choices, firewall and egress model, validation plan. |
| review-architecture.prompt.md | gcp-well-architected-review, gcp-estate-discovery, gcp-security-controls | Prioritized findings with evidence, pillar summaries, items not assessed and a roadmap. |
| validate-iac.prompt.md | gcp-iac-validation | Located findings, risk-ranked plan summary, commands with targets and exit codes, plan limits and completion report. |
| plan-migration.prompt.md | gcp-migration-planning, gcp-landing-zone, gcp-architecture-decisions, gcp-reliability-dr | Assessment, approaches, service mapping, waves, transfer and cutover plan, rollback, cost and decision records. |
| plan-resilience.prompt.md | gcp-reliability-dr, gcp-observability-operations | SLO table, failure modes, DR pattern per tier with RTO and RPO evidence, backup plan, alerting design and tests. |
| optimize-cost.prompt.md | gcp-cost-sustainability, gcp-estate-discovery | Cost drivers, ranked savings with confidence and risk, carbon considerations, governance actions and measurement plan. |
| create-google-cloud-architecture-diagram.prompt.md | drawio-core-generation, drawio-render-export-and-review, diagram-validation-and-evidence | Editable .drawio source with current Google Cloud icons, exports when a renderer is available, a validation report and a completion report. |

With APM, Copilot gets these as prompt files, Gemini CLI as commands, and Claude Code as commands without the `agent` key, which APM removes and warns about. Codex and Kiro get no prompts, so their users start the primary agent and describe the task. No skill depends on a prompt.
