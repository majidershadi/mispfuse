# MISPFuse 2.2.3 release record

Version 2.2.3 is the corrective Splunkbase release for the online SLIM
validator's Splunk Enterprise 9.0 compatibility boundary. The manifest uses
the full semantic-version constraint `>=9.0.0`.

The release artifact is `mispfuse-2.2.3.tar.gz`. Verify it against
`MISPFuse-2.2.3-SHA256.txt` before uploading it to Splunkbase.

This release does not only change metadata. It tests the complete locked
runtime dependency closure and unit suite on Python 3.7, 3.9, and 3.13.
