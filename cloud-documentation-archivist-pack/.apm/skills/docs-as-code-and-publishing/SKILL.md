---
name: docs-as-code-and-publishing
description: Design and operate repository-based documentation workflows, static-site builds, previews, versioning, publication, redirects, and documentation CI safely.
---

# Docs as Code and Publishing

Inspect the documentation toolchain, source roots, frontmatter schema, navigation, build command, link checker, preview environment, versioning model, redirects, assets, and publication trigger before editing. Do not assume Markdown renders identically across GitHub, a static site, a wiki, and a knowledge tool.

Separate authoring, validation, preview, release, and publication. Use a pull request or equivalent review gate for generated docs. Record build output, warnings, broken links, redirects, version scope, and known renderer differences.

Publishing is an external mutation. Keep it approval-gated, verify destination and audience, and provide rollback or unpublish steps. Never publish secrets, private data, internal endpoints, unapproved architecture, or unverified claims.
