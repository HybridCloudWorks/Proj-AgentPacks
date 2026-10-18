# Source Traceability

## Supplied references

- `github-expert.agent.md`: platform mission, Actions, OIDC, permissions, pinning, reusable workflows, governance, and handoff concepts.
- `github-actions-engineer.md`: workflow ownership, debugging, Copilot and agent workflow routing, query patterns, and no-deployment boundary.
- `SKILL.md`: prompt compression and progressive disclosure input.
- `SKILL (3).md`: Actions security, SHA pinning, least privilege, OIDC, injection defense, and concurrency.
- `SKILL (4).md`, `(6).md`, `(8).md`, `(9).md`, `(10).md`: bounded workflow, PR, label, issue, and discussion query patterns.
- `SKILL (5).md`, `(15).md`, `(20).md`, `(21).md`, `(22).md`, `(23).md`, `(24).md`, `(25).md`, `(26).md`: GitHub Script, summaries, error style, documentation, developer, debugging, custom agents, Copilot review, and agentic workflow concepts.
- `SKILL (7).md`, `(11).md`, `(13).md`, `(16).md`, `(17).md`, `(19).md`: GitHub MCP, Copilot agent PRs, agent tasks/sessions, temporary IDs, and merge-readiness patterns.
- `query-*.sh` and `query-discussions.py`: read-only query helper patterns, normalized into the pack's safe query-tool contract.

## Consolidation and gap fills

The canonical pack removes repository-specific Azure and gh-aw assumptions and combines overlapping query, workflow, and review material. Gap-filling Skills cover platform administration, repository lifecycle, rulesets, deployment environments, security and supply chain, releases, audit evidence, migrations, Apps/tokens/webhooks, and mutation-safe hooks.

## Current official references consulted

- https://docs.github.com/en/copilot/concepts/agents/code-review
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output
- https://docs.github.com/en/actions/how-tos/secure-your-work
- https://docs.github.com/en/actions/reference/security/oidc
- https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/slash-commands
- https://developers.openai.com/codex/skills/

These references support current behavior and boundaries; live tenant, organization, repository, plan, policy, and permission state remains not verified.
