---
description: "Build or change a Cloudflare Workers application with its bindings, storage and tests"
agent: cloudflare-subject-matter-expert
argument-hint: "[feature or change]"
---

# Build a Workers application

## Inputs

The feature and acceptance criteria, the repository, pinned Wrangler and types versions, bindings and environments. Discover local facts first; do not invent resource IDs or credentials.

## Workflow

Apply cloudflare-workers-development: run its configuration checker, retrieve current documentation for the APIs used, implement, regenerate types and test locally. Apply cloudflare-storage-and-state for any data store, Durable Object, queue or Workflow. Stop before deploying, writing secrets or running remote migrations, and prepare the release notes for cloudflare-change-control.

## Expected output

The scoped diff, checker result, tests, commands with exit codes and environment labels, release notes (bindings, secrets to set, migrations, routes) and a completion report under the `cloudflare-subject-matter-expert-contract` instruction. Without a live deploy the status is CHANGE_PREPARED_NOT_APPLIED.
