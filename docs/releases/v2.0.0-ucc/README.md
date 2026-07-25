# MISPFuse 2.0.0 — UCC transition milestone

> Engineering milestone. This source documents the redesign but is not the
> supported release.

Version 2.0.0 replaces the environment-specific streaming command with a
visible UCC-based Splunk application.

## Major changes

- UCC Configuration page.
- Multiple MISP instances.
- API keys declared as encrypted UCC fields.
- Proxy and logging tabs.
- `mispfusepush` dataset-processing command.
- `MISPFuse - Push to MISP` alert action.
- Shared push logic for command and alert execution.
- Four mapping templates.
- `single_event`, `per_row`, and `by_field` grouping.
- Live MISP taxonomy checks through PyMISP.
- Result rows with event ID, UUID, attribute count, and status.

## Example

```spl
| makeresults
| eval src_ip="192.0.2.10",
       domain="example.invalid"
| mispfusepush account=lab template=network_ioc grouping=single_event
```

## Why this is a milestone rather than the final release

The architecture is substantially better than 1.5.0, but the snapshot contains
known defects:

- UCC command syntax metadata exceeds the schema length limit.
- Python 3.13 is patched into command and alert stanzas but not REST handlers.
- Dependencies are unpinned and can change between builds.
- Account settings are not tested before saving.
- The generic template omits a MISP attribute type.
- Alert UI defaults override template defaults.
- Mapping numbers sort lexically.
- Multivalue fields are not expanded.
- Compiled `.pyc` files are committed.
- Branding and release metadata are incomplete.

Use version 2.1.x for deployment.
