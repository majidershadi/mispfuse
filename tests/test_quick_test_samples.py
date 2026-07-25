from __future__ import annotations

import configparser
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN_DIR = ROOT / "package" / "bin"
sys.path.insert(0, str(BIN_DIR))

if "solnlib" not in sys.modules:
    solnlib = types.ModuleType("solnlib")
    solnlib.conf_manager = types.SimpleNamespace(
        ConfManager=object,
        ConfManagerException=Exception,
    )
    sys.modules["solnlib"] = solnlib

from mispfuse_lib import pusher, templates
from mispfuse_lib.client import CreatedEvent


class _Logger:
    def warning(self, *args):
        pass

    def error(self, *args):
        pass


class _Client:
    def __init__(self):
        self.events = []

    def validate_mapping(self, type_, category):
        return None

    def add_event(self, event):
        self.events.append(event)
        number = str(len(self.events))
        return CreatedEvent(number, "uuid-{}".format(number), event)


class QuickTestSamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = configparser.RawConfigParser()
        parser.read(ROOT / "package" / "default" / "mispfuse_templates.conf")
        cls.template_config = parser

    def test_readme_sample_fields_match_bundled_templates(self):
        cases = {
            "network_ioc": (
                [
                    {
                        "src_ip": "192.0.2.10",
                        "dest_ip": "203.0.113.10",
                        "domain": "ioc-one.example.com",
                        "url": "https://ioc-one.example.com/login",
                        "dest_host": "host-one.example.com",
                    },
                    {
                        "src_ip": "198.51.100.20",
                        "dest_ip": "203.0.113.20",
                        "domain": "ioc-two.example.com",
                        "url": "https://ioc-two.example.com/update",
                        "dest_host": "host-two.example.com",
                    },
                ],
                1,
                10,
            ),
            "file_hashes": (
                [
                    {
                        "md5": "418236f5ada5ad5f01964e4e01c53a6d",
                        "sha1": "b6a85a1e64c45f964ac3cc4b1d498565e4155767",
                        "sha256": "e476e52ab92888bd396e336e6265720f18038ca9e71bfcae6ab47ed74e67dbcc",
                        "file_name": "mispfuse-test-1.bin",
                    },
                    {
                        "md5": "9070a04b22839e59c027768d776eff81",
                        "sha1": "ed06bc34beffce5a76513bbcbcf4087010fa2205",
                        "sha256": "a4b1e7ce258087298d0443c3f022fdd462bbb00114774b2cfa328f09687ba8af",
                        "file_name": "mispfuse-test-2.bin",
                    },
                ],
                1,
                8,
            ),
            "email_phishing": (
                [
                    {
                        "src_email": "sender-one@example.com",
                        "dest_email": "soc@example.com",
                        "subject": "MISPFuse test message one",
                        "url": "https://phish-one.example.com/login",
                    },
                    {
                        "src_email": "sender-two@example.com",
                        "dest_email": "soc@example.com",
                        "subject": "MISPFuse test message two",
                        "url": "https://phish-two.example.com/login",
                    },
                ],
                1,
                8,
            ),
            "passthrough": (
                [
                    {
                        "ioc_value": "Manual review item one",
                        "comment": "Created by the MISPFuse quick test",
                    },
                    {
                        "ioc_value": "Manual review item two",
                        "comment": "Second test record",
                    },
                ],
                2,
                2,
            ),
        }

        for name, (records, expected_events, expected_attributes) in cases.items():
            with self.subTest(template=name):
                template = templates.Template(name, self.template_config[name])
                client = _Client()
                results = pusher.push(
                    records,
                    template,
                    client,
                    pusher.Options(),
                    _Logger(),
                )
                self.assertEqual(len(results), expected_events)
                self.assertEqual(sum(result.count for result in results), expected_attributes)


if __name__ == "__main__":
    unittest.main()
