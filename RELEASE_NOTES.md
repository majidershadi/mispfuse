# MISPFuse 1.5.0 — Legacy prototype

This historical release captures the first working Splunk-to-MISP workflow.

## Included

- `mispfuse` streaming search command.
- PyMISP event creation.
- Per-result event and attribute creation.
- Basic event-field overrides from SPL result fields.

## Status

Archived and unsupported. The original source contained a plaintext credential,
disabled TLS verification, environment-specific IDs, and an unmanaged bundled
Python environment. The public GitHub snapshot must be sanitized and is
provided for engineering history only.

Do not use this release for production or attach the original source directory
as a release artifact.
