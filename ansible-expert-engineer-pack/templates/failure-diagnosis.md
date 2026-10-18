# Failure diagnosis

Produced by the `ansible-debug-runtime-failures` skill. Redact credentials, private keys, vault passwords and secret task output before pasting anything here.

## Symptom

- Command run:
- Failing hosts, and hosts that did not fail:
- Error excerpt (mark it as abridged if shortened):

```text
```

## Environment

| Item | Value | Source |
|---|---|---|
| Ansible package and `ansible-core` | | `ansible --version` |
| Config file in use | | `ansible --version` |
| Controller Python | | |
| Inventory source | | |
| Target OS and Python | | |
| Recent change | | upgrade, inventory edit, credential change, rebuild |

## Classification

Tick the first layer that fails, following the skill's triage order:

- [ ] Parse or configuration
- [ ] Inventory or host selection
- [ ] Connection
- [ ] Authentication or become
- [ ] Module or collection
- [ ] Templating or variables
- [ ] Runtime semantics (registered results, handlers, delegation, loops)
- [ ] Performance

## Reduction

The smallest scope that still fails: one host, one play, one task. Record the commands used to narrow it (`--limit`, `--start-at-task`, `--list-tasks`, verbosity level).

## Findings

| Kind | Statement | Evidence |
|---|---|---|
| Confirmed cause | | |
| Contributing factor | | |
| Hypothesis | | what would confirm or refute it |
| Missing evidence | | who or what can supply it |

## Version drift

Porting guides consulted, the release that changed the behavior, and the supported migration path. "Not applicable" if no upgrade is involved.

## Smallest safe reproduction

The command, where it runs (local fixture, localhost, approved host), and exactly what it may change.

## Fix

- Proposed or applied change:
- Alternatives rejected, and why:
- Similar latent defects found:

## Verification

Checks that prove the fix, which of them ran, and what still needs a real run on an approved host.
