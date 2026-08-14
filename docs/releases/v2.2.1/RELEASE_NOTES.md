# MISPFuse 2.2.1

MISPFuse 2.2.1 corrects the Splunk Enterprise range after Splunkbase rejected
v2.2.0 because its manifest did not include an accepted Splunk 9.x release.

## Changed

- Minimum Splunk Enterprise version is now 9.4.
- Generated commands, alert actions, and REST handlers use
  `python.version = python3.9` for Splunk 9.4 through 10.1.
- Splunk 10.2 and later continue to use
  `python.required = 3.9, 3.13` and prefer Python 3.13 when available.
- Package identity and release documentation are updated to 2.2.1.

## Why the selector changed

Splunk 9.4 interprets `python.version = python3` as Python 3.7. MISPFuse and its
locked dependencies are tested on Python 3.9 and 3.13, so merely changing the
manifest would be an incorrect compatibility claim. The build now rewrites and
verifies every generated extension point with the explicit `python3.9` value.

## Preserved from 2.2.0

- Encrypted API and proxy credentials.
- Save-time MISP authentication and taxonomy validation.
- Template-based SPL command and alert-action publishing.
- Exact, hash-locked, pure-Python runtime dependencies.
- Python 3.9 and 3.13 tests and AppInspect 4.3.0 release gate.
