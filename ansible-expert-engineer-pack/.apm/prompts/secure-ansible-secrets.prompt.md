---
description: "Find plaintext secrets in Ansible content and move them to Vault with output protection"
agent: ansible-expert-engineer
---

# Secure Ansible secrets

## Inputs

- The paths in scope: inventories, `group_vars`/`host_vars`, role defaults and vars, templates, examples and CI definitions.
- The intended Vault ID scheme per environment, or the approved external secret provider.
- How CI receives the vault password (CI secret store, runner-mounted file), and who owns each secret for rotation.

Never ask the user to paste a vault password, token or private key. Never print a matched secret value, even partially.

## Workflow

1. Apply `ansible-vault-secrets`. Search inventory, vars, templates, examples, CI and Git history for likely secrets, reporting file, line and key name only.
2. Decide rotation first: if a value may have been exposed (committed, rendered into a diff, logged by CI), list it for rotation by its owner. Encryption is not retroactive revocation. Rotation is a secret change and needs explicit authorization.
3. Separate public variables from encrypted values, for example a public `vars.yml` referencing `vault_`-prefixed names in an encrypted `vault.yml`, with environment-specific Vault IDs where ownership or rotation differs.
4. Add `no_log: true` to tasks that handle secrets and `diff: false` to sensitive file and template tasks. Check registered results, failure messages, callbacks, fact caching and artifacts for retained values.
5. Keep the scope of each variable correct with `ansible-inventory-and-variable-design`, and validate with `ansible-validate-content`, supplying the vault password out of band.
6. For `Decryption failed` or missing vault variables, verify the selected Vault ID, password source, file path, and whether the invocation reads the expected inventory.

## Expected output

Located findings without values; the rotation list with owners; the vault layout and the changed or proposed files; output-protection changes; CI password-delivery design; validation evidence; and what remains exposed, such as Git history or retained CI logs. If the vault password or secret owner is not available, stop at the prepared changes and say the work is blocked and on what.

Follow the `ansible-expert-engineer-contract` instruction for the completion report.
