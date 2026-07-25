# Apply Python 3.13 to generated REST handlers

**Suggested labels:** runtime, python, ucc  
**Status:** Resolved in 2.1.0

## Context

The post-build patch covers commands and alert actions but not UCC REST handlers.

## Acceptance criteria

- Commands, alert actions, and REST handlers all declare Python 3.13.
- Packaging fails if any declaration is missing.

## Resolution

`meta.supportedPythonVersion` and a post-build verifier were added.
