---
applyTo: "**/*.py,**/Dockerfile,**/.github/workflows/**"
---

# python-security instructions

Review identity, authorization/tenant scope, untrusted input/output, query/subprocess/path/URL handling, secrets, unsafe deserialization, dependencies/builds and retention. Follow secure-python-engineering for substantiated findings. Keep tokens/cookies/source/personal data out of diagnostic artifacts by default. Review-only assignments remain read-only. Honor scoped existing authorization; request missing authority only for the consequential action, with exact target/effect/risk/cost/recovery.
