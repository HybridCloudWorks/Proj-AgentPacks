---
name: review-kubernetes-packaging
description: Review Kubernetes manifests, Custom Resources, Helm charts and values, Kustomize bases and overlays, operators, GitOps configuration, and related deployment pipelines for cluster and namespace targeting, field ownership, rollout, security, resources, storage, rendering, and prune behavior. Use when a PR changes Kubernetes YAML, Chart.yaml, values files, templates, kustomization files, CRDs, or GitOps applications.
---

# Objective

Determine whether rendered resources target the intended cluster and namespace, preserve ownership and selectors, roll out safely, enforce least privilege, and remain operable under upgrade and failure.

## Inputs

- Cluster context, namespace, release or application identity, field manager, GitOps/controller ownership, prune behavior, and deployment command.
- Workloads, services, selectors, probes, disruption budgets, security context, RBAC, networking, resources, storage, charts, values, bases, overlays, and dependencies.
- Rendered output, schemas, policy/admission results, server-side dry-run, diff, or GitOps preview for representative existing state.

## Workflow

1. Establish cluster, context, namespace, release/application identity, field manager, controllers, prune behavior, and cluster-scoped impact.
2. Review resource renames, namespace or release changes, field ownership, selector stability, Service-to-workload labels, workload strategy, jobs, and stateful storage.
3. Review readiness/liveness/startup probes, termination, disruption budgets, surge/unavailable settings, capacity, topology, scheduling, and availability during replacement.
4. Review service accounts, RBAC, privilege escalation, capabilities, host access, network exposure, secret handling, image source/digest policy, and admission controls.
5. Review requests, limits, autoscaling, volumes, storage class, reclaim behavior, ports, DNS, and rollout triggers for ConfigMap or Secret changes.
6. For Helm, review values schema/types/defaults, release identity, hooks, CRDs, dependencies, cluster-dependent lookups, and rendered output for every affected values set.
7. For Kustomize, review base/overlay resolution, patch targets, transforms, selectors, generated names, image substitutions, secret generation, and remote-base pinning.
8. Return confirmed findings and evidence gaps to `review-infrastructure-pr`.

## Decision Rules

- A successful render proves template generation, not API admission or safe upgrade behavior.
- Client-side validation may not understand CRDs or admission-controller behavior.
- Selector, release, namespace, or ownership changes require explicit existing-environment analysis.
- Do not contact or mutate a privileged cluster solely to complete review.

## Output Contract

Return technology-specific findings and evidence gaps to `review-infrastructure-pr` with an anchor, trigger, affected target, impact, remediation, and verification evidence. Do not repeat universal gates or create another final report.

## Validation and Stop Conditions

Use `references/review-checklist.md`; verify uncertain semantics through `references/official-sources.md`. Stop when decisive target state, identity, versions, generated output, or safe access is unavailable. Never mutate targets or expose sensitive values.

## Resources

- Read `references/review-checklist.md` for the complete technology adapter.
- Read `references/official-sources.md` when behavior is version-specific, uncertain, or current verification is required.
