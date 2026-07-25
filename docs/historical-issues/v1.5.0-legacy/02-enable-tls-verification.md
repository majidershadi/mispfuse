# Enable TLS certificate verification by default

**Suggested labels:** security, legacy  
**Status:** Resolved in 2.0.0

## Context

The legacy key file sets certificate verification to false.

## Acceptance criteria

- Verification defaults to enabled.
- Insecure mode is explicit and documented as lab-only.

## Resolution

The UCC account model defaults verification to enabled.
