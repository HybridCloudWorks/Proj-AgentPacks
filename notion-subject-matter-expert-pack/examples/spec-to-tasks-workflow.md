# Worked example: offline mode spec to tasks

Synthetic scenario; the spec, database and team are invented.

Request: "Read the Offline Mode spec and create the implementation tasks in our Engineering Tasks database."

1. Find and fetch. notion-spec-to-tasks finds two candidates, "Offline Mode spec" and "Offline Mode spec (draft, old)". It asks which one; the user picks the first. The agent fetches it and its linked sync design page.
2. Parse. Nine functional requirements, three non-functional (sync within 30 seconds of reconnecting, local data encrypted at rest, no data loss on conflict), six explicit acceptance criteria. Two problems: "conflicts should be handled gracefully" is not testable, and the spec both requires last-write-wins and forbids losing edits. Both become clarification items.
3. Plan. Three phases (local storage, sync engine, conflict handling and polish) with exit criteria. Fourteen tasks of half a day to two days, sequenced along the critical path. Conflict-handling tasks are marked blocked on the clarification.
4. Database. The agent fetches Engineering Tasks: data source identified; properties Name, Status (Backlog, In progress, In review, Done), Priority (P0 to P3), Estimate (select), Blocked by (self-relation), Spec (relation), Assignee (person). It cannot see automations and asks; the user says new entries post to the team channel.
5. Approval. The agent shows the fourteen tasks with priorities, estimates and dependencies, noting that each creation will post to the channel. The user approves the eleven unblocked tasks and asks to hold the three conflict tasks.
6. Create. The plan page is created under the project page the user named. Eleven tasks are created with Status Backlog, the spec relation, and Blocked by relations. Assignee is left empty.
7. Link. The user asked for the spec to link to the plan, so the agent appends an "Implementation" section to the spec without changing its existing text.
8. Verify. The agent queries the database for tasks related to the spec: eleven found, properties valid, relations in place. The plan and the spec are fetched and their links confirmed.

Report: BLOCKED_ON_HUMAN_DECISION. Every write was confirmed, but the criterion "conflict handling is planned" cannot pass until the spec's contradiction is resolved. The eleven verified tasks are listed in `notion_changes`, the clarification items and the three held tasks in `followups`, and the team-channel posts under `notifications_and_automations`.
