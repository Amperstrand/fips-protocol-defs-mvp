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
