# Google Cloud architect hooks

This pack registers no hook with any client. If it shipped a hook definition, APM would copy the command line as written but not the script it calls, so the command would point at a file that does not exist after install. What you find here instead are portable helpers: run them by hand, wire them into a client yourself, or let the Code Workflow installer register them at the location where it keeps the pack.

| Helper | Purpose and activation | Input and dependencies | Behaviour and output | Failure handling and guardrail |
|---|---|---|---|---|
| `pre-gcp-command.sh`, `pre-gcp-command.ps1` | Classify a proposed `gcloud`, `bq`, `gsutil`, `kubectl`, `terraform` or `tofu` command before running it, manually or from a pre-tool hook | The command as arguments; Python 3.10 or later; the classifier shipped inside the gcp-estate-discovery skill | Prints the approval level (0, 1 or 2), the tools found and the reasons; exit 0 for Level 0 or 1, 2 for Level 2, 3 for invalid input | Never executes the command. Compound commands, command substitution and unknown verbs are Level 2. It is a safety aid, not an enforcement boundary |
| `post-gcp-architecture.sh`, `post-gcp-architecture.ps1` | Check a completion report before the work is declared done | Path to a completion JSON file; `tooling/completion_contract.py` | Prints `{"conforms": ..., "problems": [...]}`; exit 0 conforms, 1 problems found, 2 unreadable | Checks shape and consistency only; it does not run or trust the commands the report claims |
| `samples/google-cloud-architect.copilot-hooks.sample.json` | Reviewed example of wiring the classifier as a Copilot `preToolUse` hook | Replace `<SKILLS_HOME>` with the folder where the skills are installed | Runs the classifier in `hook` mode on each tool call | Sample only; see the limits below |

## Native hook versus portable script

- Native hooks are definitions a client reads from its hook location (for example `~/.copilot/hooks/*.json` or the `hooks` key in `~/.claude/settings.json`). This pack ships none.
- Portable scripts are the helpers above. They run anywhere Python runs and depend only on files inside this pack.

## Hook mode contract

`command_guard.py hook` reads a JSON payload from standard input (at most 256 KiB) and looks for the shell command in `tool_input.command`, in a `toolArgs` JSON string with a `command` field, or in a top-level `command` field. It prints a neutral verdict, `{"decision": "allow" | "ask", "level": ..., "tools": [...], "reasons": [...]}`, and exits 0 for allow or 2 for ask, also writing a one-line reason to standard error when it asks. It never echoes the command text, because commands can contain secrets.

## Limits

The payload field names and the way each client interprets the exit code and the printed verdict are not recorded in the repository's verified vendor facts, so verify them for your client and version before relying on the sample. Behaviour in a live client has not been exercised. The classifier recognizes Google Cloud and Kubernetes command-line tools only; other commands pass through as out of scope.
