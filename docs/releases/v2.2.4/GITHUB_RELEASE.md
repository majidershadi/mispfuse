# MISPFuse 2.2.4 — SLIM catalog compatibility correction

MISPFuse 2.2.4 fixes the SSAI SLIM failure reported for v2.2.3.

## What changed

- Changed `platformRequirements.splunk.Enterprise` from `>=9.0.0` to
  `>=8.0.0`.
- Verified the exact range with Splunk Packaging Toolkit 1.2.8. Its bundled
  Enterprise catalog contains 8.0.0, so this constraint has a proven
  intersection.
- Retained `python.version = python3` for Splunk 8.0 through 10.1.
- Retained `python.required = 3.9, 3.13` for newer Splunk releases.
- Retained the Python 3.7-compatible, exact, hash-locked dependency closure.

The generated report suggested `>=8.1.0`, but standalone SLIM 1.2.8 does not
list 8.1.0. Using `>=8.0.0` includes both its recognized 8.0.0 release and any
online supported version at 8.1 or later.

## Validation

- Standalone `slim validate` using Splunk Packaging Toolkit 1.2.8.
- 41 unit tests on Python 3.7, 3.9, and 3.13.
- UCC 6.5.3 build and post-build package verification.
- Splunk AppInspect 4.3.0 precert scan with cloud tags.

## Release artifact

`mispfuse-2.2.4.tar.gz`
