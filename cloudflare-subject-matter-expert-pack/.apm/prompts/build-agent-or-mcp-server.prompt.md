---
description: "Build an AI agent, retrieval feature or remote MCP server on Cloudflare"
agent: cloudflare-subject-matter-expert
argument-hint: "[agent, AI feature or MCP server description]"
---

# Build an agent or MCP server on Cloudflare

## Inputs

The user outcome, data classification and tenancy, tools with their effects, who may call them, model or provider constraints, budgets, and the installed SDK versions.

## Workflow

Apply cloudflare-agents-and-ai to define the contract (tools, schemas, effects, authorization, approvals, budgets), then implement with cloudflare-workers-development and cloudflare-storage-and-state. Test with fake model and tool responses; paid inference, gateway or index creation and deployment wait for explicit approval.

## Expected output

The agent or MCP contract, code, binding and migration changes, evaluation cases with results and their environment, cost notes and a completion report under the `cloudflare-subject-matter-expert-contract` instruction.
