import os
import sys
import unittest

TOOLS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "tools"))
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, TOOLS)

import render_lua

V0 = os.path.join(ROOT, "profiles", "fips-v0-ik-xk.json")
V1 = os.path.join(ROOT, "profiles", "fips-v1-xx-draft.json")


class RenderLuaTests(unittest.TestCase):
    def test_v0_constants(self):
        out = render_lua.render(render_lua.load_profile(V0))
        self.assertIn("FMP_VERSION = 0", out)
        self.assertIn('HANDSHAKE_PATTERN = "IK_XK"', out)
        self.assertIn("HAS_MSG3 = false", out)

    def test_v1_constants(self):
        out = render_lua.render(render_lua.load_profile(V1))
        self.assertIn("FMP_VERSION = 1", out)
        self.assertIn('HANDSHAKE_PATTERN = "XX"', out)
        self.assertIn("HAS_MSG3 = true", out)

    def test_link_message_types_table(self):
        out = render_lua.render(render_lua.load_profile(V0))
        self.assertIn("LINK_MESSAGE_TYPES = {", out)
        self.assertIn('[0x51] = "Heartbeat"', out)


if __name__ == "__main__":
    unittest.main()
