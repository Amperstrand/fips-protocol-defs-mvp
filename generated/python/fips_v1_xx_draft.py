# AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
# Regenerate with: python3 tools/render_all.py
#
# Source profile:   fips-v1-xx-draft
# Profile status:   draft-future
# Upstream repo:    https://github.com/jmcorgan/fips.git
# Upstream ref:     upstream-future
# Upstream commit:  <unpinned>
# Generator:        tools/render_python.py
#
# This file is downstream experimental tooling. It is NOT the canonical
# FIPS protocol specification. Upstream jmcorgan/fips remains the authority.

PROFILE_NAME = "fips-v1-xx-draft"
PROFILE_STATUS = "draft-future"
FIPS_UPSTREAM_REPO = "https://github.com/jmcorgan/fips.git"
FIPS_UPSTREAM_REF = "upstream-future"
FIPS_UPSTREAM_COMMIT = None
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
