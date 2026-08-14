# Feature matrix

| Capability | 1.5.0 legacy | 2.0.0 UCC milestone | 2.1.0 hardened | 2.2.0 compatibility milestone | 2.2.1 range milestone | 2.2.2 range milestone | 2.2.3 range milestone | 2.2.4 release |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visible Splunk app | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| SPL command | `mispfuse` | `mispfusepush` | `mispfusepush` | `mispfusepush` | `mispfusepush` | `mispfusepush` | `mispfusepush` | `mispfusepush` |
| Alert action | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Multiple MISP accounts | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Encrypted API-key storage | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Save-time connection test | No | No | Yes | Yes | Yes | Yes | Yes | Yes |
| Proxy configuration | No | Global | Global | Global | Global | Global | Global | Global |
| Logging configuration | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Mapping templates | No | Four | Four | Four | Four | Four | Four | Four |
| Live `describeTypes` validation | No | Through PyMISP | Direct REST client | Direct REST client | Direct REST client | Direct REST client | Direct REST client | Direct REST client |
| Grouping modes | Per row only | Three | Three | Three | Three | Three | Three | Three |
| Attributes per event | One | Many | Many | Many | Many | Many | Many | Many |
| Splunk multivalue support | No | No | Yes | Yes | Yes | Yes | Yes | Yes |
| Template-default inheritance | N/A | Defective in alert UI | Yes | Yes | Yes | Yes | Yes | Yes |
| Dependency versions | Copied and duplicated | Unpinned | Exact and hash locked | Exact and hash locked | Exact and hash locked | Exact and hash locked | Exact and hash locked | Exact and hash locked |
| PyMISP shipped | Multiple versions | Latest at build time | No | No | No | No | No | No |
| Native binary rejection | No | No | Yes | Yes | Yes | Yes | Yes | Yes |
| Compiled-bytecode rejection | No | No | Yes | Yes | Yes | Yes | Yes | Yes |
| Unit tests | None | None | Included | Python 3.9 and 3.13 | Python 3.9 and 3.13 | Python 3.9 and 3.13 | Python 3.7, 3.9, and 3.13 | Python 3.7, 3.9, and 3.13 |
| AppInspect release gate | No | Basic target | 4.2.1 | 4.3.0 | 4.3.0 | 4.3.0 | 4.3.0 | 4.3.0 |
| Legacy Python selector | Unspecified | `python3` | `python3` | `python3` | `python3.9` | `python3.9` | `python3` | `python3` |
| Minimum intended runtime | Legacy Python 3 code, unreliable package portability | Splunk 10.2 / Python 3.13 | Splunk 10.2 / Python 3.13 | Splunk 10.0 / Python 3.9 or 3.13 | Splunk 9.4 / Python 3.9 or 3.13 | Splunk 9.3 / Python 3.9 or 3.13 | Splunk 9.0 / Python 3.7, 3.9, or 3.13 | Splunk 8.0 / Python 3.7, 3.9, or 3.13 |
| Support status | Archived | Milestone | Historical milestone | Historical milestone | Historical milestone | Historical milestone | Historical milestone | Current release |

## Important compatibility correction

The traditional Python source uses conservative syntax and was designed around
older Splunk Python runtimes. The uploaded package itself is not broadly
portable: it includes CPython 3.9 Linux extensions, Windows executables, and
compiled files for more than one Python version. Describe it as a legacy
prototype, not as universally compatible with old Splunk versions.
