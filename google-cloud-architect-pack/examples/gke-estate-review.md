# Worked example: Well-Architected review of a GKE estate with the estate inspector

Synthetic scenario for the `review-architecture.prompt.md` workflow, showing delegation to both specialists.

## Scope

Project `shop-prod`, cluster `shop-gke` in `europe-west4`. Pillars: security, reliability, operations. Review only: no fixes, tickets or comments.

## Delegation

The primary sent gcp-estate-inspector the handoff fields: scope `shop-prod` only, identity `review-viewer@shop-admin.iam.gserviceaccount.com` by impersonation, prohibited actions (any Level 2 command), and the questions to answer. The inspector classified, validated and ran one command at a time, for example:

```text
gcloud container clusters describe shop-gke --region=europe-west4 --project=shop-prod --format="yaml(autopilot,privateClusterConfig,workloadIdentityConfig,releaseChannel,binaryAuthorization,maintenancePolicy)"
kubectl get pdb -A
kubectl get ns --show-labels
```

It skipped `kubectl get secrets -A -o yaml` (classified Level 2, prints secret data) and returned a compact inventory with the command behind each fact. The primary then sent the inventory and the cluster's Terraform to gcp-security-reviewer for an independent read.

## Findings (excerpt)

| Severity | Pillar | Location | Evidence | Impact | Recommendation | Blocking |
|---|---|---|---|---|---|---|
| High | security | cluster `shop-gke` | `privateClusterConfig` absent; nodes have external IPs | Nodes reachable from the internet if a firewall rule is loosened | Plan a new private cluster and migrate; private nodes are a Day-0 setting | yes |
| High | reliability | namespaces `checkout`, `cart` | `kubectl get pdb -A` shows none for 3-replica Deployments | Upgrades can evict all replicas at once | Add PodDisruptionBudgets that still allow one disruption | yes |
| Medium | operations | cluster `shop-gke` | `releaseChannel` not set (static versioning) | Deprecated mode; versions drift towards forced upgrades | Enrol in the Regular channel with maintenance windows and exclusions | no |
| Medium | security | node pool `default-pool` | Uses the Compute Engine default service account | Broad default permissions on every node | Dedicated least-privilege node service account | no |
| Question | security | namespace `payments` | No Pod Security labels; workload intent unknown | Unknown whether privileged Pods are expected | Confirm with the team, then apply `restricted` with warn and audit first | no |

## Result

Status CHANGES_REQUIRED (two blocking findings). Not assessed: cost pillar (out of scope) and runtime behaviour during upgrades (needs a test in non-production).
