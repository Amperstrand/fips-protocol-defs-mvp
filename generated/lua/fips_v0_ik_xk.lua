-- AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
-- Regenerate with: python3 tools/render_all.py
--
-- Source profile:   fips-v0-ik-xk
-- Profile status:   current-compatible
-- Upstream repo:    https://github.com/jmcorgan/fips.git
-- Upstream ref:     v0.4.0
-- Upstream commit:  d5ee526f0e15d6e7a6336cf5746c763f4d1779e8
-- Generator:        tools/render_lua.py
--
-- This file is downstream experimental tooling. It is NOT the canonical
-- FIPS protocol specification. Upstream jmcorgan/fips remains the authority.

local M = {}

M.PROFILE_NAME = "fips-v0-ik-xk"
M.PROFILE_STATUS = "current-compatible"
M.FIPS_UPSTREAM_REPO = "https://github.com/jmcorgan/fips.git"
M.FIPS_UPSTREAM_REF = "v0.4.0"
M.FIPS_UPSTREAM_COMMIT = "d5ee526f0e15d6e7a6336cf5746c763f4d1779e8"
M.FMP_VERSION = 0
M.HANDSHAKE_PATTERN = "IK_XK"
M.COMMON_PREFIX_SIZE = 4
M.ESTABLISHED_HEADER_SIZE = 16
M.INNER_HEADER_SIZE = 5
M.HAS_MSG1 = true
M.HAS_MSG2 = true
M.HAS_MSG3 = false

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

M.COLD_START_SAMPLES = 5
M.COORDS_REQUIRED_SIZE = 34
M.DEFAULT_COLD_START_INTERVAL_MS = 200
M.DEFAULT_LOG_INTERVAL_SECS = 30
M.DEFAULT_OWD_WINDOW_SIZE = 32
M.EPOCH_ENCRYPTED_SIZE = 24
M.EPOCH_SIZE = 8
M.HANDSHAKE_MSG1_SIZE = 106
M.HANDSHAKE_MSG2_SIZE = 57
M.JITTER_ALPHA_SHIFT = 4
M.MAX_MESSAGE_SIZE = 65535
M.MIN_SESSION_REPORT_INTERVAL_MS = 500
M.MTU_EXCEEDED_SIZE = 36
M.PATH_MTU_NOTIFICATION_SIZE = 2
M.PROTOCOL_VERSION = 1
M.PUBKEY_SIZE = 33
M.RECEIVER_REPORT_BODY_SIZE = 67
M.RECEIVER_REPORT_WIRE_SIZE = 72
M.REPLAY_WINDOW_SIZE = 2048
M.RTTVAR_BETA_SHIFT = 2
M.SENDER_REPORT_BODY_SIZE = 47
M.SENDER_REPORT_WIRE_SIZE = 52
M.SESSION_DATAGRAM_HEADER_SIZE = 36
M.SESSION_RECEIVER_REPORT_SIZE = 66
M.SESSION_SENDER_REPORT_SIZE = 46
M.SRTT_ALPHA_SHIFT = 3
M.TAG_SIZE = 16
M.XK_HANDSHAKE_MSG1_SIZE = 33
M.XK_HANDSHAKE_MSG2_SIZE = 57
M.XK_HANDSHAKE_MSG3_SIZE = 73

return M
