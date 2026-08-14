# Known limitations — 2.2.0

- Splunk 9.x is not claimed. The smallest supported and tested Enterprise
  family for this release is 10.0.
- Python 3.9 is selected through the legacy `python.version = python3` setting
  on Splunk 10.0/10.1. Splunk 10.2+ uses `python.required` and prefers 3.13.
- `splunk-sdk` 2.1.1 is published only as a pure-Python source distribution;
  it is hash-locked, and the final package is scanned for native binaries.
- Splunk Cloud availability depends on approval and vetting of the exact
  uploaded package; a local cloud-tag AppInspect pass is not publication.
- AppInspect 4.3.0 reports one `FUTURE_FAILURE` for the UCC 6.5.3-generated
  `appserver/templates/base.html`. The Configuration view currently references
  that template, so it cannot be removed without replacing the generated UCC
  page. It is not a current AppInspect failure, but must be addressed before a
  Splunk release that removes custom Mako templates.
- End-to-end pushes require a reachable MISP test instance and valid account.
