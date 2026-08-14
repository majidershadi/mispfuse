# MISPFuse 2.2.3 — Splunk 9.0 compatibility correction

MISPFuse 2.2.3 fixes the AppInspect SLIM rejection that remained in v2.2.2.
The online validator reported that `>=9.3.0` did not include a recognized
Splunk Enterprise version and required a range including 9.0.0.

## What was fixed

- Changed the manifest requirement from `>=9.3.0` to the full semantic-version
  constraint `>=9.0.0`.
- Added real Python 3.7 compatibility for Splunk 9.0 through 9.2; this is not a
  manifest-only downgrade.
- Changed generated legacy extension points to `python.version = python3`.
- Kept `python.required = 3.9, 3.13` for newer Splunk releases.
- Downgraded only the incompatible transitive pin, `packaging` 26.3, to
  hash-locked `packaging` 23.2.
- Added Python 3.7 unit, dependency-install, and syntax validation alongside
  the existing Python 3.9 and 3.13 release gates.

## Preserved behavior

The MISP client, encrypted account storage, save-time connection test,
templates, custom SPL command, scheduled alert action, TLS defaults, response
limits, and exact dependency locking are unchanged.

## Release artifact

`mispfuse-2.2.3.tar.gz`

Verify the SHA-256 checksum before uploading or installing the package.
