#!/usr/bin/env python3
"""Check that checked-in generated files match a fresh render.

Usage:
    python3 tools/check_generated.py

Exit code 0 means every generated file is up to date. Exit code 1 means one
or more generated files are missing or stale; their paths are printed.
"""
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
GENERATED_DIR = REPO_ROOT / "generated"

sys.path.insert(0, str(TOOLS_DIR))

import render_all
import render_rust
import render_python
import render_lua
import render_markdown


def _targets_for_profile(profile_path):
    profile = render_all.enrich_profile(render_all.load_profile(profile_path))
    stem = profile_path.stem
    us = render_all.underscore_name(stem)
    return [
        (render_rust.render(profile), GENERATED_DIR / "rust" / (us + ".rs")),
        (render_python.render(profile), GENERATED_DIR / "python" / (us + ".py")),
        (render_lua.render(profile), GENERATED_DIR / "lua" / (us + ".lua")),
        (render_markdown.render(profile), GENERATED_DIR / "markdown" / (stem + ".md")),
    ]


def check():
    missing = []
    stale = []
    for profile_path in sorted(render_all.PROFILES_DIR.glob("*.json")):
        for content, path in _targets_for_profile(profile_path):
            rel = path.relative_to(REPO_ROOT)
            if not path.exists():
                missing.append(str(rel))
                continue
            if path.read_text(encoding="utf-8") != content:
                stale.append(str(rel))
    return missing, stale


def main(argv=None):
    missing, stale = check()
    if not missing and not stale:
        sys.stdout.write("generated files are up to date\n")
        return 0
    if missing:
        sys.stderr.write("missing generated files:\n")
        for rel in missing:
            sys.stderr.write("  {}\n".format(rel))
    if stale:
        sys.stderr.write("stale generated files:\n")
        for rel in stale:
            sys.stderr.write("  {}\n".format(rel))
    sys.stderr.write("run: python3 tools/render_all.py\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
