# Governance, maintenance and versioning

Pack version 1.0.0 follows agent-pack-prompt v2.3. The canonical `.apm/` source is authoritative; vendor files are generated at install time by APM or by the Code Workflow installer and are never edited by hand.

## Changing the pack

1. Change the source under `.apm/` first.
2. Update `tests/capability-coverage.yml`, `tests/trigger-cases.yml` and, if the report format changes, `tests/report-contract.yml` together with the contract instruction and `tooling/completion_contract.py`.
3. Regenerate `tests/skill-coverage.yml` with the shared `tooling/skill_coverage.py` whenever a skill is added, removed or its description changes.
4. Run the pack tests and the shared validator with `--install-check`; build release archives with the shared builder.

Use semantic versioning: major for incompatible contract, status or permission changes; minor for new capabilities or skills; patch for corrections.

## Keeping Cloudflare knowledge current

The skills hold procedures and stable behavior, not numbers. Limits, prices, plan entitlements, field names and flags are retrieved at task time. Review the skills when Cloudflare announces changes to the products they name, in particular: Wrangler commands and configuration keys, the Workers static assets and gradual deployment model, the Terraform provider's major versions, Rules language field names, Agents SDK APIs, Sandbox package lines, and Cloudflare One product names. Record the review date in this file.

Last content review: 2026-10-18.

## Known limits and unresolved operational inputs

Account, zone, plan, tokens, identity provider, CI environments and approvals are discovered per task. Live behavior in Claude Code, Codex, Copilot (CLI and the VS Code agent pane), Kiro and Gemini CLI, real Cloudflare API and Wrangler behavior, Copilot hook execution, and model behavior of the agents are not established by the local tests. The bundled checkers are heuristics over local files: the Wrangler checker does not validate against the live configuration schema, the ruleset guard does not evaluate expressions, and the accounting checker cannot tell whether a mapping is semantically right.

## Genuine not-applicable artifacts

No account-specific configuration, MCP registration, tunnel token or deployment manifest is shipped: a reusable pack has no concrete environment. `docs/INTEGRATION_CONTRACT.md` explains which inputs are supplied at task time. All canonical artifact categories are present.
