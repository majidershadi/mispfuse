# AppInspect failure corrections

The local precert audit reported two failed checks.

## Custom configuration reload

`default/mispfuse_templates.conf` is an application-specific configuration
file. The source `app.conf` now declares:

```ini
[triggers]
reload.mispfuse_templates = simple
```

The source `server.conf` also includes the MISPFuse custom configuration files
in Search Head Cluster runtime replication.

## Compiled Python files

The previous release sequence cleaned the tree and then ran the test suite.
Those imports recreated `__pycache__` directories under `package/bin` before
UCC copied the package source.

The test target now sets `PYTHONDONTWRITEBYTECODE=1`, the build target removes
stale bytecode immediately before UCC generation, and `post_build.py` rejects
any `.pyc`, `.pyo`, or `__pycache__` content in the generated app.
