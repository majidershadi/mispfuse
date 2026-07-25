# Lock the complete runtime dependency closure

**Suggested labels:** dependencies, supply-chain  
**Status:** Resolved in 2.1.0

## Context

Bare package names make builds non-reproducible and can introduce native wheels.

## Acceptance criteria

- Exact versions and hashes.
- Pure-Python wheels only.
- Native-file release gate.

## Resolution

2.1.0 replaced PyMISP with a small client and hash-locked the UCC runtime closure.
