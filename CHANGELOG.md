# Changelog

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
