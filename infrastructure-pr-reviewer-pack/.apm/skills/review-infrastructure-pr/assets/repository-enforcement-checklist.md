# Repository Enforcement Checklist

- [ ] Copilot custom instructions enabled for code review.
- [ ] Infrastructure skill present on the PR head branch.
- [ ] Required parser, format, lint, schema, policy, security, and test checks configured for technologies used.
- [ ] Plans, what-if results, rendered output, or check-mode evidence tied to the reviewed commit and target.
- [ ] Deployment consumes the reviewed immutable artifact or equivalent revalidation and approval occurs.
- [ ] Production uses protected environments and accountable approval.
- [ ] CODEOWNERS or equivalent ownership covers infrastructure, automation, pipelines, identities, policies, and secrets paths.
- [ ] State, target, and pipeline concurrency controls prevent overlapping changes.
- [ ] Credentials use least privilege and short-lived federation where supported.
- [ ] Critical and High review findings must be resolved before merge or deployment.
- [ ] Re-review occurs on new pushes.
