# MISPFuse 2.2.0 release record

This release preserves the hardened functionality from 2.1.0 while widening
the tested runtime boundary required for Splunkbase publication.

The release artifact is `mispfuse-2.2.0.tar.gz`. Build it from `main`, run the
unit suite under Python 3.9 and 3.13, run the UCC post-build verifier, and run
AppInspect 4.3.0 with precert and cloud tags. The GitHub release must contain
the exact validated tarball and its SHA-256 checksum.

See [release notes](RELEASE_NOTES.md) for the compatibility changes and
[known issues](KNOWN_ISSUES.md) for the remaining validation boundary.
