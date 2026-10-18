---
name: ansible-vault-secrets
description: Manage Ansible Vault, vault IDs, secret-manager integration, plaintext-secret migration, no_log, diff suppression, and CI-safe password delivery. Use whenever Ansible variables, templates, inventory, output, or dependencies contain credentials or sensitive data.
---

# Ansible Vault and Secrets

Vault protects data at rest; it does not prevent a decrypted value from appearing in task arguments, output, diffs, facts, failure text, or artifacts. Design both storage and execution disclosure boundaries.

## Layout

Keep public variables separate from encrypted values, for example `group_vars/all/vars.yml` referencing `vault_app_password` from an encrypted `vault.yml`. Use environment-specific vault IDs when ownership or rotation differs. Never commit vault password files, real secrets, private keys, or copy-pasted decrypted examples.

Use `ansible-vault create|edit|view|encrypt|decrypt|rekey` deliberately. Prefer a CI secret manager or runner-mounted secret file over a repository password file. Keep password-file permissions restricted and provide passwords through `--vault-id` or an approved environment mechanism.

## Runtime protection

Add `no_log: true` to tasks that handle passwords, tokens, private keys, secret API payloads, or command output containing secrets. Add `diff: false` to sensitive file/template tasks. Do not debug decrypted values. Consider whether registered results, failure messages, callbacks, fact caching, and artifacts can retain the value.

## Migration

1. Search inventory, vars, templates, examples, CI, and history for likely secrets without printing matched values.
2. Rotate a secret if exposure is possible; do not treat encryption as retroactive revocation.
3. Move values to Vault or an external provider and reference them from public variables.
4. Add output protections and verify secret paths.
5. Validate with the password supplied out-of-band, then inspect the diff and repository scan.

When diagnosing `Decryption failed` or missing vault secrets, verify the selected Vault ID, password source, file path, and whether the invocation is reading the expected inventory. Do not ask the user to paste the password.
