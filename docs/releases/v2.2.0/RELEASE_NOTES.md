# MISPFuse 2.2.0

MISPFuse 2.2.0 is the backward-compatible Splunkbase publication release.

## What was fixed

- The v2.1.0 manifest declared Splunk Enterprise `>=10.2`, which the current
  Splunkbase SLIM compatibility matrix rejected.
- The manifest was not simply lowered. The runtime was first made compatible
  with Python 3.9 as well as Python 3.13.
- `splunk-sdk` 3.0.0, which requires Python 3.13, was replaced with the newest
  compatible pre-3.0 release, 2.1.1.
- UCC now generates dual runtime declarations for commands, alert actions, and
  REST handlers: `python.version = python3` for Splunk 10.0/10.1 and
  `python.required = 3.9, 3.13` for Splunk 10.2+.
- The local validation toolchain now uses Splunk AppInspect 4.3.0.
- Release checks reject missing legacy runtime declarations, incomplete modern
  runtime declarations, Python 3.10+ syntax, incorrect version identity, or an
  incorrect Splunk compatibility range.

## Compatibility

- Splunk Enterprise 10.0 or later.
- Python 3.9 and Python 3.13 extension-point runtimes.
- UCC 6.5.3 for building.
- Splunk AppInspect 4.3.0 for the local release gate.

The `v2.1.0` tag is unchanged and remains the historical Splunk 10.2/Python
3.13 milestone.

## Validation result

The local AppInspect 4.3.0 precert/cloud run reports 0 errors and 0 failures.
It reports one future failure for the UCC-generated Mako Configuration-page
template; see the known-issues record for the exact boundary.
