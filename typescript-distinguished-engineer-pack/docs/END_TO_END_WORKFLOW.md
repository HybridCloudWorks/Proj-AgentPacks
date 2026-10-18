# End-to-End Workflow Example

## Feature implementation

The primary agent inventories the repository, identifies an API and React boundary, states facts and assumptions, creates acceptance criteria, selects the strict TypeScript, API, frontend, and testing Skills, then implements a focused change with runtime validation and tests.

## Security review

It hands the same scope to `typescript-security-reviewer` with prohibited actions. The reviewer returns findings with evidence, severity, impact, remediation, and limitations. The primary agent fixes or explicitly records residual risk; the review is not treated as an approval to deploy.

## Playwright verification

`typescript-test-engineer` inspects the existing Playwright setup, exercises the critical user journey and failure states with accessible locators, captures trace diagnostics on failure, and returns exact commands and results.

## Agent evaluation

If the feature includes an agent or MCP tool, `agent-evaluation-engineer` creates scenarios for success, invalid inputs, tool errors, prompt injection, unauthorized requests, cancellation, budget exhaustion, partial completion, recovery, and rollback. Deterministic checks and model-judged criteria are labeled separately.

## Final completion report

The primary agent reviews the final diff, maps all acceptance criteria to evidence, records security, observability, cost, operations, rollback, skipped checks, and unverified items, then returns one supported completion status. It does not merge, deploy, publish, or claim production success without approval and direct evidence.
