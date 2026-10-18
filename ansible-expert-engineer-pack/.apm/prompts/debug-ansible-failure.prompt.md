---
description: "Diagnose an Ansible connection, become, module, templating, version or performance failure"
agent: ansible-expert-engineer
---

# Diagnose an Ansible failure

## Inputs

- The exact command, the error output with secrets redacted, and the output of `ansible --version`.
- The inventory source, the failing hosts and target OS, and what changed recently (core or collection upgrade, inventory edit, credential change, host rebuild).
- Whether diagnosis only, or a fix, is requested.

Never ask for or accept credentials, private keys, vault passwords or secret task output. A diagnose-only request authorizes analysis, not changes.

## Workflow

1. Apply `ansible-debug-runtime-failures`. Classify the failure using its triage order: parse/config, inventory/selection, connection, authentication/become, module/collection, templating/variables, runtime semantics, performance.
2. Reduce scope to one host, one play and one task. Start with `-v`; use `-vvv` only when connection or traceback detail is needed, because it can reveal sensitive inputs.
3. Bring in the skill that owns the failing layer: `ansible-inventory-and-variable-design` for selection, precedence and variable types; `ansible-collections-supply-chain` for unresolved modules or option mismatches; `ansible-vault-secrets` for decryption failures; `ansible-execution-control` for handler, delegation, `serial` or `run_once` surprises.
4. When an upgrade is involved, read the relevant official porting guide before changing code.
5. Propose the smallest safe reproduction and state exactly what it may change. Prefer a local fixture or localhost reproduction; any run against a real host needs explicit approval.
6. If a fix is authorized, validate it with `ansible-validate-content`.

## Expected output

Confirmed cause, contributing factors, hypotheses and missing evidence, each kept separate; the smallest safe reproduction; the proposed fix or authorized patch; regression checks; and similar latent defects found while diagnosing. A passing syntax check is not connectivity proof, `--check` does not exercise every module path, and one passing run does not prove convergence.

Follow the `ansible-expert-engineer-contract` instruction for the completion report.
