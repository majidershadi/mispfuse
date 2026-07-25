# Issue ledger

This ledger connects the limitations discovered in one stage to the release
that addressed them.

| ID | Issue | Discovered | Resolution |
|---|---|---|---|
| `SEC-001` | Plaintext MISP key | 1.5.0 | Encrypted UCC credential storage in 2.0.0 |
| `SEC-002` | TLS verification disabled | 1.5.0 | Enabled by default in 2.0.0; lab override remains |
| `DATA-001` | One event and one attribute per result row | 1.5.0 | Grouping and templates in 2.0.0 |
| `DATA-002` | IP-oriented mapping | 1.5.0 | Four mapping templates in 2.0.0 |
| `OPS-001` | No scheduled alert action | 1.5.0 | UCC alert action in 2.0.0 |
| `PKG-001` | Copied venv, duplicate dependencies, native files | 1.5.0 | Clean UCC build in 2.0.0; strict lock/rejection in 2.1.0 |
| `BUILD-001` | UCC command syntax exceeds schema limit | 2.0.0 | Short syntax metadata in 2.1.0 |
| `RUNTIME-001` | REST handlers not forced to Python 3.13 | 2.0.0 | `supportedPythonVersion` and verifier in 2.1.0 |
| `CONFIG-001` | Invalid accounts can be saved | 2.0.0 | Save-time MISP connection test in 2.1.0 |
| `TPL-001` | Generic template has no MISP type | 2.0.0 | Explicit `text` type in 2.1.0 |
| `TPL-002` | `map.10` sorts before `map.2` | 2.0.0 | Numeric sort in 2.1.0 |
| `UI-001` | Alert defaults override template values | 2.0.0 | Tri-state/inherit options in 2.1.0 |
| `DATA-003` | Multivalue fields treated as one value | 2.0.0 | Value expansion in 2.1.0 |
| `DEP-001` | Unpinned runtime dependency tree | 2.0.0 | Exact hashes and direct MISP client in 2.1.0 |
| `REL-001` | Compiled Python copied into release | 2.1.0 preparation | Build purge and post-build rejection |
| `REL-002` | Missing custom-conf reload/SHC replication | 2.1.0 preparation | `app.conf` trigger and `server.conf` includes |
| `API-001` | `describeTypes` `result` envelope rejected | 2.1.0 preparation | Response normalizer |
| `REL-003` | Uploaded final manifest is malformed JSON | Current source audit | Must be corrected before publication |
