# MISPFuse 2.2.4 release record

Version 2.2.4 corrects the remaining SSAI SLIM catalog mismatch. The manifest
uses `>=8.0.0`, which directly intersects Splunk Packaging Toolkit 1.2.8's
bundled Enterprise catalog at 8.0.0.

The release artifact is `mispfuse-2.2.4.tar.gz`. Verify it against
`MISPFuse-2.2.4-SHA256.txt` before uploading it to Splunkbase.

The code and complete dependency closure are tested on Python 3.7, 3.9, and
3.13. Splunk Enterprise 8.x supports Python 3.7 and the app's explicit
`python.version = python3` selector.
