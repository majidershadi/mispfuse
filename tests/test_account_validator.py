from __future__ import annotations

import importlib.util
import sys
import types
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


class FakeRestError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


class FakeAdminExternalHandler:
    def __init__(self):
        self.payload = {}
        self.callerArgs = SimpleNamespace(id=None)
        self.base_calls = []

    def getSessionKey(self):
        return "session-key"

    def handleList(self, conf_info):
        self.base_calls.append(("list", conf_info))
        return "listed"

    def handleCreate(self, conf_info):
        self.base_calls.append(("create", conf_info))
        return "created"

    def handleEdit(self, conf_info):
        self.base_calls.append(("edit", conf_info))
        return "edited"

    def handleRemove(self, conf_info):
        self.base_calls.append(("remove", conf_info))
        return "removed"


class FakeConfigError(Exception):
    pass


class FakeConnectionTestError(Exception):
    pass


def _load_handler_module():
    """Load the custom handler with small Splunk/UCC dependency stubs."""

    module_names = [
        "import_declare_test",
        "splunktaucclib",
        "splunktaucclib.rest_handler",
        "splunktaucclib.rest_handler.admin_external",
        "splunktaucclib.rest_handler.error",
        "mispfuse_lib",
        "mispfuse_lib.config",
        "mispfuse_lib.connection",
    ]
    previous = {name: sys.modules.get(name) for name in module_names}

    import_declare_test = types.ModuleType("import_declare_test")
    splunktaucclib = types.ModuleType("splunktaucclib")
    rest_handler = types.ModuleType("splunktaucclib.rest_handler")
    admin_external = types.ModuleType(
        "splunktaucclib.rest_handler.admin_external"
    )
    admin_external.AdminExternalHandler = FakeAdminExternalHandler
    error = types.ModuleType("splunktaucclib.rest_handler.error")
    error.RestError = FakeRestError

    mispfuse_lib = types.ModuleType("mispfuse_lib")
    mispfuse_lib.__path__ = []
    config = types.ModuleType("mispfuse_lib.config")
    config.ConfigError = FakeConfigError
    config.get_account = Mock()
    config.get_proxies = Mock(return_value={})
    connection = types.ModuleType("mispfuse_lib.connection")
    connection.ConnectionTestError = FakeConnectionTestError
    connection.resolve_account_values = Mock()
    connection.test_misp_connection = Mock()

    replacements = {
        "import_declare_test": import_declare_test,
        "splunktaucclib": splunktaucclib,
        "splunktaucclib.rest_handler": rest_handler,
        "splunktaucclib.rest_handler.admin_external": admin_external,
        "splunktaucclib.rest_handler.error": error,
        "mispfuse_lib": mispfuse_lib,
        "mispfuse_lib.config": config,
        "mispfuse_lib.connection": connection,
    }
    sys.modules.update(replacements)

    path = (
        Path(__file__).resolve().parents[1]
        / "package"
        / "bin"
        / "mispfuse_account_validator_rh.py"
    )
    spec = importlib.util.spec_from_file_location(
        "mispfuse_account_validator_rh_under_test", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load custom account handler")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        for name, old_module in previous.items():
            if old_module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old_module
    return module


handler_module = _load_handler_module()


class AccountValidatorHandlerTest(unittest.TestCase):
    def setUp(self):
        self.handler = handler_module.MispAccountValidator()
        self.handler.payload = {
            "misp_url": "https://misp.example",
            "misp_key": "secret",
            "verify_ssl": "1",
        }
        self.handler.callerArgs = SimpleNamespace(id="prod")

    def test_create_validates_before_persisting(self):
        resolved = {
            "misp_url": "https://misp.example",
            "misp_key": "secret",
            "verify_ssl": True,
        }
        with ExitStack() as stack:
            resolve = stack.enter_context(patch.object(
                handler_module, "resolve_account_values", return_value=resolved
            ))
            stack.enter_context(patch.object(
                handler_module, "get_proxies", return_value={"https": "proxy"}
            ))
            test_connection = stack.enter_context(patch.object(
                handler_module,
                "test_misp_connection",
                return_value={
                    "url": "https://misp.example",
                    "version": "2.5.12",
                    "type_count": 42,
                },
            ))
            result = self.handler.handleCreate({"marker": 1})

        self.assertEqual(result, "created")
        self.assertEqual(self.handler.base_calls, [("create", {"marker": 1})])
        resolve.assert_called_once_with(self.handler.payload, existing=None)
        test_connection.assert_called_once_with(
            "https://misp.example",
            "secret",
            verify_ssl=True,
            proxies={"https": "proxy"},
        )

    def test_failed_connection_blocks_save(self):
        with ExitStack() as stack:
            stack.enter_context(patch.object(
                handler_module,
                "resolve_account_values",
                return_value={
                    "misp_url": "https://misp.example",
                    "misp_key": "secret",
                    "verify_ssl": True,
                },
            ))
            stack.enter_context(
                patch.object(handler_module, "get_proxies", return_value={})
            )
            stack.enter_context(patch.object(
                handler_module,
                "test_misp_connection",
                side_effect=FakeConnectionTestError("MISP rejected the API key."),
            ))
            with self.assertRaises(FakeRestError) as raised:
                self.handler.handleCreate({})

        self.assertEqual(raised.exception.status, 400)
        self.assertIn("rejected", raised.exception.message)
        self.assertEqual(self.handler.base_calls, [])

    def test_edit_loads_existing_decrypted_account(self):
        existing = {
            "misp_url": "https://misp.example",
            "misp_key": "existing-secret",
            "verify_ssl": True,
        }
        resolved = dict(existing)
        with ExitStack() as stack:
            get_account = stack.enter_context(patch.object(
                handler_module, "get_account", return_value=existing
            ))
            resolve = stack.enter_context(patch.object(
                handler_module, "resolve_account_values", return_value=resolved
            ))
            stack.enter_context(
                patch.object(handler_module, "get_proxies", return_value={})
            )
            stack.enter_context(patch.object(
                handler_module,
                "test_misp_connection",
                return_value={
                    "url": "https://misp.example",
                    "version": "2.5.12",
                    "type_count": 42,
                },
            ))
            result = self.handler.handleEdit({"marker": 2})

        self.assertEqual(result, "edited")
        get_account.assert_called_once_with("session-key", "prod")
        resolve.assert_called_once_with(self.handler.payload, existing=existing)
        self.assertEqual(self.handler.base_calls, [("edit", {"marker": 2})])

    def test_delete_is_offline_safe(self):
        with patch.object(handler_module, "test_misp_connection") as test_connection:
            result = self.handler.handleRemove({"marker": 3})

        self.assertEqual(result, "removed")
        test_connection.assert_not_called()
        self.assertEqual(self.handler.base_calls, [("remove", {"marker": 3})])


if __name__ == "__main__":
    unittest.main()
