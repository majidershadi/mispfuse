# Splunkbase listing draft

## Identity

- Type: App
- Title: MISPFuse
- Package ID: `mispfuse`
- Version: 2.2.2
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

- Uses the full semantic-version range `>=9.3.0` identified by Splunkbase's
  online SLIM validator as an accepted 9.x compatibility boundary.
- Keeps the explicit `python.version = python3.9` selector for Splunk 9.3
  through 10.1.
- Retained Python 3.9 and 3.13 declarations for Splunk 10.2 and later.
- Added generated-config regression checks for commands, alert actions, and
  REST handlers.
- Preserved encrypted credentials, save-time MISP validation, the direct MISP
  client, templates, SPL command, alert action, and hardened packaging.

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
