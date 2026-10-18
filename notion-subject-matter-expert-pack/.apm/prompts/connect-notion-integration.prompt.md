---
description: "Connect a tool or agent to Notion, or build and debug Notion API code"
agent: notion-subject-matter-expert
---

# Connect or build a Notion integration

## Inputs

What must read or write which pages or databases, the project's language and Notion client, the pinned API version, the authentication method, a test page tree, and for failures the status, error code and request ID with tokens removed.

## Workflow

Apply notion-api-integration. Choose the smallest capability set, pin the API version, resolve schema at runtime, implement bounded retries and pagination, keep tokens out of code and logs, and test with recorded responses first. Connecting a server or integration, sharing pages with it and writing to a real workspace need the user's approval.

## Expected output

Code or configuration changes with test results, the access and capability list, or an error diagnosis with the fix; what was not exercised against a live workspace; and the completion report from the `notion-subject-matter-expert-contract` instruction.
