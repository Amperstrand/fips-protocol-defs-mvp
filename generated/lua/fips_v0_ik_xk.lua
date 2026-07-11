-- AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
-- Regenerate with: python3 tools/render_all.py
--
-- Source profile:   fips-v0-ik-xk
-- Profile status:   current-compatible
-- Upstream repo:    https://github.com/jmcorgan/fips.git
-- Upstream ref:     v0.4.0
-- Upstream commit:  780dbadea096
-- Generator:        tools/render_lua.py
--
-- This file is downstream experimental tooling. It is NOT the canonical
-- FIPS protocol specification. Upstream jmcorgan/fips remains the authority.

local M = {}

M.PROFILE_NAME = "fips-v0-ik-xk"
M.PROFILE_STATUS = "current-compatible"
M.FIPS_UPSTREAM_REPO = "https://github.com/jmcorgan/fips.git"
M.FIPS_UPSTREAM_REF = "v0.4.0"
M.FIPS_UPSTREAM_COMMIT = "780dbadea096"
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

return M
