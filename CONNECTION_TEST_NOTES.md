# MISP account validation

MISPFuse tests a MISP account before UCC saves it.

The check runs when an account is added, cloned, or edited. When an existing
API key is left unchanged, UCC sends a masked value; the handler retrieves the
stored key for the test instead of sending the mask to MISP. Deleting an
account does not require the MISP server to be online.

The test checks:

- the base URL and optional MISP sub-path;
- proxy connectivity when the global proxy is enabled;
- TLS certificate validation;
- API-key authentication and access to the current user;
- the MISP server version;
- `attributes/describeTypes.json`.

No MISP event or attribute is created. A failed test returns an error to the
Configuration page and leaves the stored account unchanged.

Each request uses a 5-second connection timeout and a 15-second read timeout.
Because the check makes several requests, the complete save can take longer
than 15 seconds on a slow server.
