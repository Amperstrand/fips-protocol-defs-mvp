// AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
// Regenerate with: python3 tools/render_all.py
//
// Source profile:   fips-v1-xx-draft
// Profile status:   draft-future
// Upstream repo:    https://github.com/jmcorgan/fips.git
// Upstream ref:     next
// Upstream commit:  81baeebf2247cc26e13ca631066b7ee6bc6380ca
// Generator:        tools/render_rust.py
//
// This file is downstream experimental tooling. It is NOT the canonical
// FIPS protocol specification. Upstream jmcorgan/fips remains the authority.

pub const PROFILE_NAME: &str = "fips-v1-xx-draft";
pub const PROFILE_STATUS: &str = "draft-future";
pub const FIPS_UPSTREAM_REPO: &str = "https://github.com/jmcorgan/fips.git";
pub const FIPS_UPSTREAM_REF: &str = "next";
pub const FIPS_UPSTREAM_COMMIT: Option<&str> = Some("81baeebf2247cc26e13ca631066b7ee6bc6380ca");
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

pub const COORDS_REQUIRED_SIZE: usize = 34;
pub const ENCRYPTED_MIN_SIZE: usize = 32;
pub const EPOCH_ENCRYPTED_SIZE: usize = 24;
pub const EPOCH_SIZE: usize = 8;
pub const HANDSHAKE_MSG1_SIZE: usize = 33;
pub const HANDSHAKE_MSG2_SIZE: usize = 106;
pub const HANDSHAKE_MSG3_SIZE: usize = 73;
pub const MAX_MESSAGE_SIZE: usize = 65535;
pub const MSG1_WIRE_SIZE: usize = 41;
pub const MSG2_WIRE_SIZE: usize = 118;
pub const MSG3_WIRE_SIZE: usize = 85;
pub const MTU_EXCEEDED_SIZE: usize = 36;
pub const NEGOTIATION_HEADER_SIZE: usize = 10;
pub const PATH_MTU_NOTIFICATION_SIZE: usize = 2;
pub const PUBKEY_SIZE: usize = 33;
pub const RECEIVER_REPORT_SIZE: usize = 54;
pub const REPLAY_WINDOW_SIZE: usize = 2048;
pub const SENDER_REPORT_SIZE: usize = 20;
pub const SESSION_DATAGRAM_HEADER_SIZE: usize = 36;
pub const SESSION_RECEIVER_REPORT_SIZE: usize = 53;
pub const SESSION_SENDER_REPORT_SIZE: usize = 19;
pub const TAG_SIZE: usize = 16;
