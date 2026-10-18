# Notion subject matter expert hooks

Nothing in this folder is installed as a native hook. APM copies hook commands verbatim and does not deploy the scripts they call, so a pack-relative command would break after install. The helpers below run by hand or from CI, and the sample shows how an installer, or you, can wire one of them as a Claude Code hook once the pack's location on disk is known.

| Helper | Purpose and activation | Inputs and dependencies | Behaviour and output | Failure handling and guardrails |
|---|---|---|---|---|
| `pre-notion-publish.sh` / `.ps1` (manual) | Check a local draft before it is written to Notion or shared outward | A UTF-8 Markdown draft; optional `--audience internal or external` and `--kind research, decision, agenda, preread, howto, plan, task or any`; Python 3.10+ | Runs `tooling/notion_draft_check.py`; prints JSON findings by line and check name; exit 0 clean, 1 errors found, 2 unreadable | Never echoes matched text; reads only the named file; drafts over 2 MB are refused |
| `post-notion-work.sh` / `.ps1` (manual) | Check a completion report against the pack's report contract | A completion report JSON file; Python 3.10+ | Runs `tooling/completion_contract.py`; prints `valid` and error names; exit 0 valid, 1 invalid, 2 unreadable | Checks structure and consistency only; a valid report is not proof that the work happened |
| `samples/notion-sme.claude-settings.sample.json` (native sample, not installed) | Block Notion write tool calls that carry credentials | Claude Code `hooks` key in `settings.json`; the MCP server name you registered for Notion; `<PACK_HOME>` replaced with the installed pack path | `notion_draft_check.py --hook` reads the tool call on stdin, scans the tool input for credential patterns, exits 2 with a reason on stderr to block, 0 to allow | Inputs over 2 MB are blocked; unreadable input exits 1, which reports but does not block; the hook never prints the content it scanned |

## Scope of the checks

- Credential patterns: Notion integration tokens (`ntn_` and `secret_` prefixes), private key blocks, AWS access key IDs, GitHub tokens, Slack tokens and bearer tokens. Pattern matching misses secrets in other shapes; it is a safety net, not a control.
- Draft mode adds: unfilled placeholders outside code blocks, mention tags without a real URL, internal-only markers and pre-read references in drafts for external readers, and the required sections for the chosen document kind.
- Hook mode checks credentials only, so it does not block legitimate internal writes on stylistic grounds.

## Wiring the sample

1. Replace `<PACK_HOME>` with the absolute path where the installer placed the pack.
2. Replace `notion` in the matcher with the name of your Notion MCP server as registered in Claude Code; tool names follow the `mcp__<server>__<tool>` form.
3. Merge the `hooks` block into `~/.claude/settings.json` (user level) or a project's settings, then confirm with a harmless test write to a scratch page.
4. The sample assumes Claude Code's convention that exit code 2 from a PreToolUse hook blocks the call and shows stderr to the model. Confirm the convention against the client's hooks documentation before relying on it, and adapt the event name and output format for other clients.
