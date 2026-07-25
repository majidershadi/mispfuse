# Migration from 2.0.0 to 2.1.0

## Configuration

Existing UCC account and settings concepts remain, but account create/edit now
performs a real connection test. Ensure MISP is reachable during upgrade
validation.

## Runtime

PyMISP is removed from the shipped package. MISPFuse uses a direct REST client
for server version, current user, taxonomy, and event creation.

## Templates

Every mapping must declare a MISP type. Update any custom mapping with an empty
type before installing 2.1.0.

The old generic mapping:

```ini
map.1 = ioc_value:::0:0:comment
```

becomes:

```ini
map.1 = ioc_value:text:Other:0:0:comment
```

## Alert action

Blank override values now inherit from the selected template. Review saved
alerts that relied on the old UI defaults.

## Dependencies

Do not copy the old `lib/` directory forward. Build 2.1.0 from its exact,
hash-locked requirements.
