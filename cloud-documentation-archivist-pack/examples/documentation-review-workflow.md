# Worked example: reviewing a networking documentation pull request

Synthetic scenario. File names, line numbers and pull request numbers are illustrative.

Prompt used: `review-documentation.prompt.md`.

## Request

"Review PR #233 (refresh networking docs) before we merge. Findings only, don't change anything."

The review is read-only. Posting review comments on the pull request is an external write that was not requested, so the findings are delivered in the session.

## Inventory and automated checks

documentation-hooks-and-automation runs first, bounded to the repository working tree:

```text
$ hooks/pre-documentation.sh --out build/docs-inventory.json
{"out": ".../build/docs-inventory.json", "document_count": 46, "published": false}
Pre-documentation inventory written to build/docs-inventory.json. No publication or network call was made.

$ hooks/post-documentation.sh docs/networking/overview.md docs/networking/peering.md docs/networking/vpn.md
FAIL
- docs/networking/overview.md: heading levels skip a depth
- docs/networking/vpn.md: secret-like value detected
```

The inventory shows that `mkdocs.yml` is present, but `mkdocs` is not installed in this environment, so a rendered build could not be produced.

## Manual review

- **docs-security-privacy-and-redaction.** The flagged line in `vpn.md` is a sample IPsec configuration whose `shared_secret` holds a 32-character value. It does not look like an example value. The value is not repeated here.
- **diataxis-content-design.** `overview.md` is an explanation page that switches to a nine-step peering procedure halfway through.
- **documentation-validation-and-link-checking.** There are 31 relative links and one is broken: `../runbooks/dns-failover.md` was renamed to `dns-failover-runbook.md` in PR #201. Fourteen external links were classified as external and not checked, because network access was not authorized.
- **repository-and-project-doc-governance.** `peering.md` says spoke-to-spoke traffic is routed through the hub firewall. `infra/network/routes.tf` on `main` has no such route for `spoke-prod`. The page states something the implementation does not do.
- **documentation-style-and-editorial-quality.** The topology image in `overview.md` has no alt text. Tone and word choice were left alone, because they are preferences.

## Completion report

Recommendation: **CHANGES_REQUIRED**

### Scope and audience

The three changed files in PR #233, read by network and platform engineers. Review only: no edits were made and no comments were posted.

### Source and evidence

| Claim or section | Source | Version or date | Evidence label |
| --- | --- | --- | --- |
| Changed files and lines | PR #233 diff | head commit of 2026-10-17 | observed |
| Routing behaviour | `infra/network/routes.tf` | `main`, commit of 2026-10-16 | observed |
| Runbook rename | PR #201 | merged 2026-09-12 | observed |
| Whether the `shared_secret` value is live | — | — | not verified; the owner must confirm |

### Content decision

Read-only review. No files were changed. The procedure in `overview.md` is recommended to move to a how-to guide (F2).

### Validation

| Check | Method or command | Result | Notes |
| --- | --- | --- | --- |
| Inventory | `hooks/pre-documentation.sh` | passed | 46 documents |
| Structure and secret scan | `hooks/post-documentation.sh` on the three files | failed | Two failures, mapped to F1 and F2 |
| Relative links | Manual resolution | failed | One broken link (F3) |
| External links (14) | — | not run | Network access not authorized |
| Rendered site build | — | not run | `mkdocs` not installed |
| Claims compared with infrastructure code | Read `routes.tf` | failed | F4 |

| id | severity | source | impact | remediation | verification |
| --- | --- | --- | --- | --- | --- |
| F1 | High | `docs/networking/vpn.md:42` | A value that may be a live VPN pre-shared key is in the PR branch and its history | Replace it with `VPN_SHARED_SECRET`. The network owner confirms whether it is live and, if so, rotates it, because removing it from the file does not remove it from git history | The post-documentation check passes; the owner confirms rotation or that the value was never used |
| F2 | Medium | `docs/networking/overview.md:30-75` | Explanation and procedure are mixed, and headings jump from level 2 to level 4 | Move the steps to `docs/how-to/configure-spoke-peering.md` and link to it; fix the heading levels | The heading check passes; the overview contains no numbered procedure |
| F3 | Medium | `docs/networking/overview.md:88` | On-call readers following the failover link reach a missing page | Link to `../runbooks/dns-failover-runbook.md` | The link resolves |
| F4 | Medium | `docs/networking/peering.md:17` | Engineers will assume firewall inspection that does not exist | Correct the statement to match `routes.tf`, or add a decision record if the route is intended | The text matches the routes on `main` |
| F5 | Low | `docs/networking/peering.md:1-6` | `last_reviewed` is 2024-03-02 and there is no `owner`, so nobody keeps the page current | Add an owner and the review date of this change | Frontmatter has both fields |
| F6 | Low | `docs/networking/overview.md:12` | Screen-reader users get no description of the topology | Add alt text that describes the hub and spokes | The image has alt text |

### Limitations

External links and the rendered output were not checked. Whether the F1 value is live cannot be decided from the documentation.

### Ownership and next review

- Owner: Network platform team
- Reviewer or decider: author of PR #233; network owner for F1
- Document status: in review
- Next review: re-review PR #233 after the fixes
- Handoff: fix F1 to F4 before merging; F5 and F6 can be fixed in the same PR
