# fips-protocol-defs-mvp

> Experimental MVP tooling for extracting, comparing, and rendering FIPS
> protocol definitions for microcontroller, lab, and Wireshark experiments.

> **WARNING — experimental downstream tooling.**
> This repository is **not** the canonical FIPS protocol specification. It is
> **not** upstream FIPS. It is **not** a stable crate yet. Upstream
> [`jmcorgan/fips`](https://github.com/jmcorgan/fips) remains the authority.
> Everything here is a proving ground so `microfips`, `fips-lab`, and
> Wireshark experiments can stay wire-compatible.

## What problem this solves

FIPS is an evolving protocol with at least two relevant shapes today:

1. the **current-compatible** FMP v0 / IK-XK behavior that existing
   `microfips` firmware and `fips-lab` captures speak, and
2. a **future/draft** FMP v1 / Noise XX shape that is being designed but is
   not yet shipping upstream.

Downstream consumers need a single, reviewable place where these protocol
shapes are described, compared, and rendered into the constants each toolchain
actually uses — without each consumer hand-maintaining its own copy.

## Why it exists

- **`microfips`** runs on microcontrollers and cannot simply depend on the
  full upstream FIPS crate. It needs small, `no_std`-friendly Rust constants.
- **`fips-lab`** is Python-based capture/decode tooling. It needs Python
  constants and types for decoding btsnoop / packet captures.
- **Wireshark experiments** can consume Lua tables for constant lookup in a
  handwritten dissector.

This repo generates all three from one normalized JSON profile, plus a
Markdown summary for humans, and provides a diff tool so protocol changes are
obvious during review.

## What this repo is **not**

- Not the canonical FIPS protocol spec.
- Not upstream `jmcorgan/fips`.
- Not a fork of the protocol.
- Not a stable crate yet (no Cargo project, no published packages).
- Not a source of real secrets, keys, passwords, or credentials.

## Architecture

```text
jmcorgan/fips pinned ref
        ↓
profile JSON
        ↓
generated Rust / Python / Lua / Markdown
        ↓
microfips / fips-lab / Wireshark experiments
```

The normalized JSON profile under `profiles/` is the source of truth inside
this repo. Every generated file embeds provenance and a "do not edit by hand"
notice. CI verifies generated files are reproducible.

## Profiles

| Profile | Status | Targets | Upstream ref |
| --- | --- | --- | --- |
| [`fips-v0-ik-xk`](profiles/fips-v0-ik-xk.json) | current-compatible | `microfips` PR [#133](https://github.com/Amperstrand/microfips/pull/133) | `v0.4.0` @ `780dbadea096` |
| [`fips-v1-xx-draft`](profiles/fips-v1-xx-draft.json) | draft-future | `microfips` PR [#132](https://github.com/Amperstrand/microfips/pull/132) | `upstream-future` (unpinned) |

The v1 profile is draft only and must stay gated until upstream ships
compatible FMP v1 / Noise XX behavior.

## Repository layout

```text
fips-protocol-defs-mvp/
  README.md
  LICENSE
  .gitignore
  .secret-patterns.txt
  fips-upstream.json          # upstream pin table
  profiles/                   # source of truth: hand-authored profile JSON
  schema/                     # JSON Schema (draft-07 style) for profiles
  tools/                      # renderers + diff + reproducibility check
  generated/                  # AUTO-GENERATED rust/python/lua/markdown
  docs/                       # anchoring, consumer integration, diff example
  tests/                      # unittest (Python stdlib only)
  .github/workflows/ci.yml
```

## Commands

```bash
# Render every profile into generated/<lang>/
python3 tools/render_all.py

# Diff two profiles (stable, testable output)
python3 tools/diff_profiles.py profiles/fips-v0-ik-xk.json profiles/fips-v1-xx-draft.json

# Fail if checked-in generated files are stale
python3 tools/check_generated.py

# Run the test suite (Python stdlib only)
python3 -m unittest discover tests
```

Each renderer is also usable as a CLI against a single profile, e.g.:

```bash
python3 tools/render_rust.py   profiles/fips-v0-ik-xk.json
python3 tools/render_python.py profiles/fips-v0-ik-xk.json
python3 tools/render_lua.py    profiles/fips-v0-ik-xk.json
python3 tools/render_markdown.py profiles/fips-v0-ik-xk.json
```

## Constraints

- **Python standard library only.** No external runtime dependencies.
- **No real secrets.** See `.secret-patterns.txt` for the patterns this repo
  rejects. No keys, tokens, passwords, or credentials are stored here.
- **Deterministic output.** No timestamps, no machine-specific paths. Sort
  order is stable: messages sort as `msg1, msg2, msg3`; link message types
  sort numerically by value.
- **No upstream parsing yet.** This MVP is hand-authored profiles plus
  render/diff tooling. Upstream Rust source extraction is future work.

## Long-term plan

- Add **upstream source extraction** so constants come from pinned
  `jmcorgan/fips` source instead of hand-authored values.
- Add **golden vectors** for FMP handshake and link messages.
- Add **`fips-lab` capture validation** against profile metadata.
- Add **`microfips` generated Rust consumption** behind a feature flag.
- Propose **upstream docs / test-vectors / a `fips-proto-core` `no_std`
  crate** later, so this MVP can shrink to a thin consumer.

See [`docs/upstream-anchoring.md`](docs/upstream-anchoring.md),
[`docs/consumer-integration.md`](docs/consumer-integration.md), and
[`docs/protocol-diff-example.md`](docs/protocol-diff-example.md) for detail.

## License

MIT — see [`LICENSE`](LICENSE).
