# FinOps review guidance for this repository

Optional repository-level instructions for GitHub Copilot code review. Copy to `.github/copilot-instructions.md` in a repository that holds cost queries, FinOps reports or infrastructure code where cost and tagging matter. Nothing in the user-level pack depends on this file.

When reviewing changes:

- SQL that reads billing data states its cost column and filters, bounds the scan by date or partition, excludes corrections from trends and does not sum Purchase and Usage rows of ListCost or ContractedCost together.
- Infrastructure changes carry the organization's mandatory cost tags (for example owner, cost center, environment, application) with allowed values; flag new resources without them.
- Changes that add always-on resources, cross-region or cross-zone data paths, new gateways, larger instance classes or higher availability tiers mention the expected monthly cost range.
- Reports and dashboards label each figure as BilledCost or EffectiveCost and compare cost per day rather than raw monthly totals.
- Savings figures are labelled estimated until measured after the change.
- Billing exports, negotiated rates and account identifiers are not committed to the repository.

Review comments are suggestions. Purchases, deletions, policy changes and publishing figures need human approval.
