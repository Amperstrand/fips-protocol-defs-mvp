#![no_std]
//! FIPS wire-protocol definition constants — `no_std`, zero-alloc.
//!
//! Thin wrapper over the extraction-fed generated constants from the
//! `fips-protocol-defs-mvp` project. This is **experimental downstream
//! tooling**, not the canonical FIPS specification; upstream `jmcorgan/fips`
//! remains the authority.
//!
//! Enable exactly one profile feature. `fips-v0-ik-xk` (default) is the
//! current-compatible FMP v0 / IK-XK profile, pinned to
//! `jmcorgan/fips@v0.4.0 @ d5ee526`. The generated file embeds full provenance
//! (upstream repo/ref/commit) and a "do not edit by hand" notice.

#[cfg(feature = "fips-v0-ik-xk")]
include!("../../../generated/rust/fips_v0_ik_xk.rs");
