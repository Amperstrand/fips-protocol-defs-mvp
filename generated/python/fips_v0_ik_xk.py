# AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
# Regenerate with: python3 tools/render_all.py
#
# Source profile:   fips-v0-ik-xk
# Profile status:   current-compatible
# Upstream repo:    https://github.com/jmcorgan/fips.git
# Upstream ref:     v0.4.0
# Upstream commit:  d5ee526f0e15d6e7a6336cf5746c763f4d1779e8
# Generator:        tools/render_python.py
#
# This file is downstream experimental tooling. It is NOT the canonical
# FIPS protocol specification. Upstream jmcorgan/fips remains the authority.

PROFILE_NAME = "fips-v0-ik-xk"
PROFILE_STATUS = "current-compatible"
FIPS_UPSTREAM_REPO = "https://github.com/jmcorgan/fips.git"
FIPS_UPSTREAM_REF = "v0.4.0"
FIPS_UPSTREAM_COMMIT = "d5ee526f0e15d6e7a6336cf5746c763f4d1779e8"
FMP_VERSION = 0
HANDSHAKE_PATTERN = "IK_XK"
COMMON_PREFIX_SIZE = 4
ESTABLISHED_HEADER_SIZE = 16
INNER_HEADER_SIZE = 5
HAS_MSG1 = True
HAS_MSG2 = True
HAS_MSG3 = False
LINK_MESSAGE_TYPES = {
    0x00: "SessionDatagram",
    0x01: "SenderReport",
    0x02: "ReceiverReport",
    0x10: "TreeAnnounce",
    0x20: "FilterAnnounce",
    0x30: "LookupRequest",
    0x31: "LookupResponse",
    0x50: "Disconnect",
    0x51: "Heartbeat",
}

COLD_START_SAMPLES = 5
COORDS_REQUIRED_SIZE = 34
DEFAULT_COLD_START_INTERVAL_MS = 200
DEFAULT_LOG_INTERVAL_SECS = 30
DEFAULT_OWD_WINDOW_SIZE = 32
EPOCH_ENCRYPTED_SIZE = 24
EPOCH_SIZE = 8
HANDSHAKE_MSG1_SIZE = 106
HANDSHAKE_MSG2_SIZE = 57
JITTER_ALPHA_SHIFT = 4
MAX_MESSAGE_SIZE = 65535
MIN_SESSION_REPORT_INTERVAL_MS = 500
MTU_EXCEEDED_SIZE = 36
PATH_MTU_NOTIFICATION_SIZE = 2
PROTOCOL_VERSION = 1
PUBKEY_SIZE = 33
RECEIVER_REPORT_BODY_SIZE = 67
RECEIVER_REPORT_WIRE_SIZE = 72
REPLAY_WINDOW_SIZE = 2048
RTTVAR_BETA_SHIFT = 2
SENDER_REPORT_BODY_SIZE = 47
SENDER_REPORT_WIRE_SIZE = 52
SESSION_DATAGRAM_HEADER_SIZE = 36
SESSION_RECEIVER_REPORT_SIZE = 66
SESSION_SENDER_REPORT_SIZE = 46
SRTT_ALPHA_SHIFT = 3
TAG_SIZE = 16
XK_HANDSHAKE_MSG1_SIZE = 33
XK_HANDSHAKE_MSG2_SIZE = 57
XK_HANDSHAKE_MSG3_SIZE = 73
