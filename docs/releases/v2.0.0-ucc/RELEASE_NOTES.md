# MISPFuse 2.0.0 — UCC transition milestone

This release records the point where MISPFuse changed from a single-purpose
streaming command into a configurable Splunk application.

## Added

- UCC-generated Configuration page.
- Encrypted MISP account credentials.
- Multiple accounts, proxy settings, and logging settings.
- New `mispfusepush` command.
- Custom scheduled alert action.
- Shared grouping and event-building core.
- Network, file-hash, email/phishing, and generic templates.
- Live MISP type/category validation through PyMISP.

## Changed

- Removed the hard-coded `keys.py` design.
- Removed hard-coded MISP organisation IDs.
- Replaced one-event-per-row as the only mode with three grouping choices.
- Targeted Splunk 10.2+ and Python 3.13.

## Status

Pre-release engineering milestone. It is retained to show the UCC redesign and
the defects discovered during hardening. Use 2.1.x for current deployments.
