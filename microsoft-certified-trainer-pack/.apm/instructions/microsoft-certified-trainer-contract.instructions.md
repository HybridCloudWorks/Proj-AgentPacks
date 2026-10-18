---
description: "Approval, handoff and completion-report rules for the microsoft certified trainer pack. Always on; the agents, skills and prompts in this pack refer to it."
applyTo: "**"
---
# Microsoft certified trainer contract

This instruction is installed with the pack so that every agent, skill and prompt can rely on it. It replaces references to pack documents that are not installed.

## Approval matrix

| Action | Default |
|---|---|
| Read supplied files and official docs | Allowed |
| Create or edit local drafts, notes, reports, and generated targets | Allowed within workspace |
| Run local validation and inspect archives | Allowed |
| Use live learner or organizational data | Ask first; synthetic data preferred |
| Modify GitHub repository, workflow, branch, issue, or PR | Ask first |
| Modify Azure, Microsoft 365, Graph, Copilot Studio, or tenant settings | Ask first |
| Publish an agent, flow, course, or external page | Ask first |
| Send email, announcements, or learner communications | Ask first |
| Delete data or incur cloud cost | Ask first with exact target and rollback |

## Deliverable contract

A completed course-preparation or delivery bundle should include:

- audience, assumptions, prerequisites, duration, and delivery mode;
- source and change-log map with current Microsoft Learn links;
- measurable objectives and objective-to-activity/evidence matrix;
- agenda/syllabus with timing, breaks, buffer, optional cuts, and extensions;
- deck/instructor-guide plan with notes, questions, transitions, and accessibility;
- demo and lab runbooks with preflight, seed data, expected results, reset, troubleshooting, and fallback;
- knowledge checks with answer rationale and remediation;
- Azure/GitHub handoff packets where needed;
- evaluation plan and maintenance/refresh triggers;
- validation status and explicit unverified assumptions.

## Handoff contract

When work crosses into an Azure Architect or GitHub Expert pack, provide:

- course, module, objective, learner action, and acceptance evidence;
- source and version/change-log references;
- audience, duration, delivery mode, and accessibility needs;
- environment, account, license, role, network, repo, branch, and tool assumptions;
- synthetic data design and privacy classification;
- cost ceiling, quotas, lifecycle, cleanup, and rollback;
- exact requested action, read-only checks already completed, and unanswered questions;
- evidence required to call the handoff complete.

The trainer agent must not report a deployment, repository change, or live readiness result until the partner returns evidence. A static plan is not a live result.

## Completion report

Required sections: assumptions, source_map, objectives, agenda, activity_and_demo_map, lab_requirements, assessment_plan, accessibility_notes, risks_and_fallbacks, deliverables, verification_evidence.

Evidence labels: source, static, local_rehearsal, live, unverified.

Required disclosures: no_claim_of_mct_status, no_claim_of_license_or_tenant_access, no_claim_of_live_publication_without_evidence.

Never describe an unexecuted check as passed; state what was not verified.
