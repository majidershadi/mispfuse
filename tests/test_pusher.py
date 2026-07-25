from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

BIN_DIR = Path(__file__).resolve().parents[1] / "package" / "bin"
sys.path.insert(0, str(BIN_DIR))
from mispfuse_lib import pusher
from mispfuse_lib.client import CreatedEvent


class FakeLogger:
    def warning(self, *args):
        pass
    def error(self, *args):
        pass


class FakeClient:
    def __init__(self):
        self.sent = []
    def validate_mapping(self, type_, category):
        return None
    def add_event(self, event):
        self.sent.append(event)
        return CreatedEvent("7", "uuid-7", event)


class PusherTest(unittest.TestCase):
    def test_builds_standard_misp_event_json(self):
        template = SimpleNamespace(
            grouping="single_event",
            event_info="IOCs from $host$",
            distribution=0,
            threat_level_id=4,
            analysis=0,
            publish=False,
            tags=["source:splunk"],
            default_to_ids=True,
            strict=True,
            mappings=[SimpleNamespace(
                field="src_ip", type="ip-src", category="Network activity",
                to_ids=None, disable_correlation=False, comment_field=None,
            )],
        )
        client = FakeClient()
        results = pusher.push(
            [{"host": "sensor1", "src_ip": "198.51.100.10"}],
            template,
            client,
            pusher.Options(),
            FakeLogger(),
        )
        self.assertTrue(results[0].ok)
        event = client.sent[0]
        self.assertEqual(event["info"], "IOCs from sensor1")
        self.assertEqual(event["Attribute"][0]["type"], "ip-src")
        self.assertTrue(event["Attribute"][0]["to_ids"])
        self.assertEqual(event["Tag"], [{"name": "source:splunk"}])

    def test_multivalue_field_creates_one_attribute_per_value(self):
        template = SimpleNamespace(
            grouping="single_event", event_info="IOCs", distribution=0,
            threat_level_id=4, analysis=0, publish=False, tags=[],
            default_to_ids=True, strict=True,
            mappings=[SimpleNamespace(
                field="domains", type="domain", category="Network activity",
                to_ids=None, disable_correlation=False, comment_field=None,
            )],
        )
        client = FakeClient()
        result = pusher.push(
            [{"domains": ["one.example", "two.example"]}], template, client,
            pusher.Options(), FakeLogger(),
        )[0]
        self.assertTrue(result.ok)
        self.assertEqual(
            [a["value"] for a in client.sent[0]["Attribute"]],
            ["one.example", "two.example"],
        )


if __name__ == "__main__":
    unittest.main()
