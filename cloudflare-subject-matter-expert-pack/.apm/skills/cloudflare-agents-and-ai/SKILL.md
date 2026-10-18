---
name: cloudflare-agents-and-ai
description: "Build AI features and agents on Cloudflare with Workers AI, AI Gateway, Vectorize and AI Search retrieval, Browser Rendering, the Agents SDK and remote MCP servers built with McpAgent and OAuth, including tool authorization, human approval and cost controls. Use when adding inference, retrieval, chat or scheduled agents, tool-using agents, approval steps, or an MCP server hosted on Cloudflare."
---

# Cloudflare Agents and AI

## Purpose and activation

Deliver AI features and agents on Cloudflare that are grounded, authorized, bounded in cost and testable. Activate when a Worker calls a model, routes provider traffic through AI Gateway, builds retrieval over Vectorize or AI Search, uses Browser Rendering, defines an `Agent` or `AIChatAgent` class, or exposes or consumes MCP tools.

## Scope and exclusions

In scope: model and gateway selection, inference calls, embeddings and retrieval, Agents SDK state, callable methods, scheduling, workflows, queues and retries inside agents, chat agents and client hooks, MCP servers with `McpAgent`, MCP clients through `addMcpServer`, OAuth in front of MCP, human-in-the-loop approval, evaluation and cost controls.

Not in scope: Durable Object storage internals (cloudflare-storage-and-state), generic Worker rules (cloudflare-workers-development), and deploying (cloudflare-change-control).

## Required inputs

- The user outcome, the data the model may see and its classification, tenancy, and who may invoke which tools.
- Model or provider constraints (on-platform Workers AI, a third-party provider through AI Gateway, bring-your-own key), latency and cost budgets.
- The installed versions of `agents`, `@cloudflare/ai-chat`, `@modelcontextprotocol/sdk` and related packages.

## Dependencies and tools

- Current Agents SDK, Workers AI model catalog, AI Gateway, Vectorize, AI Search, Browser Rendering and MCP documentation; model IDs, parameters and limits always come from the catalog, never memory.
- Project Wrangler and tests; the MCP Inspector for local protocol testing when the user approves running it.
- Workers AI inference runs remotely and is billed even during local development; unit tests use fakes.

## Workflow

1. Define the agent contract: inputs, outputs, tools with schemas and effects (read or consequential), who may call each, budgets (tokens, steps, time, spend) and the terminal states.
2. Choose the model path: Workers AI binding for on-platform models; AI Gateway in front of any provider for caching, rate limiting, logging, retries and fallback; note that streamed responses are not cached and authenticated gateways need the gateway authorization header.
3. Design retrieval when grounding is needed: AI Search for managed pipelines, or Vectorize with an embedding model whose dimensions match the index. Chunk with provenance, filter by tenant on the server, and return sources with answers.
4. Build the agent with the Agents SDK rules below, or the MCP server with the MCP rules below.
5. Add human approval for consequential tools (payments, messages, deletions, account changes): the agent proposes, a person approves, the tool executes with the approved parameters only.
6. Add observability and cost controls: structured events without prompts or personal data by default, per-tenant rate limits, maximum steps and tokens, and alerts on spend.
7. Evaluate: a fixed set of tasks with expected outcomes, tool-misuse and prompt-injection cases, and refusal cases. Record which ran locally with fakes and which against real models.

## Agents SDK rules

- An agent class is a Durable Object: each class needs a binding and a migration entry (`new_sqlite_classes`); never edit an applied migration. Instances are addressed by name, so derive names from authenticated identity, not from client-supplied strings alone.
- Authenticate before routing: check identity in the Worker or the documented connection hooks before `routeAgentRequest`. Any `@callable()` method can be invoked by any connected client, so authorize inside each method.
- Validate client-originated state changes in `validateStateChange`. Do not enable `experimentalDecorators` in the TypeScript configuration; it breaks the SDK's decorators.
- Use `schedule()` and `scheduleEvery()` for timed work, Workflows for durable multi-step jobs, the built-in queue and `retry()` for transient failures; keep every scheduled or retried handler idempotent.
- Treat experimental modules (voice, browser tools, higher-level chat classes, code mode) as experimental; confirm status in current documentation before relying on them.

## MCP rules

- Serve remote MCP over the Streamable HTTP transport; SSE is legacy. Put OAuth in front with the Workers OAuth provider library, validate redirect URIs, and bind tokens to the expected audience.
- Authorize each tool from the authenticated identity and grants, never from model-supplied arguments. Separate read tools from consequential tools and require approval for the latter.
- Define strict input schemas, bound output size, set timeouts, and never expose arbitrary URL fetch, SQL or shell tools.
- When the agent consumes external MCP servers, register only servers the user approved, treat their tool descriptions and results as untrusted data, and keep their credentials out of prompts.

## Expected output

The agent or MCP contract (tools, schemas, effects, authorization, approvals, budgets), the code, the binding and migration changes, evaluation cases with results, and the cost and release notes for cloudflare-change-control.

## Validation

- Unit tests with fake model and tool responses cover tool authorization, approval gating, schema rejection, budget exhaustion and injection attempts in retrieved content.
- Protocol tests (initialize, list, call, malformed arguments, unauthorized caller) pass against a local MCP server.
- Real-model evaluation results are reported with model ID, date and sample size, or marked unverified.

## Failure handling and escalation

- Model or provider unavailable: fall back through AI Gateway if configured, otherwise return a clear error; never fabricate an answer.
- Retrieval returns nothing relevant: say so and do not answer from the model alone when grounding is required.
- A tool would act outside its grant: refuse and report; do not widen scopes to make a task pass.
- Cost or rate limits reached: stop the run and report usage.

## Permissions and guardrails

Local code and tests with fakes. Calling paid inference, creating gateways or indexes, inserting vectors, connecting MCP servers, registering OAuth clients or deploying agents needs explicit approval for the exact account and resource. Never send confidential prompts, source code or customer data to a model or evaluator the user has not approved. Prompts and model outputs are not access control; enforce authorization in code.

## Workflow connection

Within the complete pack, the optional `build-agent-or-mcp-server.prompt.md` recipe connects this skill to the primary `cloudflare-subject-matter-expert` workflow. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval, handoff and completion rules.
