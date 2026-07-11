#!/usr/bin/env python3
"""Extract FIPS protocol constants from canonical upstream jmcorgan/fips at a pinned ref.

Stdlib only. The output is a normalized snapshot JSON that carries the EXACT upstream
commit it was extracted from, so every profile/snapshot is reproducible and traceable.

Canonical upstream is jmcorgan/fips. The Amperstrand/fips fork is NOT used.

Usage:
    # extract a tagged release (shallow clone)
    python3 tools/extract_upstream.py --name v0.4.0 --ref v0.4.0

    # extract a moving branch
    python3 tools/extract_upstream.py --name master --ref master

    # use an existing local checkout (dev)
    python3 tools/extract_upstream.py --name v0.4.0 --ref v0.4.0 --fips-root /path/to/fips
"""
import argparse
import ast
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_REPO = "https://github.com/jmcorgan/fips.git"
REPO_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOTS_DIR = REPO_ROOT / "snapshots"

# Dual-layout resolution: v0.4.0 paths first (src/protocol + src/mmp), then master
# (src/proto, where protocol + mmp were folded). src/noise is stable across both.
MODULE_CANDIDATES = {
    "noise": ["src/noise/mod.rs"],
    "link": ["src/protocol/link.rs", "src/proto/link.rs", "src/proto/fmp/wire.rs"],
    "protocol_mod": ["src/protocol/mod.rs", "src/proto/mod.rs"],
    "session": [
        "src/protocol/session.rs",
        "src/proto/session.rs",
        "src/proto/mmp/wire.rs",
        "src/proto/routing/wire.rs",
    ],
    "mmp": [
        "src/mmp/mod.rs",
        "src/proto/mmp.rs",
        "src/proto/mmp/mod.rs",
        "src/proto/mmp/wire.rs",
    ],
}

# Expected-symbol allowlist. If any are missing we fail loudly (reorg detection).
EXPECTED_CONSTS = [
    ("noise", "MAX_MESSAGE_SIZE"),
    ("noise", "TAG_SIZE"),
    ("noise", "PUBKEY_SIZE"),
    ("noise", "EPOCH_SIZE"),
    ("noise", "EPOCH_ENCRYPTED_SIZE"),
    ("noise", "HANDSHAKE_MSG1_SIZE"),
    ("noise", "HANDSHAKE_MSG2_SIZE"),
    ("noise", "XK_HANDSHAKE_MSG1_SIZE"),
    ("noise", "XK_HANDSHAKE_MSG2_SIZE"),
    ("noise", "XK_HANDSHAKE_MSG3_SIZE"),
    ("noise", "REPLAY_WINDOW_SIZE"),
    ("protocol_mod", "PROTOCOL_VERSION"),
    ("link", "SESSION_DATAGRAM_HEADER_SIZE"),
    ("session", "SESSION_SENDER_REPORT_SIZE"),
    ("session", "SESSION_RECEIVER_REPORT_SIZE"),
    ("session", "PATH_MTU_NOTIFICATION_SIZE"),
    ("session", "COORDS_REQUIRED_SIZE"),
    ("session", "MTU_EXCEEDED_SIZE"),
    ("mmp", "SENDER_REPORT_BODY_SIZE"),
    ("mmp", "RECEIVER_REPORT_BODY_SIZE"),
    ("mmp", "SENDER_REPORT_WIRE_SIZE"),
    ("mmp", "RECEIVER_REPORT_WIRE_SIZE"),
]

EXPECTED_ENUMS = [
    ("link", "LinkMessageType"),
    ("link", "DisconnectReason"),
]

CONST_RE = re.compile(r"pub\s+const\s+([A-Z][A-Z0-9_]*)\s*:\s*([A-Za-z0-9_]+)\s*=\s*([^;]+);")
ENUM_RE = re.compile(r"pub\s+enum\s+([A-Z][A-Za-z0-9_]*)\s*\{([^}]*)\}", re.S)
ENUM_VARIANT_RE = re.compile(r"([A-Z][A-Za-z0-9_]*)\s*=\s*(0x[0-9A-Fa-f]+|\d+)")
NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

_ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
}


def _safe_arith(node):
    if isinstance(node, ast.Expression):
        return _safe_arith(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_safe_arith(node.operand)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        return _ALLOWED_BINOPS[type(node.op)](_safe_arith(node.left), _safe_arith(node.right))
    raise ValueError("unsupported expression node: " + type(node).__name__)


def _eval_int_expr(expr, symbols):
    """Evaluate a Rust integer const expression over known symbol values."""
    def repl(m):
        name = m.group(0)
        if name in symbols:
            return "(" + str(symbols[name]) + ")"
        raise ValueError("unknown symbol in const expr: " + name)

    substituted = NAME_RE.sub(repl, expr.strip())
    substituted = re.sub(r"(\d)_(\d)", r"\1\2", substituted)
    substituted = re.sub(r"(\d)(?:i|u)(?:8|16|32|64|128|size)", r"\1", substituted)
    if not re.fullmatch(r"[0-9+\-*/%() \t]+", substituted):
        raise ValueError("unsafe const expr after substitution: %r -> %r" % (expr, substituted))
    return _safe_arith(ast.parse(substituted, mode="eval"))


def _candidate_files(root):
    seen = set()
    files = []
    for cands in MODULE_CANDIDATES.values():
        for rel in cands:
            if rel in seen:
                continue
            seen.add(rel)
            path = root / rel
            if path.is_file():
                files.append(path)
    return files


def extract(root):
    """Return ({const_name: {value, type}}, {enum_name: {variant: value}})."""
    consts = {}
    enums = {}
    files = _candidate_files(root)
    # Two passes so a const expression can reference a const defined in another file.
    for _ in range(2):
        for path in files:
            text = path.read_text(encoding="utf-8")
            for name, typ, expr in CONST_RE.findall(text):
                if name in consts:
                    continue
                try:
                    consts[name] = {
                        "value": _eval_int_expr(expr, {k: v["value"] for k, v in consts.items()}),
                        "type": typ,
                    }
                except ValueError:
                    continue
            for enum_name, body in ENUM_RE.findall(text):
                variants = {vname: int(vval, 0) for vname, vval in ENUM_VARIANT_RE.findall(body)}
                if variants and enum_name not in enums:
                    enums[enum_name] = variants
    return consts, enums


def drift_report(consts, enums):
    """Return (missing_const_names, missing_enum_names) vs the expected allowlist.

    Non-empty on a moving branch is drift information, not a failure — it is
    captured in the snapshot so version-to-version diffs are honest.
    """
    missing_consts = [n for (_, n) in EXPECTED_CONSTS if n not in consts]
    missing_enums = [n for (_, n) in EXPECTED_ENUMS if n not in enums]
    return sorted(set(missing_consts)), sorted(set(missing_enums))


def fetch(repo, ref, fips_root):
    if fips_root is not None:
        root = Path(fips_root)
        subprocess.run(["git", "-C", str(root), "checkout", "--quiet", ref], check=True)
    else:
        root = Path(tempfile.mkdtemp(prefix="fips-extract-"))
        subprocess.run(
            ["git", "clone", "--quiet", "--depth", "1", "--branch", ref, repo, str(root)],
            check=True,
        )
    commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"]).decode().strip()
    return root, commit


def build_snapshot(name, repo, ref, commit, consts, enums, missing):
    return {
        "name": name,
        "upstream": {"repo": repo, "ref": ref, "commit": commit, "authority": "jmcorgan/fips"},
        "consts": {k: consts[k] for k in sorted(consts)},
        "enums": {k: {vk: enums[k][vk] for vk in sorted(enums[k])} for k in sorted(enums)},
        "missing_expected": {"consts": missing[0], "enums": missing[1]},
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--ref", required=True)
    p.add_argument("--repo", default=DEFAULT_REPO)
    p.add_argument("--fips-root", default=None)
    p.add_argument("--out", default=None)
    args = p.parse_args(argv)

    root, commit = fetch(args.repo, args.ref, args.fips_root)
    consts, enums = extract(root)
    missing = drift_report(consts, enums)
    if missing[0] or missing[1]:
        sys.stderr.write("drift vs expected allowlist (captured as missing_expected):\n")
        for n in missing[0]:
            sys.stderr.write("  missing const: %s\n" % n)
        for n in missing[1]:
            sys.stderr.write("  missing enum:  %s\n" % n)

    snapshot = build_snapshot(args.name, args.repo, args.ref, commit, consts, enums, missing)
    out = Path(args.out) if args.out else SNAPSHOTS_DIR / (args.name + ".json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sys.stdout.write("wrote %s (upstream %s@%s)\n" % (out.relative_to(REPO_ROOT), args.ref, commit[:11]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
