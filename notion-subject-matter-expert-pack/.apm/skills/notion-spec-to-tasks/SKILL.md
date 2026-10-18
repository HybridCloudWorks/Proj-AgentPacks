---
name: notion-spec-to-tasks
description: Turn a product or technical specification in Notion into an implementation plan, right-sized tasks in the team's task database with testable acceptance criteria and dependencies, and progress updates that keep spec, plan and tasks linked as work and the spec change. Use when a user asks to break down a spec, PRD or design document into tasks, create an implementation plan, track progress against a spec, or update tasks after a spec changes.
---

# Notion Spec to Tasks

## Purpose and activation

Make the path from requirements to done visible in Notion: every requirement maps to tasks, every task knows why it exists and how it will be accepted, and status reflects reality. Activate for spec breakdowns, implementation plans, task creation, progress tracking and spec-change propagation.

## Scope and exclusions

- In scope: locating and reading specs, extracting requirements and acceptance criteria, gap and conflict detection, phased plans, task sizing and sequencing, task pages in an existing task database, dependencies, progress notes, milestone summaries and spec-change logs.
- Out of scope: writing the code itself, creating the task database from scratch (notion-database-design), assigning people or notifying them without being asked, and sprint commitments the team has not made.

## Inputs

- The spec: a page link, or a name to search for.
- The task database to use, or permission to search for it.
- Team conventions: sizing unit, priority scale, status values, whether tasks carry assignees and due dates.
- Any delivery constraints: deadlines, fixed scope, dependencies on other teams.

## Dependencies and tools

- The Notion connector's search, fetch, create-pages and update-page tools; a data-source query tool when available for progress roll-ups.
- plan-and-task-templates.md in this skill folder: spec parsing checklist, plan outline, task page outline, sizing and naming rules, progress note and spec-change log.

## Workflow

1. Find the spec. If search returns several candidates, show them and ask. Fetch the full page and any linked design pages it depends on.
2. Parse it with the checklist: functional and non-functional requirements, explicit and implied acceptance criteria rewritten to be testable, constraints, in and out of scope, dependencies, risks, open questions and conflicts. Record a short quality assessment.
3. Plan phases and milestones, the technical approach at the level the spec supports, risks with mitigations, and success criteria. Unclear requirements become clarification items, not guesses.
4. Break work into tasks of roughly half a day to two days, each with one deliverable and testable acceptance criteria. Choose slicing by component, by vertical feature slice or by priority, and sequence along the critical path.
5. Find the task database, fetch its schema and identify its data source, required properties, status values and relation properties (project, spec, blocked by). Ask whether automations fire on new entries if the connector cannot show them.
6. Show the task list (title, priority, estimate, dependencies) before creating it, unless the user already approved this exact list. Creating entries in a shared database can trigger automations and notifications.
7. Create the plan page in the agreed location, then the tasks with the database's data source as the parent and properties set exactly as fetched. Leave assignees and due dates empty unless the user supplied them. Set dependencies with relation properties when the database has them.
8. Link: the plan cites the spec, every task cites the spec and the plan, and the plan lists its tasks. Adding an "Implementation" link section to the spec page is an edit to that page; do it when the user asked, otherwise propose it.
9. Track progress on request: status changes with a dated progress note (done, in progress, next, blockers, decisions), plan phase status from the task database, and honest reporting of slips.
10. When the spec changes, compare it with the plan, list added, changed and removed requirements and their task impact, update or create tasks after approval, and append a dated entry to the plan's change log.
11. Verify by fetching the plan and querying or fetching the created tasks: count, properties, relations and links.

## Output

An implementation plan page, task entries with URLs, a requirement-to-task trace, clarification items, and the completion report. Progress updates and change logs on request.

## Validation

- Every requirement maps to at least one task or is explicitly deferred; every task maps back to a requirement.
- Every acceptance criterion is testable as written.
- No task estimate exceeds the team's limit without being split or justified.
- The number of created entries matches the approved list, and every property value exists in the fetched schema.

## Failure handling and escalation

- Spec not found or ambiguous: ask for the link; do not plan from a guessed page.
- Task database not found: ask for it, or offer notion-database-design to create one in an agreed location.
- Conflicting requirements: record the conflict and return BLOCKED_ON_HUMAN_DECISION for the affected tasks while creating the unaffected ones if the user agrees.
- Creation fails partway: stop, list what was created with URLs, and do not retry blindly into duplicates.

## Permissions and guardrails

- Creating the plan page and the approved tasks where the user asked is Level 1. Assigning people, mentioning them, setting reminders, editing tasks the user did not name, and bulk status changes are Level 2.
- Never mark a task done without evidence that its acceptance criteria are met.
- Never invent estimates the team will read as commitments; label them as proposals.

## Workflow connection

The primary `notion-subject-matter-expert` agent uses this skill through the pack's spec prompt. Installed alone, it is self-contained: read the spec freely, show the task list before bulk creation, and never assign or notify people unless asked. With the full pack installed, the `notion-subject-matter-expert-contract` instruction supplies the approval levels, handoff rules and completion report.
