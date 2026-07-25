# Feature matrix

| Capability | 1.5.0 legacy | 2.0.0 UCC milestone | 2.1.0 final |
|---|---:|---:|---:|
| Visible Splunk app | No | Yes | Yes |
| SPL command | `mispfuse` | `mispfusepush` | `mispfusepush` |
| Alert action | No | Yes | Yes |
| Multiple MISP accounts | No | Yes | Yes |
| Encrypted API-key storage | No | Yes | Yes |
| Save-time connection test | No | No | Yes |
| Proxy configuration | No | Global | Global |
| Logging configuration | No | Yes | Yes |
| Mapping templates | No | Four | Four |
| Live `describeTypes` validation | No | Through PyMISP | Direct REST client |
| Grouping modes | Per row only | Three | Three |
| Attributes per event | One | Many | Many |
| Splunk multivalue support | No | No | Yes |
| Template-default inheritance | N/A | Defective in alert UI | Yes |
| Dependency versions | Copied and duplicated | Unpinned | Exact and hash locked |
| PyMISP shipped | Multiple versions | Latest at build time | No |
| Native binary rejection | No | No | Yes |
| Compiled-bytecode rejection | No | No | Yes |
| Unit tests | None | None | Included |
| AppInspect release gate | No | Basic target | Integrated target |
| Minimum intended runtime | Legacy Python 3 code, unreliable package portability | Splunk 10.2 / Python 3.13 | Splunk 10.2 / Python 3.13 |
| Support status | Archived | Milestone | Current candidate |

## Important compatibility correction

The traditional Python source uses conservative syntax and was designed around
older Splunk Python runtimes. The uploaded package itself is not broadly
portable: it includes CPython 3.9 Linux extensions, Windows executables, and
compiled files for more than one Python version. Describe it as a legacy
prototype, not as universally compatible with old Splunk versions.
