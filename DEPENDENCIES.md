# Runtime dependencies

`package/lib/requirements.txt` contains the complete runtime dependency set.
Every package has an exact version and SHA-256 hash. Pip is instructed to use
wheels except for `splunk-sdk` 2.1.1, the newest release compatible with Python
3.9 and 3.13. That SDK release is published only as a pure-Python source
distribution, so it has a package-specific source exception. The post-build
check rejects native binaries in the generated app regardless of origin.

PyMISP is not bundled. MISPFuse uses four MISP API operations—server version,
current user, `describeTypes`, and event creation—through a small urllib3
client. This keeps the package independent of operating-system and CPython
extension wheels.

The UCC runtime libraries currently require urllib3 1.x. MISPFuse disables
redirects and automatic decompression for MISP requests, sends
`Accept-Encoding: identity`, and limits responses to 8 MiB. Review the urllib3
pin when a compatible `splunktaucclib` release supports urllib3 2.x.


## Development and test environment

`requirements-test.txt` repeats the exact runtime versions without the
packaging-only hash directives. `requirements-dev.txt` includes that file, so
a single development install provides UCC, AppInspect, and the libraries
imported by the unit tests. A release test checks that the test versions remain
synchronized with `package/lib/requirements.txt`.
