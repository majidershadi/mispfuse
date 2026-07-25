#!/usr/bin/env python3
"""Force Python 3.13 for the command and the alert action.

UCC writes `python.version = python3` into commands.conf and
alert_actions.conf, and on Splunk 10.2+ that still lands on 3.9 unless you
say otherwise. PyMISP needs 3.10+, so we add `python.required = 3.13` to the
right stanzas. Run it between `ucc-gen build` and `ucc-gen package`.

    python3 post_build.py output/mispfuse
"""
import configparser
import os
import sys

PATCHES = {
    "commands.conf": ["mispfusepush"],
    "alert_actions.conf": ["mispfuse_push"],
}
PY_REQUIRED = "3.13"


def patch(conf_path, stanzas):
    if not os.path.exists(conf_path):
        print("  skip (not found): {}".format(conf_path))
        return
    parser = configparser.RawConfigParser(strict=False)
    parser.optionxform = str  # preserve key case
    parser.read(conf_path)
    changed = False
    for stanza in stanzas:
        if not parser.has_section(stanza):
            print("  warn: [{}] not in {}".format(stanza, conf_path))
            continue
        if parser.get(stanza, "python.required", fallback=None) != PY_REQUIRED:
            parser.set(stanza, "python.required", PY_REQUIRED)
            changed = True
            print("  set python.required={} in [{}]".format(PY_REQUIRED, stanza))
    if changed:
        with open(conf_path, "w") as fh:
            parser.write(fh, space_around_delimiters=True)


def main(out_dir):
    default_dir = os.path.join(out_dir, "default")
    print("Patching python.required in {}".format(default_dir))
    for fname, stanzas in PATCHES.items():
        patch(os.path.join(default_dir, fname), stanzas)
    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
