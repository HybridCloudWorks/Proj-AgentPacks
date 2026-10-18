---
description: "Trace a multi-tool infrastructure execution chain and review every handoff between pipeline, template, script, configuration and manifest"
agent: infrastructure-pr-reviewer
---

# Trace cross-tool handoffs

Use this workflow when one pull request changes several tools that pass data to each other, for example a pipeline that deploys a template, transforms its outputs in a script, and feeds the result to configuration management or a manifest.

## Inputs

- The diff with base and head revisions, and every file in the chain even when only some changed.
- Entry points and the order in which the pipeline runs them.
- Example or captured outputs at each boundary, when supplied, with any secret values removed.

## Workflow

1. Apply the `review-infrastructure-pr` Skill and build full changed-line coverage.
2. Write the execution sequence as that Skill's `references/review-protocol.md` describes, one step per tool, naming the input each step consumes and the output it produces.
3. At every boundary, check type and representation, serialization depth, escaping, quoting, encoding, empty and singleton collections, secret masking and ownership.
4. Activate each technology Skill in the chain, such as `review-cicd-deployment`, `review-bicep-arm`, `review-terraform-opentofu`, `review-powershell-automation`, `review-ansible-automation` and `review-kubernetes-packaging`. Review each tool on its own terms.
5. Confirm that a failure at any step stops the chain and that later steps cannot run on empty, partial or stale output.
6. Apply `verify-infrastructure-evidence` for safe parsers, linters and builds. Do not execute the chain.
7. Report one finding per root cause at the line where the incompatible contract is introduced, citing the consumer path in the body.

Stay read-only. Do not run deployment, transformation or configuration steps to observe their output.

## Expected output

The review report in the structure of the `review-infrastructure-pr` Skill's `assets/review-report-template.md`. List the execution sequence in Review Scope and every handoff reviewed, with its result, in Coverage and Evidence.

Follow the `infrastructure-pr-reviewer-contract` instruction. Never describe an unexecuted check as passed.
