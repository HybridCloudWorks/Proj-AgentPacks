# Worked example: usage report without the optional hook

Prompt: `.apm/prompts/report-agent-usage.prompt.md`. Skill applied: `agent-usage-reporting`. The outcome is partly **unverified**: the counts are observed, but the optional hook described by the skill was not available. Paths, identifiers and counts are illustrative.

## Request

> How many agents, skills and tools did my last Claude Code session use? The transcript is `~/.claude/projects/inventory-service/3f9e1c2a.jsonl`.

## 1. Choose the source

| Question | Answer | Label |
|---|---|---|
| Optional Claude Stop hook installed? | no hook script in the repository's Claude hooks folder | observed |
| `AGENT_REPORT_ENABLED` set? | unset | observed |
| Source used | the transcript file named by the user | observed |
| Session window | first to last timestamp in the file: 2026-10-17 14:02 to 15:47 UTC | observed |

The skill describes an optional hook script. This pack build does not ship that script, so the hook path cannot be tested here. The agent does not install or enable a hook. It reads the transcript directly, which the skill allows: "actually observable in the selected transcript".

## 2. Count rules

- A tool call is one `tool_use` block in an `assistant` entry.
- An agent call is a `tool_use` named `Agent`, counted by its `subagent_type` value. The session's own primary agent is not a tool call and is not counted.
- A skill call is a `tool_use` named `Skill`, counted by its `skill` value. No other tool argument is read into the report.
- Lines that are not valid JSON are counted as malformed and skipped.

## 3. Count (read-only)

```python
import collections, json, sys

tools, skills, agents, malformed = collections.Counter(), collections.Counter(), collections.Counter(), 0
for line in open(sys.argv[1], encoding="utf-8"):
    try:
        entry = json.loads(line)
    except json.JSONDecodeError:
        malformed += 1
        continue
    if entry.get("type") != "assistant":
        continue
    for block in entry.get("message", {}).get("content") or []:
        if isinstance(block, dict) and block.get("type") == "tool_use":
            tools[block["name"]] += 1
            if block["name"] == "Skill":
                skills[block.get("input", {}).get("skill", "unknown")] += 1
            if block["name"] == "Agent":
                agents[block.get("input", {}).get("subagent_type", "unknown")] += 1
print(dict(tools), dict(skills), dict(agents), "malformed:", malformed)
```

The script prints names and counts only, never message text.

## 4. Report

| Category | Name | Count | Basis |
|---|---|---|---|
| Agent | `Explore` | 1 | exact |
| Agent | `general-purpose` | 1 | exact |
| Skill | `agentic-workflows` | 1 | exact |
| Skill | `workflow-lifecycle-and-release` | 1 | exact |
| Tool | `Read` | 34 | exact |
| Tool | `Grep` | 12 | exact |
| Tool | `Bash` | 9 | exact |
| Tool | `Edit` | 7 | exact |
| Tool | `Glob` | 6 | exact |
| Tool | `Agent` | 2 | exact |
| Tool | `Skill` | 2 | exact |
| Malformed lines | | 1 | exact; the last line was cut off |

Not reported: tokens, cost and latency. The user asked for activity counts, and the transcript holds no billing data. These counts are operational telemetry. They do not show that the session's work was correct.

## Completion report

Outcome: activity counts observed from the transcript; hook-based reporting unverified because the hook script is not available.

**objective**: Report which agents, skills and tools the user's last Claude Code session used.

**scope-and-authorization**: Read-only access to the transcript the user named. No hook was installed or enabled, and nothing was written.

**actions-and-changed-files**: No files changed. Ran a read-only count over `~/.claude/projects/inventory-service/3f9e1c2a.jsonl`.

**evidence**:
- Observed: the count table, the session window, one malformed line, and the absence of the hook script and `AGENT_REPORT_ENABLED`.
- Inferred: the malformed last line is a write still in progress, since it is the final line and is cut off.
- Unavailable: hook-based counts and per-session byte-offset behavior; token, cost and latency figures.

**validation**:

| Check | Method | Result |
|---|---|---|
| Counts reproducible | script run twice on the same file | passed: identical output |
| No transcript content in the report | report review | passed |
| Hook disabled by default; repeated Stop events not double-counted | hook tests in `agent-usage-reporting` | not run: hook script not available |

**risks-and-limitations**: Counts reflect one transcript file. If the session continued after the file was read, later calls are missing. Permissions: read only. No secrets, network access or safe outputs involved.

**next-safe-action**: If ongoing reporting is wanted, the maintainer supplies the hook script and the repository owner approves enabling it. Until then, reports run on request from transcripts.
