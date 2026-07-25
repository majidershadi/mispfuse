# Known limitations — 2.1.0

## Release blocker in the uploaded source

- `package/app.manifest` contains an unquoted email value and is invalid JSON.

## Security and deployment

- HTTP is accepted.
- TLS verification can be disabled.
- No custom CA-bundle or certificate-pinning field.
- Proxy configuration is global, not per MISP account.
- API-key security still depends on Splunk RBAC and host security.
- Splunk Cloud compatibility must not be claimed before vetting.

## Functional

- Outbound event creation only.
- No update/append-to-existing-event mode.
- No idempotency or duplicate-event prevention.
- No automatic retry/backoff for transient MISP failures.
- No dry-run preview of the event payload.
- No MISP objects, sightings, galaxies, or sharing-group selector.
- Templates are edited in configuration files and the alert dropdown is
  statically declared.
- Account creation/edit is blocked when MISP is temporarily unavailable.
- Complete result sets are materialized for grouping, so very large searches
  need operational limits.

## Compatibility

- Requires Splunk 10.2+ and Python 3.13.
- The direct client intentionally implements only the API surface MISPFuse
  needs; it is not a general PyMISP replacement.
