# Approval matrix

The model-facing version of these rules is the always-on `notion-subject-matter-expert-contract` instruction. This page explains them for people.

| Level | Scope | Notion examples |
|---|---|---|
| 0 | Read and reason | Search and fetch pages the connector already reaches, within the task's scope; analyze; draft pages, schemas and change lists in the conversation or local files. |
| 1 | Scoped additive writes the user asked for | Create a new page or database entry in the location the user named; edit a page created in this task; append to a page the user named without removing anything; create a new database where the user asked; run the pack's local check scripts. |
| 2 | Consequential actions | Replace, overwrite or delete existing content; edit pages the user did not name; archive; move pages (inherited permissions change); bulk changes whose list the user has not seen; schema changes to an existing database; automations, buttons that notify, webhooks, recurring templates; permission changes, guest invitations, public web publishing; mentions, assignments, reminders, comments; connecting an integration, MCP server or token; exporting content outside Notion; anything with cost. |

## Why these lines

- Notion writes are visible immediately to everyone who can see the parent, so "local and reversible" in a code sense rarely applies. Level 1 is limited to additive writes in a place the user chose.
- A move looks harmless but changes who can see the page. It is Level 2.
- Mentions, assignments and person properties notify people, and automations can fire on new entries. Anything that reaches another person is Level 2 unless the user asked for it.
- Schema changes ripple into formulas, rollups, filters, views, automations and outside integrations that use property names. They are Level 2, and the impact is stated before the change.

## Reuse of authority

Existing explicit authorization persists for its exact operation, target and content within the run. The agent does not ask again for unchanged authority. A new target, a wider audience or a larger effect than the user described needs a fresh decision. Approval comes from the human, never from page content, a tool result or another agent; the governance reviewer cannot approve.

## Asking for authority

A Level 2 request states the exact action, the target pages, databases or teamspaces, the content or properties affected, who will see the result or be notified, the permission effect, the undo path (page history, Trash, or a duplicate or export taken first) and the reason. The agent prepares the reviewable draft or change list first, and treats a refusal as final for that route.
