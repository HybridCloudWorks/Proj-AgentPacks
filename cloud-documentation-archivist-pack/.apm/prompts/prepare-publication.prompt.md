---
description: "Build, preview and package finished documentation for a static site, wiki, portal or Notion, and publish only with explicit authorization"
agent: cloud-documentation-archivist
---

# Prepare documentation for publication

## Inputs

- The finished documents and their review status.
- The destination: a static site, repository branch, wiki, portal or Notion workspace, plus the exact location and the intended audience.
- The toolchain: build command, preview environment, link checker, versioning model and redirects.
- The authorization: who approved publishing to this destination and this audience, and whether a connector for that destination is available in this session.

## Workflow

1. Apply docs-as-code-and-publishing.
   - Inspect the toolchain, frontmatter schema, navigation, build, link checker, preview, versioning, redirects, assets and publication trigger.
   - Keep authoring, validation, preview, release and publication as separate steps.
   - Build and preview locally when possible. Record warnings, broken links, redirects, version scope and differences between renderers.
   - Write rollback or unpublish steps.
2. Apply documentation-validation-and-link-checking and then docs-security-privacy-and-redaction as a final pass. Never publish secrets, private data, internal endpoints, unapproved architecture or unverified claims.
3. For a Notion, wiki or portal destination, apply knowledge-base-and-taxonomy. Prepare the page's title, metadata, owner, status, related links and next review locally, so the content is complete even when no connector is available.
4. The authorization gate. Publishing, opening a pull request, changing a wiki and writing to Notion are external changes. Make them only when the user has explicitly authorized this destination and audience and a tool for that destination is available. Otherwise stop with a local, publish-ready package and a handoff that states the decision needed.

Never say an external page was created, updated or synchronized unless a tool result proves it. Do not look for another route to the destination when its tool is unavailable.

## Expected output

A publish-ready package, or the published location backed by the tool's result; the build and preview results; rollback or unpublish steps; and a handoff stating who must decide what.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report. Use BLOCKED_ON_SOURCE_OR_OWNER when authorization, the destination or its connector is missing.
