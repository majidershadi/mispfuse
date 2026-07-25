# Remove environment-specific MISP organisation IDs

**Suggested labels:** bug, portability, legacy  
**Status:** Resolved in 2.0.0

## Context

Event organisation IDs are fixed to one environment.

## Acceptance criteria

- No organisation ID is hard-coded.
- MISP derives the organisation from the authenticated API user.

## Resolution

The template-based pusher removed `org_id` and `orgc_id` assignments.
