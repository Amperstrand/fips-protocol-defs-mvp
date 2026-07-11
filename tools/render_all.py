#!/usr/bin/env python3
"""Render every profile under profiles/ into generated/<lang>/ outputs.

Usage:
    python3 tools/render_all.py
"""
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
PROFILES_DIR = REPO_ROOT / "profiles"
GENERATED_DIR = REPO_ROOT / "generated"

sys.path.insert(0, str(TOOLS_DIR))

import render_rust
import render_python
import render_lua
import render_markdown


def load_profile(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def enrich_profile(profile):
    """Attach the extraction snapshot linked by upstream.snapshot_ref, if any.

    Renderers read profile['snapshot'] to emit extraction-fed constants. Profiles
    without a snapshot_ref (e.g. draft future profiles) pass through unchanged.
    """
    snap_ref = (profile.get("upstream") or {}).get("snapshot_ref")
    if not snap_ref:
        return profile
    snap_path = REPO_ROOT / snap_ref
    if not snap_path.is_file():
        return profile
    merged = dict(profile)
    with open(snap_path, "r", encoding="utf-8") as f:
        merged["snapshot"] = json.load(f)
    return merged


def underscore_name(name):
    return name.replace("-", "_")


# (subdir, extension, module, use_dashed_stem_for_filename)
RENDERERS = [
    ("rust", "rs", render_rust, False),
    ("python", "py", render_python, False),
    ("lua", "lua", render_lua, False),
    ("markdown", "md", render_markdown, True),
]


def render_all():
    profile_paths = sorted(PROFILES_DIR.glob("*.json"))
    written = []
    for profile_path in profile_paths:
        profile = enrich_profile(load_profile(profile_path))
        stem = profile_path.stem
        us = underscore_name(stem)
        for subdir, ext, module, use_dashed in RENDERERS:
            out_dir = GENERATED_DIR / subdir
            out_dir.mkdir(parents=True, exist_ok=True)
            base = stem if use_dashed else us
            out_path = out_dir / "{}.{}".format(base, ext)
            content = module.render(profile)
            out_path.write_text(content, encoding="utf-8")
            written.append(out_path)
    return written


def main(argv=None):
    written = render_all()
    for path in written:
        sys.stdout.write("wrote {}\n".format(path.relative_to(REPO_ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
