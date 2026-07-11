import os
import sys
import unittest

TOOLS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "tools"))
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, TOOLS)

import render_python

V0 = os.path.join(ROOT, "profiles", "fips-v0-ik-xk.json")
V1 = os.path.join(ROOT, "profiles", "fips-v1-xx-draft.json")


class RenderPythonTests(unittest.TestCase):
    def test_v0_constants(self):
        out = render_python.render(render_python.load_profile(V0))
        self.assertIn("FMP_VERSION = 0", out)
        self.assertIn('HANDSHAKE_PATTERN = "IK_XK"', out)
        self.assertIn("HAS_MSG3 = False", out)

    def test_v1_constants(self):
        out = render_python.render(render_python.load_profile(V1))
        self.assertIn("FMP_VERSION = 1", out)
        self.assertIn('HANDSHAKE_PATTERN = "XX"', out)
        self.assertIn("HAS_MSG3 = True", out)

    def test_link_message_types_dict(self):
        out = render_python.render(render_python.load_profile(V0))
        self.assertIn("LINK_MESSAGE_TYPES = {", out)
        self.assertIn('0x50: "Disconnect"', out)


if __name__ == "__main__":
    unittest.main()
