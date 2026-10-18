# Worked example: replacing a private-access product with Cloudflare One

Request: "We are leaving our current private-access product. Here are its exports (applications, server groups, connector groups, access rules). Map them to Cloudflare and tell us what will not move." Identity provider: SCIM already syncs groups to Cloudflare.

1. Assessment (cloudflare-migration-planning). The primary confirms the exports are structured JSON, lists missing items (hit counts for access rules), and records the target account's plan and the per-application destination limit retrieved from current documentation.
2. Delegation. The exports run to about 1,400 objects, so the primary assigns `cloudflare-migration-analyst` with: export paths, the output folder `migration/`, the documentation excerpts for Access application types, tunnel routes and split tunnels, prohibited actions (no network, no account calls), and the requested output.
3. Analyst result. One tunnel per connector group with replica counts matching connector instances; application IPs and CIDRs as tunnel routes and domains as hostname routes; each access rule as a reusable Access policy; bypass entries as split-tunnel excludes; two IP-allowlisted applications marked `manual_review` pending an egress decision; one rule using a source-only behavior marked `not_migrated` with security impact and owner. The accounting checker reports no errors and `ready_to_enable: false` because two rows need decisions.
4. Primary review. The primary checks the mapping against the Zero Trust design rules (default-deny Access, routes and split tunnels aligned, the private-application allow rule ahead of broad network blocks) and adds the prerequisites in order.
5. Wave plan. Wave 1: one engineering team and two applications, objects created disabled with a `MIG-` prefix, device profile change for the pilot group only, old client left installed for a week, logs compared daily. Rollback: revert the pilot group's device profile and disable the migrated policies by prefix.

Report: ANALYSIS_ONLY with the accounting table, the two owner decisions, and the wave plan. Nothing is created until the owner approves wave 1.
