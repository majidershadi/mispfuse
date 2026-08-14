# Runtime dependencies

`package/lib/requirements.txt` contains the complete runtime dependency set.
Every package has an exact version and SHA-256 hash. Pip is instructed to use
wheels except for `splunk-sdk` 2.1.1, which is compatible with the tested Python
3.7, 3.9, and 3.13 runtimes. That SDK release is published only as a pure-Python source
distribution, so it has a package-specific source exception. The post-build
check rejects native binaries in the generated app regardless of origin.

`packaging` is pinned to 23.2 because it is the newest release in this closure
that supports Python 3.7. The full locked dependency set is installed and the
unit suite is executed under Python 3.7, 3.9, and 3.13 before release.

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
packaging-only hash directives. Install it in separate Python 3.7, 3.9, and
3.13 test environments. `requirements-dev.txt` contains only UCC and
AppInspect because UCC 6.5.3 requires `packaging>=25`, which intentionally
differs from the app's Python 3.7-compatible `packaging==23.2` runtime pin. A
release test checks that test versions remain synchronized with
`package/lib/requirements.txt` and that the build/runtime locks stay separate.
