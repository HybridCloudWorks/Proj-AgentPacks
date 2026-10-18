---
description: "Python packaging and dependency changes: build backend, requires-python, lockfiles, package identity and transitive compatibility."
applyTo: "**/pyproject.toml,**/*requirements*.txt,**/uv.lock,**/poetry.lock,**/Pipfile*"
---

# python-packaging instructions

Follow python-packaging. Inspect backend, requires-python, extras/groups/indexes and lock workflow before changes. Verify package identity and transitive compatibility; do not invent package APIs or install commands. Generate locks with repository tooling, inspect distributions, check imports/builds/clean installs when affected, and preserve platform support. Artifact creation does not authorize publishing.
