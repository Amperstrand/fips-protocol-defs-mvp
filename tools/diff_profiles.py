#!/usr/bin/env python3
"""Diff two FIPS protocol profile JSON files and print a stable, human-readable summary.

Usage:
    python3 tools/diff_profiles.py <old.json> <new.json>

Exit code is 0 even when differences exist. It is nonzero only when input
files are missing or invalid.
"""
import json
import sys


def load_profile(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _msg_sort_key(name):
    digits = "".join(ch for ch in name if ch.isdigit())
    return (int(digits) if digits else 0, name)


def _parse_link_types(profile):
    raw = (profile.get("link") or {}).get("message_types", {}) or {}
    parsed = {}
    for key, name in raw.items():
        parsed[int(str(key), 0)] = name
    return parsed


def _fmt_payload(value):
    if value is None or value == "":
        return "<none>"
    return str(value)


def _scalar(lines, label, old_value, new_value):
    if old_value != new_value:
        lines.append("{}: {} -> {}".format(label, old_value, new_value))


def diff(old, new):
    lines = []

    old_up = old.get("upstream") or {}
    new_up = new.get("upstream") or {}
    old_fmp = old.get("fmp") or {}
    new_fmp = new.get("fmp") or {}

    _scalar(lines, "PROFILE_NAME", old.get("profile_name"), new.get("profile_name"))
    _scalar(lines, "STATUS", old.get("status"), new.get("status"))
    _scalar(lines, "UPSTREAM_REPO", old_up.get("repo"), new_up.get("repo"))
    _scalar(lines, "UPSTREAM_REF", old_up.get("ref"), new_up.get("ref"))
    _scalar(lines, "UPSTREAM_COMMIT", old_up.get("commit"), new_up.get("commit"))

    _scalar(lines, "FMP_VERSION", old_fmp.get("version"), new_fmp.get("version"))
    _scalar(lines, "HANDSHAKE_PATTERN", old_fmp.get("handshake_pattern"), new_fmp.get("handshake_pattern"))
    _scalar(lines, "COMMON_PREFIX_SIZE", old_fmp.get("common_prefix_size"), new_fmp.get("common_prefix_size"))
    _scalar(lines, "ESTABLISHED_HEADER_SIZE", old_fmp.get("established_header_size"), new_fmp.get("established_header_size"))
    _scalar(lines, "INNER_HEADER_SIZE", old_fmp.get("inner_header_size"), new_fmp.get("inner_header_size"))

    old_msgs = old_fmp.get("messages") or {}
    new_msgs = new_fmp.get("messages") or {}
    for key in sorted(set(old_msgs) | set(new_msgs), key=_msg_sort_key):
        upper = key.upper()
        if key not in old_msgs:
            lines.append("{}: added".format(upper))
            continue
        if key not in new_msgs:
            lines.append("{}: removed".format(upper))
            continue
        om = old_msgs[key] or {}
        nm = new_msgs[key] or {}
        if om.get("present") != nm.get("present"):
            lines.append("{}.PRESENT: {} -> {}".format(upper, om.get("present"), nm.get("present")))
        if om.get("role") != nm.get("role"):
            lines.append("{}.ROLE: {} -> {}".format(upper, om.get("role"), nm.get("role")))
        if om.get("payload_pattern") != nm.get("payload_pattern"):
            lines.append("{}.PAYLOAD_PATTERN: {} -> {}".format(upper, _fmt_payload(om.get("payload_pattern")), _fmt_payload(nm.get("payload_pattern"))))
        if om.get("wire_size") != nm.get("wire_size"):
            lines.append("{}.WIRE_SIZE: {} -> {}".format(upper, om.get("wire_size"), nm.get("wire_size")))

    old_lt = _parse_link_types(old)
    new_lt = _parse_link_types(new)
    for value in sorted(set(old_lt) | set(new_lt)):
        if value not in old_lt:
            lines.append("LINK_TYPE_0x{:02X}: added ({})".format(value, new_lt[value]))
            continue
        if value not in new_lt:
            lines.append("LINK_TYPE_0x{:02X}: removed ({})".format(value, old_lt[value]))
            continue
        if old_lt[value] != new_lt[value]:
            lines.append("LINK_TYPE_0x{:02X}: {} -> {}".format(value, old_lt[value], new_lt[value]))

    return lines


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if len(argv) != 3:
        sys.stderr.write("usage: diff_profiles.py <old.json> <new.json>\n")
        return 2
    try:
        old = load_profile(argv[1])
        new = load_profile(argv[2])
    except (OSError, ValueError) as exc:
        sys.stderr.write("error loading profiles: {}\n".format(exc))
        return 1
    for line in diff(old, new):
        sys.stdout.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
