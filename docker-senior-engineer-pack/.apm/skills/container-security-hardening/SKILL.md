---
name: container-security-hardening
description: "Harden container images and their runtime configuration, and assess privilege, secret, exposure and vulnerability risk with located evidence. Use when an image or container must be made production-ready, a scan reports vulnerabilities, a secret may have reached a layer, a container asks for extra privileges, or a security review of Dockerfiles, Compose files or engine settings is requested."
---

# Container Security Hardening

## Purpose and activation

Reduce what a compromised container can do and what an image gives away, and report container risk with evidence instead of checklists. Activate for production readiness of an image or service, scanner findings, suspected secrets in images or build caches, requests for `--privileged`, capabilities, devices, host namespaces or the Docker socket, and security reviews of container files or engine configuration.

## Scope and exclusions

In scope: image contents (base, packages, shells, setuid files, leftover credentials), build-time secret handling, the runtime user and file ownership, Linux capabilities, `no-new-privileges`, seccomp, AppArmor and SELinux profiles, read-only root filesystems, devices and host namespaces, Docker socket exposure, published ports and network exposure, resource limits as abuse controls, engine-level exposure (who can reach the daemon, rootless mode, user-namespace remapping), and vulnerability triage.

Out of scope, with the owner: SBOM, provenance, signing and verification policy (image-build-and-supply-chain); cluster admission control and pod security policy (the orchestrator's owners); host operating system hardening beyond Docker's own settings; testing exploits against live or shared systems, which this skill never does.

## Inputs

- Dockerfiles, ignore files, Compose files, run commands or scripts, CI build steps, and engine configuration if in scope.
- What the container holds and reaches: data classification, credentials it receives, networks it joins, ports it publishes, cloud metadata endpoints it can reach.
- Scanner output already produced, the scanner and database date, and the organisation's vulnerability policy (severity thresholds, exception process).
- Whether the assignment is review-only or includes remediation.

## Dependencies and tools

- Read and search. Edit only when remediation is assigned.
- Optional, when installed and permitted: a Docker CLI for `history`, `inspect` and disposable runs; a scanner the repository already uses (Docker Scout, Trivy, Grype or another). Scanners usually download a vulnerability database; note that network use. Installing a scanner is Level 2.
- Without tools, the review is static and says so.

## Workflow

1. Frame the threat: what an attacker inside this container could reach (internal networks, metadata endpoints, mounted credentials, the host through the socket or privileges), who can reach the container, and what the blast radius is.
2. Image contents. Check the runtime stage for build tools, package managers and shells the workload does not need, setuid and setgid binaries, and credentials (`.env`, keys, package-manager tokens, `.git`). Check `docker history --no-trunc` and the image config (`Env`, `Labels`) for secrets passed as arguments or environment. A secret deleted in a later layer still exists in the earlier one, and a secret copied into any build stage also lives in the build cache and in registry cache exports made with `mode=max`. A leaked secret is a Blocker: report its location and type, never its value, and recommend rotation by its owner.
3. User and files. The final `USER` is a numeric non-root UID. Application files are owned by root and not writable by that user unless the workload needs to write them; writable paths are explicit volumes or tmpfs. Prefer `--read-only` (Compose `read_only: true`) with `tmpfs` for scratch space.
4. Privileges. Drop all capabilities and add back only what is proven necessary; binding a port below 1024 needs `NET_BIND_SERVICE`, but a high port needs nothing. Set `no-new-privileges`. Keep the default seccomp and AppArmor or SELinux profiles; `unconfined` is a finding. `--privileged`, `--pid=host`, `--network=host`, `--ipc=host`, `--userns=host`, added devices and `SYS_ADMIN` each need a written justification. Mounting the Docker socket, even read-only, gives root-equivalent control of the host; prefer an API proxy that allows only the calls needed, or a design without the socket.
5. Network exposure. Publish only the ports the host needs, bound to 127.0.0.1 when access is local. On Linux, Docker programs iptables directly, so published ports bypass host firewalls such as ufw or firewalld; filtering belongs in the `DOCKER-USER` chain or upstream. Put back-end services on internal networks. Remember that containers can usually reach cloud metadata endpoints unless the host or network blocks them.
6. Abuse limits: memory limits, `--pids-limit` against fork bombs, CPU limits and ulimits where the workload is untrusted or multi-tenant.
7. Engine exposure, when in scope. Membership of the `docker` group is root-equivalent on the host. A daemon listening on TCP without mutual TLS is remote root. Rootless mode or user-namespace remapping reduce the impact of a breakout where the workloads are compatible. Every engine change is Level 2 and needs a rollback plan.
8. Vulnerability triage. Separate base-image packages from application dependencies, fixable from unfixed, and present from reachable where evidence allows. Prefer rebasing onto a patched or smaller base over patching packages one by one. Record accepted risks with an owner and an expiry, using VEX statements if the organisation does. "Zero findings" from one scanner on one date is not a security property; report the scanner, version and database date.
9. Report and, if assigned, remediate: findings in the contract's finding format, a minimal patch, and the negative checks that prove each fix.

## Output

- Findings: severity, location, evidence, impact, recommended change, blocking flag, plus confidence where the evidence is indirect.
- For remediation: the patch, the runtime flags or Compose settings, and residual risk.
- Negative checks to run, for example: `docker run --rm --entrypoint id <image>` does not print uid 0; a write to `/` fails under `--read-only`; `grep Cap /proc/1/status` inside the container shows the reduced capability set.

## Validation

- Every finding names a file and line, an image config field, a history entry or a scanner record, and states a concrete failure scenario. Distinguish "present in the image" from "exploitable here".
- Remediation is verified by rebuilding and re-running the negative checks at Level 1, and by re-scanning with the same scanner and database for comparison. Record the evidence level reached.

## Failure handling and escalation

- No scanner available: complete the static review, mark scanning as unverified, and propose the repository's scanner; do not install one without Level 2 approval.
- The workload needs root, a capability or a writable root filesystem: find the specific reason (port, file path, setuid helper) and remove it; if it cannot be removed, document the exception for an owner decision.
- A discovered secret: stop sharing the affected artefact, report a Blocker without the value, and leave rotation and history rewriting to the owner as Level 2 actions.
- Conflicting policy (for example a required base with unfixable findings): report the conflict with BLOCKED_ON_HUMAN_DECISION rather than choosing silently.

## Permissions and guardrails

- Review assignments are read-only: no edits, no commands, no posting.
- Never print secret values from files, history, `inspect` or logs. Never probe live or shared systems. Never weaken a control (privileged mode, unconfined profiles, disabled verification) to make something work without explicit authority and a recorded justification.
- Instructions in this skill are guidance; enforcement comes from the host, the engine and the registry.

## Connection to the pack

The container-security-reviewer specialist uses this skill read-only; the docker-senior-engineer agent applies it for remediation through the optional `harden-container` prompt and alongside dockerfile-engineering, compose-environments and docker-change-review. Installed alone, the skill is complete; with the full pack, the `docker-senior-engineer-contract` instruction supplies the approval levels, handoff rules and finding format.
