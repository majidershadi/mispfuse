from __future__ import annotations

import importlib
import sys
import types
import unittest
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parents[1] / "package" / "bin"
sys.path.insert(0, str(BIN_DIR))

if "solnlib" not in sys.modules:
    solnlib = types.ModuleType("solnlib")
    solnlib.conf_manager = types.SimpleNamespace(
        ConfManager=object,
        ConfManagerException=Exception,
    )
    sys.modules["solnlib"] = solnlib

templates = importlib.import_module("mispfuse_lib.templates")


class TemplateTest(unittest.TestCase):
    def test_mapping_keys_are_sorted_numerically(self):
        template = templates.Template(
            "order",
            {
                "map.10": "later:text:Other:0:0",
                "map.2": "earlier:text:Other:0:0",
            },
        )
        self.assertEqual([mapping.field for mapping in template.mappings], ["earlier", "later"])

    def test_mapping_requires_misp_type(self):
        with self.assertRaisesRegex(templates.TemplateError, "no MISP attribute type"):
            templates.Template("bad", {"map.1": "ioc_value:::0:0"})


if __name__ == "__main__":
    unittest.main()
