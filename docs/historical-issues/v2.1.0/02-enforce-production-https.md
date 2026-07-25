# Add production HTTPS and custom-CA policy

**Suggested labels:** security, enhancement  
**Status:** Proposed

## Context

The current account model permits HTTP and disabled certificate verification for labs.

## Acceptance criteria

- Optional production mode rejects HTTP.
- Custom CA bundle can be selected safely.
- Cloud implications are documented and tested.
