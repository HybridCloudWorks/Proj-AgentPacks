---
description: "Save a conversation, decision, procedure or lesson to Notion as a durable page"
agent: notion-subject-matter-expert
---

# Capture knowledge in Notion

## Inputs

The material to capture (this conversation, pasted notes or a page to revise), the audience, and a destination if the user has one.

## Workflow

Apply notion-knowledge-curation: extract specifics, classify the page type, search for an existing page to update, choose the destination, fetch the schema if it is a database, draft from the page outline, write, propose hub links, and verify by fetching. Ask for the destination when nothing fits rather than guessing a parent. Without a Notion connector, return a ready-to-paste draft.

## Expected output

The page URL, properties set, links added or proposed, and the completion report from the `notion-subject-matter-expert-contract` instruction.
