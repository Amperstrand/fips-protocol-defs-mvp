# AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
# Regenerate with: python3 tools/render_all.py
#
# Source profile:   fips-v1-xx-draft
# Profile status:   draft-future
# Upstream repo:    https://github.com/jmcorgan/fips.git
# Upstream ref:     next
# Upstream commit:  81baeebf2247cc26e13ca631066b7ee6bc6380ca
# Generator:        tools/render_python.py
#
# This file is downstream experimental tooling. It is NOT the canonical
# FIPS protocol specification. Upstream jmcorgan/fips remains the authority.

PROFILE_NAME = "fips-v1-xx-draft"
PROFILE_STATUS = "draft-future"
FIPS_UPSTREAM_REPO = "https://github.com/jmcorgan/fips.git"
FIPS_UPSTREAM_REF = "next"
FIPS_UPSTREAM_COMMIT = "81baeebf2247cc26e13ca631066b7ee6bc6380ca"
FMP_VERSION = 1
HANDSHAKE_PATTERN = "XX"
COMMON_PREFIX_SIZE = 4
ESTABLISHED_HEADER_SIZE = 16
INNER_HEADER_SIZE = 5
HAS_MSG1 = True
HAS_MSG2 = True
HAS_MSG3 = True
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

COORDS_REQUIRED_SIZE = 34
ENCRYPTED_MIN_SIZE = 32
EPOCH_ENCRYPTED_SIZE = 24
EPOCH_SIZE = 8
HANDSHAKE_MSG1_SIZE = 33
HANDSHAKE_MSG2_SIZE = 106
HANDSHAKE_MSG3_SIZE = 73
MAX_MESSAGE_SIZE = 65535
MSG1_WIRE_SIZE = 41
MSG2_WIRE_SIZE = 118
MSG3_WIRE_SIZE = 85
MTU_EXCEEDED_SIZE = 36
NEGOTIATION_HEADER_SIZE = 10
PATH_MTU_NOTIFICATION_SIZE = 2
PUBKEY_SIZE = 33
RECEIVER_REPORT_SIZE = 54
REPLAY_WINDOW_SIZE = 2048
SENDER_REPORT_SIZE = 20
SESSION_DATAGRAM_HEADER_SIZE = 36
SESSION_RECEIVER_REPORT_SIZE = 53
SESSION_SENDER_REPORT_SIZE = 19
TAG_SIZE = 16
