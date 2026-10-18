# Worked example: shrinking a JVM image and its CI build time

Synthetic scenario for the `optimize-image` prompt and the dockerfile-engineering and image-build-and-supply-chain skills. All numbers are illustrative, not measurements.

## Baseline

The single-stage Dockerfile uses a full JDK image, copies the whole repository, runs the Gradle build, and starts the jar. `docker image ls` reports roughly 900 MB; `docker history` shows the Gradle cache and source tree inside the image; every CI run downloads all dependencies because the runner is ephemeral and no cache is exported. The baseline is recorded with the engine version, builder and runner type, because numbers from different environments are not comparable.

## Changes, one at a time

1. Ignore file: excludes `.git`, `build/`, `.gradle/` and IDE folders. Context transfer drops; nothing else changes.
2. Stages: a JDK builder stage and a JRE runtime stage. The runtime keeps only the application and its dependencies.
3. Layer order: copy the Gradle wrapper, settings and build files first and resolve dependencies, then copy source. A source-only change now reuses the dependency layer.
4. Cache mount for the Gradle cache in the builder, so dependency downloads are not stored in any layer.
5. The framework's layered-jar extraction splits dependencies, loaders and application classes into separate `COPY` layers, so a code change ships a small layer instead of the whole jar.
6. CI cache export with `type=gha` scoped to the branch, so the ephemeral runner reuses layers between runs.
7. Heap sizing from the container limit with `-XX:MaxRAMPercentage` instead of a fixed `-Xmx`.

## Result and trade-offs

Before and after are measured with the same commands on the same runner type: image size, cold build, warm build after a one-line source change, and pull time on a clean host. The report states each number with its environment. Trade-offs recorded: the JRE image has no JDK diagnostic tools, so debugging uses a separate debug container; the branch-scoped cache costs CI cache storage; the runtime contract (port, user, entrypoint) is unchanged, so consumers need no change.

## Checks not run

Production start-up time and memory under real load were not measured; they are listed as unverified rather than inferred from the smaller image.
