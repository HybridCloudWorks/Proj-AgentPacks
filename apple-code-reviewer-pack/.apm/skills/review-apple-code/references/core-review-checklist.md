# Core Review Checklist

## Scope

Record:

- Files, symbols, modules, targets, packages, services, extensions, and workflows in scope.
- Languages, frameworks, runtime, build system, and major dependencies.
- Change type: pull request, feature, bug fix, refactor, security, performance, or audit.
- User goals, supported platforms, deployment targets, and constraints.
- Evidence available and evidence that cannot be obtained.

Do not begin detailed findings until the boundary is clear.

## Architecture

Evaluate:

- Role of changed code in the larger system.
- Dependency direction, ownership, coupling, cohesion, and layer placement.
- Existing repository patterns and explicit architecture decisions.
- New hidden dependencies, duplicated responsibilities, or architectural drift.
- Whether state, business logic, UI logic, persistence, and external integration live in appropriate owners.

Record a finding only when the change creates a material correctness, security, operability, testability, or change-safety risk.

## Code Quality

Evaluate:

- Names at the point of use, not declarations alone.
- Unit size, branching, nesting, separation of concerns, and hidden side effects.
- Duplicated logic and inappropriate or missing abstractions.
- Dead or unused code introduced or exposed by the change.
- Comments that contradict behavior or explain mechanics instead of intent.
- Consistency with nearby conventions when those conventions are safe.
- Ability to test and modify the code without broad unrelated changes.

Avoid style-only findings unless the style issue obscures behavior, creates misuse risk, or materially raises maintenance cost.

## Evidence

Valid evidence includes source, tests, configuration, build scripts, dependency locks, CI output, logs, crash reports, performance traces, user-provided context, and current official documentation.

For a potential defect, state the missing experiment or evidence that would confirm or reject it.

## Dot-Prefixed Folders

Folders such as `.claude/`, `.cursor/`, `.windsurf/`, `.github/`, `.vscode/`, `.devcontainer/`, `.azure/`, `.config/`, `.codex/`, and `.gemini/` are excluded from broad documentation churn.

Inspect one only when:

1. The request targets it.
2. Reviewed code directly depends on it.
3. The change cannot be evaluated without it.
4. It contains a real CI, release, secret-handling, security, or supply-chain defect relevant to the change.

Exclusion never protects broken infrastructure. Inspect the minimum necessary files and do not generalize a local defect into a repository reorganization proposal.
