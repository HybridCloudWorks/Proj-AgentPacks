# Apple Build and Test Matrix

Run commands only when their prerequisites exist. Prefer repository-provided scripts and CI commands over invented command lines.

## Capability Detection

Always run the bundled detector first. Record OS, architecture, `xcodebuild`, `swift`, project or workspace files, package manifests, dependency files, test directories, and CI files.

## Xcode Project or Workspace on macOS

Candidate read-only discovery:

```bash
xcodebuild -list -json -project <project>.xcodeproj
xcodebuild -list -json -workspace <workspace>.xcworkspace
xcodebuild -showBuildSettings -json -scheme <scheme> -project <project>.xcodeproj
```

Candidate validation when repository instructions identify a scheme and destination:

```bash
xcodebuild build -scheme <scheme> -destination '<approved destination>'
xcodebuild test -scheme <scheme> -destination '<approved destination>'
```

Do not guess schemes, destinations, signing flags, or workspace selection when multiple options exist. Use `CODE_SIGNING_ALLOWED=NO` only when repository practice supports it and the target can build without signing.

## Swift Package

When a compatible Swift toolchain exists:

```bash
swift package describe
swift package resolve --skip-update
swift build
swift test
```

Do not resolve or update dependencies if doing so would modify `Package.resolved`. Compare the tree before and after any command.

## Dependency Systems

Inspect, but do not mutate without approval:

- SwiftPM: `Package.swift`, `Package.resolved`, binary targets, plugins, source URLs, version requirements.
- CocoaPods: `Podfile`, `Podfile.lock`, local podspecs, script phases, and generated workspace assumptions.
- Carthage: `Cartfile`, `Cartfile.resolved`, binary frameworks, and build scripts.
- Tuist or XcodeGen: manifest and generated-project reproducibility.
- Bundler and fastlane: `Gemfile.lock`, lanes, actions, signing and release assumptions.

## Test Coverage by Risk

- Unit: deterministic logic, state transitions, parsing, formatting, errors, cancellation.
- Integration: persistence, network adapters, dependencies, migrations, app extensions, notifications.
- UI: critical user paths, navigation, error recovery, permissions, account state.
- Accessibility: semantic queries, Dynamic Type, focus and state announcements where risk warrants.
- Concurrency: cancellation, ordering, isolation boundaries, repeated invocation, races with deterministic controls.
- Security: authorization, invalid input, deep links, sensitive logging, denied permissions.
- Performance: explicit requirements, regression baselines, large datasets, memory or launch metrics.

Tests should assert observable behavior and avoid brittle timing, ordering, locale, device, or environment assumptions.

## CI Review

Verify:

- Required jobs and branch protections actually cover the changed targets and configurations.
- macOS image and Xcode selection match project requirements.
- Dependency caches cannot mask missing lockfiles or stale generated artifacts.
- Secrets are referenced, not printed.
- Cancelled, timed out, skipped, neutral, or allowed-to-fail jobs are understood.
- Test result bundles, coverage, archives, and logs are retained when needed for release evidence.
