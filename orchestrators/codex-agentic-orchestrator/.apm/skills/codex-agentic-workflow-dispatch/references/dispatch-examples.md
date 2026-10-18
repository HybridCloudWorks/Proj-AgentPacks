# Dispatch Examples

## One agent

Use the smallest capable agent, for example `cloud-documentation-archivist` for a documentation-only request. Create the workflow with one required node, ask Codex to spawn that exact custom agent, validate its handoff, then report.

## Selected agents

For a Terraform change requiring architecture and documentation, select `terraform-expert-engineer` followed by `cloud-documentation-archivist`. The documentation node depends on the Terraform node's findings and must receive its handoff path as an input.

## All available agents

Use `mode: all` only when the user asks for a broad cross-domain review. Discover installed agents first. Spawn independent reviewers with bounded concurrency, then synthesize only after all required handoffs are present. Uninstalled optional agents are recorded as skipped rather than treated as failures.
