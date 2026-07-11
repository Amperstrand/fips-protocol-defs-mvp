#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOTS_DIR = REPO_ROOT / "snapshots"


def load(name):
    with open(SNAPSHOTS_DIR / (name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def diff(old, new):
    lines = []
    oc = {k: v["value"] for k, v in old.get("consts", {}).items()}
    nc = {k: v["value"] for k, v in new.get("consts", {}).items()}
    for k in sorted(set(oc) | set(nc)):
        if k not in oc:
            lines.append("CONST_ADDED:   {} = {}".format(k, nc[k]))
        elif k not in nc:
            lines.append("CONST_REMOVED: {} = {}".format(k, oc[k]))
        elif oc[k] != nc[k]:
            lines.append("CONST_CHANGED: {}: {} -> {}".format(k, oc[k], nc[k]))

    oe = old.get("enums", {})
    ne = new.get("enums", {})
    for k in sorted(set(oe) | set(ne)):
        if k not in oe:
            lines.append("ENUM_ADDED:    {}".format(k))
        elif k not in ne:
            lines.append("ENUM_REMOVED:  {}".format(k))
        elif oe[k] != ne[k]:
            lines.append("ENUM_CHANGED:  {}".format(k))

    ou, nu = old.get("upstream", {}), new.get("upstream", {})
    if ou.get("commit") != nu.get("commit"):
        lines.append("UPSTREAM: {}@{} -> {}@{}".format(
            ou.get("ref", "?"), str(ou.get("commit", "?"))[:7],
            nu.get("ref", "?"), str(nu.get("commit", "?"))[:7]))
    return lines


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if len(argv) != 3:
        sys.stderr.write("usage: diff_snapshots.py <old_name> <new_name>\n")
        return 2
    try:
        old, new = load(argv[1]), load(argv[2])
    except OSError as exc:
        sys.stderr.write("error: {}\n".format(exc))
        return 1
    for line in diff(old, new):
        sys.stdout.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
