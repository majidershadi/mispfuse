# Engineering evolution

## Stage 1: make the workflow possible

The traditional version is a direct Splunk `StreamingCommand`. Each incoming
result row becomes a new `MISPEvent`, one attribute is added, and PyMISP submits
the event.

That design was effective as a proof of concept because it had almost no
infrastructure. It also tied the implementation to one environment:

- MISP URL and key in `bin/keys.py`;
- TLS verification disabled;
- fixed organisation IDs;
- fixed default tag;
- IP-oriented type selection;
- one event and one attribute per row;
- published events by default;
- no alert action or configuration UI.

The source also accumulated a copied Python environment. The uploaded snapshot
contains more than a thousand compiled files, native extensions, Windows
executables, and multiple versions of several libraries.

## Stage 2: turn the script into a Splunk application

The intermediate version uses UCC to generate the Configuration page, REST
handlers, alert action, and command wrapper. The key moves into Splunk encrypted
credential storage. Accounts become selectable, and proxy/logging settings are
available.

The data model changes from hard-coded IP handling to templates:

```text
source field -> MISP type -> category -> to_ids -> correlation behavior
```

Three grouping modes address the one-event-per-row limitation:

- one event for the complete result set;
- one event per row;
- one event for each value of a selected field.

The same pusher is used by the SPL command and alert action.

This stage exposed the difference between an architecture that is conceptually
correct and a package that is release-ready. UCC schema limits, Python-runtime
selection, unpinned dependencies, template defaults, and packaging artifacts
all required further work.

## Stage 3: harden the application

The final version keeps the UCC configuration model but narrows the runtime
surface. PyMISP is replaced by a small client for four endpoints:

```text
GET  servers/getVersion
GET  users/view/me
GET  attributes/describeTypes.json
POST events/add
```

This removes the large transitive PyMISP/Requests dependency tree and makes it
possible to ship an exact, hash-locked, pure-Python dependency closure.

The final implementation also adds:

- save-time authentication and taxonomy checks;
- explicit type requirements for mappings;
- template-default inheritance in the alert UI;
- numeric mapping order;
- multivalue field support;
- proxy-credential encoding;
- API-key redaction;
- timeout and response-size controls;
- disabled redirects and decompression;
- release tests for identity, dependencies, bytecode, and native binaries;
- AppInspect-specific reload and Search Head Cluster settings.

## What should remain separate

The historical releases should not be rewritten to look like the final
application. Their value is that the limitations are visible and traceable.
Only security-sensitive material should be removed from the public snapshots:

- credentials;
- private infrastructure names;
- local configuration;
- compiled artifacts;
- copied virtual environments.

Functional improvements belong in later releases.

## Stage 4: make the hardened release backward compatible

Version 2.1.0 intentionally used Splunk SDK 3.0.0 and Python 3.13, which made
Splunk 10.2 the true minimum. Splunkbase's SLIM matrix rejected the corresponding
`>=10.2` manifest range. Lowering only the manifest would have created a false
compatibility claim.

Version 2.2.0 instead changes the runtime boundary first. It uses the newest
pre-3.0 Splunk SDK, tests the application on Python 3.9 and 3.13, keeps the
legacy `python.version = python3` selector for Splunk 10.0/10.1, and declares
`python.required = 3.9, 3.13` for Splunk 10.2+. Only after those changes does
the manifest move to Splunk Enterprise 10.0 or later.
