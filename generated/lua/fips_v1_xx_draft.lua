-- AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
-- Regenerate with: python3 tools/render_all.py
--
-- Source profile:   fips-v1-xx-draft
-- Profile status:   draft-future
-- Upstream repo:    https://github.com/jmcorgan/fips.git
-- Upstream ref:     next
-- Upstream commit:  81baeebf2247cc26e13ca631066b7ee6bc6380ca
-- Generator:        tools/render_lua.py
--
-- This file is downstream experimental tooling. It is NOT the canonical
-- FIPS protocol specification. Upstream jmcorgan/fips remains the authority.

local M = {}

M.PROFILE_NAME = "fips-v1-xx-draft"
M.PROFILE_STATUS = "draft-future"
M.FIPS_UPSTREAM_REPO = "https://github.com/jmcorgan/fips.git"
M.FIPS_UPSTREAM_REF = "next"
M.FIPS_UPSTREAM_COMMIT = "81baeebf2247cc26e13ca631066b7ee6bc6380ca"
M.FMP_VERSION = 1
M.HANDSHAKE_PATTERN = "XX"
M.COMMON_PREFIX_SIZE = 4
M.ESTABLISHED_HEADER_SIZE = 16
M.INNER_HEADER_SIZE = 5
M.HAS_MSG1 = true
M.HAS_MSG2 = true
M.HAS_MSG3 = true

M.LINK_MESSAGE_TYPES = {
    [0x00] = "SessionDatagram",
    [0x01] = "SenderReport",
    [0x02] = "ReceiverReport",
    [0x10] = "TreeAnnounce",
    [0x20] = "FilterAnnounce",
    [0x30] = "LookupRequest",
    [0x31] = "LookupResponse",
    [0x50] = "Disconnect",
    [0x51] = "Heartbeat",
}

M.COORDS_REQUIRED_SIZE = 34
M.ENCRYPTED_MIN_SIZE = 32
M.EPOCH_ENCRYPTED_SIZE = 24
M.EPOCH_SIZE = 8
M.HANDSHAKE_MSG1_SIZE = 33
M.HANDSHAKE_MSG2_SIZE = 106
M.HANDSHAKE_MSG3_SIZE = 73
M.MAX_MESSAGE_SIZE = 65535
M.MSG1_WIRE_SIZE = 41
M.MSG2_WIRE_SIZE = 118
M.MSG3_WIRE_SIZE = 85
M.MTU_EXCEEDED_SIZE = 36
M.NEGOTIATION_HEADER_SIZE = 10
M.PATH_MTU_NOTIFICATION_SIZE = 2
M.PUBKEY_SIZE = 33
M.RECEIVER_REPORT_SIZE = 54
M.REPLAY_WINDOW_SIZE = 2048
M.SENDER_REPORT_SIZE = 20
M.SESSION_DATAGRAM_HEADER_SIZE = 36
M.SESSION_RECEIVER_REPORT_SIZE = 53
M.SESSION_SENDER_REPORT_SIZE = 19
M.TAG_SIZE = 16

return M
