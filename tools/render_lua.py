#!/usr/bin/env python3
"""Render a FIPS protocol profile JSON into Lua constants for Wireshark.

Usage:
    python3 tools/render_lua.py path/to/profile.json
"""
import json
import sys

GENERATOR_NAME = "tools/render_lua.py"

_SHAPE_EMIT = frozenset({
    "FMP_VERSION",
    "COMMON_PREFIX_SIZE",
    "ESTABLISHED_HEADER_SIZE",
    "INNER_HEADER_SIZE",
})


def load_profile(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _lua_str(value):
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return '"' + escaped + '"'


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
    commit = upstream.get("commit")

    lines = []
    lines.append("-- AUTO-GENERATED FILE. DO NOT EDIT BY HAND.")
    lines.append("-- Regenerate with: python3 tools/render_all.py")
    lines.append("--")
    lines.append("-- Source profile:   {}".format(profile.get("profile_name", "")))
    lines.append("-- Profile status:   {}".format(profile.get("status", "")))
    lines.append("-- Upstream repo:    {}".format(upstream.get("repo", "")))
    lines.append("-- Upstream ref:     {}".format(upstream.get("ref", "")))
    lines.append("-- Upstream commit:  {}".format(commit if commit else "<unpinned>"))
    lines.append("-- Generator:        {}".format(GENERATOR_NAME))
    lines.append("--")
    lines.append("-- This file is downstream experimental tooling. It is NOT the canonical")
    lines.append("-- FIPS protocol specification. Upstream jmcorgan/fips remains the authority.")
    lines.append("")
    lines.append("local M = {}")
    lines.append("")
    lines.append("M.PROFILE_NAME = {}".format(_lua_str(profile.get("profile_name", ""))))
    lines.append("M.PROFILE_STATUS = {}".format(_lua_str(profile.get("status", ""))))
    lines.append("M.FIPS_UPSTREAM_REPO = {}".format(_lua_str(upstream.get("repo", ""))))
    lines.append("M.FIPS_UPSTREAM_REF = {}".format(_lua_str(upstream.get("ref", ""))))
    lines.append("M.FIPS_UPSTREAM_COMMIT = {}".format(_lua_str(commit) if commit is not None else "nil"))
    lines.append("M.FMP_VERSION = {}".format(int(fmp.get("version", 0))))
    lines.append("M.HANDSHAKE_PATTERN = {}".format(_lua_str(fmp.get("handshake_pattern", ""))))
    lines.append("M.COMMON_PREFIX_SIZE = {}".format(int(fmp.get("common_prefix_size", 0))))
    lines.append("M.ESTABLISHED_HEADER_SIZE = {}".format(int(fmp.get("established_header_size", 0))))
    lines.append("M.INNER_HEADER_SIZE = {}".format(int(fmp.get("inner_header_size", 0))))

    for key in ("msg1", "msg2", "msg3"):
        present = bool((messages.get(key) or {}).get("present", False))
        const_name = "HAS_MSG" + key[-1]
        lines.append("M.{} = {}".format(const_name, "true" if present else "false"))

    lines.append("")
    lines.append("M.LINK_MESSAGE_TYPES = {")
    for value, name in _ordered_link_types(profile):
        lines.append("    [0x{:02X}] = {},".format(value, _lua_str(name)))
    lines.append("}")
    lines.append("")
    snapshot = profile.get("snapshot")
    if snapshot:
        for name in sorted(snapshot.get("consts", {})):
            if name in _SHAPE_EMIT:
                continue
            lines.append("M.{} = {}".format(name, snapshot["consts"][name]["value"]))
        lines.append("")
    lines.append("return M")
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if len(argv) != 2:
        sys.stderr.write("usage: render_lua.py <profile.json>\n")
        return 2
    profile = load_profile(argv[1])
    sys.stdout.write(render(profile))
    return 0


if __name__ == "__main__":
    sys.exit(main())
