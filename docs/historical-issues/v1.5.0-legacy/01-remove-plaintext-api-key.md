# Remove plaintext MISP API key

**Suggested labels:** security, critical, legacy  
**Status:** Resolved in 2.0.0

## Context

The legacy command imports the MISP URL and API key from `bin/keys.py`, which is included in the app source.

## Acceptance criteria

- No secret is committed.
- The exposed key is revoked.
- Runtime configuration uses Splunk credential storage.

## Resolution

UCC encrypted account fields replaced `keys.py` in 2.0.0.
