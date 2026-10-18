# Worked example: a publication request that stops at a local package

Synthetic scenario. The article, owners and identifiers are illustrative.

Prompt used: `prepare-publication.prompt.md`.

## Request

"Publish the completed cost-anomaly article to Notion."

The article is `docs/explanation/cost-anomaly-alerts.md`. It is an explanation page, and its frontmatter records a review by the FinOps lead on 2026-10-15.

## What the gate found

| Precondition | Finding |
| --- | --- |
| Authorization | The user asked for publication, which authorizes publishing in principle |
| Destination | The request says "Notion" but names no workspace, teamspace or parent page |
| Audience | Not stated. The article names internal cost-centre codes, and a screenshot caption shows two cloud account identifiers |
| Connector | No Notion tool or MCP server is available in this session |

Any one of the last three is enough to stop. Creating a page in an unknown location for an unknown audience is not a reversible preview, and without a connector the page cannot be created at all. The agent does **not** look for another route, such as a browser session, a personal API token or a copy-paste macro.

## Work done locally

- **documentation-validation-and-link-checking.** Ran the post-documentation check on the article (`PASS`). Its 6 relative links resolve. The 2 external links to the cloud provider's cost-anomaly documentation were classified time-sensitive and were not checked.
- **docs-security-privacy-and-redaction.** In the publish copy, the two account identifiers became `ACCOUNT_ID_PROD` and `ACCOUNT_ID_SHARED`. The source article was left unchanged. Whether the cost-centre codes may be shown depends on the audience, so the handoff leaves that decision to the owner.
- **knowledge-base-and-taxonomy.** Prepared `publish/notion/cost-anomaly-alerts.md` with these Notion-ready properties: Title, Type = Explanation, Owner = FinOps, Status = Reviewed, Last reviewed = 2026-10-15, Next review = 2027-01-15, Tags = cost, alerts, anomaly detection, and Related = ADR 0009 (budget alert thresholds).
- **docs-as-code-and-publishing.** Wrote unpublish steps (archive the page and remove it from the parent's link list) into the handoff, ready for when publication happens.
- Wrote `publish/notion/HANDOFF.md` from `templates/handoff.md`.

No Notion page exists, and none is claimed to exist.

## Completion report

Recommendation: **BLOCKED_ON_SOURCE_OR_OWNER**

### Scope and audience

Publication of one reviewed explanation article to Notion. The intended Notion audience is unknown, and that is one of the blockers.

### Source and evidence

| Claim or section | Source | Version or date | Evidence label |
| --- | --- | --- | --- |
| Article content and review | `docs/explanation/cost-anomaly-alerts.md` frontmatter | reviewed 2026-10-15 | observed |
| No Notion connector available | Tools available in this session | 2026-10-18 | observed |
| Destination and audience | — | — | not supplied |

### Content decision

The article itself was not changed. Created a redacted, Notion-ready copy and a handoff under `publish/notion/`. The copy differs from the source only in the redacted identifiers and the property block.

### Validation

| Check | Method or command | Result | Notes |
| --- | --- | --- | --- |
| Structure and secret scan | `hooks/post-documentation.sh publish/notion/cost-anomaly-alerts.md` | passed | |
| Relative links (6) | Manual resolution | passed | |
| External links (2) | — | not run | Network access not authorized |
| Rendering in Notion | — | not run | No destination and no connector |
| Publication | — | not run | Blocked |

| id | severity | source | impact | remediation | verification |
| --- | --- | --- | --- | --- | --- |
| F1 | Medium | `docs/explanation/cost-anomaly-alerts.md:58` | Account identifiers in the source article would be exposed if it were published unredacted elsewhere | The owner decides whether the source should also use placeholders | The owner's decision is recorded; the source is updated or the risk is accepted |

### Limitations

How the page renders in Notion (callouts, tables, the Mermaid diagram) is unknown. The external links were not checked. Nothing was published.

### Ownership and next review

- Owner: FinOps lead
- Reviewer or decider: FinOps lead, for the destination, the audience and the cost-centre codes
- Document status: Reviewed, not published
- Next review: 2027-01-15
- Handoff: supply the Notion parent page and audience, then run the request again in a session with an authorized Notion connector. The agent will create the page and report its URL from the tool result
