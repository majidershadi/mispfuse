# Roadmap ideas

These are proposed features, not current capabilities.

## Security

- Production mode that enforces HTTPS.
- Custom CA-bundle support.
- Per-account proxy and trust settings.
- Dedicated Splunk capability for configuring MISP accounts.
- Optional certificate pinning.

## Reliability

- Retry with bounded exponential backoff.
- Idempotency key and duplicate-event prevention.
- Maximum row, event, and attribute limits.
- Partial-failure retry report.
- Health dashboard and operational metrics.

## Workflow

- Dry-run payload preview.
- Append attributes to an existing MISP event.
- MISP object support.
- Sightings and galaxy/tag support.
- Sharing-group selection.
- Template editor populated from the connected server taxonomy.
- Dynamic template discovery in the alert-action form.

## Delivery

- CI workflow for tests, UCC build, AppInspect, SBOM, and checksums.
- Upgrade tests from the 2.0.0 configuration model.
- Documented standalone, SHC, and Cloud deployment matrices.
