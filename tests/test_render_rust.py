import os
import sys
import unittest

TOOLS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "tools"))
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, TOOLS)

import render_rust

V0 = os.path.join(ROOT, "profiles", "fips-v0-ik-xk.json")
V1 = os.path.join(ROOT, "profiles", "fips-v1-xx-draft.json")


class RenderRustTests(unittest.TestCase):
    def test_v0_constants(self):
        out = render_rust.render(render_rust.load_profile(V0))
        self.assertIn("pub const FMP_VERSION: u8 = 0;", out)
        self.assertIn('pub const HANDSHAKE_PATTERN: &str = "IK_XK";', out)
        self.assertIn("pub const HAS_MSG3: bool = false;", out)

    def test_v1_constants(self):
        out = render_rust.render(render_rust.load_profile(V1))
        self.assertIn("pub const FMP_VERSION: u8 = 1;", out)
        self.assertIn('pub const HANDSHAKE_PATTERN: &str = "XX";', out)
        self.assertIn("pub const HAS_MSG3: bool = true;", out)

    def test_provenance_header_present(self):
        out = render_rust.render(render_rust.load_profile(V0))
        self.assertIn("DO NOT EDIT BY HAND", out)
        self.assertIn("Source profile:", out)


if __name__ == "__main__":
    unittest.main()
