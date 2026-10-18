---
name: cloudflare-zero-trust
description: "Design, configure, troubleshoot and review Cloudflare One deployments: Access applications and policies, identity providers and SCIM, service tokens, Gateway DNS, network and HTTP policies, TLS inspection, DLP and CASB, device client enrollment, device profiles and split tunnels, Cloudflare Tunnel and private networks. Use when replacing a VPN, protecting internal or SaaS applications, filtering user traffic, or diagnosing an Access, Gateway, device client or Tunnel problem."
---

# Cloudflare Zero Trust

## Purpose and activation

Give the right people and devices access to the right applications, inspect and filter their traffic as policy requires, and connect private networks to Cloudflare, rolled out in stages that cannot lock everyone out. Activate for Access, Gateway, device client, Tunnel, private networking, DLP, CASB, device posture and identity integration work, and for any "why was this blocked or allowed" question in Cloudflare One.

## Scope and exclusions

In scope: Access application types and policies, identity providers, SCIM and group claims, service tokens and mutual TLS, Gateway DNS, network, HTTP, egress and resolver policies, TLS inspection and Do Not Inspect rules, DLP profiles, CASB integrations, device enrollment, device profiles, split tunnels, posture checks, Cloudflare Tunnel, private network and hostname routes, virtual networks, infrastructure access for SSH, browser-rendered SSH, RDP and VNC, Cloudflare WAN at the design level, and logs and digital experience monitoring.

Not in scope: mapping a source vendor's export (cloudflare-migration-planning), public-site WAF rules (cloudflare-application-security), and applying changes (cloudflare-change-control).

## Required inputs

- Users and groups, identity provider, SCIM status and the exact group claim names; contractors and service accounts.
- Applications: type (public web, private web, SSH, RDP, database, SaaS), hostnames, IPs and ports, and who needs them.
- Networks: sites, data centers, cloud VPCs, overlapping address spaces, private DNS zones, and where connectors can run with outbound access.
- Devices: managed or unmanaged, MDM, operating systems, other VPN or security agents installed.
- Rollout: pilot group, success criteria, rollback owner, compliance and logging requirements.

## Dependencies and tools

- Current Cloudflare One documentation for application types, policy actions and evaluation, Gateway order of enforcement, selectors, resolver policies, split tunnels, device profiles and Tunnel; never guess category IDs, application IDs, selector names or API bodies.
- Read-only inventory through the dashboard export, API or a connected Cloudflare tool when the user has put the account in scope.
- `cloudflared` and the device client CLI for local diagnostics on machines the user controls.

## Workflow

1. Classify the ask: architecture, configuration, troubleshooting, review or rollout.
2. Inventory before proposing: Access applications, policies and groups, identity providers, Gateway rules by type and precedence, lists, device profiles and enrollment rules, posture checks, tunnels, routes, virtual networks and resolver settings.
3. Design with the rules below. For each application, choose the application type and the on-ramp (clientless browser, device client, WARP Connector or Tunnel, or SaaS federation) before writing policy.
4. Write the change set in dependency order: identity and SCIM, connectors and tunnels, routes and DNS, lists, Do Not Inspect exceptions and root certificate deployment, Access applications and policies, Gateway policies, DLP and CASB, logging.
5. Stage: create new policies disabled or scoped to a pilot group, enable inspection for pilot devices first, and keep the previous path available until the pilot passes.
6. Hand the change set to cloudflare-change-control and validate with the cases below after each stage.

## Design rules

Access and identity
- Access decides who may reach an application; Gateway decides what traffic is allowed or inspected. Requirements that span both need both.
- Access is default-deny: an application without a matching Allow policy blocks everyone. Bypass skips identity entirely; use it rarely and never for sensitive applications. Machine-to-machine access uses service tokens or mutual TLS with a Service Auth policy.
- Public-hostname applications can be clientless. Private IP or private hostname applications need an on-ramp (device client or another connector), a route and DNS resolution; an Access application alone is not enough.
- Group-based rules depend on IdP group claims or SCIM. Access Groups are Cloudflare objects; Gateway identity selectors use synced IdP groups. Group names and claim values are case-sensitive, and membership changes apply after sync and re-authentication.

Device client
- Enrollment permissions are an Access application for device enrollment; debug enrollment there. Device profiles match in precedence order, first match wins, with a default profile for the rest.
- Split tunnel mode is per profile: Include sends only listed destinations through Cloudflare (VPN replacement or coexistence with another VPN); Exclude sends everything except listed destinations (secure web gateway). Entries must agree with tunnel routes in both directions, or traffic is dropped or never enters the tunnel.
- MDM-deployed settings override dashboard settings. Headless or service enrollments authenticate as a non-identity user and match no IdP groups.

Gateway, TLS inspection and DLP
- DNS, network, HTTP and egress policies are evaluated in different stages with different selectors; retrieve the order of enforcement before reasoning about precedence.
- HTTP inspection and DLP need TLS inspection, which needs the Cloudflare root certificate deployed to devices and Do Not Inspect rules for certificate-pinned applications. Do Not Inspect rules are evaluated before allow, block and isolate.
- DLP profiles detect nothing until a Gateway HTTP policy or CASB setting references them. Start in log mode, tune false positives, then block.
- In default-deny network designs, add an explicit allow for private Access application traffic ahead of broad layer-4 blocks.
- API-based CASB scans are periodic and out of band; inline control of SaaS actions is a Gateway HTTP capability.

Tunnel and private networks
- Prefer remotely managed, token-based tunnels. Run at least two `cloudflared` replicas on separate hosts for production and update them one at a time.
- A healthy tunnel only proves the connector reaches Cloudflare; published hostnames, network routes or hostname routes, and DNS resolution must also be correct, and the connector must reach every origin.
- Use virtual networks when address spaces overlap and hostname routing is not used. Keep `noTLSVerify` off outside development.
- Tunnel tokens and IPsec pre-shared keys are credentials; some are shown only once and must go straight into a secret store.

## Validation

Run these cases with pilot users and devices after each stage, and report any case not run as unverified.

- Access: allowed user, denied user, posture-failing device, expired session, service token, each identity provider.
- Private access: route lookup, tunnel replicas healthy, origin reachable from the connector, split tunnel behavior, DNS resolution and an end-to-end request from a pilot device.
- Gateway: rule type, action, expression, precedence, referenced lists and logging verified in Gateway activity logs before broad enablement.
- TLS inspection and DLP: Do Not Inspect exceptions and root certificate trust tested before inspection; DLP tested with known samples.

## Troubleshooting

Work from logs to configuration: find the Gateway activity log, Access authentication log, device client diagnostic or tunnel log line that shows the failure, then trace it to the rule, route, profile or policy responsible. Check the user's last authenticated identity and groups, not only the IdP's current state.

## Expected output

Designs: assumptions, target architecture, product responsibilities, rollout phases, validation and open decisions. Configuration: prerequisites, exact resources to inspect, create or change, tests and rollback. Troubleshooting: traffic path, failure point with evidence, and the next test.

## Failure handling and escalation

- SCIM or group claims missing: do not invent group selectors; propose user lists as a stopgap only with the owner's agreement, or block on the identity work.
- Inspection would break a critical application: keep it in Do Not Inspect and record the risk.
- A limit (for example destinations per application) blocks the design: retrieve the current limit and ask the account owner about increases before splitting objects.
- Lockout risk: stop and require a rollback path that does not depend on the policy being changed.

## Permissions and guardrails

Read-only inventory and local planning. Creating or changing Access applications, policies, identity providers, service tokens, Gateway rules, lists, device profiles, enrollment rules, posture checks, tunnels, routes, resolver policies, DLP or CASB settings needs explicit approval for the exact account and object. Broad block, allow, inspection or DLP policies start disabled or limited to a pilot unless the owner approves wider scope. Never paste tunnel tokens, service-token secrets or pre-shared keys into chat or files.

## Workflow connection

Within the complete pack, the optional `deploy-zero-trust-access.prompt.md` recipe connects this skill to the primary `cloudflare-subject-matter-expert` workflow; the `cloudflare-security-reviewer` uses it to review policies and the `cloudflare-migration-analyst` uses it for Cloudflare One targets. This skill is self-contained when installed alone. With the full pack installed, the `cloudflare-subject-matter-expert-contract` instruction supplies the approval, handoff and completion rules.
