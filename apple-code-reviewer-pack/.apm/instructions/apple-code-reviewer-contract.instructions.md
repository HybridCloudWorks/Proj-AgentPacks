---
description: "Approval, handoff and completion-report rules for the apple code reviewer pack. Always on; the agents, skills and prompts in this pack refer to it."
applyTo: "**"
---
# Apple code reviewer contract

This instruction is installed with the pack so that every agent, skill and prompt can rely on it. It replaces references to pack documents that are not installed.

## Completion report

Required sections: Executive Summary, Review Scope, Findings Summary, Detailed Findings, Category Results, Documentation Impact, Merge or Release Recommendation, Engineer Handoff Notes.

Required finding fields: Severity, Label, File, Location, Category, Confidence, Description, Evidence, Trigger or reproduction, Expected behavior, Observed or likely behavior, Impact, Recommendation, Suggested fix, Validation needed, Risk if unfixed.

Allowed recommendations: Approved, Approved with comments, Changes requested, Blocked.

Never describe an unexecuted check as passed; state what was not verified.
