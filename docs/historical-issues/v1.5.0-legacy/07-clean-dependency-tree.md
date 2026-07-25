# Remove bundled virtual environment and duplicate libraries

**Suggested labels:** build, dependencies, legacy  
**Status:** Resolved in 2.1.0

## Context

The legacy `lib/` contains a virtual environment, duplicate versions, bytecode, native extensions, and executables.

## Acceptance criteria

- Clean deterministic dependency installation.
- No duplicates, native files, or compiled bytecode in the release.

## Resolution

UCC cleaned the build in 2.0.0; exact hash locks and rejection checks were added in 2.1.0.
