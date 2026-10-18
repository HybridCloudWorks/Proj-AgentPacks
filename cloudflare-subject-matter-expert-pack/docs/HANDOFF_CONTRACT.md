# Handoff contract

The installed contract instruction carries these rules for the agents; `templates/handoff.md` is the human-readable form.

## Parent request

The primary sends: goal; scope and non-goals; target scope (account, zone, Worker, environment, identifiers redacted unless the specialist needs them); products and plan tier as known; verified facts and assumptions; relevant files; sources consulted with dates; acceptance criteria; risks; prohibited actions; approval state; requested output.

It never sends credentials, raw secrets or unredacted personal data. For the migration analyst it also sends the export file paths, the workspace folder the analyst may write to, and the Cloudflare documentation excerpts it needs, because the analyst has no web access.

## Specialist return

Findings with location and evidence; changes made inside the assignment (the analyst's mapping files; nothing for the reviewer); checks with results and skips; unverified items; next action.

- The security reviewer returns findings with severity (Critical, High, Medium, Low, Informational), location, evidence, impact, recommended change, blocking flag, confidence and residual uncertainty. It never edits, executes or calls account APIs.
- The migration analyst returns the accounting table, counts by disposition, the checker output, unresolved references, owner decisions, prerequisites in order and unverified items. It never contacts Cloudflare or source-vendor systems.

## Reconciliation

The primary resolves conflicts against the current request, the acceptance criteria and verified facts, reviews the final diff and change plan, and owns completion. A specialist cannot approve its own scope expansion or any Level 2 step. If the host cannot delegate, the primary does the same narrow task with the same skills and reports that limit.
