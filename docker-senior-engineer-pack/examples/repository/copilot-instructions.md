# Container review instructions

Optional repository-level instructions for GitHub Copilot code review on GitHub.com. Copy to `.github/copilot-instructions.md` in a repository that wants them. The pack does not need this file; it works from its installed instructions in every client.

When reviewing Dockerfiles, ignore files, Compose files, Bake files or CI steps that build images:

- Flag base images on `latest` or a bare major version; recommend a specific version and a digest where builds must be reproducible.
- Flag credentials in `ARG`, `ENV`, labels or copied files in any stage, and registry cache exports with `mode=max` that could publish them. Never quote a secret value; give its location.
- Flag runtime stages without a numeric non-root `USER`, shell-form `ENTRYPOINT`/`CMD`, toolchains or source copied into the runtime stage, and `COPY . .` without an ignore file.
- In Compose, flag the obsolete `version` key, `privileged`, host namespaces, Docker socket mounts, unconfined security profiles, literal secrets in `environment`, databases published on all interfaces, and `depends_on` conditions without a healthcheck.
- In CI, flag unpinned third-party actions, registry write permissions outside the pushing job, pushes reachable from untrusted pull requests, and signing by tag instead of digest.
- Give each finding a severity (Blocker, High, Medium, Low, Suggestion, Question), the location, the evidence, the impact, a recommended change and whether it blocks merging. Do not report checks you did not run as passed.
