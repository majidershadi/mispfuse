# Known limitations — 2.2.2

- The Splunkbase online validator remains authoritative; a local AppInspect
  pass cannot guarantee portal approval.
- The UCC 6.5.3 Configuration page produces one AppInspect future failure for
  its generated Mako base template.
- Python 3.7 and Splunk Enterprise 9.0 through 9.2 are intentionally unsupported.
- A live MISP server is required for end-to-end command and alert-action tests.
- Splunk Cloud deployment requires vetting for this exact package.
