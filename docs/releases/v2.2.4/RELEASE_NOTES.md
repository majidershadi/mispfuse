# MISPFuse 2.2.4

MISPFuse 2.2.4 fixes the SLIM validation failure reported for v2.2.3.

## Fixed

- Changed the Splunk Enterprise requirement from `>=9.0.0` to `>=8.0.0`.
- Verified that the new constraint intersects Splunk Packaging Toolkit 1.2.8's
  bundled Enterprise catalog, which explicitly contains version 8.0.0.
- Avoided the report's proposed `>=8.1.0` constraint because the standalone
  catalog does not contain 8.1.0 and would reject that range.

## Compatibility evidence

- Splunk Enterprise 8.x supports Python 3.7 and `python.version = python3`.
- The complete locked dependency closure installs on Python 3.7.
- The unit suite passes on Python 3.7, 3.9, and 3.13.
- Newer platforms retain `python.required = 3.9, 3.13`.

All application behavior and security controls are unchanged.
