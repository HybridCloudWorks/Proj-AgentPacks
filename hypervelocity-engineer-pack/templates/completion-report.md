# Completion report

The seven section names come from the `hypervelocity-engineer-contract` instruction and `tests/report-contract.yml`. Keep them verbatim and in this order so a report can be checked mechanically. Replace every `<...>`.

```markdown
Outcome: <one plain sentence: what was achieved, and what is blocked or unverified>

**objective**: <the outcome the user asked for, in one or two sentences>

**scope-and-authorization**: <what this task was authorized to do; what it was not authorized to do and therefore did not do; approvals asked for during the task and the answers; earlier approvals reused and the scope they covered>

**actions-and-changed-files**: <each action taken; each file created or changed, source and generated; each external write with its target, such as a push, pull request, comment, reply, thread resolution or run>

**evidence**:
- Observed: <facts seen directly, each with its source: command, log, run ID, file, API response>
- Inferred: <conclusions drawn from observed facts, with the reasoning>
- Unavailable: <evidence that could not be obtained, and why>

**validation**:

| Check | Command or method | Result |
|---|---|---|
| <check> | <exact command or method> | <passed / failed: reason / not run: reason> |

**risks-and-limitations**: <what remains unverified, including live behavior when only static checks ran. Always state permissions, safe outputs, secrets, network and approval boundaries, even when unchanged.>

**next-safe-action**: <the single next step, who takes it, and any approval it needs>
```

## Rules

- Never report an unexecuted check as passed. "not run" with a reason is a valid result.
- Never claim a live workflow result from `gh aw compile` or `gh aw validate` alone.
- Ask before external writes, permission changes, merges, releases or production impact, and record the question and answer under scope-and-authorization.
- The contract defines sections, not status codes. Say the outcome in plain words.
