#!/usr/bin/env python3
"""Run release checks against the UCC-generated app directory."""

from __future__ import annotations

import configparser
import json
import os
import re
import sys
from collections.abc import Callable

REQUIRED_VERSIONS = {"3.9", "3.13"}
LEGACY_PYTHON_VERSION = "python3"


def _load(path: str) -> configparser.RawConfigParser:
    parser = configparser.RawConfigParser(strict=False, interpolation=None)
    parser.optionxform = str
    with open(path, encoding="utf-8") as handle:
        parser.read_file(handle)
    return parser


def _versions(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}


def _check(
    path: str,
    select: Callable[[str], bool],
    description: str,
) -> list[str]:
    errors: list[str] = []
    if not os.path.exists(path):
        return [f"missing generated file: {path}"]

    parser = _load(path)
    selected = [section for section in parser.sections() if select(section)]
    if not selected:
        return [f"no {description} stanza found in {path}"]

    for section in selected:
        configured = parser.get(section, "python.required", fallback="")
        configured_versions = _versions(configured)
        if configured_versions != REQUIRED_VERSIONS:
            errors.append(
                f"{path} [{section}] has python.required={configured!r}; "
                "expected exactly 3.9, 3.13"
            )
        else:
            print(
                "  verified python.required includes 3.9 and 3.13 "
                f"in {os.path.basename(path)} [{section}]"
            )
        legacy = parser.get(section, "python.version", fallback="")
        if legacy != LEGACY_PYTHON_VERSION:
            errors.append(
                f"{path} [{section}] has python.version={legacy!r}; "
                "expected python3 for Splunk 10.0/10.1 compatibility"
            )
        else:
            print(
                "  verified python.version=python3 in "
                f"{os.path.basename(path)} [{section}]"
            )
    return errors


def _check_custom_account_handler(out_dir: str) -> list[str]:
    """Verify that UCC wired the custom connection validator into account CRUD."""

    bin_dir = os.path.join(out_dir, "bin")
    custom_module = os.path.join(bin_dir, "mispfuse_account_validator_rh.py")
    if not os.path.exists(custom_module):
        return [f"missing custom account validator module: {custom_module}"]

    generated_handlers: list[str] = []
    if os.path.isdir(bin_dir):
        for filename in os.listdir(bin_dir):
            if (
                not filename.endswith(".py")
                or filename == os.path.basename(custom_module)
            ):
                continue
            path = os.path.join(bin_dir, filename)
            try:
                with open(path, encoding="utf-8") as handle:
                    content = handle.read()
            except OSError:
                continue
            compact = "".join(content.split())
            if "SingleModel(" in content and (
                'config_name="account"' in compact
                or "config_name='account'" in compact
            ):
                generated_handlers.append(path)

    if not generated_handlers:
        return [f"no generated UCC account REST handler found in {bin_dir}"]

    for path in generated_handlers:
        with open(path, encoding="utf-8") as handle:
            content = handle.read()
        compact = "".join(content.split())
        if (
            "frommispfuse_account_validator_rhimportMispAccountValidator"
            in compact
            and "handler=MispAccountValidator" in compact
        ):
            print(
                "  verified custom MISP account connection validator in "
                f"{os.path.basename(path)}"
            )
            return []

    return [
        "generated account REST handler does not use "
        "mispfuse_account_validator_rh.MispAccountValidator"
    ]



_COMPILED_PYTHON_SUFFIXES = (".pyc", ".pyo")


def _check_no_compiled_python(out_dir: str) -> list[str]:
    offenders: list[str] = []
    for current, directories, files in os.walk(out_dir):
        for directory in directories:
            if directory == "__pycache__":
                offenders.append(
                    os.path.relpath(os.path.join(current, directory), out_dir)
                )
        for filename in files:
            if filename.lower().endswith(_COMPILED_PYTHON_SUFFIXES):
                offenders.append(
                    os.path.relpath(os.path.join(current, filename), out_dir)
                )
    if offenders:
        return [
            "compiled Python content found: {}".format(
                ", ".join(sorted(set(offenders)))
            )
        ]
    print("  verified package contains no compiled Python files")
    return []


_NATIVE_SUFFIXES = (
    ".so",
    ".pyd",
    ".dll",
    ".dylib",
    ".a",
    ".lib",
    ".exe",
)


def _check_no_native_binaries(out_dir: str) -> list[str]:
    offenders: list[str] = []
    for current, _, files in os.walk(out_dir):
        for filename in files:
            lower = filename.lower()
            if lower.endswith(_NATIVE_SUFFIXES):
                offenders.append(os.path.relpath(os.path.join(current, filename), out_dir))
    if offenders:
        return [
            "platform-specific binary content found: {}".format(
                ", ".join(sorted(offenders))
            )
        ]
    print("  verified package contains no native binary files")
    return []


def _check_locked_dependencies(source_root: str) -> list[str]:
    path = os.path.join(source_root, "package", "lib", "requirements.txt")
    if not os.path.exists(path):
        return [f"missing runtime requirements file: {path}"]
    errors: list[str] = []
    with open(path, encoding="utf-8") as handle:
        lines = handle.readlines()
    if not any(line.strip() == "--require-hashes" for line in lines):
        errors.append("runtime requirements do not enable --require-hashes")
    if not any(line.strip() == "--only-binary=:all:" for line in lines):
        errors.append("runtime requirements do not require wheel distributions")
    joined = "".join(lines)
    for name in (
        "defusedxml",
        "deprecation",
        "packaging",
        "PySocks",
        "sortedcontainers",
        "solnlib",
        "splunk-sdk",
        "splunktaucclib",
        "urllib3",
    ):
        pattern = re.compile(
            r"(?mi)^" + re.escape(name) + r"==[^\s\\]+\s+\\\s*$"
        )
        if not pattern.search(joined):
            errors.append(f"dependency {name} is not exactly pinned")
    if "pymisp" in joined.lower() or "requests==" in joined.lower():
        errors.append("removed PyMISP/requests dependency unexpectedly remains")
    if not errors:
        print("  verified exact, hash-locked pure-Python dependency closure")
    return errors


def _check_identity(source_root: str, out_dir: str) -> list[str]:
    expected_id = "mispfuse"
    expected_label = "MISPFuse"
    expected_version = "2.2.0"
    errors: list[str] = []

    app_conf = os.path.join(out_dir, "default", "app.conf")
    parser = _load(app_conf)
    if parser.get("package", "id", fallback="") != expected_id:
        errors.append("generated app.conf package id is not mispfuse")
    if parser.get("ui", "label", fallback="") != expected_label:
        errors.append("generated app.conf UI label is not MISPFuse")
    if parser.get("launcher", "version", fallback="") != expected_version:
        errors.append("generated app.conf launcher version is not 2.2.0")
    generated_build = parser.get("install", "build", fallback="").strip()
    if not generated_build.isdigit() or int(generated_build) <= 0:
        errors.append(
            "generated app.conf install build is not a positive integer"
        )
    if parser.get("package", "check_for_updates", fallback="") not in ("1", "true"):
        errors.append("generated app.conf does not enable Splunkbase update checks")

    global_path = os.path.join(source_root, "globalConfig.json")
    with open(global_path, encoding="utf-8") as handle:
        global_config = json.load(handle)
    meta = global_config.get("meta", {})
    if meta.get("name") != expected_id:
        errors.append("globalConfig meta.name is not mispfuse")
    if meta.get("displayName") != expected_label:
        errors.append("globalConfig displayName is not MISPFuse")
    if meta.get("version") != expected_version:
        errors.append("globalConfig version is not 2.2.0")
    if meta.get("checkForUpdates") is not True:
        errors.append("globalConfig does not enable Splunkbase update checks")

    manifest_path = os.path.join(source_root, "package", "app.manifest")
    with open(manifest_path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    manifest_version = (
        manifest.get("info", {}).get("id", {}).get("version")
    )
    if manifest_version != expected_version:
        errors.append("app.manifest version is not 2.2.0")
    enterprise = (
        manifest.get("platformRequirements", {})
        .get("splunk", {})
        .get("Enterprise")
    )
    if enterprise != ">=10.0":
        errors.append("app.manifest Splunk Enterprise requirement is not >=10.0")

    if not errors:
        print(
            "  verified app id, label, version, and generated build "
            f"{generated_build}"
        )
    return errors

def main(out_dir: str) -> int:
    default_dir = os.path.join(out_dir, "default")
    print(f"Verifying generated Python runtime declarations in {default_dir}")

    errors: list[str] = []
    errors += _check(
        os.path.join(default_dir, "commands.conf"),
        lambda section: section == "mispfusepush",
        "MISPFuse command",
    )
    errors += _check(
        os.path.join(default_dir, "alert_actions.conf"),
        lambda section: section == "mispfuse_push",
        "MISPFuse alert action",
    )
    errors += _check(
        os.path.join(default_dir, "restmap.conf"),
        lambda section: section.startswith(("admin_external:", "script:")),
        "Python REST handler",
    )
    errors += _check_custom_account_handler(out_dir)
    source_root = os.path.dirname(os.path.abspath(__file__))
    errors += _check_no_compiled_python(out_dir)
    errors += _check_no_native_binaries(out_dir)
    errors += _check_locked_dependencies(source_root)
    errors += _check_identity(source_root, out_dir)

    if errors:
        print("\nRelease checks failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        print(
            "\nCorrect the reported release-check failures and rebuild.",
            file=sys.stderr,
        )
        return 1

    print("Release checks passed: Python 3.9/3.13 declarations, legacy "
          "python3 fallback, custom validator, identity, locked dependencies, "
          "no compiled Python, and no native binaries.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
