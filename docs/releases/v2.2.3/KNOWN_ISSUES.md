# Known limitations — 2.2.3

- Splunk Cloud installation remains subject to Splunk Cloud vetting for the
  exact package, even when local cloud-tag AppInspect validation passes.
- The UCC 6.5.3 generated Configuration-page Mako template may be reported by
  AppInspect as a future failure. It is generated framework code, not custom
  MISPFuse application logic.
- Operators should validate the package against their real MISP deployment
  and test every Splunk platform and deployment type claimed in a listing.
