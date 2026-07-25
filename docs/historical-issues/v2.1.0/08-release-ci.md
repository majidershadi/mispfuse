# Automate release validation in CI

**Suggested labels:** build, release  
**Status:** Proposed

## Context

The release workflow is currently maintainer-driven.

## Acceptance criteria

- Tests, UCC build, JSON validation, AppInspect, checksum, and SBOM steps.
- Artifacts retained from the same job.
- No secret-bearing integration data in logs.
