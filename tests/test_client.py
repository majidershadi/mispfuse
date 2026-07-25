from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parents[1] / "package" / "bin"
sys.path.insert(0, str(BIN_DIR))

from mispfuse_lib.client import CreatedEvent, MispApiError, MispClient


class FakeResponse:
    def __init__(self, status, payload):
        self.status = status
        self._raw = (
            payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        )
        self.released = False

    def read(self, amount, decode_content=False):
        return self._raw[:amount]

    def close(self):
        pass

    def release_conn(self):
        self.released = True


class FakeManager:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.responses.pop(0)


class MispClientTest(unittest.TestCase):
    def make_client(self, responses):
        client = object.__new__(MispClient)
        client._url = "https://misp.example"
        client._key = "secret"
        client._verify_ssl = True
        client._types = None
        client._timeout = None
        client._http = FakeManager(responses)
        return client

    def test_connection_checks_version_user_and_wrapped_taxonomy(self):
        client = self.make_client([
            FakeResponse(200, {"version": "2.5.12"}),
            FakeResponse(200, {"User": {"id": "1"}}),
            FakeResponse(
                200,
                {
                    "result": {
                        "types": ["ip-src"],
                        "categories": ["Network activity"],
                        "category_type_mappings": {
                            "Network activity": ["ip-src"]
                        },
                    }
                },
            ),
        ])
        result = client.test_connection()
        self.assertEqual(result, {"version": "2.5.12", "type_count": 1})
        self.assertEqual(client.taxonomy["types"], ["ip-src"])
        self.assertEqual(len(client._http.calls), 3)
        for _, _, kwargs in client._http.calls:
            self.assertFalse(kwargs["redirect"])
            self.assertFalse(kwargs["decode_content"])
            self.assertEqual(kwargs["headers"]["Accept-Encoding"], "identity")

    def test_legacy_unwrapped_taxonomy_remains_supported(self):
        client = self.make_client([
            FakeResponse(200, {"types": ["domain"], "category_type_mappings": {}})
        ])
        self.assertEqual(client.taxonomy["types"], ["domain"])

    def test_invalid_taxonomy_error_describes_expected_shape(self):
        client = self.make_client([FakeResponse(200, {"result": {"categories": []}})])
        with self.assertRaisesRegex(MispApiError, "result.types or types"):
            _ = client.taxonomy

    def test_add_event_wraps_payload_and_parses_id(self):
        client = self.make_client([
            FakeResponse(200, {"Event": {"id": "42", "uuid": "abc"}})
        ])
        created = client.add_event({"info": "test", "Attribute": []})
        self.assertIsInstance(created, CreatedEvent)
        self.assertEqual(created.id, "42")
        body = json.loads(client._http.calls[0][2]["body"].decode("utf-8"))
        self.assertEqual(body["Event"]["info"], "test")

    def test_http_error_does_not_include_api_key(self):
        client = self.make_client([FakeResponse(403, {"message": "Forbidden"})])
        with self.assertRaises(MispApiError) as raised:
            client._request("GET", "users/view/me")
        self.assertEqual(raised.exception.status, 403)
        self.assertNotIn("secret", str(raised.exception))

    def test_non_json_response_is_rejected(self):
        client = self.make_client([FakeResponse(200, b"<html>login</html>")])
        with self.assertRaisesRegex(MispApiError, "non-JSON"):
            client._request("GET", "servers/getVersion")


if __name__ == "__main__":
    unittest.main()
