# Worked example: recording why the team chose private endpoints

Synthetic scenario. Record numbers, review identifiers and pull requests are illustrative.

Prompt used: `record-decision.prompt.md`.

## Request

"Record why we're moving the orders database to a private endpoint." The platform lead asks for a decision record in the infrastructure repository.

## Sources

- `docs/decisions/0007-database-public-endpoint-allowlist.md`: Accepted on 2024-05-02. It keeps the database's public endpoint and restricts it with an IP allowlist.
- Security review SR-2026-031, supplied as a file. Finding: the database is reachable from the internet on allowlisted ranges, and one of those ranges is a broad hosted CI runner range.
- Meeting notes from 2026-10-09, supplied. Three options were discussed and the platform and security leads favoured a private endpoint. No decision is recorded in them.
- Infrastructure pull request #418, a draft. It adds a private endpoint and a private DNS zone, and disables public network access. It has not been merged.

The decision log uses `docs/decisions/` with four-digit numbering, and the highest number is 0011.

## Applying adr-and-decision-records

One decision goes in one record: `docs/decisions/0012-database-private-endpoint.md`, built from `templates/adr.md`.

- Status: **Proposed**. The meeting notes show a preference, not an acceptance, and the user did not say the deciders had accepted it.
- Deciders: the platform lead and the security lead, as named in the meeting notes.
- Options, with trade-offs taken from the sources:
  1. Tighten the allowlist. Cheapest change, but the database stays internet-reachable and the hosted runner ranges remain broad.
  2. Private endpoint with private DNS, and public access disabled. Removes internet reachability. Hosted CI runners can no longer reach the database, and name resolution comes to depend on the private DNS zone.
  3. Defer until next quarter's network redesign. No work now, and the review finding stays open.
- Decision: option 2. Its rationale cites SR-2026-031.
- Consequences: schema migrations must run from a job inside the application network, which is follow-up work. Private DNS becomes a dependency of the application's startup path. The endpoint carries hourly and data-processing charges. **No figure is given**; the record asks the owner to price it.
- Links: SR-2026-031, the meeting notes, draft PR #418, and the networking runbook.

ADR 0007 is **not edited**. Its decision text is never changed, and its status changes only when 0012 is accepted. Record 0012 says "Supersedes 0007 when accepted". The follow-ups ask the deciders to set 0007 to "Superseded by 0012" and add the reverse link at acceptance.

## Neighbouring content

The explanation page `docs/architecture/orders-data.md` already says "the database is reachable only through a private endpoint". That text was drawn from PR #418, which has not been merged. explanation-and-architecture-docs says a proposal is not deployed state, so this is finding F1. The page was not edited, because the request was for the decision record only.

## Completion report

Recommendation: **REVIEW_REQUIRED**

### Scope and audience

One decision record for platform, security and application engineers. It covers network access to the orders database. Out of scope: the implementation in PR #418, cost estimation, and the migration-runner redesign.

### Source and evidence

| Claim or section | Source | Version or date | Evidence label |
| --- | --- | --- | --- |
| Current state is a public endpoint with an allowlist | ADR 0007; infrastructure code on `main` | 2024-05-02; commit of 2026-10-17 | observed |
| Exposure of a broad runner range | SR-2026-031 | 2026-09-30 | supplied |
| The options and the leads' preference | Meeting notes | 2026-10-09 | supplied |
| Proposed implementation | Draft PR #418 | not merged | observed (proposal only) |
| Endpoint cost | — | — | not verified; owner to price |

### Content decision

Created `docs/decisions/0012-database-private-endpoint.md` with status Proposed. Left ADR 0007 unchanged. Added 0012 to the decision log index at `docs/decisions/README.md`, marked Proposed.

### Validation

| Check | Method or command | Result | Notes |
| --- | --- | --- | --- |
| Structure and secret-like values | `hooks/post-documentation.sh docs/decisions/0012-database-private-endpoint.md docs/decisions/README.md` | passed | |
| Links to 0007, the runbook and the meeting notes | Manual resolution | passed | |
| Link to SR-2026-031 | — | not run | Stored in the security team's tracker, which needs sign-in |
| Numbering and index order | Compared with the existing records 0001 to 0011 | passed | |

| id | severity | source | impact | remediation | verification |
| --- | --- | --- | --- | --- | --- |
| F1 | Medium | `docs/architecture/orders-data.md:23` | Readers are told the database is private while it is still internet-reachable | Label the statement as proposed and link ADR 0012 (`explain-architecture.prompt.md`) | The page shows current and proposed state separately, and the current state matches the infrastructure code on `main` |

### Limitations

The cost of option 2 is not estimated. Whether the deciders will accept option 2 is unknown. The impact of private DNS on startup time was not measured.

### Ownership and next review

- Owner: Platform lead
- Reviewer or decider: Platform lead and security lead
- Document status: Proposed
- Next review: at the deciders' acceptance, or 2026-11-15 if the record is still Proposed then
- Handoff: accept or reject 0012. On acceptance, set 0007 to Superseded and add the reverse link
