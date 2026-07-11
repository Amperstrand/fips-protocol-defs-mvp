#!/usr/bin/env python3
"""Render a FIPS protocol profile JSON into Rust no_std constants.

Usage:
    python3 tools/render_rust.py path/to/profile.json
"""
import json
import sys

GENERATOR_NAME = "tools/render_rust.py"

_SHAPE_EMIT = frozenset({
    "FMP_VERSION",
    "COMMON_PREFIX_SIZE",
    "ESTABLISHED_HEADER_SIZE",
    "INNER_HEADER_SIZE",
})


def load_profile(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _rust_str(value):
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return '"' + escaped + '"'


def _rust_option_str(value):
    if value is None:
        return "None"
    return "Some(" + _rust_str(value) + ")"


def _msg_sort_key(name):
    digits = "".join(ch for ch in name if ch.isdigit())
    return (int(digits) if digits else 0, name)


def _ordered_link_types(profile):
    raw = (profile.get("link") or {}).get("message_types", {}) or {}
    parsed = []
    for key, name in raw.items():
        parsed.append((int(str(key), 0), name))
    parsed.sort(key=lambda kv: kv[0])
    return parsed


def render(profile):
    upstream = profile.get("upstream") or {}
    fmp = profile.get("fmp") or {}
    messages = fmp.get("messages") or {}

    lines = []
    lines.append("// AUTO-GENERATED FILE. DO NOT EDIT BY HAND.")
    lines.append("// Regenerate with: python3 tools/render_all.py")
    lines.append("//")
    lines.append("// Source profile:   {}".format(profile.get("profile_name", "")))
    lines.append("// Profile status:   {}".format(profile.get("status", "")))
    lines.append("// Upstream repo:    {}".format(upstream.get("repo", "")))
    lines.append("// Upstream ref:     {}".format(upstream.get("ref", "")))
    commit = upstream.get("commit")
    lines.append("// Upstream commit:  {}".format(commit if commit else "<unpinned>"))
    lines.append("// Generator:        {}".format(GENERATOR_NAME))
    lines.append("//")
    lines.append("// This file is downstream experimental tooling. It is NOT the canonical")
    lines.append("// FIPS protocol specification. Upstream jmcorgan/fips remains the authority.")
    lines.append("")

    lines.append("pub const PROFILE_NAME: &str = {};".format(_rust_str(profile.get("profile_name", ""))))
    lines.append("pub const PROFILE_STATUS: &str = {};".format(_rust_str(profile.get("status", ""))))
    lines.append("pub const FIPS_UPSTREAM_REPO: &str = {};".format(_rust_str(upstream.get("repo", ""))))
    lines.append("pub const FIPS_UPSTREAM_REF: &str = {};".format(_rust_str(upstream.get("ref", ""))))
    lines.append("pub const FIPS_UPSTREAM_COMMIT: Option<&str> = {};".format(_rust_option_str(commit)))
    lines.append("pub const FMP_VERSION: u8 = {};".format(int(fmp.get("version", 0))))
    lines.append("pub const HANDSHAKE_PATTERN: &str = {};".format(_rust_str(fmp.get("handshake_pattern", ""))))
    lines.append("pub const COMMON_PREFIX_SIZE: usize = {};".format(int(fmp.get("common_prefix_size", 0))))
    lines.append("pub const ESTABLISHED_HEADER_SIZE: usize = {};".format(int(fmp.get("established_header_size", 0))))
    lines.append("pub const INNER_HEADER_SIZE: usize = {};".format(int(fmp.get("inner_header_size", 0))))

    for key in ("msg1", "msg2", "msg3"):
        present = bool((messages.get(key) or {}).get("present", False))
        const_name = "HAS_MSG" + key[-1]
        lines.append("pub const {}: bool = {};".format(const_name, "true" if present else "false"))

    link_types = _ordered_link_types(profile)
    lines.append("pub const LINK_MESSAGE_TYPES: &[(u8, &str)] = &[")
    for value, name in link_types:
        lines.append("    (0x{:02X}, {}),".format(value, _rust_str(name)))
    lines.append("];")
    lines.append("")
    snapshot = profile.get("snapshot")
    if snapshot:
        for name in sorted(snapshot.get("consts", {})):
            if name in _SHAPE_EMIT:
                continue
            c = snapshot["consts"][name]
            lines.append("pub const {}: {} = {};".format(name, c["type"], c["value"]))
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if len(argv) != 2:
        sys.stderr.write("usage: render_rust.py <profile.json>\n")
        return 2
    profile = load_profile(argv[1])
    sys.stdout.write(render(profile))
    return 0


if __name__ == "__main__":
    sys.exit(main())
