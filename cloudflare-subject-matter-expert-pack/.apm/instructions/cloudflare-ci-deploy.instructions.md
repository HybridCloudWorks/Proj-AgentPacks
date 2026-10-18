---
description: "Rules for CI workflows that build, test or deploy to Cloudflare: token handling, environment gates, preview versus production, and verification steps."
applyTo: "**/.github/workflows/**"
---

# Cloudflare deployments from CI

These rules apply only where a workflow runs Wrangler, Terraform or Pulumi against Cloudflare, or calls the Cloudflare API; ignore them otherwise.

- Read the Cloudflare API token and account ID from repository or environment secrets. Never echo them, never pass them as positional arguments, and never expose them to workflows triggered by untrusted pull requests from forks.
- Give each workflow the narrowest token it needs, ideally one per environment, and keep the workflow's own `permissions` minimal.
- Gate production deploys behind a protected environment or manual approval. Preview uploads (for example `wrangler versions upload` or Pages preview branches) are separate from production promotion.
- Pin the action and Wrangler, Terraform or Pulumi versions the repository already uses. Run `wrangler types --check`, type checks, tests and `wrangler deploy --dry-run` or a plan before the deploy step.
- Follow a deploy with a verification step against the environment that changed, and keep the rollback command documented next to it.
- Use the cloudflare-change-control skill for rollout and rollback, and cloudflare-iac-and-api-automation for pipeline review. Changing a workflow that deploys to production is a reviewable change; running it is a Level 2 action under the contract.
