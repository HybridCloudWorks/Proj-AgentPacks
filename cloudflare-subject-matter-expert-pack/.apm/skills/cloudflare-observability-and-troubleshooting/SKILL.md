---
name: cloudflare-observability-and-troubleshooting
description: "Diagnose Cloudflare incidents and instrument Workers using Ray IDs, Cloudflare error codes, response headers, Workers Logs and traces, wrangler tail, Tail Workers, Logpush, the GraphQL Analytics API, Analytics Engine, Security Events, Gateway and Access logs and Tunnel diagnostics. Use when a site, API or Worker returns errors, behaves differently through Cloudflare, is slow, is blocked unexpectedly, or needs logging, metrics and alerts."
---

# Cloudflare Observability and Troubleshooting

## Purpose and activation

Find where a request fails or slows down on its path through Cloudflare, prove it with evidence, and leave the service observable enough that the next incident is faster. Activate for error pages and status codes, unexpected blocks or challenges, cache or routing surprises, latency, Worker exceptions, Zero Trust connectivity failures, and requests to add logging, metrics, traces or alerts.

## Scope and exclusions

In scope: triage, request-path reasoning, Cloudflare error codes, response headers, Ray ID lookups, Workers Logs, traces, `wrangler tail`, Tail Workers, Analytics Engine, Logpush, GraphQL Analytics API, Security Events, Gateway and Access logs, device client and Tunnel diagnostics, notifications and alerting.

Not in scope: fixing the cause (hand to the relevant product skill) and applying fixes (cloudflare-change-control).

## Required inputs

- Symptom and impact: what fails, for whom, since when, how often; sample URLs, timestamps with time zone, and Ray IDs.
- Recent changes: deployments, rule or DNS edits, certificate events, origin changes.
- Access the user has put in scope: dashboard exports, log destinations, a configured Wrangler login or API token with read permissions.

## Dependencies and tools

- Current Cloudflare troubleshooting documentation for 5xx and 1xxx errors, Workers errors and limits, and the log and analytics datasets for the plan.
- Read-only probes against hostnames the user owns: `curl -sI` and `curl -v` (headers `cf-ray`, `cf-cache-status`, `server`), `curl --resolve` to compare edge and origin, `dig` against authoritative nameservers and public resolvers, `openssl s_client` for certificates, `cloudflared tunnel info`, and the device client's diagnostic commands.
- `wrangler tail` and Workers Logs for Worker traffic; GraphQL Analytics API and Logpush data for aggregates.

## Workflow

1. Frame: write the symptom as a testable statement with scope (hostnames, paths, methods, regions, clients) and start time.
2. Correlate with change history; the most recent change touching the failing path is the first hypothesis, not the conclusion.
3. Locate the layer. Read the status code and error page: a Cloudflare-branded error points at the edge or the edge-to-origin leg, an application error page points at the origin, and a Worker exception points at code. Use the `cf-ray` suffix to identify the data center.
4. Follow the path in order: DNS resolution, TLS at the edge, security rules (Security Events by Ray ID), cache (`cf-cache-status`), Worker (logs, exceptions, limits), origin connection and TLS, origin response.
5. Test one hypothesis at a time and change one variable per test: through Cloudflare versus directly to the origin (only where the origin permits it), proxied versus DNS-only hostnames on a test record, another data center or resolver.
6. Confirm the cause with evidence that predicts the failure, then hand the fix to the right skill with the evidence attached.
7. Close the observability gap the incident exposed: missing logs, sampling too low, no alert, no correlation ID.

## Error code guide

Retrieve the current troubleshooting page before stating causes; the meanings below are starting points.

| Code | Usual meaning | First checks |
|---|---|---|
| 520 | Origin returned an empty, invalid or unexpected response | Origin logs, crashes, oversized headers |
| 521 | Origin refused the connection | Origin down, firewall blocking Cloudflare ranges |
| 522 | Connection to the origin timed out | Firewall drops, routing, overloaded origin |
| 523 | Origin unreachable | DNS record target, routing |
| 524 | Origin accepted the connection but did not respond in time | Slow endpoints; move long work off the request path |
| 525 | TLS handshake with the origin failed | Origin TLS configuration, SNI, protocol versions |
| 526 | Origin certificate invalid under Full (strict) | Certificate hostname, expiry, chain |
| 530 with a 1xxx code | Cloudflare-side error detailed by the 1xxx code | Read the 1xxx code, for example origin DNS or Tunnel down |
| 1020 | Blocked by a security rule | Security Events for the Ray ID, then the rule |
| 1101 | Worker threw an uncaught exception | Workers Logs or `wrangler tail` for the stack |
| 1102 | Worker exceeded a resource limit | CPU or memory use, limits for the plan |

Other frequent signals: `cf-cache-status: DYNAMIC` (not eligible for cache), challenges on API clients (a bot or WAF rule challenging non-browser traffic), redirect loops (Flexible SSL with an HTTPS-redirecting origin), and SERVFAIL on validating resolvers (a stale DNSSEC DS record).

## Worker diagnostics

- Enable `observability` and choose a sampling rate that keeps errors visible; raise it temporarily for an investigation and lower it afterwards.
- `wrangler tail` streams live production requests and may include personal data; filter by status, method or search term, keep the session short, and do not paste raw payloads into chat.
- Log structured JSON with a correlation ID passed to downstream services; never log secrets, tokens, cookies or full request bodies.
- Tail Workers and Logpush move events to other systems; Analytics Engine records custom metrics, and aggregates must account for sampling (sum the sample interval rather than counting rows).
- CPU time and wall time are different limits; timing APIs inside Workers are coarsened, so use traces for precise spans.

## Zero Trust diagnostics

- Gateway activity logs explain DNS, network and HTTP decisions; Access authentication logs explain allow and deny decisions with the matching policy; device client diagnostics show profile, mode and connectivity; `cloudflared tunnel info` shows connector health; digital experience monitoring tests show reachability over time.
- Work from the log line to the responsible rule, route, profile or policy.

## Expected output

A diagnostic report: symptom statement, scope and timeline, request path with the failing layer, evidence (commands with environment, outputs summarized and redacted, Ray IDs, log queries), confirmed cause or ranked hypotheses with the next test, the recommended fix and owning skill, and observability improvements.

## Validation

- The confirmed cause reproduces the failure, and the proposed fix is predicted to remove it; after the fix is applied, the same probe passes in the same environment.
- Evidence is labeled by environment and time; anything inferred is labeled as inference.
- Status is ANALYSIS_ONLY until a fix is applied and verified.

## Failure handling and escalation

- Logs are unavailable for the plan or retention has expired: say so, use what remains (headers, Ray IDs, synthetic probes), and recommend the logging change.
- The evidence points inside Cloudflare's network rather than the configuration: collect Ray IDs, timestamps, data centers and probe output for a support case; the account owner opens it.
- The probe would need production credentials or heavy traffic: ask first and keep request rates low.

## Permissions and guardrails

Read-only diagnostics on hostnames and accounts the user has put in scope. Changing sampling rates, enabling Logpush jobs, creating notifications, deploying Tail Workers or toggling settings to test a hypothesis are consequential and need explicit approval for the exact target. Redact personal data, tokens and internal hostnames from anything shared outside the session.

## Workflow connection

Within the complete pack, the optional `troubleshoot-cloudflare-issue.prompt.md` recipe connects this skill to the primary `cloudflare-subject-matter-expert` workflow, and fixes flow through `release-cloudflare-change.prompt.md`. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval, handoff and completion rules.
