# Migration from 1.5.0 to the UCC architecture

## Security migration

1. Revoke the API key that was stored in `keys.py`.
2. Create a dedicated MISP automation account.
3. Add the new key through the UCC Configuration page.
4. Enable TLS verification.
5. Remove the legacy app before installing the new package.

## SPL migration

Legacy:

```spl
... | eval target=src_ip | mispfuse
```

UCC version:

```spl
... | mispfusepush account=prod template=network_ioc
```

The new command consumes named fields from a mapping template instead of a
single `target` field.

## Behavior changes

| Legacy | UCC version |
|---|---|
| one event per row | selectable grouping |
| one attribute per event | many mapped attributes |
| fixed account | multiple configured accounts |
| plaintext key | encrypted credential storage |
| manual command only | command and alert action |
| fixed IP behavior | templates for network, files, email, and generic text |
| hard-coded org IDs | MISP derives organisation from the API user |
