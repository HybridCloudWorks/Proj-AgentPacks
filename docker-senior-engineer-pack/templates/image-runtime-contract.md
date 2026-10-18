# Image runtime contract

What an image promises to whoever runs it: Compose, an orchestrator, a cloud container service or a developer. Fill it in when containerising an application and hand it to the owners of the runtime platform; update it whenever a change alters any line, and say so in the completion report.

| Item | Value | Notes |
|---|---|---|
| Image repository and tag scheme | | Deploy by digest |
| Platforms | | For example linux/amd64, linux/arm64 |
| Process and arguments | | Exec form; PID 1 or init |
| Listening ports and protocol | | Bound to all interfaces inside the container |
| User and UID/GID | | Numeric, non-root |
| Writable paths | | Volumes or tmpfs; root filesystem read-only if possible |
| Persistent data | | Named volumes or external storage, and who backs it up |
| Configuration inputs | | Environment variables and files, with required and default values |
| Secrets | | Source at runtime (files under /run/secrets or the platform's secret store); never baked into the image |
| Health | | Endpoint or command; which consumer probes it; start-up time |
| Stop behaviour | | Stop signal, drain time, grace period to configure |
| Resources | | Measured memory and CPU at idle and under expected load; heap sizing from limits |
| Capabilities and privileges | | Expected to run with all capabilities dropped and no-new-privileges unless listed here |
| Outbound dependencies | | Services, ports and DNS names it must reach |
| Logs and metrics | | stdout and stderr format; metrics endpoint if any |
| Provenance | | Source repository, revision label, SBOM and signature locations |
