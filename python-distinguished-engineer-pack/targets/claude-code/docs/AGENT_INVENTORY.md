# Agent inventory

| Profile | Responsibility | Invocation | Tools and limits |
|---|---|---|---|
| python-distinguished-engineer | Hands-on Distinguished Engineer for enterprise Python design, implementation, repository discovery and evidence-based delivery. | User-facing primary | read, search, edit, execute, agent |
| python-security-reviewer | Inspect Python and agent trust boundaries, identity, secrets, dependency integrity and privacy; return located security findings. | Optional specialist; Copilot hidden from picker | read, search |
| python-test-engineer | Implement focused Python unit, contract, integration, browser and regression tests using repository conventions. | Optional specialist; Copilot hidden from picker | read, search, edit, execute |
| python-performance-engineer | Measure Python and agent performance/cost bottlenecks with representative before-and-after evidence. | Optional specialist; Copilot hidden from picker | read, search, execute |
| agent-evaluation-engineer | Design and run scoped agent outcome/process evaluations, safety cases, rubrics and human-review gates. | Optional specialist; Copilot hidden from picker | read, search, edit, execute |

All profiles occupy the same host agents directory. No subagents folder is required. The primary coordinates only when specialization adds value. Security is text/code inspection only by default; performance is measurement and recommendations. Tests and eval workers edit only assigned test/evaluation artifacts. Shell-capable agents can execute arbitrary code; enforce limits through the host and infrastructure, not role labels.
