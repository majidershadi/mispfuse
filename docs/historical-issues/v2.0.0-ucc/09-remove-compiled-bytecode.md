# Remove committed and generated compiled Python

**Suggested labels:** build, appinspect  
**Status:** Resolved in 2.1.0

## Context

The milestone source contains `.pyc` files and tests can recreate them before packaging.

## Acceptance criteria

- Tests disable bytecode writing.
- Build purges bytecode.
- Release gate rejects bytecode.

## Resolution

The final Makefile and post-build verifier enforce this.
