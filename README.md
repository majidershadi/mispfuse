# MISPFuse

MISPFuse sends selected Splunk search results to MISP as events and attributes.
It provides an SPL command for manual pushes and a custom alert action for
scheduled searches. Field-to-attribute mappings are stored in templates, so the
same search can be reused without hard-coding MISP types in SPL.

MISPFuse is an independent project. It is not affiliated with or endorsed by
Splunk or the MISP Project.

## What is included

- A Configuration page for MISP accounts, proxy settings, and logging.
- Encrypted storage for MISP API keys.
- A connection check before an account is created or changed.
- The `mispfusepush` custom search command.
- The **MISPFuse - Push to MISP** alert action.
- Four templates: `network_ioc`, `file_hashes`, `email_phishing`, and
  `passthrough`.

## Project evolution

This repository preserves seven stages of MISPFuse:

- `v1.5.0-legacy`: traditional IP-only SPL prototype;
- `v2.0.0-ucc`: UCC migration and alert-action milestone;
- `v2.1.0`: hardened Splunk 10.2/Python 3.13 engineering milestone;
- `v2.2.0`: Python 3.9/3.13 compatibility milestone targeting Splunk 10.0+;
- `v2.2.1`: Splunk 9.4 range-validation milestone;
- `v2.2.2`: Splunk 9.3 range-validation milestone;
- `v2.2.3`: current release with genuine Splunk 9.0+/Python 3.7 compatibility.

See [Engineering evolution](docs/EVOLUTION.md) and the
[feature matrix](docs/FEATURE_MATRIX.md).

## Requirements

| Component | Supported version |
|---|---|
| Splunk Enterprise | 9.0.0 or later |
| Splunk Python runtime | 3.7, 3.9, or 3.13 |
| MISP | 2.5.x |
| UCC framework, build only | 6.5.3 |

Splunk Cloud deployment still requires cloud-tag AppInspect validation and
Splunk Cloud vetting for this exact package.

## Install and configure

1. Install `mispfuse-2.2.3.tar.gz` from **Apps > Manage Apps > Install app from
   file**.
2. Restart Splunk.
3. Open **MISPFuse > Configuration**.
4. Add a MISP instance with its base URL, API key, and TLS setting.
5. Configure the proxy only when the MISP server is reached through one.

The account is saved only after MISPFuse can authenticate, read the MISP server
version, read the current API user, and fetch `attributes/describeTypes.json`.
The connection check does not create an event.

## Quick tests

These searches create real MISP events. Use a test MISP instance or a test
organisation. The examples keep distribution at `0` and publishing disabled.
Replace `lab` with the exact account name configured in MISPFuse.

The sample indicators use documentation-only IP ranges and domains. They are
not intended to represent active threats.

### Test the custom search command

Run each search from the Splunk Search page. A successful push returns a summary
row containing `misp_status`, `misp_event_id`, `misp_event_uuid`, and
`misp_attributes`.

#### Network IOC template

This creates one MISP event with ten attributes.

```spl
| makeresults count=2
| streamstats count AS sample
| eval src_ip=if(sample=1,"192.0.2.10","198.51.100.20"),
       dest_ip=if(sample=1,"203.0.113.10","203.0.113.20"),
       domain=if(sample=1,"ioc-one.example.com","ioc-two.example.com"),
       url=if(sample=1,"https://ioc-one.example.com/login","https://ioc-two.example.com/update"),
       dest_host=if(sample=1,"host-one.example.com","host-two.example.com")
| fields - _time sample
| mispfusepush account=lab template=network_ioc event_info="MISPFuse network test" distribution=0 tags="mispfuse:test" publish=false
```

#### File hash template

This creates one MISP event with eight attributes.

```spl
| makeresults count=2
| streamstats count AS sample
| eval md5=if(sample=1,"418236f5ada5ad5f01964e4e01c53a6d","9070a04b22839e59c027768d776eff81"),
       sha1=if(sample=1,"b6a85a1e64c45f964ac3cc4b1d498565e4155767","ed06bc34beffce5a76513bbcbcf4087010fa2205"),
       sha256=if(sample=1,"e476e52ab92888bd396e336e6265720f18038ca9e71bfcae6ab47ed74e67dbcc","a4b1e7ce258087298d0443c3f022fdd462bbb00114774b2cfa328f09687ba8af"),
       file_name=if(sample=1,"mispfuse-test-1.bin","mispfuse-test-2.bin")
| fields - _time sample
| mispfusepush account=lab template=file_hashes event_info="MISPFuse file hash test" distribution=0 tags="mispfuse:test" publish=false
```

#### Email and phishing template

This creates one MISP event with eight attributes.

```spl
| makeresults count=2
| streamstats count AS sample
| eval src_email=if(sample=1,"sender-one@example.com","sender-two@example.com"),
       dest_email="soc@example.com",
       subject=if(sample=1,"MISPFuse test message one","MISPFuse test message two"),
       url=if(sample=1,"https://phish-one.example.com/login","https://phish-two.example.com/login")
| fields - _time sample
| mispfusepush account=lab template=email_phishing event_info="MISPFuse phishing test" distribution=0 tags="mispfuse:test" publish=false
```

#### Generic text template

The `passthrough` template uses `per_row` grouping, so this search creates two
MISP events with one text attribute each.

```spl
| makeresults count=2
| streamstats count AS sample
| eval ioc_value=if(sample=1,"Manual review item one","Manual review item two"),
       comment=if(sample=1,"Created by the MISPFuse quick test","Second test record")
| fields - _time sample
| mispfusepush account=lab template=passthrough event_info="MISPFuse text test" distribution=0 tags="mispfuse:test" publish=false
```

### Test the alert action from SPL

Splunk's `sendalert` command invokes the same alert-action code used by a saved
search. Disable search preview before running these examples; Splunk can invoke
`sendalert` more than once while preview is enabled. The user role also needs
the `run_sendalert` capability.

For each quick-test search above, replace the final `mispfusepush` line with the
matching line below.

Network IOC:

```spl
| sendalert mispfuse_push param.account="lab" param.template="network_ioc" param.event_info="MISPFuse network alert test" param.distribution="0" param.tags="mispfuse:test" param.publish="false"
```

File hashes:

```spl
| sendalert mispfuse_push param.account="lab" param.template="file_hashes" param.event_info="MISPFuse file hash alert test" param.distribution="0" param.tags="mispfuse:test" param.publish="false"
```

Email and phishing:

```spl
| sendalert mispfuse_push param.account="lab" param.template="email_phishing" param.event_info="MISPFuse phishing alert test" param.distribution="0" param.tags="mispfuse:test" param.publish="false"
```

Generic text:

```spl
| sendalert mispfuse_push param.account="lab" param.template="passthrough" param.event_info="MISPFuse text alert test" param.distribution="0" param.tags="mispfuse:test" param.publish="false"
```

### Test a scheduled alert

Use the data-producing part of one sample search and stop before the
`mispfusepush` or `sendalert` command.

1. Run the search and confirm that it returns the expected fields.
2. Select **Save As > Alert**.
3. Use a scheduled alert and trigger it when the number of results is greater
   than zero.
4. Set the alert to trigger once for the result set, not once per result.
5. Add **MISPFuse - Push to MISP** as the alert action.
6. Select the MISP account and the template that matches the search fields.
7. Set **Distribution** to `0`, **Publish event(s)** to **No**, and add a test
   tag such as `mispfuse:test`.
8. Let the alert run once, verify the event in MISP, then disable or delete the
   test alert.

Do not include `mispfusepush` or `sendalert` in the saved alert search. The
configured alert action performs the push.

## Templates

Templates are stored in `default/mispfuse_templates.conf`. Each stanza defines
MISP event defaults and one or more field mappings.

```ini
[example]
grouping = single_event
event_info = Example event from Splunk
distribution = 0
threat_level_id = 4
analysis = 0
publish = 0
to_ids = 1
tags = source:splunk
strict = 0
map.1 = src_ip:ip-src:Network activity:1:0
```

Mapping syntax:

```text
map.N = source_field:type:category:to_ids:disable_correlation[:comment_field]
```

The MISP attribute type is required. The category can be left empty. Before an
attribute is sent, MISPFuse compares the type and category with the connected
server's `describeTypes` response.

Template grouping modes:

| Mode | Result |
|---|---|
| `single_event` | All search rows become one MISP event. |
| `per_row` | Each search row becomes a separate MISP event. |
| `by_field` | Rows with the same field value become one event. |

The four included templates expect these fields:

| Template | Splunk fields |
|---|---|
| `network_ioc` | `src_ip`, `dest_ip`, `domain`, `url`, `dest_host` |
| `file_hashes` | `md5`, `sha1`, `sha256`, `file_name` |
| `email_phishing` | `src_email`, `dest_email`, `subject`, `url` |
| `passthrough` | `ioc_value`, optional `comment` |

Add a stanza to `mispfuse_templates.conf` for a new template. To expose it in
the alert-action dropdown, add the same template name to `globalConfig.json`
and rebuild the app.

## `mispfusepush` options

| Option | Required | Purpose |
|---|---:|---|
| `account` | yes | Configured MISP account name. |
| `template` | no | Mapping template; default is `network_ioc`. |
| `grouping` | no | Override `single_event`, `per_row`, or `by_field`. |
| `group_field` | for `by_field` | Field used to group rows. |
| `event_info` | no | Override the MISP event title. |
| `distribution` | no | MISP distribution value `0` through `4`. |
| `threat_level_id` | no | MISP threat level `1` through `4`. |
| `analysis` | no | MISP analysis state `0` through `2`. |
| `tags` | no | Comma-separated event tags. |
| `to_ids` | no | Override the template's `to_ids` setting. |
| `publish` | no | Publish the event after creation. |

Any option left unset inherits from the selected template.

## Security and packaging

- MISP API keys are stored through Splunk's encrypted credential storage.
- TLS certificate validation is enabled by default.
- Connection-test errors redact API keys and proxy credentials.
- MISP responses are limited to 8 MiB.
- HTTP redirects and automatic response decompression are disabled.
- Runtime dependencies are exact-version and SHA-256 hash locked.
- The release check rejects native files such as `.so`, `.pyd`, `.dll`, and
  `.dylib`.
- MISPFuse sends no telemetry to the publisher.

## Build from source

Use Python 3.13 for the UCC/AppInspect build environment and run the unit suite
under Python 3.7, Python 3.9, and Python 3.13 before packaging.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
# In separate Python 3.7, 3.9, and 3.13 environments:
python -m pip install -r requirements-test.txt
make test-python37
make test-python39
make test-python313
make package
```

For the full release gate, including AppInspect:

```bash
make release
```

`requirements-dev.txt` contains only UCC and AppInspect. Install
`requirements-test.txt` separately in each test interpreter; it mirrors the
exact shipped runtime dependency versions. Build and test dependencies are
kept apart because UCC 6.5.3 requires a newer `packaging` release than the
Python 3.7-compatible runtime lock.

The package is written to `mispfuse-2.2.3.tar.gz`.

## Project layout

```text
globalConfig.json                    UCC UI, command, and alert definition
post_build.py                        release checks after UCC generation
package/default/mispfuse_templates.conf
package/bin/mispfuse_command_logic.py
package/bin/mispfuse_push_logic.py
package/bin/mispfuse_account_validator_rh.py
package/bin/mispfuse_lib/            shared configuration, template, HTTP, and push code
package/lib/requirements.txt         hash-locked packaged dependencies
requirements-test.txt                 matching dependencies for local tests
tests/                               unit tests
```

## Troubleshooting

**The Configuration page reports a Python type error**

Confirm that Splunk Enterprise is 9.0.0 or later. Generated `commands.conf`,
`alert_actions.conf`, and `restmap.conf` must contain both
`python.version = python3` and `python.required = 3.9, 3.13`. Splunk 9.0-9.2
use the legacy selector with Python 3.7; newer releases select 3.9 or 3.13.

**The account cannot be saved**

The save-time test checks the URL, proxy, TLS chain, API key, current user,
server version, and `describeTypes`. Correct the displayed error and save again.

**`account not found`**

The account value in SPL or the alert action must exactly match the name under
**Configuration > MISP Instances**.

**`no mappable attributes`**

The search did not return fields used by the selected template, or all mapped
values were empty.

**MISP rejects an attribute**

Check the field value, MISP type, and category in the active template. Set
`strict = 1` while developing a template to skip mappings rejected by the
server taxonomy check.

## Upgrade from 1.x

Rotate any API key previously stored in a plaintext `keys.py` file. Version 2.x
uses Splunk encrypted credential storage and no longer reads that file.

## References

- [MISP project](https://www.misp-project.org/)
- [Splunk `makeresults` command](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/9.4/search-commands/makeresults)
- [Splunk `sendalert` command](https://help.splunk.com/?resourceId=SplunkCloud_SearchReference_Sendalert)
- [Splunk custom alert actions](https://dev.splunk.com/enterprise/docs/devtools/customalertactions)

## License

Apache License 2.0. See `LICENSE`.
