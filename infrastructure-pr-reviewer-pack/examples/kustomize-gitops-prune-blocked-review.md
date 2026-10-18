# Worked example: GitOps prune with an unrenderable overlay (blocked)

Synthetic walkthrough. The repository, SHAs, line numbers and command output are illustrative; nothing was run against real infrastructure.

- Prompts: `review-infrastructure-pull-request.prompt.md`, then `request-review-evidence.prompt.md` for the follow-up
- Skills: `review-infrastructure-pr`, `review-kubernetes-packaging`, `verify-infrastructure-evidence`
- Outcome: Insufficient evidence for a safe recommendation

This example shows the review stopping instead of inferring. The decisive behavior depends on rendered output and live cluster state that the reviewer cannot obtain within the authorized scope.

## Request

> PR #57 in `gitops-apps` moves the orders service under the payments team prefix and turns on automated sync for prod. Review only; no cluster access, and don't download anything.

## The change

Base `5c0d7e2`, head `a9b13f4`. Two files, 7 added and 1 deleted line:

```diff
--- a/apps/orders/overlays/prod/kustomization.yaml
+++ b/apps/orders/overlays/prod/kustomization.yaml
@@ -1,6 +1,8 @@
 apiVersion: kustomize.config.k8s.io/v1beta1
 kind: Kustomization
 namespace: orders-prod
+namePrefix: payments-
 resources:
   - ../../base
-  - ../../../../bases/postgres
+  - github.com/example-org/kustomize-bases//postgres?ref=main
```

```diff
--- a/argocd/orders-prod.yaml
+++ b/argocd/orders-prod.yaml
@@ -14,3 +14,8 @@ spec:
   destination:
     server: https://kubernetes.default.svc
     namespace: orders-prod
+  syncPolicy:
+    automated:
+      prune: true
+      selfHeal: true
```

## Walkthrough

1. **Inventory and ownership (`review-kubernetes-packaging`).** Argo CD Application `orders-prod` owns everything the prod overlay renders into `orders-prod`. Today it syncs manually and does not prune. After the change it syncs automatically, prunes resources that disappear from the rendered output, and reverts manual changes.
2. **What `namePrefix` does.** Kustomize prefixes the name of every rendered resource and rewrites references inside the rendered set. To Argo CD, each prefixed object is a new resource and each old name is no longer in Git. With `prune: true`, the old-named live objects are candidates for deletion on the first automated sync.
3. **What cannot be established.** Whether that deletion reaches anything data-bearing depends on the rendered set. The local base `bases/postgres` is replaced by a remote base at `ref=main`, and the reviewer cannot render it:

   ```text
   [SKIP] Kustomize build: apps/orders/overlays/prod
   remote reference detected; use --allow-downloads to permit resolution
   ```

   Downloads were not permitted, so the reviewer did not pass `--allow-downloads`. The old local base defined a standalone `PersistentVolumeClaim` named `orders-db-data`; whether the remote base still defines it as a standalone claim, or through a StatefulSet's `volumeClaimTemplates` that Argo CD does not track the same way, is unknown. Whether any Service consumed outside this repository (for example `orders.orders-prod.svc`) is renamed is also unknown.
4. **Stop condition reached.** `review-infrastructure-pr` stops when target, state or ownership cannot be established for a high-risk action, and when safe validation would require target access or untrusted downloads. Both apply: a prune on production with an unknown rendered set. The reviewer did not run `argocd app diff`, `kubectl diff` or a server-side dry-run, because each contacts the cluster.
5. **What is confirmed anyway.** The remote base is pinned to the mutable branch `main`. With automated sync and self-heal, a later commit to that branch changes what production renders the next time Argo CD regenerates manifests, without any pull request in `gitops-apps`. That is a defect in the diff itself and does not depend on the missing evidence.
6. **Checks (`verify-infrastructure-evidence`).** yamllint pass; Kustomize build skip (remote reference, downloads not permitted); Helm not applicable.

## Completion report

### Executive Summary

- Overall assessment: Safety cannot be determined; the change may prune production objects that the reviewer cannot see.
- Highest-risk finding: F-01, Pin the remote Postgres base to an immutable revision.
- Reviewed transition: manual, non-pruning sync of `orders-prod` to automated sync with prune and self-heal, plus a rename of every resource.
- Release or merge readiness: No recommendation possible until the evidence below is attached.

### Review Scope

- Base and head: `5c0d7e2` → `a9b13f4`
- Files and technologies: `apps/orders/overlays/prod/kustomization.yaml` (Kustomize), `argocd/orders-prod.yaml` (Argo CD Application)
- Entry points and execution order: Argo CD renders the prod overlay → compares with live objects in `orders-prod` → automated sync applies and prunes
- Targets, identities, state, and ownership: in-cluster destination, namespace `orders-prod`; Argo CD owns the rendered objects
- Evidence reviewed: diff and the previous local base `bases/postgres` at the base commit
- Constraints and exclusions: no cluster access; no downloads; the remote base was not read

### Coverage and Evidence

- Changed lines: 8 / 8
- Deletions, renames, generated artifacts, mode, or binary changes: 1 deleted line (local Postgres base) replaced by a remote base; `namePrefix` renames every rendered resource
- Cross-tool handoffs reviewed: Kustomize rendered set → Argo CD prune; rendered Service names → external consumers (not established)
- Existing-environment evidence: None
- Missing or non-authoritative evidence: rendered output for base and head; Argo CD diff against the live application
- Checks: yamllint pass; `kustomize build`, skip (remote reference detected, downloads not permitted)

### Findings Summary

`Critical: 0 · High: 1 · Medium: 0 · Low: 0 · Evidence gaps: 3`

### Findings

```text
Finding ID: F-01
Severity: High
Confidence: Medium
File: apps/orders/overlays/prod/kustomization.yaml
Location: line 7 (new)
Technology: Kustomize, Argo CD
Category: Version and supply-chain integrity
Title: Pin the remote Postgres base to an immutable revision
Execution path or trigger: Any commit to main in example-org/kustomize-bases, once automated sync is enabled by argocd/orders-prod.yaml.
Description: The base is referenced by the mutable branch ref=main, so the manifests Argo CD renders for production can change without a commit or review in this repository.
Impact: Unreviewed changes, including deletions under prune, reach the production orders database automatically.
Remediation direction: Reference the base by commit SHA or immutable tag, and update it through pull requests in this repository.
Verify with: kustomization.yaml showing a commit or immutable ref, and two renders at different times producing identical output.
```

Confidence is Medium only on timing: when Argo CD next regenerates manifests depends on its cache and refresh settings, which the repository does not show. The mutability itself is certain.

### Evidence Gaps

```text
[High evidence gap] Provide the rendered prod overlay for base and head
Artifact: kustomize build output for apps/orders/overlays/prod
Commit: 5c0d7e2 and a9b13f4, with the remote base pinned to the revision the PR intends
Inputs, target, identity: the prod overlay as committed; no cluster identity needed
Risk it resolves: which resources are renamed, and whether a standalone PersistentVolumeClaim is in the set
```

```text
[High evidence gap] Provide an Argo CD diff for orders-prod at the head commit
Artifact: argocd app diff (or the UI diff) for application orders-prod
Commit: a9b13f4, or the fixed head
Inputs, target, identity: the production cluster, generated by an operator with read access
Risk it resolves: which live objects the first automated sync would prune, especially orders-db-data
```

```text
[Medium evidence gap] Identify consumers of the current Service names
Artifact: list of clients of orders.orders-prod.svc and any other renamed Service
Commit: not applicable
Inputs, target, identity: service owners outside this repository
Risk it resolves: whether the rename breaks callers before they are updated
```

### Residual Risk

Until the rendered set and the live diff are reviewed, the first automated sync after merge may delete the orders database volume and rename Services that other teams call. This risk is the reason for the disposition, not a confirmed defect.

### Disposition

Insufficient evidence for a safe recommendation

### Handoff

- Required corrections: F-01 (High): pin the remote base, `apps/orders/overlays/prod/kustomization.yaml:7`.
- Suggested work order: (1) pin the base; (2) attach the renders and the Argo CD diff; (3) re-review. Consider enabling automated sync without prune for the rename, then enabling prune once old objects are confirmed safe to remove.
- Validation required after fixes: the three artifacts under Evidence Gaps, from the fixed head.
- Human decisions or approvals: deleting or retaining the old `orders-db-data` claim is a data decision for the service owner.
- Configuration and operational dependencies: drafted evidence request for the author, from `request-review-evidence.prompt.md`:

  > Before this can be reviewed, please attach: (1) `kustomize build apps/orders/overlays/prod` at `5c0d7e2` and at your head, with the remote base pinned to a commit; (2) an Argo CD diff for `orders-prod` at your head, generated by someone with read access to the production cluster; (3) the list of clients that call `orders.orders-prod.svc`. Please also say whether `orders-db-data` must survive the rename.
