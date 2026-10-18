---
description: "Diagnose a Cloudflare error, block, cache surprise, slowdown or connectivity failure"
agent: cloudflare-subject-matter-expert
argument-hint: "[symptom, URL, Ray ID or time window]"
---

# Troubleshoot a Cloudflare issue

## Inputs

Symptom, scope and start time, sample URLs and Ray IDs, recent changes, and the logs or accounts the user has put in scope.

## Workflow

Apply cloudflare-observability-and-troubleshooting to locate the failing layer with read-only probes and logs. Use cloudflare-edge-delivery-and-performance for DNS, TLS, cache and performance causes, cloudflare-application-security for blocks and challenges, cloudflare-zero-trust for Access, Gateway, device client and Tunnel, and cloudflare-workers-development for Worker errors. Hand any fix to cloudflare-change-control.

## Expected output

A diagnostic report with the request path, evidence labeled by environment and time, the confirmed cause or ranked hypotheses with the next test, the recommended fix, observability improvements, and an ANALYSIS_ONLY status unless a fix was applied and verified, under the `cloudflare-subject-matter-expert-contract` instruction.
