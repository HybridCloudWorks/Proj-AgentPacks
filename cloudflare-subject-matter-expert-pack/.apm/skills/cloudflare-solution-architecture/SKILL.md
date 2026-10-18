---
name: cloudflare-solution-architecture
description: "Choose Cloudflare products and design solution architectures across compute, storage, AI, networking, delivery, security and Zero Trust, recording limits, plan entitlements, cost drivers, alternatives and open decisions. Use when someone asks which Cloudflare product fits, how to architect a workload on Cloudflare, or whether a design will hold within platform limits."
---

# Cloudflare Solution Architecture

## Purpose and activation

Turn requirements into a Cloudflare architecture whose every product choice is justified, whose limits and entitlements have been checked against current documentation, and whose open decisions are explicit. Activate for product-selection questions, new workload designs, design reviews, capacity or cost questions, and "can Cloudflare do X" questions.

## Scope and exclusions

In scope: request path and data flow design, product fit, consistency and state placement, data locality, identity and security boundaries, cost drivers, failure modes, and decision records.

Not in scope: writing the implementation (hand to cloudflare-workers-development, cloudflare-storage-and-state or cloudflare-agents-and-ai), configuring zones or policies (cloudflare-edge-delivery-and-performance, cloudflare-application-security, cloudflare-zero-trust), quoting contract pricing, or promising features that depend on an unconfirmed plan.

## Required inputs

- Workload: users and geography, request rates and burst shape, payload sizes, latency targets, read/write ratio.
- State: what must be strongly consistent, what can be eventually consistent, durability and retention, data residency or jurisdiction rules.
- Existing estate: current cloud, origins, databases, DNS, identity provider, CI and IaC tooling.
- Constraints: plan tier (Free, Pro, Business, Enterprise, Workers Paid), compliance, budget, team skills.
- Missing inputs are recorded as assumptions with the decision they affect; do not stall a design for an input that only changes a detail.

## Dependencies and tools

- Current Cloudflare documentation for each candidate product, especially its limits and pricing pages, retrieved through web access or a connected Cloudflare documentation tool. Without retrieval, mark every number as unverified.
- `decision-record-template.md` in this skill folder.
- Read access to the repository when the design extends an existing project.

## Workflow

1. Restate the outcome, users, non-goals and success measures. Separate hard constraints from preferences.
2. Draw the request path: client, DNS, Cloudflare edge, rule phases (redirects, WAF, rate limiting, cache, transforms), Worker or origin, bindings and backends. Mark where identity is established and where data is stored.
3. Choose products with the decision guide below. For each choice write the reason, the rejected alternative and the condition that would change the choice.
4. Check fit. Retrieve the limits page for each chosen product and list the specific limits the design approaches: CPU time, memory, subrequests, request and response sizes, storage per database or object, write rates, message sizes, connection counts. Flag plan-gated features and confirm the plan, or mark the feature as conditional.
5. Place state and define consistency per store. Identify the coordination atom for anything strongly consistent and confirm no single object becomes a global bottleneck.
6. Design failure behavior: retries and idempotency keys, queues and dead-letter handling, timeouts, fallbacks when a backend or AI provider is unavailable, and what users see.
7. Identify cost drivers by product (requests, CPU time, reads and writes, operations, storage, duration, inference units, log volume, seats) and the workload numbers that multiply them. Use current pricing pages; never quote remembered prices.
8. Define security boundaries: origin lockdown, secrets placement, token scope, Access or authentication in front of internal surfaces, tenant isolation.
9. Record each significant decision with `decision-record-template.md`, and list open decisions with an owner.
10. Propose a validation plan: a spike or load test in a non-production account, limit probes, and the measurements that would falsify the design.

## Decision guide

Compute
- Stateless HTTP logic, APIs, edge middleware: Workers. Worker-to-Worker calls use service bindings (RPC), not public HTTP.
- Full-stack app or static site with server logic: Workers with static assets for new projects; keep Pages where a project already uses it. Confirm the current recommendation in the documentation.
- Per-entity coordination, strong consistency, WebSockets, per-entity schedules: Durable Objects, one object per room, document, tenant or user.
- Durable multi-step processes with retries, sleeps and waiting for external events: Workflows.
- Background and bursty work off the request path: Queues. Scheduled work: Cron Triggers.
- A full Linux runtime, other languages or large memory: Containers. Running untrusted or generated code: the Sandbox SDK on Containers.
- Customers uploading their own code: Workers for Platforms.
- Header, redirect or URL changes without application logic: Rules (Redirect, Transform, Origin, Configuration) or Snippets before a Worker.
- Worker latency dominated by a distant backend: Smart Placement.

Data
- Read-heavy, globally cached, eventually consistent values (configuration, flags, sessions that tolerate staleness): KV. Not for counters, locks or read-after-write.
- Relational data: D1 (SQLite), often one database per tenant when size caps matter; existing PostgreSQL or MySQL: Hyperdrive in front of it.
- Objects and files, S3-compatible access: R2. Large binaries never go in D1 or KV values when R2 fits.
- Strongly consistent per-entity state: Durable Object SQLite storage.
- Vector search: Vectorize; managed retrieval: AI Search.
- High-cardinality custom metrics written from Workers: Analytics Engine.
- Secrets shared across Workers: Secrets Store. Streaming ingestion into Iceberg tables on R2: Pipelines with R2 Data Catalog and R2 SQL.
- Transactional email: Cloudflare Email Service (Workers binding or REST API) for sending and Email Routing with Email Workers for inbound mail; it is not a bulk marketing platform, and the sending domain must be onboarded first.

AI
- Inference on Cloudflare: Workers AI. Any provider with caching, rate limiting, logging and fallback: AI Gateway. Stateful agents and MCP servers: Agents SDK. Headless browsing: Browser Rendering.

Network, delivery and security
- Authoritative DNS, CDN caching, TLS, Load Balancing, Argo Smart Routing; Spectrum for non-HTTP TCP/UDP; Cloudflare Tunnel to reach origins without inbound ports; Cloudflare WAN and Magic Transit for enterprise networks.
- WAF, rate limiting, bot management, always-on DDoS mitigation, API Shield, Turnstile; Cloudflare One (Access, Gateway, device client, DLP, CASB) for workforce and private-application access.

Anti-patterns to reject
- A single global Durable Object for all traffic; KV as a counter or lock; reading KV immediately after writing it elsewhere.
- Calling the Cloudflare REST API from inside a Worker when a binding exists; public HTTP between Workers.
- Direct database connections from Workers without Hyperdrive; unbounded work inside the request path.
- A proxied hostname whose origin still accepts traffic from anywhere.

## Expected output

An architecture brief with: assumptions; request-path and data-flow description (a diagram when the client can render one); product choices with rationale and rejected alternatives; a limits table (limit, value, source URL, date checked, headroom); plan entitlements required; consistency and failure behavior; cost drivers; security boundaries; decision records; open decisions with owners; and the validation plan.

## Validation

- Every number in the brief has a source and check date, or is marked unverified.
- Each product appears for a stated requirement; nothing is included only because it exists.
- The design is walked through for the peak workload and for one backend failure.
- Status is reported as ANALYSIS_ONLY unless a spike or test actually ran.

## Failure handling and escalation

- A requirement exceeds a documented limit: propose a sharding, batching or product change, or escalate the limit question to the account team; never assume an increase.
- A required feature is plan-gated and the plan is unknown: mark it conditional and report BLOCKED_ON_HUMAN_DECISION for that part only.
- Documentation cannot be retrieved: deliver the design with every limit marked unverified and say so in the first line.
- Conflicting requirements, such as strict residency and global low latency: present the trade-off and let the owner decide.

## Permissions and guardrails

Read and reason only. Creating resources, enabling paid features, running load tests or contacting Cloudflare sales or support are consequential actions that need explicit approval for the exact account and effect. Never put customer data, account identifiers or internal hostnames into web searches.

## Workflow connection

Within the complete pack, the optional `design-cloudflare-architecture.prompt.md` recipe connects this skill to the primary `cloudflare-subject-matter-expert` workflow, and its output feeds the build, security and migration skills. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval, handoff and completion rules.
