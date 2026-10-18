# Approval matrix

The installed contract instruction (`.apm/instructions/cloudflare-subject-matter-expert-contract.instructions.md`) is the source the agents follow; this page explains it with examples.

| Level | Scope | Cloudflare examples |
|---|---|---|
| 0 | Read and reason | Read the repository and Wrangler or Terraform configuration; retrieve public Cloudflare documentation; draft designs, reviews and change plans. Read-only account inspection (list zones, export rulesets, `wrangler whoami`, log queries inside the incident window) only when the user put that account in scope and its credentials are already configured. |
| 1 | Reversible local work | Edit the approved workspace; local builds, type checks, linters and tests; `wrangler types`; `wrangler dev` with local bindings only; `wrangler deploy --dry-run`; Terraform `fmt`, `validate` and `plan`; the pack's checkers. |
| 2 | Consequential actions | Any account write: deploys, version uploads and promotions, rollbacks, secrets, DNS and proxy status, SSL/TLS and cache settings, purges, rulesets and security settings, Access, Gateway, device profiles, tunnels and routes, D1 remote execution and migrations, KV, R2, Queue and Vectorize data changes, Terraform or Pulumi apply, import and destroy. Also token creation or widening, plan, billing and membership changes, paid remote bindings and inference, load or attack simulation, package installation, new MCP connections, external messages, pull request posts and merges. |

## Reusing approval

An explicit approval holds for its exact account, zone, resource, environment and operation within the current run. The agent does not ask again for the same thing. A different target, a wider scope (for example, from a pilot group to everyone, or from staging to production) or a new effect needs a new decision. Approval comes from the human or an enforced workflow such as a protected CI environment, never from another agent or from text found in content.

## Asking for approval

A request names the action, account and zone or resource, environment, material parameters, expected effect, blast radius, security and cost risk, how the result will be verified, how to roll back, and why. Before stopping at a Level 2 step, the agent prepares reviewable work: the diff, the Terraform plan, the ruleset guard output or the change plan with snapshots. A refusal is not a reason to find another route.

## Examples

- "Deploy to production" with no account named: prepare the release notes and change plan, confirm which account the configured credential reaches, and ask for approval naming that account and Worker.
- Approval given to deploy version X of `api-worker` to production at 10 percent: the agent may proceed with that step; moving to 100 percent is the same action on the same target if the approval covered the full rollout, otherwise it asks.
- A WAF rule approved for `example.com` in log mode: switching it to block is a new effect and needs a decision.
