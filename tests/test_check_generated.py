import os
import sys
import unittest

TOOLS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "tools"))
sys.path.insert(0, TOOLS)

import render_all
import check_generated


class CheckGeneratedTests(unittest.TestCase):
    def test_generated_is_fresh_after_render(self):
        render_all.render_all()
        missing, stale = check_generated.check()
        self.assertEqual(missing, [])
        self.assertEqual(stale, [])

    def test_check_detects_stale_file(self):
        render_all.render_all()
        # Locate one generated python file and corrupt it.
        gen_dir = render_all.GENERATED_DIR / "python"
        any_py = sorted(gen_dir.glob("*.py"))[0]
        original = any_py.read_text(encoding="utf-8")
        try:
            any_py.write_text("# tampered\n", encoding="utf-8")
            missing, stale = check_generated.check()
            self.assertEqual(missing, [])
            self.assertTrue(any(str(any_py.relative_to(render_all.REPO_ROOT)).endswith(".py") for _ in stale) or stale)
        finally:
            any_py.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
