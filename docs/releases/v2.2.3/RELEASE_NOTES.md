# MISPFuse 2.2.3

MISPFuse 2.2.3 fixes the remaining Splunkbase SLIM validation failure by
supporting the validator's accepted Splunk Enterprise 9.0.0 boundary.

## Fixed

- Changed `platformRequirements.splunk.Enterprise` from `>=9.3.0` to
  `>=9.0.0` using full semantic versioning.
- Added genuine Python 3.7 compatibility for Splunk 9.0 through 9.2 instead of
  lowering the manifest alone.
- Replaced `packaging` 26.3 with hash-locked `packaging` 23.2, allowing the
  complete pure-Python dependency closure to install on Python 3.7.
- Restored the generated legacy selector to `python.version = python3` for
  commands, alert actions, and REST handlers.

## Retained

- `python.required = 3.9, 3.13` on platforms that support the modern selector.
- Encrypted credentials, save-time MISP validation, templates, the SPL
  command, alert action, and hardened HTTP behavior.
- Exact dependency pins, SHA-256 hashes, and checks rejecting native binaries
  and compiled Python files.

## Validation

- Unit tests on Python 3.7, 3.9, and 3.13.
- Python 3.7 grammar check for all shipped Python modules.
- UCC 6.5.3 build and packaging checks.
- Splunk AppInspect 4.3.0 precert validation with cloud tags.
