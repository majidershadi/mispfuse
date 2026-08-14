# MISPFuse 2.2.2

MISPFuse 2.2.2 corrects the remaining SLIM version-range rejection reported for
v2.2.1.

## Changed

- The Splunk Enterprise requirement is now `>=9.3.0`.
- The constraint uses major, minor, and patch components as requested by the
  online validator.
- Splunk 9.3 through 10.1 continue to use
  `python.version = python3.9`.
- Splunk 10.2 and later continue to use
  `python.required = 3.9, 3.13`.

## Compatibility boundary

MISPFuse does not claim support for Splunk 9.0 through 9.2 because those
releases use Python 3.7. Splunk 9.3 is the first 9.x release in the declared
range and provides the Python 3.9 runtime used by MISPFuse and its locked
dependencies.

All application features and security controls from v2.2.1 are unchanged.
