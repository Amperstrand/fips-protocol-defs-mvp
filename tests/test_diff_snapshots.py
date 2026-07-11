import os
import sys
import unittest

TOOLS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "tools"))
sys.path.insert(0, TOOLS)

import diff_snapshots


class DiffSnapshotsTests(unittest.TestCase):
    def _diff(self, old, new):
        return diff_snapshots.diff(diff_snapshots.load(old), diff_snapshots.load(new))

    def test_v040_to_next_shows_xx_migration(self):
        lines = self._diff("v0.4.0", "next")
        self.assertIn("CONST_ADDED:   HANDSHAKE_MSG3_SIZE = 73", lines)
        self.assertIn("CONST_REMOVED: XK_HANDSHAKE_MSG3_SIZE = 73", lines)
        self.assertIn("CONST_ADDED:   FMP_VERSION = 1", lines)
        self.assertTrue(any(line.startswith("UPSTREAM:") for line in lines))

    def test_v040_to_master_shows_drift(self):
        lines = self._diff("v0.4.0", "master")
        self.assertTrue(any(line.startswith("UPSTREAM:") for line in lines))

    def test_exit_code_zero_on_diff(self):
        self.assertEqual(diff_snapshots.main([None, "v0.4.0", "next"]), 0)

    def test_exit_nonzero_on_bad_input(self):
        self.assertNotEqual(diff_snapshots.main([None, "nonexistent", "next"]), 0)


if __name__ == "__main__":
    unittest.main()
