# MISPFuse 2.2.1 — Splunk 9.x compatibility correction

MISPFuse 2.2.1 fixes the remaining Splunkbase SLIM range rejection for the
2.2 series. The package now truthfully includes Splunk Enterprise 9.4 in its
supported range without claiming compatibility with the Python 3.7 runtime in
older 9.x releases.

## Fixed

- Changed the Splunk Enterprise requirement from `>=10.0` to `>=9.4`, giving
  the Splunkbase validator the required 9.x intersection.
- Changed generated command, alert-action, and REST-handler selectors from
  `python.version = python3` to `python.version = python3.9`. Splunk 9.4 maps
  the former value to Python 3.7.
- Added a post-build regression check that normalizes and verifies every legacy
  selector after UCC generation.

## Runtime compatibility

- Splunk Enterprise 9.4 through 10.1: Python 3.9 selected explicitly.
- Splunk Enterprise 10.2 and later: Python 3.13 preferred, Python 3.9 fallback.
- Splunk SDK for Python 2.1.1 and the complete pure-Python runtime dependency
  closure remain exact-version and SHA-256 locked.

## Validation

- Unit tests on Python 3.9.25 and Python 3.13.14.
- Python 3.9 grammar validation for packaged source and the release verifier.
- UCC 6.5.3 build and packaging.
- AppInspect 4.3.0 precert inspection with cloud tags.
- Generated configuration checks for `commands.conf`, `alert_actions.conf`,
  and `restmap.conf`.
- Native-library and compiled-bytecode rejection checks.

Local AppInspect results do not replace Splunkbase online validation or Cloud
vetting. See `KNOWN_ISSUES.md` for the remaining generated-template warning.

## Artifact

`mispfuse-2.2.1.tar.gz`
