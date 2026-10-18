# Design Decisions

## Reviewer boundary

The Agent sits after implementation/build and before pull-request or deployment approval. It reviews and reports; it does not implement fixes, merge, publish, or mutate cloud state.

## Thin router, focused review Skills

The supplied files repeat code review, architecture review, security, policy, onboarding, validation, role verification, and error guidance. They were consolidated into focused Skills so a routine review does not load unrelated cloud, security, or deployment material.

## Evidence and severity discipline

Findings must be grounded in a file, line, diff, test, preview, or authorized read-only observation. Confirmed defects, validation hypotheses, accepted risks, human blockers, skipped checks, and not-verified evidence are distinct. Severity is tied to impact and trigger, not reviewer preference.

## Safe automation

Pre-review inventory and post-review report validation are deterministic, non-mutating helpers. They do not run `apply`, `deploy`, `delete`, `force-unlock`, identity/policy changes, PR publication, or live queries without explicit authorization.

## Azure preview and policy

The reviewer recognizes Bicep `validate`/`what-if`, AZD preview, Terraform plan, and Azure Policy evidence as bounded evidence. It does not treat a plan or what-if as a successful deployment or live compliance proof.

## Handoff over hidden autonomy

The final report has one recommendation and a precise engineer handoff. A clean report is not authorization to deploy; the next actor and approval gate remain explicit.
