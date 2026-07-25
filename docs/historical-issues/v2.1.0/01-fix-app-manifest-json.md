# Fix malformed app.manifest author email

**Suggested labels:** release-blocker, bug  
**Status:** Open

## Context

The uploaded final source has an unquoted email value in `package/app.manifest`, so the JSON is invalid.

## Acceptance criteria

- `python -m json.tool package/app.manifest` succeeds.
- Publisher details are consistent with `app.conf` and GitHub.
- Full release workflow passes.
