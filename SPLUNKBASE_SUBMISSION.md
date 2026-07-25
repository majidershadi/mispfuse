# Splunkbase submission notes: MISPFuse

The fields Splunkbase asks for when you create or edit the app, plus the
compatibility and vetting steps, with what to put in each. Anything marked
"you" needs something from you before you submit.

## App identity

| Field | Value |
|---|---|
| Type | App (visible), not add-on |
| Name / title | MISPFuse |
| App id | `mispfuse`: has to match `app.conf [package] id` and the manifest |
| Version | `2.0.0`: same in `app.conf`, `app.manifest`, and the tarball name |
| Built by | you |
| Author | MISPFuse (in `app.conf [launcher] author`) |

## Descriptions

| Field | What to write |
|---|---|
| Short summary (~255 chars) | Push Splunk search results into MISP as events and attributes, with templates that get validated against your own MISP server. Ships a `mispfusepush` search command and a push alert action. |
| Long description | Pull from the README: what it does, usage, templates. Cover the multi-instance config, the template model, and the live `describeTypes` validation. |
| Release notes (2.0.0) | Rewritten on UCC. Multi-instance encrypted config UI, `mispfusepush` command plus a push alert action, server-validated templates, and three grouping modes. |

## Categories

| Field | Value |
|---|---|
| Category | Security, Fraud & Compliance |
| Use case | Threat intelligence export / enrichment |
| Tags | misp, threat intelligence, ioc, pymisp, security, alert action, custom command |
| CIM | None (this exports data rather than mapping it). Set None unless you add CIM-mapped output. |

## Compatibility

This is the part AppInspect and Cloud vetting actually read.

| Field | Value |
|---|---|
| Products | Splunk Enterprise, Splunk Cloud Platform |
| Enterprise versions | 10.2 and up (min 10.2, because of Python 3.13) |
| Cloud | Yes, 10.2+ (Victoria) |
| CIM | None |
| Platform / OS | Platform-independent: PyMISP is pure Python, no OS binaries. Confirm after build. |
| Python | Python 3 only (`python.version = python3`, `python.required = 3.13`) |
| FIPS / FedRAMP | Don't claim it unless you've tested for it |
| Arch-specific libs | None expected. If AppInspect flags `aarch64`, see UCC's OS-dependent-libraries page. |

Why 10.2 is the floor: the latest PyMISP needs Python 3.10+, and Splunk only
offers 3.13 from 10.2 on. Anything older runs on 3.9, where PyMISP won't
import.

## Legal

| Field | Value |
|---|---|
| License | Apache-2.0 (`LICENSE`) |
| Source | Optional: link the repo |
| EULA | Standard, unless yours is custom (you) |
| Privacy | The app only sends the fields you choose to the MISP instance you configured. No telemetry. Say so here. |
| Export control | Standard open source; check your org's stance (you) |

## Assets: you

These aren't in the code package.

| Field | Requirement |
|---|---|
| App icon | `appserver/static/appIcon.png` (36x36) and `appIconAlt.png`; optionally a 2x version |
| Banner | Per the current Splunkbase spec |
| Screenshots | At least one: the config page, a `mispfusepush` search, the alert form, and the resulting MISP event are the obvious ones |
| Docs URL | Link the README / repo |
| Support | An email or an issues URL (you) |
| Video | Optional |

## The artifact

| Field | Value |
|---|---|
| Package | `mispfuse-2.0.0.tar.gz` from `make package` |
| AppInspect | Has to pass. `make appinspect`, or the AppInspect service/API. |
| Cloud vetting | Ask for Cloud compatibility during or after upload; it runs the cloud tag set. |

## Before you hit submit

- [ ] `app.conf`, `app.manifest`, and the tarball all read `2.0.0`.
- [ ] `make appinspect` is clean with `--included-tags cloud`.
- [ ] Icons and at least one screenshot are ready.
- [ ] Long description, release notes, and a support URL are written.
- [ ] The old plaintext API key from 1.x is rotated.
- [ ] You've tested it on a real 10.2+ instance against a real MISP 2.5 server.
