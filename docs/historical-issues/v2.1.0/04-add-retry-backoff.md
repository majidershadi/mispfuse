# Add bounded retry and backoff

**Suggested labels:** reliability, enhancement  
**Status:** Proposed

## Context

The direct client disables retries; transient network or 5xx failures fail immediately.

## Acceptance criteria

- Retry only safe/transient cases.
- Bounded exponential backoff.
- No duplicate event creation after ambiguous POST failures.
