# Cloudflare knowledge and integration contract

## Knowledge sources

Current Cloudflare documentation at developers.cloudflare.com (product pages, limits and pricing pages, the API reference, the Rules language reference, the traffic sequence and changelog), the project's installed `node_modules/wrangler/config-schema.json` and `@cloudflare/workers-types`, and the documentation for the exact Terraform provider or SDK version pinned in the repository. The skills deliberately carry no limits or prices; those are retrieved at task time with source and date.

## Wrangler

The project's pinned Wrangler runs credential-free local commands. Account commands use the user's existing `wrangler login` session or `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` from the environment, never a token typed into chat or passed as an argument. If Wrangler is missing, installing it is a package change the user approves.

## Cloudflare API, SDKs, Terraform and Pulumi

Scoped API tokens only, with permission groups and resources limited to the job; separate tokens per pipeline and environment. Scripts page through results, bound concurrency, honor `Retry-After` and make writes idempotent. Ruleset replacements go through the ruleset guard. Terraform and Pulumi follow the pinned provider version, import before managing, and apply only reviewed plans.

## Cloudflare MCP servers

Cloudflare publishes remote MCP servers for documentation, bindings, builds, observability and API access. This pack does not declare or register them, because connecting a server is a Level 2 action the user must choose. When the user has connected them, agents call them by fully qualified tool names, use read tools inside scope and treat write tools as account writes.

## CI

The repository's existing workflow and action versions. Tokens come from CI secrets, production deploys sit behind a protected environment, and every deploy step is followed by verification. Workflows triggered by untrusted forks never receive Cloudflare secrets.

## Other tools

`cloudflared` and the device client CLI for local diagnostics on machines the user controls; `curl`, `dig` and `openssl` for read-only probes of hostnames the user owns; a browser trace tool or a DevTools MCP server for performance audits when the user has one.

## What is not configured

No account, zone, plan, token, tunnel, MCP server, CI secret or paid model is configured by the pack. Missing integration details are task-time inputs, never placeholders filled with guesses in runnable configuration.
