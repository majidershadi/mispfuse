# Prevent duplicate MISP events on repeated searches

**Suggested labels:** reliability, enhancement  
**Status:** Proposed

## Context

Repeated command or alert execution can create duplicate events.

## Acceptance criteria

- Deterministic idempotency strategy.
- Configurable duplicate window.
- Clear result when an event is reused or skipped.
