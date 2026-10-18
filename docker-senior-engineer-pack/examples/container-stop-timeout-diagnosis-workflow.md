# Worked example: exit 137 on every deploy, without an OOM kill

Synthetic scenario for the `diagnose-container-issue` prompt and the container-runtime-operations skill. The request is diagnose-only.

## Symptom

A queue worker on a single Compose host shows exit code 137 after each deploy, and a few jobs are processed twice. The team suspects memory.

## Engine and evidence

`docker context show` names a remote context for the shared host. The user has authorised read-only inspection of that host for this investigation, so the evidence below is Level 0 on an authorised engine; nothing is changed there.

- `docker inspect --format '{{.State.ExitCode}} {{.State.OOMKilled}} {{.State.FinishedAt}}' worker-1`: `137 false`, at the deploy time.
- `docker events --since <deploy time> --filter container=worker-1`: `kill` with signal 15, then `kill` with signal 9 ten seconds later, then `die`.
- `docker inspect --format '{{json .Config.Entrypoint}} {{json .Config.Cmd}}'`: shell form, so `/bin/sh -c` is PID 1.
- Logs (summarised, not pasted): no shutdown message from the worker.

## Diagnosis

Not memory: `OOMKilled` is false and the events show SIGTERM followed by SIGKILL after the default 10-second stop timeout. The shell is PID 1 and does not forward SIGTERM, so the worker never starts its graceful shutdown, is killed mid-job, and the job is redelivered. Ruled out: memory limit (no OOM flag, `docker stats` well under the limit), restart policy (the kills come from `compose up` recreating the container).

## Proposed fix (not applied)

- Exec-form `ENTRYPOINT`, or `exec` in the wrapper script, so the worker is PID 1 and receives SIGTERM.
- `init: true` because the worker spawns child processes.
- `stop_grace_period` longer than the longest job's drain time.
- Make job handling idempotent so a forced kill cannot double-process.

## Verification plan

Locally at Level 1: run the fixed image under a task name, start a long synthetic job, `docker stop`, and confirm a shutdown log line and exit 0 or 143 within the grace period. On the shared host the deploy itself is Level 2 and belongs to the owners.

## Report

Status ANALYSIS_ONLY: cause confirmed from events and configuration, fix proposed, nothing changed on the host.
