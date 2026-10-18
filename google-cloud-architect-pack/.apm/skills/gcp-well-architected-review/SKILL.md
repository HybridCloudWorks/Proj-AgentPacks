---
name: gcp-well-architected-review
description: "Review a Google Cloud design, estate or infrastructure change against the six pillars of the Google Cloud Well-Architected Framework - security, reliability, operational excellence, cost, performance and sustainability - with evidence-based findings, severities and a remediation roadmap. Use when asked to assess, audit, review or score an architecture, a production readiness gate, or an existing Google Cloud environment."
---

# Google Cloud Well-Architected Review

## Purpose and activation

Tell an owner, with evidence, where their architecture is exposed and what to fix first. Activate for design reviews, production readiness gates, periodic audits, post-incident reviews, acquisition due diligence, or a user asking whether an architecture follows Google Cloud best practices.

## Scope and exclusions

In scope: scoping, evidence gathering, pillar-by-pillar assessment, findings with severity, a maturity summary and a remediation roadmap. Remediation itself is out of scope: a review-only request never authorizes fixing, applying or posting anything. Perspectives such as the AI and ML or financial services lenses are applied when the workload calls for them.

## Inputs

What to review (documents, diagrams, IaC, plan output, or a named organization, folder or project and the identity to use), the workload's requirements and SLOs, the pillars or risks the owner cares most about, compliance obligations, and any previous review findings.

## Dependencies and tools

[Well-Architected Framework](https://docs.cloud.google.com/architecture/framework) and its pillar pages for security, reliability, operational excellence, cost optimization, performance optimization and sustainability; the [AI and ML perspective](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml/printable.md.txt) and [financial services perspective](https://docs.cloud.google.com/architecture/framework/perspectives/fsi/printable.md.txt). gcp-estate-discovery or the gcp-estate-inspector specialist for live evidence; gcp-security-reviewer for an independent security read; Security Command Center, Recommender and Workload Manager results when the user shares or authorizes them. The pillar skills in this pack hold the detailed design guidance.

## Workflow

1. Scope: agree what is in and out, the pillars, the depth (quick scan or full review), the evidence available and the deadline. Record what cannot be inspected.
2. Gather evidence before judging: read the design and IaC, and for a live estate run read-only discovery with explicit scope and data reduction. Ask the owner only the assessment questions the evidence cannot answer.
3. Assess each pillar. Typical questions and checks:
   - Security: Are identities federated and keys absent? Is access group-based and least-privilege? Are default networks removed and external IPs restricted? Are sensitive datasets inside VPC Service Controls and encrypted to requirement? Is infrastructure deployed through IaC with scanning and Binary Authorization? Are audit logs centralized, Security Command Center active and incident response rehearsed? For AI, are prompts and responses inspected and tools least-privilege?
   - Reliability: Are SLIs and SLOs user-centred and monitored? Is there any single zone or region dependency the SLO does not allow? Do autoscaling, health checks and automated failover exist and work? Are backups restore-tested against RTO and RPO? Are retries, timeouts, rate limits and degraded modes designed in? Are failure tests and blameless postmortems routine?
   - Operational excellence: Are readiness criteria defined? Do SLO burn-rate alerts with runbooks exist? Are incident roles and channels defined? Are all changes made through IaC and CI with automated tests and progressive rollout? Is utilization reviewed regularly?
   - Cost: Are all resources labelled for attribution? Is billing export enabled and reviewed? Do budgets and alerts exist per project? Are Recommender findings acted on and commitment coverage reviewed? Are idle resources removed and storage lifecycle policies active? Are managed or serverless services preferred where they fit?
   - Performance: Is sizing based on load tests or history? Is caching used at the right layers? Are storage types matched to I/O? Are components decoupled with bulkheads? Do dashboards, tracing and profiling exist for key indicators? Are autoscaling rules validated?
   - Sustainability: Is region carbon considered? Do idle environments scale to zero? Are current machine generations and suitable accelerators used? Is batch work scheduled flexibly? Is DR cold or on-demand where objectives allow? Is dark data identified and is carbon data analyzed?
4. Write findings, each with severity (Critical, High, Medium, Low, Advisory, Question), pillar, location (resource, file and line, or document section), evidence (what was observed and how), impact (the failure or loss it enables), recommendation (specific and Google Cloud-native) and a blocking flag. A finding without evidence becomes a Question.
5. Summarize per pillar: strengths, top risks and a maturity statement in words, not a numeric score that implies more precision than the evidence supports.
6. Build the roadmap: fix-now items (Critical and blocking), next-quarter items and longer-term improvements, each with an owner suggestion and the pillar trade-offs it involves.

## Output

Scope statement, evidence list with the commands and documents used, findings table, pillar summaries, roadmap, items not assessed and why, and a status of CHANGES_REQUIRED when any blocking finding exists, otherwise ANALYSIS_ONLY.

## Validation

Every finding has evidence and a location; no finding rests on an assumption presented as fact; every pillar in scope has at least a summary even when it has no findings; severities follow impact and likelihood, not checklist position; and live evidence came from Level 1 read-only commands only.

## Failure handling and escalation

Evidence not available for a pillar: mark it not assessed with the reason instead of guessing. Active compromise or imminent data loss discovered: stop the review and tell the owner immediately. Owner disputes a finding: record the dispute and the evidence; do not delete the finding.

## Permissions and guardrails

Reviewing supplied material is Level 0; live read-only discovery is Level 1 on the scope the user named; any fix, policy change, ticket, comment or message is Level 2 and outside a review-only request. Do not paste secrets, tokens or full IAM policies into the report. Without the pack's contract installed, treat every change as needing explicit approval.

## Connection to the pack

The optional `review-architecture.prompt.md` recipe runs this skill, delegating live discovery to gcp-estate-inspector and the security pillar to gcp-security-reviewer when independence is wanted. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
