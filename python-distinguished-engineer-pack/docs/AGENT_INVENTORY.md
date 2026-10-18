# Agent inventory

| Profile | Responsibility | Invocation | Declared intent (see TOOL_PERMISSION_MATRIX.md) |
|---|---|---|---|
| python-distinguished-engineer | Hands-on Distinguished Engineer for enterprise Python design, implementation, repository discovery and evidence-based delivery. | User-facing primary | read, edit, shell, delegate |
| python-security-reviewer | Inspect Python and agent trust boundaries, identity, secrets, dependency integrity and privacy; return located security findings. | Optional specialist; Copilot hidden from picker | read |
| python-test-engineer | Implement focused Python unit, contract, integration, browser and regression tests using repository conventions. | Optional specialist; Copilot hidden from picker | read, edit, shell |
| python-performance-engineer | Measure Python and agent performance/cost bottlenecks with representative before-and-after evidence. | Optional specialist; Copilot hidden from picker | read, shell |
| agent-evaluation-engineer | Design and run scoped agent outcome/process evaluations, safety cases, rubrics and human-review gates. | Optional specialist; Copilot hidden from picker | read, edit, shell |

All profiles occupy the same host agents directory. No subagents folder is required. The primary coordinates only when specialization adds value. Security is text/code inspection only by default; performance is measurement and recommendations. Tests and eval workers edit only assigned test/evaluation artifacts. Shell-capable agents can execute arbitrary code; enforce limits through the host and infrastructure, not role labels. Canonical agents declare no `tools` field; APM-generated agents inherit the host's tools, and the intents above are what an installer that generates vendor files should apply.
