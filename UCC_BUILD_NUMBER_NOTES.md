# UCC-generated app build number

UCC 6.5.3 owns the generated `[install] build` value in `default/app.conf`.

During `ucc-gen build`, the framework creates a positive Unix timestamp and
writes it into the generated `app.conf`. A source value such as `build = 2100`
is overwritten during the merge.

MISPFuse therefore validates that the final generated build value is a positive
integer. It does not require a fixed value.

To inspect the final release build:

```bash
grep -A4 '^\[install\]' output/mispfuse/default/app.conf
```

The displayed build number must be retained in the package produced by the same
build run.
