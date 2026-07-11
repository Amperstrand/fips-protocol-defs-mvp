// AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
// Regenerate with: python3 tools/render_all.py
//
// Source profile:   fips-v1-xx-draft
// Profile status:   draft-future
// Upstream repo:    https://github.com/jmcorgan/fips.git
// Upstream ref:     upstream-future
// Upstream commit:  <unpinned>
// Generator:        tools/render_rust.py
//
// This file is downstream experimental tooling. It is NOT the canonical
// FIPS protocol specification. Upstream jmcorgan/fips remains the authority.

pub const PROFILE_NAME: &str = "fips-v1-xx-draft";
pub const PROFILE_STATUS: &str = "draft-future";
pub const FIPS_UPSTREAM_REPO: &str = "https://github.com/jmcorgan/fips.git";
pub const FIPS_UPSTREAM_REF: &str = "upstream-future";
pub const FIPS_UPSTREAM_COMMIT: Option<&str> = None;
pub const FMP_VERSION: u8 = 1;
pub const HANDSHAKE_PATTERN: &str = "XX";
pub const COMMON_PREFIX_SIZE: usize = 4;
pub const ESTABLISHED_HEADER_SIZE: usize = 16;
pub const INNER_HEADER_SIZE: usize = 5;
pub const HAS_MSG1: bool = true;
pub const HAS_MSG2: bool = true;
pub const HAS_MSG3: bool = true;
pub const LINK_MESSAGE_TYPES: &[(u8, &str)] = &[
    (0x00, "SessionDatagram"),
    (0x01, "SenderReport"),
    (0x02, "ReceiverReport"),
    (0x10, "TreeAnnounce"),
    (0x20, "FilterAnnounce"),
    (0x30, "LookupRequest"),
    (0x31, "LookupResponse"),
    (0x50, "Disconnect"),
    (0x51, "Heartbeat"),
];
