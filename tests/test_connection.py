from __future__ import annotations

import importlib
import ssl
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

BIN_DIR = Path(__file__).resolve().parents[1] / "package" / "bin"
sys.path.insert(0, str(BIN_DIR))
connection = importlib.import_module("mispfuse_lib.connection")


class FakeClient:
    def __init__(self, url, key, verify_ssl=True, proxies=None, timeout=None):
        self.args = (url, key, verify_ssl, proxies, timeout)

    def test_connection(self):
        return {"version": "2.5.12", "type_count": 42}


class ConnectionHelpersTest(unittest.TestCase):
    def test_normalize_url_keeps_subpath_and_removes_trailing_slash(self):
        self.assertEqual(
            connection.normalize_misp_url(" HTTPS://misp.example/MISP/ "),
            "https://misp.example/MISP",
        )

    def test_normalize_url_rejects_embedded_credentials(self):
        with self.assertRaisesRegex(connection.ConnectionTestError, "embedded"):
            connection.normalize_misp_url("https://user:pass@misp.example")

    def test_normalize_url_rejects_query(self):
        with self.assertRaisesRegex(connection.ConnectionTestError, "query"):
            connection.normalize_misp_url("https://misp.example/?x=1")

    def test_masked_secret_detection(self):
        self.assertTrue(connection.is_masked_secret("********"))
        self.assertTrue(connection.is_masked_secret("••••••••"))
        self.assertFalse(connection.is_masked_secret("abc*def"))

    def test_edit_reuses_existing_key_for_masked_placeholder(self):
        resolved = connection.resolve_account_values(
            {
                "misp_url": "https://new.example",
                "misp_key": "********",
                "verify_ssl": "0",
            },
            existing={
                "misp_url": "https://old.example",
                "misp_key": "real-key",
                "verify_ssl": True,
            },
        )
        self.assertEqual(resolved["misp_key"], "real-key")
        self.assertFalse(resolved["verify_ssl"])

    def test_create_rejects_missing_key(self):
        with self.assertRaisesRegex(connection.ConnectionTestError, "API key"):
            connection.resolve_account_values(
                {"misp_url": "https://misp.example", "misp_key": ""}
            )

    def test_success_uses_runtime_client_and_timeout(self):
        with patch.object(connection, "MispClient", FakeClient):
            result = connection.test_misp_connection(
                "https://misp.example/",
                "secret",
                verify_ssl=True,
                proxies={"https": "http://proxy:8080"},
            )
        self.assertEqual(result["version"], "2.5.12")
        self.assertEqual(result["type_count"], 42)
        self.assertEqual(result["url"], "https://misp.example")

    def test_tls_error_is_user_friendly_and_does_not_leak_key(self):
        class TLSFailingClient:
            def __init__(self, *args, **kwargs):
                raise connection.urllib3_exceptions.SSLError("secret bad cert")

        with patch.object(connection, "MispClient", TLSFailingClient):
            with self.assertRaises(connection.ConnectionTestError) as raised:
                connection.test_misp_connection(
                    "https://misp.example", "secret", verify_ssl=True
                )
        self.assertIn("TLS certificate verification failed", str(raised.exception))
        self.assertNotIn("secret", str(raised.exception))

    def test_stdlib_tls_error_is_classified(self):
        error = connection._classify_failure(
            ssl.SSLError("bad certificate"), "https://misp.example", "secret"
        )
        self.assertIn("TLS certificate verification failed", str(error))


if __name__ == "__main__":
    unittest.main()
