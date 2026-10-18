---
name: notion-meeting-materials
description: Prepare and follow up meetings in Notion - gather project context from the workspace, write an internal pre-read and a participant-facing agenda that keeps internal material out of external hands, and record decisions and action items afterwards. Use when a user asks to prep for, plan or run a meeting, build an agenda or pre-read, set up a recurring meeting page, or capture meeting notes, decisions and follow-ups in Notion.
---

# Notion Meeting Materials

## Purpose and activation

Help people arrive prepared, run focused meetings and leave with decisions and owners written down. Activate for meeting preparation, agendas, pre-reads, recurring meeting pages and post-meeting capture.

## Scope and exclusions

- In scope: decision, status, planning, brainstorming, retrospective, one-to-one and external (customer, partner, vendor) meetings; internal pre-reads; agendas; meeting series pages and meeting databases; post-meeting decisions and action items.
- Out of scope: sending invitations or messages, booking calendars, recording or transcribing meetings, and creating tasks in a task database unless the user asks (then use notion-spec-to-tasks conventions for the task pages).

## Inputs

- Purpose of the meeting and the outcome needed. The purpose decides the structure; if it is unclear, ask.
- Date, time with time zone, duration, attendees, and which attendees are external.
- The related project, previous meetings in the series and specific topics.
- Where meeting documents live: a meetings database, a project page or a series page.

## Dependencies and tools

- The Notion connector's search, fetch and create-pages tools; a data-source query tool when available for task or project status.
- meeting-templates.md in this skill folder: the pre-read outline, agenda outlines per meeting type, the post-meeting capture outline and series structure.

## Workflow

1. Frame the meeting: purpose, outcome, attendees and audience split, timing and location of the documents.
2. Gather context. Search for the project page, previous notes in the series, specifications, open decisions and task status. Fetch the most relevant pages and note their last-edited dates. List gaps instead of filling them.
3. Choose the document set. Every meeting gets an agenda. Add an internal pre-read when internal background, candid assessment or options analysis will help the team. For one-to-one meetings, keep private notes private to the two people.
4. Draft the pre-read. Mark it internal in the title and the first line. Cover the meeting overview, background with cited sources, current status, options with trade-offs, a recommendation if the user wants one, and what the team needs from the meeting. Label general knowledge separately from workspace facts. Aim for two pages or less.
5. Draft the agenda. State the objective, list timed items that fit the duration, name the decisions needed and the questions to answer, and leave an empty action-items section. Keep it professional and free of internal assessments, pricing strategy, negotiation positions and personal data.
6. Link in one direction when the audiences differ: the pre-read links to the agenda; an agenda read by external participants never links to or names the internal pre-read, because the title itself can leak. When every agenda reader is internal, link both ways.
7. Run the pre-publication check on the agenda before it is written or shared. For high-stakes external meetings, ask notion-governance-reviewer for an independent separation review when delegation is available.
8. Write both pages to the agreed location (Level 1). If a meetings database exists, fetch its schema and set properties exactly. Setting attendee person properties or mentioning people notifies them; do it only when asked.
9. After the meeting, capture decisions with rationale and owner, action items with owner and due date, and key outcomes. Update the series page. Create follow-up tasks only on request.
10. Verify by fetching each page; report URLs and what was shared with whom.

## Output

An internal pre-read and an agenda (or the agenda alone), linked as described, with URLs; after the meeting, an updated page with decisions and action items. Without a connector, ready-to-paste drafts.

## Validation

- Agenda item times add up to no more than the meeting length.
- Every factual claim in the pre-read cites a fetched page or is labeled as general knowledge.
- Pre-publication check on anything external readers will see: no internal-only markers, no internal pre-read title or link, no credentials, no unfilled placeholders, and every mention uses a URL from a fetched result.
- Both titles carry the meeting date.

## Failure handling and escalation

- Purpose or audience unclear: ask before drafting; the structure depends on it.
- No relevant workspace context: say so in the pre-read and keep it short; do not pad with generic advice.
- Context is stale: flag the last-edited dates and the questions to confirm in the meeting.
- Leak found in an external draft: fix the draft, or return CHANGES_REQUIRED when the user must decide what to remove.

## Permissions and guardrails

- Creating the documents in the agreed location is Level 1. Sharing them with guests, publishing them, mentioning attendees, commenting or sending notifications is Level 2.
- Never invent attendees, metrics, prices or commitments.
- Customer and partner research uses only workspace content and clearly labeled public, general knowledge.

## Workflow connection

The primary `notion-subject-matter-expert` agent uses this skill through the pack's meeting prompt, often together with notion-research-synthesis for the background section. Installed alone, it is self-contained: create documents only where the user agreed, keep external agendas clean, and verify by fetching. With the full pack installed, the `notion-subject-matter-expert-contract` instruction supplies the approval levels, handoff rules and completion report.
