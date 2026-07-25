# Shorten UCC custom-command syntax metadata

**Suggested labels:** build, ucc  
**Status:** Resolved in 2.1.0

## Context

The original syntax description exceeds the UCC schema length limit and blocks the build.

## Acceptance criteria

- `globalConfig.json` validates under the pinned UCC version.
- Full arguments remain declared separately.

## Resolution

The displayed syntax was shortened while preserving the argument definitions.
