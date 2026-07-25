# Allow alert fields to inherit template defaults

**Suggested labels:** bug, ui, templates  
**Status:** Resolved in 2.1.0

## Context

Concrete alert-form defaults silently replace the selected template values.

## Acceptance criteria

- Every optional override has a Use-template/blank state.
- Blank values reach the pusher as `None`.

## Resolution

Tri-state and blank options were added.
