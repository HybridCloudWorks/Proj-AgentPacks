# Kubernetes, Helm, and Kustomize Review Adapter

Apply this adapter to Kubernetes YAML, Custom Resources, Helm charts and values, Kustomize bases and overlays, operators, GitOps configuration, and pipelines that render or apply them.

## 1. Target and ownership

Identify cluster, context, namespace, release name, GitOps application, field manager, and controller ownership.

Verify:

- Context and namespace are explicit and validated.
- Helm, kubectl, Kustomize, an operator, and GitOps controller do not fight over the same fields.
- Resource renames, release renames, namespace changes, and selector changes do not orphan or duplicate resources.
- Cluster-scoped resources receive appropriate review and permissions.
- Prune or deletion behavior is understood.

## 2. Workload identity and rollout

Review:

- Deployment, StatefulSet, DaemonSet, Job, and CronJob strategy.
- Immutable selectors and stable service selectors.
- Pod-template labels and workload ownership.
- Readiness, liveness, startup probes, termination grace, preStop hooks, and disruption budgets.
- Rolling-update surge and unavailable settings relative to capacity and quota.
- Stateful storage, ordered rollout, and data migration.
- Job retry, backoff, deadlines, concurrency policy, and idempotency.

## 3. Security

Verify:

- Service accounts, RBAC verbs, resources, namespaces, and impersonation follow least privilege.
- Pod and container security contexts, privilege escalation, capabilities, host namespaces, host paths, and device access.
- Network policies and ingress exposure.
- Secret handling, external secret references, projected volumes, and logs.
- Image source, digest or tag policy, pull policy, and signature or admission controls.
- Admission policies, policy exemptions, and namespace labels.

## 4. Resources, scheduling, and availability

Review:

- CPU, memory, ephemeral storage, limits, requests, and autoscaling behavior.
- Node selectors, affinity, topology spread, taints, tolerations, and zone resilience.
- PersistentVolume claims, storage classes, reclaim policy, expansion, and access modes.
- Service ports, target ports, protocols, load balancer behavior, and DNS.
- ConfigMap or Secret changes that require rollout triggers.

## 5. Helm

Verify:

- Values schema, defaults, null handling, type preservation, and environment overrides.
- Template functions, quoting, indentation, and generated names.
- Release-name and namespace stability.
- Hooks, weights, delete policies, and failure behavior.
- CRDs and upgrade ordering.
- Chart dependencies and versions.
- Rendered manifests for every affected values combination.
- `lookup` or cluster-dependent template behavior.

A successful `helm template` proves rendering, not cluster admission or safe upgrade behavior.

## 6. Kustomize

Verify:

- Base and overlay resolution.
- Patch targets remain unique and match the intended objects.
- Name prefixes, suffixes, namespace transforms, labels, and image substitutions preserve selectors and references.
- Generated ConfigMap and Secret names trigger intended rollout and do not leak secrets.
- Remote bases or components are version constrained and trusted.
- Rendered output is reviewed for every changed overlay.

## 7. Validation evidence

Use, when available:

- YAML and schema validation.
- `helm lint` and `helm template` with affected values.
- `kustomize build` or `kubectl kustomize` for affected overlays.
- Policy and security scanners.
- Server-side dry-run against a safe target when appropriate.
- Diff or GitOps preview against representative existing cluster state.

Do not assume client-side validation understands Custom Resource schemas or admission-controller behavior.
