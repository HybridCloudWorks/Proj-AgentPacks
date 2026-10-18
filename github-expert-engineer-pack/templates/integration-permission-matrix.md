# GitHub integration permission matrix and threat model template

What `github-apps-tokens-and-webhooks` requires before an App, token, OAuth app, webhook, callback, permission or secret is created or changed. The agent fills in the design; the integration owner creates the identity and the secrets.

## Workload and identity

- Workload: <what the integration does>
- Identity model: <GitHub App installation token | user token | OAuth app | fine-grained PAT>
- Why this model: <bounded automation, user attribution, or another reason>
- Installation scope: <all repositories | selected: list>
- Token lifetime and rotation: <installation tokens expire after one hour; private key rotation every N days by owner>
- Owner: <team or role>

## Permission matrix

| Permission | Level | Repository or organization | Reason | Calls that need it |
|---|---|---|---|---|
| Contents | read | repository | <reason> | `GET /repos/{owner}/{repo}/contents/...` |
| <permission> | <none / read / write / admin> | | | |

Every write permission names the call that needs it. Remove any permission no call needs.

## API usage

| Call | Method | Mutates state | Pagination | Rate-limit budget | Behavior on 403 or 429 |
|---|---|---|---|---|---|

## Webhooks

- Events subscribed: <minimal list; why each is needed>
- Signature validation: <HMAC SHA-256 `X-Hub-Signature-256` with constant-time compare>
- Replay defense: <delivery ID (`X-GitHub-Delivery`) store and window>
- Idempotency key: <field>; duplicate handling: <behavior>
- Ordering assumptions: <none, or how out-of-order events are reconciled>
- Timeout and response: <acknowledge fast, queue the work>
- Retries and redelivery: <who redelivers and how>
- Downstream actions: <least-privilege actions the handler may take>

## Threat model

| Threat | Entry point | Control | Residual risk |
|---|---|---|---|
| Forged webhook | receiver URL | signature validation | |
| Replayed delivery | receiver URL | delivery ID store | |
| Commands embedded in issue, PR or comment text | payload fields | treated as data; never executed | |
| Leaked private key or token | secret store, logs | <storage, redaction, rotation> | |
| Over-broad installation | installation settings | selected repositories | |

## Rollback

- <suspend the installation, revoke tokens, disable the webhook, restore the previous permission set>

## Verification plan

- <read-back of installation permissions and repository selection>
- <a signed test delivery accepted, an unsigned one rejected>
- <a replayed delivery ignored>

## Never in this document

Private keys, client secrets, webhook secrets and token values. Name each secret and its owner only.
