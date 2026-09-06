#!/usr/bin/env python3
"""Consumer drift check: generated profile vs a consumer's vendored constants.

Compares the integer/bool constants of a generated profile Rust file (e.g.
``generated/rust/fips_v0_ik_xk.rs``) against a consumer file that vendors
wire constants (e.g. ``microfips``'s generated ``fips_protocol_types.rs``).

Only the intersection of const names is compared — each side legitimately
carries names the other does not (profile metadata on one side, consumer
runtime constants on the other). A mismatching value for a shared name is
DRIFT and fails the check (``--fail-on-drift``), because both files claim to
describe the same wire protocol.

Arithmetic values (``EPOCH_SIZE + TAG_SIZE``) are resolved against constants
defined earlier in the same file, so derived sizes compare like literals.

Stdlib only, matching the repo's tooling convention.
"""

from __future__ import annotations

import argparse
import re
import sys

CONST_RE = re.compile(
    r'^\s*pub const (?P<name>[A-Z][A-Z0-9_]*)\s*:\s*(?P<ty>[^=]+?)\s*=\s*(?P<val>[^;]+);'
)


def _parse_value(raw: str) -> object:
    raw = raw.strip()
    raw = re.sub(r'\s*//.*$', '', raw).strip()  # strip trailing comments
    if raw.startswith(('b"', 'b\'')) or raw.startswith(('"', '\'')):
        return raw.lstrip('b').strip('"\'')
    if raw in ('true', 'false'):
        return raw == 'true'
    if raw.startswith('Some(') and raw.endswith(')'):
        return _parse_value(raw[5:-1])
    return raw


def extract_constants(path: str) -> dict[str, object]:
    consts: dict[str, object] = {}
    unresolved: dict[str, str] = {}
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            m = CONST_RE.match(line)
            if not m:
                continue
            name, val = m.group('name'), _parse_value(m.group('val'))
            if isinstance(val, str) and not _is_literal(val):
                unresolved[name] = val
            else:
                consts[name] = val
    # resolve arithmetic/derived values against known constants (bounded passes)
    for _ in range(len(unresolved) + 1):
        progress = False
        for name, expr in list(unresolved.items()):
            if _try_eval(expr, consts) is not None:
                consts[name] = _try_eval(expr, consts)
                del unresolved[name]
                progress = True
        if not unresolved or not progress:
            break
    return consts


_NUM_RE = re.compile(r'^\s*(?:0x[0-9a-fA-F]+|\d+)\s*$')


def _is_literal(val: str) -> bool:
    return bool(_NUM_RE.match(val))


def _try_eval(expr: str, known: dict[str, object]) -> object | None:
    """Evaluate ``A + B``-style usize arithmetic, or None if not resolvable."""
    tokens = [t.strip() for t in expr.split('+')]
    total = 0
    for tok in tokens:
        if not tok:
            return None
        if _NUM_RE.match(tok):
            total += int(tok, 0)
        elif tok in known and isinstance(known[tok], int):
            total += int(known[tok])
        else:
            return None
    return total


def compare(profile: dict[str, object], consumer: dict[str, object]) -> tuple[list[tuple[str, object, object]], int]:
    shared = sorted(set(profile) & set(consumer))
    drift = [
        (n, profile[n], consumer[n])
        for n in shared
        if profile[n] != consumer[n]
    ]
    return drift, len(shared)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('profile_rs', help='generated profile Rust file (source of truth)')
    ap.add_argument('consumer_rs', help='consumer Rust file with vendored constants')
    ap.add_argument('--fail-on-drift', action='store_true')
    args = ap.parse_args(argv)

    profile = extract_constants(args.profile_rs)
    consumer = extract_constants(args.consumer_rs)
    drift, compared = compare(profile, consumer)

    only_profile = sorted(set(profile) - set(consumer))
    only_consumer = sorted(set(consumer) - set(profile))
    print(f'compared {compared} shared constants '
          f'({len(only_profile)} profile-only, {len(only_consumer)} consumer-only — informational)')
    if drift:
        print('DRIFT between profile and consumer:')
        for name, pv, cv in drift:
            print(f'  {name}: profile={pv!r} consumer={cv!r}')
    else:
        print('no drift: all shared constants agree')
    if drift and args.fail_on_drift:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
