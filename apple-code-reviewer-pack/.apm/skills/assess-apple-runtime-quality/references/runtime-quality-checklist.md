# Runtime Quality Checklist

## Responsiveness and Rendering

- Synchronous network, file, database, image decode, compression, parsing, or large computation on the main actor.
- SwiftUI invalidation caused by overly broad observable state or unstable identity.
- Repeated layout, diffing, formatting, sorting, filtering, or image work in frequently evaluated UI paths.
- Large lists without lazy loading, pagination, stable IDs, or bounded prefetching.
- Animations or transitions that trigger expensive work or ignore reduced-motion settings.

## CPU, Memory, and Resources

- Unbounded arrays, caches, histories, logs, queues, task creation, or buffered streams.
- Retained controllers, views, models, tasks, observers, timers, subscriptions, or image buffers.
- File handles, sockets, streams, database transactions, security-scoped resources, or background tasks not ended on every path.
- Large-value copying, repeated bridging, serialization, or decoding on hot paths.
- Cache keys, eviction, invalidation, and memory-warning behavior.

## Network and Persistence

- N+1 network or database operations, chatty request patterns, missing batching, and redundant refresh.
- Missing pagination, range requests, conditional requests, compression, or deduplication where scale supports it.
- Writes on every keystroke or state update without debounce, transaction, or coalescing.
- Fetches or observers that return more data than the UI consumes.
- Offline, slow, intermittent, metered, and background-transfer behavior.

## Energy and Background Work

- Excessive timers, polling, location accuracy, sensor use, wakeups, animation, network reconnect, or background refresh.
- Background work that ignores expiration, cancellation, or permitted execution windows.
- Retry loops without caps, jitter, backoff, reachability awareness, or idempotency.
- Work that continues after the screen, scene, account, or task is no longer relevant.

## Errors and Recovery

- Errors swallowed, converted into empty success, or logged without useful context.
- Retry of non-idempotent operations or retry storms across layers.
- User messages that are vague, expose internals, or provide no recovery path.
- Fallbacks that hide stale, partial, or invalid data.
- Cancellation treated as an error when it is expected control flow, or real failure mistaken for cancellation.

## Observability

- Important failures lack stable event names, safe context, correlation, or outcome.
- Logs include sensitive values or produce high-volume noise on hot paths.
- Use appropriate privacy annotations with unified logging.
- Signposts and metrics measure user-relevant latency or resource use when diagnostics justify them.
- Crash and assertion strategy preserves evidence without crashing on recoverable external input.
