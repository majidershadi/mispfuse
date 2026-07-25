# Known issues — 2.0.0 UCC milestone

## Build and runtime

- The custom search-command `syntax` value exceeds UCC's schema limit.
- `schemaVersion` is declared as `0.0.9` and is updated by newer UCC.
- `python.required = 3.13` is added only to commands and alert actions.
  Configuration REST handlers can run with the wrong interpreter.
- Build and runtime requirements are not pinned.

## Configuration

- Invalid URL/API-key combinations can be saved.
- Connection failure is detected only when a command or alert runs.
- Proxy credentials are inserted without URL encoding.
- HTTP and disabled TLS verification are accepted.

## Templates and data

- `passthrough` has no MISP type and can fail in PyMISP.
- `map.10` sorts before `map.2`.
- Alert-form defaults silently replace template defaults.
- Splunk multivalue fields are not split into separate MISP attributes.
- Taxonomy-fetch failures are ignored during mapping validation.

## Packaging and product identity

- Committed `.pyc` files are present.
- Runtime dependencies may introduce native wheels.
- Visible product is named as an add-on.
- App icons, privacy text, and release notes are incomplete.
- License path in the manifest does not match a packaged license directory.

These defects are resolved or explicitly controlled in 2.1.0.
