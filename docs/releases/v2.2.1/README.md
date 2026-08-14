# MISPFuse 2.2.1 release record

Version 2.2.1 is the Splunkbase compatibility correction for the 2.2 series.
It preserves the v2.2.0 Python 3.9/3.13 implementation while expanding the
manifest to Splunk Enterprise 9.4 or later and explicitly selecting Python 3.9
on Splunk releases that do not understand `python.required`.

The release artifact is `mispfuse-2.2.1.tar.gz`. Build it from the `v2.2.1`
tag and verify its digest against `MISPFuse-2.2.1-SHA256.txt`.
