import os
import sys
import unittest

TOOLS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "tools"))
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, TOOLS)

import diff_profiles

V0 = os.path.join(ROOT, "profiles", "fips-v0-ik-xk.json")
V1 = os.path.join(ROOT, "profiles", "fips-v1-xx-draft.json")


class DiffProfilesTests(unittest.TestCase):
    def _diff_lines(self):
        old = diff_profiles.load_profile(V0)
        new = diff_profiles.load_profile(V1)
        return diff_profiles.diff(old, new)

    def test_fmp_version_change(self):
        self.assertIn("FMP_VERSION: 0 -> 1", self._diff_lines())

    def test_handshake_pattern_change(self):
        self.assertIn("HANDSHAKE_PATTERN: IK_XK -> XX", self._diff_lines())

    def test_msg3_added(self):
        self.assertIn("MSG3: added", self._diff_lines())

    def test_exit_code_zero_on_diff(self):
        rc = diff_profiles.main([None, V0, V1])
        self.assertEqual(rc, 0)

    def test_exit_code_nonzero_on_bad_input(self):
        rc = diff_profiles.main([None, "/nonexistent/profile.json", V1])
        self.assertNotEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
