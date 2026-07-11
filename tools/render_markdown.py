#!/usr/bin/env python3
"""Render a FIPS protocol profile JSON into a human-readable Markdown summary.

Usage:
    python3 tools/render_markdown.py path/to/profile.json
"""
import json
import sys

GENERATOR_NAME = "tools/render_markdown.py"


def load_profile(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _msg_sort_key(name):
    digits = "".join(ch for ch in name if ch.isdigit())
    return (int(digits) if digits else 0, name)


def _ordered_messages(profile):
    messages = (profile.get("fmp") or {}).get("messages") or {}
    return sorted(messages.items(), key=lambda kv: _msg_sort_key(kv[0]))


def _ordered_link_types(profile):
    raw = (profile.get("link") or {}).get("message_types", {}) or {}
    parsed = []
    for key, name in raw.items():
        parsed.append((int(str(key), 0), name))
    parsed.sort(key=lambda kv: kv[0])
    return parsed


def _fmt_optional(value, default="—"):
    if value is None or value == "":
        return default
    return str(value)


def render(profile):
    upstream = profile.get("upstream") or {}
    fmp = profile.get("fmp") or {}
    compatibility = profile.get("compatibility") or {}
    commit = upstream.get("commit")

    lines = []
    lines.append("# Profile: {}".format(profile.get("profile_name", "")))
    lines.append("")
    lines.append("> AUTO-GENERATED FILE. DO NOT EDIT BY HAND.")
    lines.append("> Regenerate with: `python3 tools/render_all.py`")
    lines.append("> Generator: `{}`".format(GENERATOR_NAME))
    lines.append("")
    lines.append("- **Status:** {}".format(profile.get("status", "")))
    lines.append("- **Description:** {}".format(profile.get("description", "")))
    lines.append("")

    lines.append("## Upstream provenance")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("| --- | --- |")
    lines.append("| Repo | {} |".format(upstream.get("repo", "")))
    lines.append("| Ref | {} |".format(upstream.get("ref", "")))
    lines.append("| Commit | {} |".format(commit if commit else "<unpinned>"))
    lines.append("| Source | {} |".format(upstream.get("source", "")))
    lines.append("")
    lines.append("> This profile is downstream experimental tooling. It is NOT the canonical")
    lines.append("> FIPS protocol specification. Upstream `jmcorgan/fips` remains the authority.")
    lines.append("")

    lines.append("## Intended consumers")
    lines.append("")
    for consumer in profile.get("intended_consumers", []) or []:
        lines.append("- {}".format(consumer))
    lines.append("")

    lines.append("## Compatibility")
    lines.append("")
    lines.append("- **microfips PR:** {}".format(_fmt_optional(compatibility.get("microfips_pr"))))
    lines.append("- **fips-lab:** {}".format(compatibility.get("fips_lab", "")))
    lines.append("- **Upstream requirement:** {}".format(compatibility.get("upstream_requirement", "")))
    lines.append("")

    lines.append("## FMP")
    lines.append("")
    lines.append("- **Version:** {}".format(int(fmp.get("version", 0))))
    lines.append("- **Handshake pattern:** {}".format(fmp.get("handshake_pattern", "")))
    lines.append("- **Common prefix size:** {} bytes".format(int(fmp.get("common_prefix_size", 0))))
    lines.append("- **Established header size:** {} bytes".format(int(fmp.get("established_header_size", 0))))
    lines.append("- **Inner header size:** {} bytes".format(int(fmp.get("inner_header_size", 0))))
    lines.append("")

    lines.append("### Messages")
    lines.append("")
    lines.append("| Message | Present | Role | Wire size | Payload pattern | Summary |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for name, msg in _ordered_messages(profile):
        present = "yes" if msg.get("present") else "no"
        role = msg.get("role", "")
        if msg.get("wire_size_known") and msg.get("wire_size") is not None:
            wire = "{} bytes".format(msg.get("wire_size"))
        else:
            wire = "unknown"
        payload = _fmt_optional(msg.get("payload_pattern"))
        summary = msg.get("summary", "")
        lines.append("| {} | {} | {} | {} | {} | {} |".format(name, present, role, wire, payload, summary))
    lines.append("")

    lines.append("## Link message types")
    lines.append("")
    lines.append("| Value | Name |")
    lines.append("| --- | --- |")
    for value, name in _ordered_link_types(profile):
        lines.append("| 0x{:02X} | {} |".format(value, name))
    lines.append("")

    notes = profile.get("notes", []) or []
    if notes:
        lines.append("## Notes")
        lines.append("")
        for note in notes:
            lines.append("- {}".format(note))
        lines.append("")

    snapshot = profile.get("snapshot")
    if snapshot:
        lines.append("## Extracted constants (canonical upstream)")
        lines.append("")
        lines.append("| Constant | Type | Value |")
        lines.append("| --- | --- | --- |")
        for name in sorted(snapshot.get("consts", {})):
            c = snapshot["consts"][name]
            lines.append("| {} | {} | {} |".format(name, c["type"], c["value"]))
        lines.append("")

    return "\n".join(lines)


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if len(argv) != 2:
        sys.stderr.write("usage: render_markdown.py <profile.json>\n")
        return 2
    profile = load_profile(argv[1])
    sys.stdout.write(render(profile))
    return 0


if __name__ == "__main__":
    sys.exit(main())
