---
description: "Create or update a GitHub Agentic Workflow with least privilege, safe outputs, and a compiled lock file reviewed before any live run"
agent: hypervelocity-engineer
---

# Author a GitHub Agentic Workflow

## Inputs

- Purpose, trigger and target repository; the existing workflow source when updating.
- Expected outputs and which repository writes, if any, are acceptable.
- Engine preference, network destinations, MCP servers and secrets the workflow needs.
- Whether a live `gh aw run` is authorized in this task.

## Workflow

1. Apply `agentic-workflows`: classify the request as create or update, load only the matching gh-aw procedure, then the repository overlay `.github/aw/instructions.md` if present. If the procedure or reference is unavailable, say so and work from the official gh-aw documentation; never invent frontmatter fields.
2. Apply `agent-governance-and-guardrails` before writing: minimal `permissions`, structured safe outputs instead of direct writes, explicit network and MCP allowlists, secrets only through the secret mechanism, and issue, pull request and web content treated as untrusted input.
3. Apply `workflow-lifecycle-and-release`: edit the Markdown source, run `gh aw compile`, review the generated `.lock.yml` diff for broadened permissions or added tools, run `gh aw validate`, and keep source and lock in the same change when the repository tracks both.
4. Ask before `gh aw run`. After an authorized run, collect `gh aw logs` evidence; without one, report live behavior as unverified.

## Expected output

The source diff, a lock-diff summary, a table of permissions, safe outputs, network, MCP servers and secrets with how each is enforced, compile and validate results, live-run status, open release-gate items, and the completion report required by the `hypervelocity-engineer-contract` instruction. A successful compile is never reported as proof of safe live behavior.
