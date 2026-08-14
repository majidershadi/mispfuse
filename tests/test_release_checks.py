from __future__ import annotations

import configparser
import importlib.util
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("post_build_under_test", ROOT / "post_build.py")
if spec is None or spec.loader is None:
    raise RuntimeError("unable to load post_build.py")
post_build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(post_build)


class ReleaseChecksTest(unittest.TestCase):
    def test_source_dependencies_are_exact_and_hash_locked(self):
        self.assertEqual(post_build._check_locked_dependencies(str(ROOT)), [])

    def test_test_dependencies_match_runtime_lock(self):
        runtime = self._read_exact_versions(ROOT / "package" / "lib" / "requirements.txt")
        test = self._read_exact_versions(ROOT / "requirements-test.txt")
        self.assertEqual(test, runtime)

    def test_build_dependencies_are_separate_from_runtime_test_lock(self):
        lines = {
            line.strip()
            for line in (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertNotIn("-r requirements-test.txt", lines)
        self.assertIn("splunk-add-on-ucc-framework==6.5.3", lines)
        self.assertIn("splunk-appinspect==4.3.0", lines)

    def test_generated_ucc_build_number_is_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            default = Path(temp) / "default"
            default.mkdir()
            build = str(int(time.time()))
            (default / "app.conf").write_text(
                "[launcher]\n"
                "version = 2.2.3\n"
                "\n"
                "[install]\n"
                f"build = {build}\n"
                "\n"
                "[package]\n"
                "id = mispfuse\n"
                "check_for_updates = true\n"
                "\n"
                "[ui]\n"
                "label = MISPFuse\n",
                encoding="utf-8",
            )
            self.assertEqual(
                post_build._check_identity(str(ROOT), temp),
                [],
            )

    def test_invalid_generated_build_number_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            default = Path(temp) / "default"
            default.mkdir()
            (default / "app.conf").write_text(
                "[launcher]\n"
                "version = 2.2.3\n"
                "\n"
                "[install]\n"
                "build = release-2200\n"
                "\n"
                "[package]\n"
                "id = mispfuse\n"
                "check_for_updates = true\n"
                "\n"
                "[ui]\n"
                "label = MISPFuse\n",
                encoding="utf-8",
            )
            errors = post_build._check_identity(str(ROOT), temp)
            self.assertIn(
                "generated app.conf install build is not a positive integer",
                errors,
            )

    def test_source_app_conf_does_not_pin_ucc_build_number(self):
        parser = configparser.RawConfigParser(interpolation=None)
        parser.read(ROOT / "package" / "default" / "app.conf")
        self.assertFalse(parser.has_option("install", "build"))

    def test_ucc_footer_is_hidden(self):
        import json

        config = json.loads((ROOT / "globalConfig.json").read_text(encoding="utf-8"))
        meta = config["meta"]
        self.assertIs(meta.get("hideUCCVersion"), True)
        self.assertIs(meta.get("showFooter"), False)

    def test_declared_python_versions_are_dual_runtime(self):
        import json

        config = json.loads((ROOT / "globalConfig.json").read_text(encoding="utf-8"))
        self.assertEqual(config["meta"]["supportedPythonVersion"], ["3.9", "3.13"])

    def test_manifest_targets_supported_splunk_9x_range(self):
        import json

        manifest = json.loads(
            (ROOT / "package" / "app.manifest").read_text(encoding="utf-8")
        )
        self.assertEqual(
            manifest["platformRequirements"]["splunk"]["Enterprise"],
            ">=9.0.0",
        )

    def test_legacy_selector_is_normalized_to_python3(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "commands.conf"
            path.write_text(
                "[mispfusepush]\n"
                "filename = mispfuse_command_logic.py\n"
                "python.version = python3.9\n"
                "python.required = 3.9, 3.13\n",
                encoding="utf-8",
            )
            errors = post_build._normalize_legacy_python_version(
                str(path),
                lambda section: section == "mispfusepush",
                "MISPFuse command",
            )
            self.assertEqual(errors, [])

            parser = configparser.RawConfigParser(interpolation=None)
            parser.read(path)
            self.assertEqual(
                parser.get("mispfusepush", "python.version"),
                "python3",
            )
            self.assertEqual(
                post_build._check(
                    str(path),
                    lambda section: section == "mispfusepush",
                    "MISPFuse command",
                ),
                [],
            )

    def test_package_source_parses_as_python37(self):
        paths = [ROOT / "post_build.py"]
        paths.extend((ROOT / "package" / "bin").rglob("*.py"))
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                post_build._parse_python37(
                    path.read_text(encoding="utf-8"), str(path)
                )

    def test_post_build_python37_syntax_gate(self):
        self.assertEqual(post_build._check_python37_syntax(str(ROOT)), [])

    @staticmethod
    def _read_exact_versions(path: Path) -> dict[str, str]:
        versions: dict[str, str] = {}
        logical = ""
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("--") and not logical:
                continue
            if line.endswith("\\"):
                logical += line[:-1].strip() + " "
                continue
            logical += line
            requirement = logical.split(" --hash=", 1)[0].strip()
            logical = ""
            if requirement.startswith("-"):
                continue
            name, separator, version = requirement.partition("==")
            if not separator:
                raise AssertionError(f"dependency is not exact in {path}: {requirement}")
            versions[name.lower()] = version.strip()
        return versions

    def test_compiled_python_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            cache = Path(temp) / "bin" / "__pycache__"
            cache.mkdir(parents=True)
            (cache / "module.cpython-313.pyc").write_bytes(b"bytecode")
            errors = post_build._check_no_compiled_python(temp)
        self.assertEqual(len(errors), 1)
        self.assertIn("module.cpython-313.pyc", errors[0])

    def test_clean_tree_passes_compiled_python_check(self):
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / "module.py").write_text(
                "value = 1\n",
                encoding="utf-8",
            )
            self.assertEqual(
                post_build._check_no_compiled_python(temp),
                [],
            )

    def test_custom_template_conf_reload_and_replication_are_declared(self):
        app_parser = configparser.RawConfigParser(interpolation=None)
        app_parser.read(ROOT / "package" / "default" / "app.conf")
        self.assertEqual(
            app_parser.get("triggers", "reload.mispfuse_templates"),
            "simple",
        )

        server_parser = configparser.RawConfigParser(interpolation=None)
        server_parser.read(ROOT / "package" / "default" / "server.conf")
        for conf_name in (
            "mispfuse_account",
            "mispfuse_settings",
            "mispfuse_templates",
        ):
            self.assertTrue(
                server_parser.getboolean(
                    "shclustering",
                    f"conf_replication_include.{conf_name}",
                )
            )

    def test_native_binary_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            lib = Path(temp) / "lib"
            lib.mkdir()
            (lib / "native.cpython-313-x86_64-linux-gnu.so").write_bytes(b"ELF")
            errors = post_build._check_no_native_binaries(temp)
        self.assertEqual(len(errors), 1)
        self.assertIn("native.cpython-313-x86_64-linux-gnu.so", errors[0])

    def test_clean_tree_passes_native_check(self):
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / "module.py").write_text("value = 1\n", encoding="utf-8")
            self.assertEqual(post_build._check_no_native_binaries(temp), [])


if __name__ == "__main__":
    unittest.main()
