# Handoff contract

The model follows the installed `google-cloud-architect-contract` instruction; this page explains the same rules for people, and `templates/specialist-handoff.md` is a form to fill in.

## What the primary sends

The original goal and current task; scope and non-goals; the functional and non-functional requirements that matter; verified facts and labelled assumptions; the exact organization, folder or project identifiers; the identity to use and how to obtain it; relevant files; acceptance criteria; the output wanted; prohibited actions; and what is already approved. Strip secrets and personal data and send only what the specialist needs, because it sees nothing else from the primary's conversation.

## What a specialist returns

Findings tied to locations and evidence; every command run, with its target and result; commands deliberately not run, with the reason; risks and limitations; and the suggested next step.

- gcp-security-reviewer reads only: it does not edit, run commands or call cloud APIs.
- gcp-estate-inspector runs read-only Level 1 commands, changes nothing in the cloud, and hands any Level 2 command back as a proposal.
- Neither can widen its own assignment.

## Who decides

When results disagree, the primary weighs them against the current request, the requirements and the verified facts, checks each deliverable itself, and is accountable for the outcome. In a client without delegation, the primary does the specialist's task with gcp-security-controls or gcp-estate-discovery and says so in its report.
