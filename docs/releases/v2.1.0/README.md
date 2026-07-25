# MISPFuse 2.1.0

MISPFuse sends selected Splunk search results to MISP as events and attributes.
It supports manual SPL execution and scheduled alert actions, using reusable
field-to-MISP templates.

## Current capabilities

- Visible Splunk application with overview and Configuration pages.
- Multiple MISP accounts.
- Encrypted MISP API-key storage.
- Save-time connection and authentication test.
- Global proxy and logging configuration.
- `mispfusepush` custom search command.
- `MISPFuse - Push to MISP` alert action.
- Four bundled templates.
- Three event-grouping modes.
- Live MISP type/category validation.
- Multivalue field expansion.
- Exact, hash-locked, pure-Python dependencies.
- Release checks for native binaries and compiled bytecode.

## Runtime architecture

MISPFuse does not ship PyMISP in this release. The runtime uses these MISP API
operations:

```text
GET  servers/getVersion
GET  users/view/me
GET  attributes/describeTypes.json
POST events/add
```

The client applies timeouts, disables redirects, requests uncompressed JSON,
limits responses to 8 MiB, and redacts the API key from surfaced errors.

## Requirements

- Splunk Enterprise 10.2 or later.
- Splunk Python 3.13 runtime.
- A reachable MISP instance and automation API key.
- HTTPS with certificate verification for production deployments.

## Quick test

Replace `lab` with a configured account name:

```spl
| makeresults
| eval src_ip="192.0.2.10",
       dest_ip="198.51.100.20",
       domain="mispfuse-test.example"
| mispfusepush account=lab
                   template=network_ioc
                   event_info="MISPFuse network test"
                   distribution=0
                   publish=false
```

This creates a real MISP event. Use a test organisation.

## Templates

| Template | Expected fields |
|---|---|
| `network_ioc` | `src_ip`, `dest_ip`, `domain`, `url`, `dest_host` |
| `file_hashes` | `md5`, `sha1`, `sha256`, `file_name` |
| `email_phishing` | `src_email`, `dest_email`, `subject`, `url` |
| `passthrough` | `ioc_value`, optional `comment` |

Grouping can create one event for all results, one event per row, or one event
per value of a selected field.

## Security

The API key is stored through Splunk encrypted credential storage. It is
decrypted in memory when required and sent in the MISP `Authorization` header.
Use a dedicated least-privileged MISP key.

HTTP and disabled TLS verification remain available for isolated labs. They are
not recommended for production.

## Release status

The uploaded source must not be published until `package/app.manifest` is valid
JSON and the exact release tarball passes unit tests and AppInspect.
