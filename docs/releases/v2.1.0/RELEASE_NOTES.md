# MISPFuse 2.1.0

MISPFuse 2.1.0 is the hardened application release.

## Highlights

- Encrypted multi-account configuration.
- Connection test before account create or edit.
- Manual SPL command and scheduled alert action.
- Four templates and three grouping modes.
- Live MISP taxonomy validation.
- Direct, bounded MISP REST client.
- Multivalue attribute expansion.
- Exact dependency versions and SHA-256 hashes.
- No PyMISP, Requests, native extensions, or compiled bytecode in the release.
- Unit tests and AppInspect-oriented release checks.
- Full Splunk app branding.

## Important changes from 2.0.0

- Custom mappings must include an explicit MISP type.
- Blank alert-action overrides inherit template defaults.
- Proxy credentials are URL-encoded.
- Mapping sequence is numeric.
- Current and legacy `describeTypes` response envelopes are supported.
- Python 3.13 is required for command, alert, and REST handlers.

## Upgrade note

Review custom templates and saved alerts before upgrading. Build the release
from a clean Python 3.13 environment and attach only the tarball that passes the
complete release workflow.
