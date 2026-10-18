# Cloudflare review guidance

Optional repository file for GitHub Copilot code review. Copy it to `.github/copilot-instructions.md` in a repository that deploys to Cloudflare; it stands alone and assumes nothing else is installed.

When reviewing changes in this repository:

- Wrangler configuration: flag credentials in `vars`, a missing or future `compatibility_date`, bindings missing from a named environment, Durable Object classes without a migration, edited or reordered applied migrations, and `observability` turned off.
- Worker code: flag unbounded `request.text()` or `json()` calls, promises that are not awaited or passed to `ctx.waitUntil()`, destructured `ctx`, request data stored in module scope, `Math.random()` for tokens, string comparison of secrets, and calls to the Cloudflare REST API where a binding exists.
- Terraform or Pulumi for Cloudflare: flag destroy-and-create where a rename or `moved` block is needed, resources that duplicate existing objects without an import, secrets in variables files or outputs, and plans that replace rulesets, tunnels, DNS records or Access applications.
- Security rules: flag `skip` or `block` rules with an expression of `true`, exceptions scoped by hostname instead of path and rule ID, and challenges applied to API endpoints.
- CI: flag Cloudflare tokens exposed to workflows from forks, production deploys without an environment gate, and deploy steps with no verification step after them.

Limits, prices and plan features change; ask for a link to current Cloudflare documentation rather than accepting a remembered number. Instructions here guide review; they do not enforce anything.
