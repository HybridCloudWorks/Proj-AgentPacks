# GitHub migration and recovery plan template

The plan `github-migrations-backups-and-recovery` asks for when a migration, backup, restore or disaster-recovery exercise is assessed. An assessment never deletes or overwrites the source, rotates credentials or cuts over traffic.

## Scope

- Source: <host and version, enterprise or organization, repositories>
- Destination: <host and version, enterprise or organization>
- Tool: <chosen tool and version, or "to be chosen">
- Recovery point objective: <value and owner> · Recovery time objective: <value and owner>
- Freeze window: <window, or "to be agreed">

## Data-class inventory

| Data class | Count or size | Migrates | Lossy | Recreated manually | Owner | Notes |
|---|---|---|---|---|---|---|
| Git history, branches, tags | | | | | | |
| LFS objects, submodules | | | | | | |
| Issues, PRs, review comments | | | | | | |
| Discussions, Projects | | | | | | |
| Releases and assets, packages | | | | | | |
| Actions workflows and history | | | | | | |
| Secrets and variables | | never copied | | re-issued | | |
| Environments and protection rules | | | | | | |
| Rulesets and branch protection | | | | | | |
| Webhooks, Apps, external integrations | | | | | | |
| Teams, access, CODEOWNERS references | | | | | | |

## Lossy-conversion register

| Item | What is lost or changed | Impact | Mitigation |
|---|---|---|---|

## Phase plan

| Phase | Steps | Entry criteria | Exit evidence | Rollback point |
|---|---|---|---|---|
| Export | | | | |
| Transform | | | | |
| Import | | | | |
| Verification | | | | |
| Freeze | | | | |
| Cutover | | | | |
| Rollback | | | | |

## Restore test

- Isolated destination: <test organization or GHES instance>
- Representative sample: <repositories and why they were chosen>
- Pass criteria: <what must match: commit counts, tag SHAs, issue and PR counts, links>

## Post-migration verification

Read back on the destination; never assume a control migrated.

- [ ] Rulesets and branch protection match the before-state
- [ ] Required checks report on a test PR
- [ ] Code scanning, secret scanning, push protection and Dependabot enabled as before
- [ ] Environments and required reviewers present
- [ ] Webhooks and Apps reinstalled with the intended permissions
- [ ] Issue, PR and release links resolve or redirect

## Secrets re-issuance

| Secret name | Scope | Owner | Re-issued on destination | Old value revoked |
|---|---|---|---|---|

Secret values are never copied into exports, backups or this plan.

## Owners and sign-off

- Migration owner: <role> · Security owner: <role> · Rollback decision owner: <role>
