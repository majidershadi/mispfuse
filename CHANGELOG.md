# Changelog

## 2.2.3 — Splunk 9.0 and Python 3.7 compatibility

### Changed

- Lowered the Splunk Enterprise constraint from `>=9.3.0` to the validator's
  accepted full semantic-version boundary, `>=9.0.0`.
- Restored `python.version = python3` for extension points used by Splunk
  9.0 through 10.1 while retaining `python.required = 3.9, 3.13` for Splunk
  10.2 and later.
- Replaced `packaging` 26.3 with hash-locked `packaging` 23.2 so the complete
  runtime dependency closure supports Python 3.7, 3.9, and 3.13.

### Added

- Python 3.7 unit-test and source-grammar release gates alongside the existing
  Python 3.9 and Python 3.13 gates.

### Fixed

- Splunkbase SLIM rejection of v2.2.2 because `>=9.3.0` did not intersect the
  Enterprise versions recognized by the online validator.

## 2.2.2 — SLIM-supported 9.3 range

### Changed

- Changed the Splunk Enterprise constraint from `>=9.4` to the full semantic
  version `>=9.3.0`, matching the version boundary identified by Splunkbase's
  online SLIM validator.
- Retained `python.version = python3.9` for Splunk 9.3 through 10.1 and
  `python.required = 3.9, 3.13` for Splunk 10.2 and later.

### Fixed

- Splunkbase rejection of v2.2.1 because the online validator did not include
  Splunk 9.4 in its supported-version matrix.
- Ambiguous major/minor-only manifest formatting by using a complete semantic
  version with major, minor, and patch components.

## 2.2.1 — Splunk 9.x compatibility correction

### Changed

- Expanded the declared Splunk Enterprise range from 10.0+ to 9.4+ after the
  Splunkbase SLIM matrix required an intersection with a supported 9.x release.
- Changed the legacy runtime selector from `python.version = python3` to
  `python.version = python3.9` for commands, alert actions, and REST handlers.
  On Splunk 9.4, the `python3` alias selects Python 3.7; the explicit selector
  is required for MISPFuse's tested Python 3.9 dependency boundary.
- Retained `python.required = 3.9, 3.13` for Splunk 10.2 and later.

### Added

- A post-build normalization and regression test that verifies every generated
  Python extension point uses the explicit Python 3.9 legacy selector.

### Fixed

- Splunkbase rejection of v2.2.0 because its `>=10.0` manifest range did not
  include a Splunk Enterprise 9.x version accepted by the validator.

## 2.2.0 — Backward-compatible Splunkbase release

### Changed

- Expanded the declared Splunk Enterprise range from 10.2+ to 10.0+ after
  adding real Python 3.9 compatibility.
- Declared both Python 3.9 and 3.13 for commands, alert actions, and REST
  handlers while retaining `python.version = python3` for Splunk 10.0/10.1.
- Replaced Python-3.13-only `splunk-sdk` 3.0.0 with compatible version 2.1.1.
- Updated the local release gate from Splunk AppInspect 4.2.1 to 4.3.0.

### Added

- Unit and syntax checks for the Python 3.9 compatibility boundary.
- Release verification for both modern `python.required` and legacy
  `python.version` declarations.
- A separate v2.2.0 release record; the v2.1.0 tag remains unchanged as the
  Splunk 10.2/Python 3.13 engineering milestone.

### Fixed

- Splunkbase SLIM rejected the 2.1.0 manifest because `>=10.2` did not
  intersect the validator's accepted Enterprise versions.
- Merely lowering the manifest requirement would have made a false runtime
  claim; 2.2.0 fixes the dependency and runtime compatibility before changing
  the manifest to `>=10.0`.

## 2.1.0 — Hardened release candidate

### Added

- Save-time MISP account validation.
- Multiple MISP accounts with encrypted API-key storage.
- Manual `mispfusepush` command and scheduled alert action.
- Four mapping templates and three grouping modes.
- Explicit MISP attribute types and live `describeTypes` validation.
- Splunk multivalue-field support.
- Direct MISP REST client for the four required operations.
- Proxy support, logging controls, response-size limits, disabled redirects,
  API-key redaction, and connection/read timeouts.
- Exact dependency versions and SHA-256 hashes.
- Checks that reject native binaries, `.pyc`, `.pyo`, and `__pycache__`.
- Unit tests and release-gate checks.
- Splunk app branding and release documentation.

### Changed

- Product name changed from “MISPFuse Add-on for Splunk” to `MISPFuse`.
- PyMISP and Requests were removed from the shipped runtime.
- Alert-action values can inherit template defaults.
- Mapping keys are sorted numerically.
- The generic template uses the explicit MISP `text` type.

### Fixed during release preparation

- UCC custom-command syntax exceeded the schema length limit.
- Python 3.13 was not applied to generated REST handlers.
- The UCC footer and OpenAPI link were visible in the Configuration page.
- Current MISP `describeTypes` responses were not unwrapped from `result`.
- Custom-conf reload and Search Head Cluster replication settings were absent.
- Tests recreated compiled Python files before packaging.
- The release checker incorrectly expected a fixed UCC build number.

## 2.0.0 — UCC transition milestone

- Rebuilt the project around Splunk UCC.
- Added encrypted account storage, proxy and logging pages.
- Added multiple MISP instances.
- Added `mispfusepush` and a custom alert action.
- Added mapping templates and event grouping.
- Added live MISP taxonomy checks through PyMISP.
- Targeted Splunk 10.2+ and Python 3.13.

This milestone is preserved to document the architecture transition. It has
known build, dependency, runtime, template, and release defects and should not
be deployed.

## 1.5.0 — Legacy prototype

- Added the `mispfuse` streaming search command.
- Created one MISP event and one attribute for each Splunk result row.
- Used PyMISP and the Splunk SDK directly.

This version is archived. Its original source contained a plaintext API key,
private infrastructure details, hard-coded MISP organisation IDs, disabled TLS
verification, compiled bytecode, native extensions, duplicate dependencies,
and a bundled virtual environment.
