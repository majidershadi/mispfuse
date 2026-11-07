# MISPFuse 2.2.4 release validation

Last reviewed: 14 August 2026

This record describes the build and source checks completed for version 2.2.4
on the review date above. These results do not establish compatibility with
every Splunk platform or deployment type.

## Packaging

The runtime requirements are exact-version and hash locked:

- defusedxml 0.7.1
- deprecation 2.1.0
- packaging 23.2
- PySocks 1.7.1
- sortedcontainers 2.4.0
- solnlib 7.0.0
- splunk-sdk 2.1.1
- splunktaucclib 8.2.0
- urllib3 1.26.20

PyMISP and requests are not included. The post-build script checks Python
3.7 syntax, modern 3.9/3.13 and legacy `python3` declarations, the Splunk 8.0.0+ manifest range,
the custom account handler, app identity, dependency lock, and absence of
native binary files.

## Source checks completed

- `globalConfig.json` and `app.manifest` parse successfully.
- All packaged Python files parse with the Python 3.7 grammar.
- The unit suite passes on Python 3.7, Python 3.9.25, and Python 3.13.14.
- The source tree contains no `.so`, `.pyd`, `.dll`, or `.dylib` files.
- Icons are present in the required sizes.
- Runtime requirements use exact versions and hashes.
- UCC 6.5.3 build, packaging, and post-build verification pass.
- AppInspect 4.3.0 reports 0 errors and 0 failures. One future failure remains
  for the UCC-generated Mako Configuration-page template.
- Splunk 10.4.1 `btool` resolves the command, alert action, and REST handlers
  with `python.version = python3` and `python.required = 3.9, 3.13`.
