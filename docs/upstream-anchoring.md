# Upstream Anchoring

> This repository is **experimental downstream tooling**. It is not the
> canonical FIPS protocol specification. Upstream [`jmcorgan/fips`](https://github.com/jmcorgan/fips)
> remains the authority.

## Principles

1. **Upstream remains the authority.** `jmcorgan/fips` defines the protocol.
   This MVP only describes profiles that downstream consumers
   (`Amperstrand/microfips`, `Amperstrand/fips-lab`, Wireshark experiments)
   need to stay wire-compatible.
2. **Every profile is pinned.** Each profile under `profiles/` records the
   upstream `repo`, `ref`, and `commit` it is anchored to. Draft profiles
   that are not yet upstream-compatible carry `commit: null` and a clear
   `status` of `draft-future`.
3. **Generated files carry provenance.** Every file under `generated/`
   embeds the source profile name, profile status, upstream repo/ref/commit,
   and the generator that produced it, plus a "do not edit by hand" notice.
4. **CI checks reproducibility.** `tools/check_generated.py` re-renders every
   profile and fails CI if any checked-in generated file drifts. This keeps
   the JSON profiles as the single source of truth inside this repo.
5. **No timestamps, no machine-specific paths.** Generated output is
   deterministic and diffable.

## Current pins

See [`fips-upstream.json`](../fips-upstream.json) for the canonical pin table:

| Profile | Upstream ref | Commit | Status |
| --- | --- | --- | --- |
| `fips-v0-ik-xk` | `v0.4.0` | `780dbadea096` | current-compatible |
| `fips-v1-xx-draft` | `upstream-future` | _unpinned_ | draft-future |

The `fips-v1-xx-draft` profile is intentionally unpinned because upstream
has not shipped compatible FMP v1 / Noise XX behavior. Do not enable it in
`microfips` main until upstream ships and this pin is filled in.

## Future tooling (not in MVP)

- A comparison tool that fetches the pinned ref and compares it against the
  `master` tip of `jmcorgan/fips`, surfacing drift that may require a profile
  update.
- Extraction of constants directly from the pinned upstream Rust source,
  replacing the hand-authored values in `profiles/`.
- Golden test vectors validated against pinned upstream.

## Long-term upstreamable pieces

Once the profiles and generators mature, the following pieces are candidates
to propose **upstream** into `jmcorgan/fips`, so this MVP can shrink back to a
thin consumer:

- `docs/protocol/fmp.md` — FMP (FIPS Messaging Protocol) narrative spec.
- `docs/protocol/link.md` — link-layer message type table.
- `test-vectors/fmp/*.bin` — canonical binary handshake/message vectors.
- A possible `fips-proto-core` `no_std` crate exposing the same constants
  this MVP currently generates, so `microfips` can depend on it directly.

Until those exist upstream, this repo is the proving ground.
