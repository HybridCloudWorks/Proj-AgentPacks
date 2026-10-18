---
name: cloudflare-edge-delivery-and-performance
description: "Configure and tune zone traffic on Cloudflare: DNS records and proxy status, DNSSEC, SSL/TLS modes and certificates, origin protection, caching and cache rules, redirect, transform, origin and configuration rules, load balancing, Argo and Smart Placement, Images, and Core Web Vitals audits. Use when onboarding a zone, changing DNS or TLS, raising cache hit ratio, fixing redirects or headers, or improving page and origin performance."
---

# Cloudflare Edge Delivery and Performance

## Purpose and activation

Get traffic to the right origin over the right protocol, cached as much as is safe, with origins protected and pages fast, and prove it with measurements. Activate for zone onboarding, DNS and certificate work, SSL/TLS mode changes, redirects and header rules, caching problems, load balancing, origin latency, and page performance audits.

## Scope and exclusions

In scope: DNS (records, proxy status, CNAME flattening, DNSSEC, partial setups), edge and origin certificates, SSL/TLS settings, origin lockdown, Cache Rules, cache keys, purge strategy, Tiered Cache and Cache Reserve, Redirect and Bulk Redirect rules, Transform, Origin, Configuration and Compression rules, Snippets, Load Balancing, Argo Smart Routing, Smart Placement, Spectrum for non-HTTP traffic, Images, and Core Web Vitals.

Not in scope: WAF, bot and DDoS controls (cloudflare-application-security), Worker code (cloudflare-workers-development), and making live changes (cloudflare-change-control).

## Required inputs

- Zone name, plan, setup type (full or partial), current nameservers and registrar, existing records export.
- Origins: hostnames, IPs, ports, protocols, certificate details, and whether they accept traffic only from Cloudflare.
- Content behavior: which paths are static, personalized or authenticated; current cache headers; cookies that vary content.
- For performance work: target URLs, field data if available (Web Analytics or other RUM), and the codebase if it is in scope.

## Dependencies and tools

- Current documentation for DNS, SSL/TLS, Cache, Rules, Load Balancing and the traffic sequence (the order in which rule phases run). Retrieve the traffic sequence before explaining precedence between products.
- Read-only probes against hostnames the user owns: `dig` or `nslookup` against the authoritative nameservers and a public resolver, `curl -sI` to read `cf-cache-status`, `cf-ray`, `age` and cache headers, `curl --resolve` to test a specific origin, `openssl s_client` for certificate chains.
- A browser performance trace tool (Lighthouse, DevTools or a DevTools MCP server the user has connected) for lab measurements; field data for real users.

## Workflow

1. Inventory current state read-only: records, proxy status, certificates, SSL/TLS mode, existing rules by phase, cache settings, and response headers for representative URLs.
2. Identify the gap against the goal and the rule from the guides below that addresses it.
3. Prefer the narrowest mechanism: a rule scoped by hostname and path rather than a zone-wide setting; a modern rule rather than a legacy Page Rule.
4. Write the change plan: exact settings and expressions, the expected header or behavior change, the verification probe, and the rollback.
5. Hand the plan to cloudflare-change-control for application; verify with the same probes afterwards.
6. For performance: measure first, rank opportunities by measured impact, change one thing at a time, and measure again.

## DNS guide

- Proxied records hide origin addresses and receive Cloudflare HTTP features only for HTTP and HTTPS on supported ports; other protocols need DNS-only records or Spectrum.
- Keep mail (MX, and hostnames mail servers connect to), domain-verification TXT records and non-HTTP services DNS-only. An MX or DNS-only record pointing at the web origin reveals its address.
- The apex can point at a hostname through CNAME flattening. Proxied records use automatic TTL.
- DNSSEC during a nameserver move: remove the old DS record at the registrar before switching nameservers, then enable DNSSEC in Cloudflare and add the new DS record. A stale DS record makes the zone fail to resolve on validating resolvers.
- If the zone has CAA records, they must allow the certificate authorities Cloudflare uses for edge certificates, or issuance and renewal fail. Whether Cloudflare adds those entries automatically depends on the setup; check current documentation and the live records.

## TLS and origin guide

- Use Full (strict) with a certificate the origin presents for the hostname, such as a Cloudflare Origin CA certificate (trusted by Cloudflare only) or a public certificate. Flexible encrypts only the visitor leg and loops when the origin redirects HTTP to HTTPS.
- Universal certificates cover the apex and one subdomain level; deeper names need an advanced or custom certificate. Confirm coverage before proxying a multi-level hostname.
- HSTS with long max-age, subdomains and preload is hard to undo; enable it only after every subdomain serves HTTPS correctly.
- Lock the origin so Cloudflare cannot be bypassed: allow only Cloudflare's published IP ranges, require Authenticated Origin Pulls, or remove inbound exposure with Cloudflare Tunnel.

## Cache guide

- By default only certain static file extensions are cached and HTML is not. Use Cache Rules to make content eligible and set edge and browser TTLs; respect origin `Cache-Control` unless there is a reason to override.
- Never cache personalized or authenticated responses under a shared key. Customize the cache key (query strings, headers, cookies, device) deliberately; every added dimension lowers hit ratio.
- Read `cf-cache-status`: HIT, MISS, EXPIRED, REVALIDATED, UPDATING, STALE, BYPASS and DYNAMIC each point at a different cause; DYNAMIC means the request was not eligible.
- Purge narrowly by URL, prefix, hostname or cache tag. Purging everything can overload the origin.
- Tiered Cache reduces origin requests; Cache Reserve keeps long-tail objects longer for a storage and operations cost.
- In Workers, the Cache API and `fetch` cache options behave differently from zone cache rules; check which one applies to the request path.

## Rules and routing guide

- Redirect Rules or Bulk Redirects for redirects; Transform Rules for URL rewrites and header changes; Origin Rules for host header, SNI, port and DNS override; Configuration Rules for per-path feature settings; Snippets for small logic; a Worker when real application logic is needed.
- Migrate legacy Page Rules to their modern equivalents and check that no rule in an earlier phase already handles the request.
- Load Balancing: health monitors probe from Cloudflare, so origins must allow them; choose steering and session affinity deliberately and test failover.
- Smart Placement helps Workers that make several round trips to one backend; Argo Smart Routing optimizes the Cloudflare-to-origin path.

## Performance guide

- Use Core Web Vitals (LCP, INP, CLS) with thresholds from current web.dev guidance; check field data before optimizing lab scores.
- Break down TTFB into DNS, connection and TLS, edge cache status and origin time. Fix origin and caching problems before front-end micro-optimizations.
- Quantify each recommendation (bytes, milliseconds, requests). Say plainly when a page is already fast.
- Typical levers: caching HTML where safe, compression, image resizing and modern formats through Images, removing render-blocking resources, preloading the LCP resource, setting image dimensions to avoid layout shift, and limiting third-party scripts.

## Expected output

A current-state summary, the change plan (setting, scope, expected effect, verification probe, rollback), and for audits a metrics table (metric, value, rating, source), prioritized issues with measured or estimated impact, and specific fixes.

## Validation

- Every change has a before and after probe on the same URL and resolver; cache changes show the expected `cf-cache-status` on a second request.
- TLS changes are verified with a direct origin check before the mode is tightened.
- Performance claims cite the trace or field data they came from; lab results are labeled as lab.

## Failure handling and escalation

- Records or certificates cannot be inspected: list what the user should export and continue with stated assumptions.
- A change risks resolution or certificate failure (nameserver move, DNSSEC, TLS mode, HSTS): require a rollback plan and lowered TTLs before proceeding.
- Conflicting rules across phases: stop, map the traffic sequence from documentation, and resolve ownership before adding another rule.

## Permissions and guardrails

Read-only inspection and local planning. DNS changes, proxy toggles, certificate orders, SSL/TLS and HSTS settings, rule changes, cache purges, load balancer edits and nameserver or registrar changes are consequential and need explicit approval for the exact zone and setting. Probe only hostnames the user owns or has authorized, at low request rates.

## Workflow connection

Within the complete pack, the optional `design-cloudflare-architecture.prompt.md` and `troubleshoot-cloudflare-issue.prompt.md` recipes connect this skill to the primary `cloudflare-subject-matter-expert` workflow, and changes are applied through `release-cloudflare-change.prompt.md`. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval, handoff and completion rules.
