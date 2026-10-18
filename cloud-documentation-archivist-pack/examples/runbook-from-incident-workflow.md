# Worked example: a runbook from an incident, with a credential found in the evidence

Synthetic scenario. The incident, thresholds, commands and pull request numbers are illustrative.

Prompt used: `write-runbook.prompt.md`.

## Request

"Create a runbook from INC-2291 so on-call can handle this next time." The request comes from the Orders on-call lead.

## Evidence supplied

| Source | Contents |
| --- | --- |
| `postmortems/2026-10-02-orders-events.md` | Draft postmortem. The orders-events consumer crashed after a deploy and the dead-letter queue grew for about two hours |
| `monitoring/alerts/orders-dlq.yaml` | Alert: dead-letter depth above 500 messages for 10 minutes |
| `deploy/orders-events-consumer.yaml` | Consumer deployment manifest, namespace `orders` |
| `incident-chat-INC-2291.txt` | Export of the incident channel |
| `scripts/replay-dlq.sh` | Script responders used to move dead-lettered messages back to the main queue |

## Applying research-synthesis-and-source-traceability

The timeline was rebuilt with a citation for every entry. The postmortem's cause is a **confirmed** one: payload version 3 dropped the `currency` field and the consumer crashed on it. Consumer error logs quoted in the postmortem support it. A "network blip" suggested in the chat has no supporting evidence, so it is recorded as a discarded hypothesis and left out of the runbook.

The chat also shows that responders ran `replay-dlq.sh` and 37 customers then received duplicate order-confirmation emails. Replay is not safe for side effects unless the consumer deduplicates. The idempotency fix in pull request #1290 is merged, but nothing supplied shows that it is deployed.

## Applying docs-security-privacy-and-redaction

At line 214 of the chat export, a responder pasted a full storage connection string, account key included, to help a colleague. The value appears nowhere in the runbook or in this report. Masking it in a copy would not contain it: it is still in the chat history and still valid. It is raised as finding F1 for the owner to contain and rotate. The runbook names the permission class it needs ("read access to queue metrics"), never a credential, and uses `STORAGE_ACCOUNT` as a placeholder.

## Applying runbooks-and-operational-docs

Created `docs/runbooks/orders-events-dlq-growth.md` from `templates/runbook.md`, with `last_exercised: 'Never'`.

- **Trigger and symptoms.** The dead-letter alert from `orders-dlq.yaml`, delayed order confirmations, and consumer restarts.
- **Safety and scope.** Dead-lettered messages are the only copy of the failed events. **Never purge the dead-letter queue.** Stop and escalate if depth keeps rising after mitigation.
- **Diagnose (read-only).**
  - `kubectl -n orders get deploy orders-events-consumer` and `kubectl -n orders get pods -l app=orders-events-consumer` to check restarts.
  - Read the last deploy in the pipeline history.
  - Peek one dead-lettered message's error header with the queue CLI in read-only mode.
- **Mitigate.** Roll the consumer back to the previous image tag through the deploy pipeline. On-call is authorized to do this on its own.
- **Replay (gated).** Replay needs the service owner's approval **and** confirmation that the deduplication from #1290 is deployed. Without both, leave the messages in the dead-letter queue and escalate.
- **Escalation, verification and close.** Escalate to the Orders service owner, then the platform incident commander. Verify that queue depth returns to baseline and the consumer is healthy. Open a follow-up for the postmortem.

Links: the alert definition, the consumer dashboard, the postmortem, and ADR 0009 (event schema versioning). None of their content is copied into the runbook.

## Completion report

Recommendation: **NOT_VERIFIED**

### Scope and audience

An operational runbook for Orders on-call engineers. It covers growth of the orders-events dead-letter queue caused by consumer failure. It does not cover broker outages or the event schema itself.

### Source and evidence

| Claim or section | Source | Version or date | Evidence label |
| --- | --- | --- | --- |
| Alert condition | `monitoring/alerts/orders-dlq.yaml` | commit of 2026-10-16 | observed |
| Root cause | Postmortem draft, consumer error logs quoted in it | 2026-10-05 | supplied |
| Replay caused duplicate emails | Chat export lines 300 to 342 | 2026-10-02 | supplied |
| Deduplication fix exists | Pull request #1290 | merged 2026-10-09 | observed |
| Deduplication fix is deployed | — | — | not verified |
| Every runbook step works as written | — | — | not verified; never exercised |

### Content decision

Wrote a runbook, not a how-to, because the reader is an operator under alert pressure who needs stop conditions and authority boundaries. The postmortem was left as it is and linked. Files changed: `docs/runbooks/orders-events-dlq-growth.md`.

### Validation

| Check | Method or command | Result | Notes |
| --- | --- | --- | --- |
| Structure, placeholders, secret-like values | `hooks/post-documentation.sh docs/runbooks/orders-events-dlq-growth.md` | passed | |
| Command syntax | Compared with the `kubectl` and queue CLI reference | passed | Syntax only; no command was run against a cluster |
| Dashboard link | — | not run | Needs sign-in |
| Exercise of the procedure | — | not run | Requires an approved game day or a real event |

| id | severity | source | impact | remediation | verification |
| --- | --- | --- | --- | --- | --- |
| F1 | High | `incident-chat-INC-2291.txt:214` | A storage account key is visible to everyone in the incident channel and is presumed valid | The storage owner rotates the key and asks channel administrators to remove the message under the retention policy | The owner confirms the rotation date; the old key fails authentication |
| F2 | Medium | Runbook replay step; PR #1290 | Replaying before deduplication is deployed sends duplicate emails to customers | The service owner confirms the deployed version that contains #1290, then the gate wording is updated | The deployed image tag contains #1290's commit |

### Limitations

The runbook has never been exercised. Whether the deduplication fix is deployed is unknown. The 500-message threshold is copied from the alert file, and nobody has assessed whether it is the right value.

### Ownership and next review

- Owner: Orders on-call team
- Reviewer or decider: Orders service owner (F2); storage account owner (F1)
- Document status: Draft, untested
- Next review: after the first exercise or real use, or 2026-12-01, whichever comes first
- Handoff: rotate the exposed key, confirm the deduplication deployment, and schedule a game day
