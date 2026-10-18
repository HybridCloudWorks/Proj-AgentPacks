---
name: azure-security-identity-and-compliance
description: Designs Azure identity, Zero Trust, Entra, RBAC, PIM, managed identities, secrets, network protection, policy, Defender, Sentinel, and compliance evidence.
---

# Azure Security, Identity, and Compliance

Start with the trust model and data classification. Use Microsoft Entra for authentication and identity lifecycle; use Azure RBAC with least privilege and PIM for resource-plane access; use managed identities and workload federation/OIDC instead of long-lived secrets.

Cover tenant boundaries, break-glass access, privileged roles, access reviews, conditional access assumptions, Key Vault, private endpoints, encryption/key ownership, Defender for Cloud, Sentinel, Azure Policy, activity logs, diagnostic settings, and regulatory evidence. Distinguish control-plane from data-plane permissions.

For CI/CD, document issuer, subject, audience, identity owner, scopes, token lifetime, and bootstrap dependency. Do not place the deployment identity it needs to authenticate inside the same destructive lifecycle without a recovery path. Treat compliance as a scoped assessment with evidence, not a design adjective.
