# Sort mapping keys numerically

**Suggested labels:** bug, templates  
**Status:** Resolved in 2.1.0

## Context

Lexical sorting places `map.10` before `map.2`.

## Acceptance criteria

- Numeric mapping order is stable.
- Regression test covers two-digit keys.

## Resolution

A numeric mapping sort key was added.
