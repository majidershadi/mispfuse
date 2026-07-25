# MISPFuse 1.5.0 — Legacy prototype

> Historical source only. Do not deploy this version in production.

This release records the first working MISPFuse design: a Splunk streaming
search command that creates a MISP event from each search-result row.

## What it does

The `mispfuse` command reads these fields from each result:

| Field | Behavior |
|---|---|
| `target` | Required attribute value |
| `info` | Optional MISP event title |
| `date` | Optional event date |
| `state` | Optional analysis value |
| `distribution` | Optional distribution value |
| `category` | Defaults to `Network activity` |
| `attrib-type` | Used only when category is not `Network activity` |
| `comment` | Optional attribute comment |
| `a_tag` | Optional additional tag |
| `publish` | Attempts to override publication state |

For the default `Network activity` category, the attribute type is `ip-src`.
One input row creates one MISP event with one attribute.

## Historical SPL example

This example creates a real, published MISP event in the original code. Use it
only in an isolated lab after sanitizing the configuration.

```spl
| makeresults
| eval target="192.0.2.10",
       info="Legacy MISPFuse demonstration",
       distribution=0,
       comment="Documentation-only address"
| mispfuse
```

## Architecture

```text
Splunk result row
  -> StreamingCommand.stream()
  -> MISPEvent()
  -> one MISP attribute
  -> PyMISP.add_event()
  -> original row returned
```

## Why it is archived

The original snapshot contains a plaintext API key, disabled TLS validation,
hard-coded organisation IDs, a fixed organisation tag, and a copied Python
environment with duplicate and platform-specific dependencies.

It also has functional constraints:

- one event per row;
- one attribute per event;
- IP-first mapping logic;
- no alert action;
- no configuration UI;
- no connection test;
- no response validation;
- no error isolation.

The `publish` override is unsafe because `bool("false")` is `True` in Python.
The original output field is also misspelled as `resualt`.

## Publication requirements

Before putting this tag on GitHub:

1. Revoke the original MISP key.
2. Delete `bin/keys.py` and commit a `keys.py.example`.
3. Remove private hostnames and organisation-specific values.
4. Remove `local/`, `default.old.*`, `lib/`, compiled bytecode, and native
   binaries from the public source snapshot.
5. Mark the GitHub release as a pre-release and unsupported.

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) and
[MIGRATION_TO_V2.md](MIGRATION_TO_V2.md).
