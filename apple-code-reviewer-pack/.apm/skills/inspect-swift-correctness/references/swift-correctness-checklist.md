# Swift Correctness Checklist

## Types, Optionals, and Boundaries

- Forced unwraps, casts, and `try!` on user, network, persistence, decoding, lifecycle, or timing-dependent data.
- Defaults that conceal missing required state or convert an error into plausible wrong output.
- Integer overflow, lossy numeric conversion, date, locale, calendar, time-zone, Unicode, and floating-point assumptions.
- Invalid collection indices, mutation during iteration, unstable ordering, duplicate processing, and empty-sequence behavior.
- String indexing by integer or assumptions that user-visible characters equal Unicode scalar or UTF storage length.

## State and Control Flow

- Impossible or incomplete enum states, partially initialized models, stale derived state, and invalid transition order.
- Early returns, `defer`, cleanup, and rollback behavior on every failure path.
- Idempotency and repeated callback, notification, scene, retry, and task execution.
- Lost updates, write-after-read races, duplicate side effects, and inconsistent persistence boundaries.

## Errors

- Swallowed errors, broad catches, misleading fallbacks, discarded underlying causes, and success values after failure.
- Error translation that loses actionable context or leaks sensitive implementation detail.
- Recovery that retries non-idempotent operations or changes user-visible state twice.

## ARC and Lifetime

- Strong closure capture cycles, especially owner -> closure or task -> owner -> task.
- Delegate or callback ownership that outlives the intended component.
- Notification, observation, timer, display-link, Combine, async-sequence, and task cancellation or invalidation.
- `unowned` assumptions that are not guaranteed by lifetime structure.
- Escaping closures retaining large graphs or UI objects longer than needed.

## Swift Concurrency

- Mutable state crossing isolation without an actor, lock, atomic, or immutable transfer.
- Incorrect or missing `Sendable` conformance and unsafe `@unchecked Sendable` justification.
- Main-actor work that performs blocking I/O, parsing, image processing, or large computation.
- UI state accessed outside the required isolation domain.
- Unstructured `Task` use where child-task cancellation, priority, or lifetime should be inherited.
- Detached tasks that capture non-sendable state or lose task-local values and cancellation.
- Missing cancellation checks in long loops, network pipelines, or multi-stage operations.
- Actor reentrancy across `await` where assumptions about state no longer hold.
- Continuations resumed zero, two, or multiple times; continuations retained indefinitely.
- Async streams that never finish, leak producers, or ignore termination handlers.
- Task groups that do not bound work, consume child results, or handle first failure intentionally.

## API and Protocol Design

- Evaluate clarity at the call site and prefer clarity over brevity.
- Names describe effects, mutability, and returned values consistently.
- Boolean arguments are readable at use sites.
- Protocol requirements represent coherent capability rather than implementation detail.
- Public APIs preserve source and binary compatibility appropriate to the repository.
- Generic constraints, associated types, existentials, and type erasure do not erase required guarantees.

## Interoperability and Unsafe Code

- Nullability, ownership, selector, KVO/KVC, dynamic dispatch, and exception assumptions at Objective-C boundaries.
- Pointer lifetime, alignment, binding, capacity, and buffer bounds.
- C callback context ownership and thread-affinity requirements.
- Bridged collection mutability and Foundation value semantics.

## Persistence and Data Integrity

- Schema compatibility, migration, uniqueness, ordering, transaction boundaries, and conflict resolution.
- Main-context or actor confinement for Core Data or SwiftData models.
- Partial saves, rollback, stale objects, deleted-object access, and cross-context identity.
- Codable compatibility, unknown values, missing keys, and forward or backward data evolution.
