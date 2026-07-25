# Validate MISP responses and return useful status

**Suggested labels:** bug, error-handling, legacy  
**Status:** Resolved in 2.0.0/2.1.0

## Context

The PyMISP result is assigned but not validated; the command always writes a success-like field.

## Acceptance criteria

- Transport and API failures return explicit status.
- Created event ID and UUID are surfaced.

## Resolution

Structured result rows arrived in 2.0.0; direct response validation was hardened in 2.1.0.
