---
description: "Bake files and CI steps that build, cache, attest, sign or push container images: immutable tags, safe cache export, digest-based signing, least-privilege publishing."
applyTo: "**/docker-bake.hcl,**/docker-bake.json,**/docker-bake.*.hcl,**/.github/workflows/*.yml,**/.github/workflows/*.yaml,**/.gitlab-ci.yml,**/azure-pipelines.yml"
---

# Image build instructions

Apply this only where the file builds, tags, caches, attests, signs or pushes container images; otherwise ignore it. Follow image-build-and-supply-chain.

Tag each build immutably (for example by commit) and treat moving tags as conveniences; deploy and sign by digest. Remember that registry cache export with `mode=max` publishes every intermediate stage and that `mode=max` provenance records build-argument values, so no stage or argument may carry a secret. Pin third-party CI actions or templates to an immutable reference, grant write access to the registry only in the job that pushes, never push or expose registry credentials on builds of untrusted pull requests, and prefer short-lived identity-based credentials. Render Bake with `docker buildx bake --print` before running it. Editing these files is local work; merging, publishing, pushing, signing and registry setting changes are Level 2 under the `docker-senior-engineer-contract` instruction.
