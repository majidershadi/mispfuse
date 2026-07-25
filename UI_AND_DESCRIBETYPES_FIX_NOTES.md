# Configuration UI and MISP describeTypes correction

## Configuration footer

The UCC footer is disabled through supported `globalConfig.json` metadata:

```json
"hideUCCVersion": true,
"showFooter": false
```

This removes both the UCC version label and the OpenAPI download link from the
Configuration page. The generated OpenAPI document remains in the package; it
is simply not advertised in the user interface.

## MISP taxonomy response

Current MISP releases return `attributes/describeTypes.json` in a `result`
envelope. MISPFuse previously expected `types` at the top level and rejected a
valid response.

The client now accepts both forms:

```json
{"result": {"types": []}}
```

and the legacy form:

```json
{"types": []}
```

The normalized taxonomy is used by connection testing and template validation.
