# Google Cloud review guidance

Optional repository-level file for GitHub Copilot code review. Copy it to `.github/copilot-instructions.md` in a repository that holds Google Cloud infrastructure code. It does not depend on the agent pack being installed.

When reviewing changes to Terraform, OpenTofu, gcloud scripts or Kubernetes manifests for Google Cloud:

- Flag deletes or replacements of stateful resources (databases, buckets, disks, clusters, keys, projects) and any `deletion_protection = false` on them.
- Flag authoritative IAM policy resources (`google_project_iam_policy`, `google_folder_iam_policy`, `google_organization_iam_policy`), basic roles, `allUsers` or `allAuthenticatedUsers` members and `google_service_account_key` resources.
- Flag firewall rules with `0.0.0.0/0` sources, public IPs on databases or VMs, and Cloud Run services whose ingress allows all traffic without a stated reason.
- Flag unpinned providers or modules, missing labels, secrets in variables or outputs, and resource locations that conflict with the repository's residency requirements.
- Flag scripts that mutate resources without explicit `--project` and location flags, that chain or pipe gcloud commands, or that print access tokens or secret values.

Explain the impact and propose the Google Cloud-native fix. Do not approve, merge or apply changes.
