# Worked example: auditing a partner onboarding hub before web publication

Synthetic scenario; the hub and findings are invented.

Request: "Before we publish the partner onboarding hub to the web, check that nothing internal is exposed under it."

1. Scope. The hub page and everything below it: 46 pages and one database. The connector can fetch content but cannot read sharing settings, so the agent asks the user for a screenshot of the hub's share menu and is told guests already have access to one sub-page.
2. Delegate. The primary hands the review to notion-governance-reviewer with the hub URL, the fetched page tree, the intended audience (public web), the classification (external), the user's sharing evidence, and the prohibition on writes. The reviewer is told publication is a Level 2 decision it cannot approve.
3. Review. The reviewer applies the exposure and separation checks from notion-workspace-architecture:
   - High, blocking: "Partner pricing tiers" sits under the hub and contains discount floors. Publishing the hub with sub-pages would expose it.
   - Medium, blocking: a linked view of the internal Partner Accounts database appears on the "Getting started" page; on a published page its entries may be visible.
   - Low: four pages have no owner.
   - Question: whether the guest-access page should remain once the hub is public.
   It reports that it could not verify per-page sharing beyond the user's screenshot.
4. Reconcile. The primary checks both blocking findings against the fetched content, confirms them, and proposes: move "Partner pricing tiers" to the internal partner teamspace (a Level 2 move with a permission change), replace the linked view with a static list of public resources, assign owners. No changes are made yet.

Report: CHANGES_REQUIRED, with the located findings in the contract's finding format, coverage (46 pages, sharing evidence from the user only), and the proposed remediation awaiting approval. Publication remains the user's decision after remediation.
