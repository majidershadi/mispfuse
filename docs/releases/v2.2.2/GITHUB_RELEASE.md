# MISPFuse 2.2.2 — SLIM-supported Splunk 9.3 range

MISPFuse 2.2.2 changes the manifest to the exact compatibility boundary
identified by the Splunkbase online SLIM report.

## Fixed

- Replaced `>=9.4` with the full semantic-version constraint `>=9.3.0`.
- The new range intersects the validator's supported Splunk Enterprise 9.x
  matrix without claiming Python 3.7 compatibility.

## Runtime compatibility

- Splunk Enterprise 9.3 through 10.1: Python 3.9 selected explicitly with
  `python.version = python3.9`.
- Splunk Enterprise 10.2 and later: Python 3.13 preferred and Python 3.9 used
  as fallback through `python.required = 3.9, 3.13`.
- Splunk Enterprise 9.0 through 9.2 and Python 3.7 are not supported.

## Validation

- Unit tests on Python 3.9.25 and Python 3.13.14.
- Python 3.9 grammar validation.
- UCC 6.5.3 build and package validation.
- AppInspect 4.3.0 precert inspection with cloud tags.
- Generated command, alert-action, and REST-handler runtime checks.
- Native-library and compiled-bytecode rejection checks.

Local validation does not replace the authoritative Splunkbase online SLIM
run or Splunk Cloud vetting.

## Artifact

`mispfuse-2.2.2.tar.gz`
