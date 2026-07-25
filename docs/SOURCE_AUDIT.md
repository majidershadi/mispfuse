# Source audit of the three uploaded snapshots

## Summary

| Snapshot | Files | Approximate size | `.pyc`/`.pyo` | Native/ executable files | Dependency state |
|---|---:|---:|---:|---:|---|
| Traditional | 3,134 | 32.44 MiB | 1,223 | 23 | copied environment with duplicates |
| Intermediate | 31 | 0.10 MiB | 8 | 0 in source | runtime requirements unpinned |
| Final | 55 | 0.57 MiB | 0 | 0 | exact versions and hashes |

Counts describe the uploaded source archive, not a generated package.

## Traditional findings

### Security

- `bin/keys.py` contains a real-looking API key and a private hostname.
- TLS verification is disabled.
- MISP organisation IDs are hard-coded.
- Events are published by default.
- The `publish` override uses Python `bool(value)`, so non-empty strings such
  as `"false"` still evaluate to `True`.
- No exception isolation or secret redaction is present.

### Functional behavior

- The command is a streaming command.
- Each input row creates one event and one attribute.
- `target` is required.
- Network activity defaults to `ip-src`.
- Non-network types require the result row to provide both `category` and
  `attrib-type`.
- The MISP response is assigned but not validated.
- The output field is misspelled as `resualt`.

### Packaging

- Two PyMISP versions are present.
- Three urllib3 versions are present.
- Multiple Requests, certifi, idna, wrapt, six, setuptools, and other versions
  coexist.
- The tree contains CPython 3.9 Linux extensions and Windows executables.
- A virtual environment and old configuration backup are included.
- `local/` configuration is present.

## Intermediate findings

### Improvements

- UCC-generated visible app and Configuration page.
- Encrypted API-key storage.
- Multiple accounts, proxy, and logging settings.
- Custom alert action.
- Reusable templates and grouping.
- Shared command/alert pusher.
- Live taxonomy validation through PyMISP.

### Defects discovered during evolution

- Custom command syntax exceeded UCC's schema limit.
- UCC schema version drifted from `0.0.9` to `0.0.10`.
- `python.required` was patched only into command and alert configs, not REST
  handlers.
- No connection test occurred before account save.
- Runtime dependencies were unpinned.
- The generic template omitted a required MISP type.
- Alert UI defaults overrode template defaults.
- Mapping names sorted lexically (`map.10` before `map.2`).
- Splunk multivalue fields were not expanded.
- Proxy credentials were not URL-encoded.
- Committed `.pyc` files were present.
- Branding called the visible product an add-on.
- Release assets and legal metadata were incomplete.

## Final findings

### Improvements

- Direct four-endpoint MISP client.
- Save-time account validation.
- API-key and proxy-secret redaction.
- Exact, hashed, pure-Python dependency closure.
- Explicit mapping types and corrected generic template.
- Numeric mapping order and multivalue support.
- Release gates for native binaries and compiled bytecode.
- Reload and Search Head Cluster replication settings.
- Unit and release tests.
- Full app branding.

### Current blocker in the uploaded snapshot

`package/app.manifest` is malformed because the author email value is not a
quoted JSON string. Correct it before building or publishing.

### Remaining design limitations

- HTTP and disabled certificate verification remain available for labs.
- Only outbound event creation is implemented.
- No idempotency key or duplicate-event prevention.
- No automatic retry/backoff.
- No custom CA-bundle field.
- Proxy configuration is global rather than per account.
- Templates are edited in configuration files rather than a dedicated editor.
- Account save is blocked when MISP is unavailable.
