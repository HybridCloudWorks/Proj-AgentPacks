---
description: "Break a Notion spec into an implementation plan and tracked tasks"
agent: notion-subject-matter-expert
---

# Plan a spec's implementation

## Inputs

The spec page or its name, the task database to use, team conventions for sizing, priority and status, and whether tasks carry assignees and due dates.

## Workflow

Apply notion-spec-to-tasks: find and fetch the spec, parse it with the checklist, plan phases, size and sequence tasks, fetch the task database schema and data source, show the task list for approval unless it was already approved, then create the plan and tasks, link spec, plan and tasks, and verify by fetching. Leave assignees and due dates empty unless the user supplied them.

## Expected output

The plan URL, task URLs, the requirement-to-task trace, clarification items, and the completion report from the `notion-subject-matter-expert-contract` instruction.
