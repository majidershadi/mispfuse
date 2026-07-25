# Known issues — 1.5.0 legacy

This release is not maintained.

## Critical

- API key stored in plaintext in `bin/keys.py`.
- TLS verification disabled.
- Private hostname included in source.
- MISP organisation IDs hard-coded.
- Events published by default.
- Original dependency tree contains stale, duplicate, compiled, and
  platform-specific packages.

## High

- One MISP event is created for every Splunk result row.
- Only one attribute is added to each event.
- Mapping is designed around `Network activity` and `ip-src`.
- `publish` parsing treats any non-empty string as true.
- No exception handling around MISP connection or event creation.
- No MISP response validation.

## Medium

- No alert action or scheduler integration.
- No multi-account support.
- No proxy or logging configuration.
- App is hidden from the Splunk app bar.
- Result field is misspelled `resualt`.
- Hard-coded tag and event defaults are environment-specific.

All design issues are addressed by later stages rather than patched in this
historical branch.
