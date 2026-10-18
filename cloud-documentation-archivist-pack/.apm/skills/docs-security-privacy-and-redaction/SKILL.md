---
name: docs-security-privacy-and-redaction
description: Prevent documentation from exposing secrets, personal data, customer information, private infrastructure, unsafe commands, or misleading security claims.
---

# Documentation Security and Privacy

Scan prose, code, output, screenshots, diagrams, links, metadata, filenames, comments, and generated artifacts for tokens, passwords, private keys, connection strings, personal data, customer names, internal hostnames, subscription or account identifiers, and sensitive topology.

Replace with safe placeholders and representative sanitized output. Do not merely mask a secret after it has been committed or published; coordinate containment and rotation with the owner. Document required permission classes without documenting credentials.

Review command injection, copy-paste hazards, privilege escalation, destructive examples, data retention, access controls, classification, licensing, and disclosure approval. State what was checked and what cannot be proven from documentation alone.
