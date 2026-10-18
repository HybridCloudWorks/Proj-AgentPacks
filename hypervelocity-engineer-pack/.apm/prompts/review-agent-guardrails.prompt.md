---
description: "Review an agent, GitHub Agentic Workflow, MCP configuration or automation for least privilege, safe outputs, secrets, network and approval gates"
agent: hypervelocity-engineer
---

# Review agent guardrails

## Inputs

- The artifacts in scope: workflow source and lock file, agent profile, MCP configuration, or automation script.
- Any capability change requested, such as new write access, auto-merge or release.
- Repository policy that applies (branch protection, rulesets, required reviews) and whether the task is review-only or may remediate.

## Workflow

1. Apply `agent-governance-and-guardrails`: build the decision record for every capability, mark each control as enforced by the platform, enforced by repository policy, advisory, or missing, and run its review checks.
2. For a GitHub Agentic Workflow, apply the release gate in `workflow-lifecycle-and-release`, including whether the lock file widens what the source declares.
3. Where delegates or subagents are involved, apply `agent-delegation-and-composition`: no delegate may exceed the parent's permissions, and fan-out, retries and budget are bounded.
4. A request to merge, release, grant permissions, change branch protection or enable autonomous writes is not carried out in this task. Record the approval it needs and its owner, and offer a reviewable alternative such as a safe output that opens a pull request.

## Expected output

Findings ordered by severity with location, evidence and remediation; the decision record; release-gate status; required approvals and owners; a least-privilege configuration proposal; and the completion report required by the `hypervelocity-engineer-contract` instruction. Review-only requests change no files.
