# Splunkbase listing draft

## Identity

- Type: App
- Title: MISPFuse
- Package ID: `mispfuse`
- Version: 2.1.0
- License: Apache-2.0
- Suggested category: Threat Intelligence, or Security, Fraud & Compliance

Keep the title as **MISPFuse**. Splunkbase already provides the product context,
so the title does not need “for Splunk”, “App for Splunk”, or “Add-on for
Splunk”.

## Short description

Push selected Splunk search results to MISP as events and attributes using
server-validated templates, multiple MISP accounts, an SPL command, and an
alert action.

## Long description

MISPFuse publishes selected Splunk search results to MISP as events and
attributes. Mapping templates connect Splunk field names to MISP attribute
types. Before sending an attribute, the app checks its type and category against
the connected server's `describeTypes` response.

Analysts can push results in two ways:

- `mispfusepush` for an on-demand search;
- **MISPFuse - Push to MISP** for a saved search or alert.

Templates control event titles, grouping, distribution, threat level, analysis
state, tags, `to_ids`, publication state, categories, correlation, and comments.
MISPFuse supports one event for the complete result set, one event per result,
or grouping by a field value.

Administrators can configure multiple MISP accounts. API keys use Splunk's
encrypted credential storage. New and edited accounts are tested before they
are saved, including TLS, proxy access, authentication, server version, current
user, and the remote MISP attribute taxonomy.

MISPFuse does not collect MISP data into Splunk and does not provide scheduled
inputs. It sends only fields selected by the active template to the configured
MISP server. It sends no telemetry to the publisher.

MISPFuse is an independent community project and is not affiliated with or
endorsed by Splunk or the MISP Project.

## Release notes

- Changed the visible product name to MISPFuse.
- Added the complete Splunk icon and logo set.
- Replaced PyMISP with a small MISP REST client.
- Locked the runtime dependency set by version and SHA-256 hash.
- Added a release check that rejects native binaries.
- Corrected alert-action inheritance so blank values use template defaults.
- Required an explicit MISP type in every mapping.
- Kept save-time connection validation for MISP accounts.
- Added copy-and-run SPL examples for all four templates.

## Privacy

MISPFuse sends no telemetry, analytics, or diagnostics to the publisher. It
sends only template-selected Splunk result fields to the MISP server configured
by the administrator. API keys and proxy passwords use Splunk's encrypted
credential storage. Splunk may check Splunkbase for app updates because
`check_for_updates` is enabled; that check is handled by Splunk, not by
MISPFuse code.

## Publisher fields still required

- Support email
- Documentation URL
- Issue tracker or support portal
- Source repository
- Publisher legal or account name

## Screenshots

1. MISPFuse Overview.
2. Configuration with a saved account and no exposed API key.
3. Alert-action settings with template inheritance options.
4. A `mispfusepush` result showing the MISP event ID and UUID.
5. The matching MISP event with attributes and tags.

Remove API keys, session keys, internal hostnames, private addresses, user email
addresses, and production indicators from screenshots.
