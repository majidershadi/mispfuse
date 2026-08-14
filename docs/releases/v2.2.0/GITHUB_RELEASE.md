# MISPFuse 2.2.0 — Python 3.9/3.13 compatibility release

MISPFuse 2.2.0 fixes the Splunkbase SLIM compatibility failure reported for
2.1.0 without making a manifest-only compatibility claim that the code could
not satisfy.

## Fixed

- Expanded supported Splunk Enterprise versions from 10.2+ to 10.0+ after
  adding real Python 3.9 compatibility.
- Generated both `python.version = python3` for Splunk 10.0/10.1 and
  `python.required = 3.9, 3.13` for Splunk 10.2+ across the SPL command, alert
  action, and REST handlers.
- Replaced `splunk-sdk` 3.0.0, which requires Python 3.13, with the newest
  compatible pre-3.0 SDK, version 2.1.1.
- Locked the SDK's additional `deprecation` and `packaging` dependencies by
  exact version and SHA-256 hash.
- Updated the local release gate from Splunk AppInspect 4.2.1 to 4.3.0.
- Added release checks for Python 3.9 grammar, both runtime selectors, the
  Splunk 10.0+ manifest boundary, dependency closure, bytecode, and native
  binaries.

## Preserved from 2.1.0

- Encrypted MISP credentials and save-time connection validation.
- Direct, hardened MISP REST client with TLS verification, redaction, timeout,
  redirect, decompression, and response-size controls.
- Template-driven event/attribute mapping, multivalue fields, SPL command, and
  alert action.
- Exact dependency locking and native/compiled-artifact rejection.

## Validation

- 39 unit/release tests passed on Python 3.9.25.
- 39 unit/release tests passed on Python 3.13.14.
- UCC 6.5.3 build and package verification passed.
- Splunk AppInspect 4.3.0 precert/cloud result: 0 errors, 0 failures,
  1 future failure, 8 warnings, and 117 successful checks.
- The original `check_that_app_passes_slim_validation_for_cloud` failure is no
  longer present.
- Splunk 10.4.1 `btool` validated the deployed command, alert action, REST
  handlers, and dual Python selectors.

## Known future boundary

AppInspect reports one `FUTURE_FAILURE` for the UCC 6.5.3-generated
`appserver/templates/base.html`. The generated Configuration view references
that template, so it is retained. This is not a current AppInspect failure, but
it must be addressed before Splunk removes custom Mako templates.

The SDK 2.1.1 outdated-version warning is intentional: SDK 3.0.0 requires
Python 3.13 and would invalidate the Python 3.9/Splunk 10.0 compatibility goal.

## Artifact integrity

`mispfuse-2.2.0.tar.gz`

SHA-256: `61dd1818276c0fa26893b4af1ec37bf3a7e647f7bd1b381dedf06b5cc2ee37ed`

The v2.1.0 tag remains unchanged as the historical Splunk 10.2/Python 3.13
engineering milestone.
