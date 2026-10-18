---
description: "Write changelog entries, release notes, deprecation notices or a migration guide from shipped and traceable changes"
agent: cloud-documentation-archivist
---

# Document a release, deprecation or migration

## Inputs

- The release identifier and the shipped changes: merged pull requests, commits, tags and issues.
- Compatibility, security and cost impact, and any deprecation or removal dates.
- The audience: operators, API consumers, module users or customers.
- The existing changelog format and where release notes and migration guides live.

## Workflow

1. Apply changelogs-release-notes-and-migration.
   - Record only shipped changes, using the categories Added, Changed, Fixed, Security, Deprecated, Removed and Breaking.
   - For each entry, give what changed, when, who it affects, why it matters, its compatibility, security or cost impact, the action required, and links to the implementation, issue, pull request, decision record and release evidence.
   - Put planned work in the roadmap or task list, not the changelog.
2. For a migration, state the source and target, prerequisites, inventory, sequence, data and state handling, downtime, rollback, validation, owner and version boundaries. Keep the code migration, the operational cutover and customer communication in separate sections.
3. Apply templates-and-content-models to choose the changelog or migration template.
4. Apply docs-security-privacy-and-redaction. Describe security fixes without detail that would help an attacker.
5. Apply documentation-validation-and-link-checking. Confirm every pull request, issue and tag link points to the change it is cited for.

Do not claim a deployment succeeded, describe customer impact, or call a change backward compatible unless there is evidence for it.

## Expected output

The changelog entries, release notes or migration guide; the evidence behind each entry; and a list of compatibility or impact claims that remain unverified.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report.
