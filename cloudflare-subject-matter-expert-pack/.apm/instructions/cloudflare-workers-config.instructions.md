---
description: "Rules for Wrangler configuration and local Worker secrets files: compatibility settings, bindings, environments, observability and secret handling."
applyTo: "**/wrangler.jsonc,**/wrangler.json,**/wrangler.toml,**/.dev.vars*"
---

# Cloudflare Workers configuration

- Check field names and binding shapes against the project's installed `node_modules/wrangler/config-schema.json` or current Wrangler documentation before editing; do not add keys from memory. Prefer `wrangler.jsonc` for new projects and keep the existing format in established ones.
- Keep one configuration format per Worker. Set `compatibility_date` deliberately: a recent date for new Workers, and a reviewed, tested bump for existing ones, never a future date. Add compatibility flags such as `nodejs_compat` only with a reason the code needs them.
- Never place credentials in `vars`, `[vars]` or source. Secrets go through `wrangler secret put` or the Secrets Store; local values go in `.dev.vars` or `.env`, which must be git-ignored. Never print secret values or copy them into chat, logs, commits or other files; when editing a local secrets file, change only the named key.
- After any binding change, regenerate types with `wrangler types` instead of hand-editing the `Env` interface, and keep binding names identical between configuration and code.
- Durable Object classes need a new migration tag for every class addition, rename or deletion; never edit or reorder an applied migration. New classes use `new_sqlite_classes`.
- Top-level bindings are not inherited by named environments; repeat them per environment and confirm each environment's resource IDs point at the intended account resources.
- Enable `observability` with an explicit `head_sampling_rate`. Treat `routes`, custom domains and `workers_dev` as production exposure decisions.
- Use the cloudflare-workers-development skill for its configuration checker and full procedure. Deploying, uploading versions or writing secrets is a Level 2 action under the contract.
