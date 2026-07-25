# Require a MISP type in the generic template

**Suggested labels:** bug, templates  
**Status:** Resolved in 2.1.0

## Context

The `passthrough` mapping leaves the type empty although event attribute creation requires it.

## Acceptance criteria

- Every mapping has a type.
- Invalid templates fail early.

## Resolution

The generic template now uses `text:Other`.
