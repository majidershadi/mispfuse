# Add dry-run event preview

**Suggested labels:** ux, enhancement  
**Status:** Proposed

## Context

Users cannot inspect the final MISP payload before creating an event.

## Acceptance criteria

- Command and alert test mode produces payload summary without POST.
- Secrets are never included.
- Taxonomy validation still runs.
