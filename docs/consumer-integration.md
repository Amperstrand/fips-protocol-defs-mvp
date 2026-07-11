# Consumer Integration

> This repository is **experimental downstream tooling**. Generated constants
> are not yet consumed by any downstream project. This document describes the
> intended integration path so consumers can plan around it.

The normalized JSON profile under `profiles/` is the source of truth. From it,
`tools/render_all.py` produces:

- Rust `no_std` constants under `generated/rust/`
- Plain Python constants under `generated/python/`
- Lua tables under `generated/lua/`
- Human-readable Markdown under `generated/markdown/`

## `Amperstrand/microfips`

Integration is intentionally staged so runtime behavior is not disturbed.

1. **Metadata only.** First, document in `microfips` which PR targets which
   profile:
   - PR [#133](https://github.com/Amperstrand/microfips/pull/133) targets
     `fips-v0-ik-xk` (current-compatible).
   - PR [#132](https://github.com/Amperstrand/microfips/pull/132) targets
     `fips-v1-xx-draft` (draft-future, must stay gated).
2. **Constants.** Vendor the generated Rust constants
   (`generated/rust/fips_v0_ik_xk.rs`) behind a feature flag or a new module,
   without changing existing runtime constants.
3. **Tests.** Add compile-time / unit tests that assert the local
   `microfips` wire constants match the generated profile constants. At this
   stage mismatches are test failures, not behavior changes.
4. **Behavior switch (later).** Only after tests are green across the matrix,
   switch runtime code to consume the generated constants directly.

Do not change `microfips` runtime behavior in the docs-only first PR.

## `Amperstrand/fips-lab`

1. Replace duplicated FMP/link constants inside the capture decoder with the
   generated Python constants (`generated/python/fips_v0_ik_xk.py`).
2. Validate btsnoop / packet capture decoding against the profile metadata
   (FMP version, handshake pattern, header sizes, message types).
3. Add generated capture fixtures later, once golden vectors exist.

## Wireshark experiments

- The generated Lua output (`generated/lua/*.lua`) is **constants and tables
  only**. It returns a module table `M` with `M.FMP_VERSION`, `M.LINK_MESSAGE_TYPES`,
  etc.
- A handwritten dissector should `require` / import the generated module and
  use its tables for field decoding.
- This MVP deliberately does **not** generate a full dissector.

## Reproducibility contract

Every generated file embeds:

- source profile name and status,
- upstream repo / ref / commit,
- generator name,
- a "do not edit by hand" notice.

CI runs `tools/check_generated.py` on every push and pull request, so any
consumer vendoring a generated file can trust it matches the checked-in
profile exactly.
