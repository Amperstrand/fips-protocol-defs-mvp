// AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
// Regenerate with: python3 tools/render_all.py
//
// Source profile:   fips-v0-ik-xk
// Profile status:   current-compatible
// Upstream repo:    https://github.com/jmcorgan/fips.git
// Upstream ref:     v0.4.0
// Upstream commit:  d5ee526f0e15d6e7a6336cf5746c763f4d1779e8
// Generator:        tools/render_rust.py
//
// This file is downstream experimental tooling. It is NOT the canonical
// FIPS protocol specification. Upstream jmcorgan/fips remains the authority.

pub const PROFILE_NAME: &str = "fips-v0-ik-xk";
pub const PROFILE_STATUS: &str = "current-compatible";
pub const FIPS_UPSTREAM_REPO: &str = "https://github.com/jmcorgan/fips.git";
pub const FIPS_UPSTREAM_REF: &str = "v0.4.0";
pub const FIPS_UPSTREAM_COMMIT: Option<&str> = Some("d5ee526f0e15d6e7a6336cf5746c763f4d1779e8");
pub const FMP_VERSION: u8 = 0;
pub const HANDSHAKE_PATTERN: &str = "IK_XK";
pub const COMMON_PREFIX_SIZE: usize = 4;
pub const ESTABLISHED_HEADER_SIZE: usize = 16;
pub const INNER_HEADER_SIZE: usize = 5;
pub const HAS_MSG1: bool = true;
pub const HAS_MSG2: bool = true;
pub const HAS_MSG3: bool = false;
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

pub const COLD_START_SAMPLES: u32 = 5;
pub const COORDS_REQUIRED_SIZE: usize = 34;
pub const DEFAULT_COLD_START_INTERVAL_MS: u64 = 200;
pub const DEFAULT_LOG_INTERVAL_SECS: u64 = 30;
pub const DEFAULT_OWD_WINDOW_SIZE: usize = 32;
pub const EPOCH_ENCRYPTED_SIZE: usize = 24;
pub const EPOCH_SIZE: usize = 8;
pub const HANDSHAKE_MSG1_SIZE: usize = 106;
pub const HANDSHAKE_MSG2_SIZE: usize = 57;
pub const JITTER_ALPHA_SHIFT: u32 = 4;
pub const MAX_MESSAGE_SIZE: usize = 65535;
pub const MIN_SESSION_REPORT_INTERVAL_MS: u64 = 500;
pub const MTU_EXCEEDED_SIZE: usize = 36;
pub const PATH_MTU_NOTIFICATION_SIZE: usize = 2;
pub const PROTOCOL_VERSION: u8 = 1;
pub const PUBKEY_SIZE: usize = 33;
pub const RECEIVER_REPORT_BODY_SIZE: usize = 67;
pub const RECEIVER_REPORT_WIRE_SIZE: usize = 72;
pub const REPLAY_WINDOW_SIZE: usize = 2048;
pub const RTTVAR_BETA_SHIFT: u32 = 2;
pub const SENDER_REPORT_BODY_SIZE: usize = 47;
pub const SENDER_REPORT_WIRE_SIZE: usize = 52;
pub const SESSION_DATAGRAM_HEADER_SIZE: usize = 36;
pub const SESSION_RECEIVER_REPORT_SIZE: usize = 66;
pub const SESSION_SENDER_REPORT_SIZE: usize = 46;
pub const SRTT_ALPHA_SHIFT: u32 = 3;
pub const TAG_SIZE: usize = 16;
pub const XK_HANDSHAKE_MSG1_SIZE: usize = 33;
pub const XK_HANDSHAKE_MSG2_SIZE: usize = 57;
pub const XK_HANDSHAKE_MSG3_SIZE: usize = 73;
