import os
import sys
import unittest

TOOLS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "tools"))
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, TOOLS)

import render_all
import render_rust
import render_python
import render_lua
import render_markdown

V0 = os.path.join(ROOT, "profiles", "fips-v0-ik-xk.json")


def _enriched():
    return render_all.enrich_profile(render_all.load_profile(V0))


class SnapshotRenderingTests(unittest.TestCase):
    def setUp(self):
        self.prof = _enriched()

    def test_enrichment_attaches_snapshot(self):
        self.assertIn("snapshot", self.prof)
        self.assertEqual(self.prof["snapshot"]["upstream"]["authority"], "jmcorgan/fips")

    def test_rust_emits_extraction_fed_consts(self):
        out = render_rust.render(self.prof)
        self.assertIn("pub const PROTOCOL_VERSION: u8 = 1;", out)
        self.assertIn("pub const HANDSHAKE_MSG1_SIZE: usize = 106;", out)
        self.assertIn("pub const XK_HANDSHAKE_MSG3_SIZE: usize = 73;", out)

    def test_python_emits_extraction_fed_consts(self):
        out = render_python.render(self.prof)
        self.assertIn("PROTOCOL_VERSION = 1", out)
        self.assertIn("HANDSHAKE_MSG1_SIZE = 106", out)

    def test_lua_emits_extraction_fed_consts(self):
        out = render_lua.render(self.prof)
        self.assertIn("M.PROTOCOL_VERSION = 1", out)
        self.assertIn("M.HANDSHAKE_MSG1_SIZE = 106", out)

    def test_markdown_has_extracted_constants_section(self):
        out = render_markdown.render(self.prof)
        self.assertIn("## Extracted constants (canonical upstream)", out)
        self.assertIn("| PROTOCOL_VERSION | u8 | 1 |", out)

    def test_bare_profile_omits_snapshot_block(self):
        bare = render_all.load_profile(V0)
        self.assertNotIn("snapshot", bare)
        self.assertNotIn("PROTOCOL_VERSION", render_rust.render(bare))


if __name__ == "__main__":
    unittest.main()
