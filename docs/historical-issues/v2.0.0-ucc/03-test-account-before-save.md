# Test MISP account before saving

**Suggested labels:** configuration, reliability  
**Status:** Resolved in 2.1.0

## Context

The UCC form validates field shape but not real authentication or taxonomy access.

## Acceptance criteria

- Create/edit authenticates, reads user/version, and fetches taxonomy.
- Failed tests do not save the stanza.

## Resolution

A custom account REST handler performs the connection test.
