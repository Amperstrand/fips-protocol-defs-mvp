# Profile: fips-v0-ik-xk

> AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
> Regenerate with: `python3 tools/render_all.py`
> Generator: `tools/render_markdown.py`

- **Status:** current-compatible
- **Description:** current-compatible FIPS profile for FMP v0 using IK/XK-style handshake behavior.

## Upstream provenance

| Field | Value |
| --- | --- |
| Repo | https://github.com/jmcorgan/fips.git |
| Ref | v0.4.0 |
| Commit | d5ee526f0e15d6e7a6336cf5746c763f4d1779e8 |
| Source | extraction-fed from canonical jmcorgan/fips@v0.4.0 (see snapshot_ref) |

> This profile is downstream experimental tooling. It is NOT the canonical
> FIPS protocol specification. Upstream `jmcorgan/fips` remains the authority.

## Intended consumers

- Amperstrand/microfips
- Amperstrand/fips-lab
- Wireshark Lua experiments

## Compatibility

- **microfips PR:** #133
- **fips-lab:** current generated Python constants should target this profile first
- **Upstream requirement:** current FIPS v0-compatible deployment

## FMP

- **Version:** 0
- **Handshake pattern:** IK_XK
- **Common prefix size:** 4 bytes
- **Established header size:** 16 bytes
- **Inner header size:** 5 bytes

### Messages

| Message | Present | Role | Wire size | Payload pattern | Summary |
| --- | --- | --- | --- | --- | --- |
| msg1 | yes | initiator_to_responder | 106 bytes | — | initial FMP handshake message for v0-compatible profile |
| msg2 | yes | responder_to_initiator | 57 bytes | — | response FMP handshake message for v0-compatible profile |

## Link message types

| Value | Name |
| --- | --- |
| 0x00 | SessionDatagram |
| 0x01 | SenderReport |
| 0x02 | ReceiverReport |
| 0x10 | TreeAnnounce |
| 0x20 | FilterAnnounce |
| 0x30 | LookupRequest |
| 0x31 | LookupResponse |
| 0x50 | Disconnect |
| 0x51 | Heartbeat |

## Notes

- This profile is intended to describe the stable current interop path.
- Exact byte-level vectors should be added later.
- Constants should eventually be extracted from pinned upstream source instead of hand-authored.

## Extracted constants (canonical upstream)

| Constant | Type | Value |
| --- | --- | --- |
| COLD_START_SAMPLES | u32 | 5 |
| COORDS_REQUIRED_SIZE | usize | 34 |
| DEFAULT_COLD_START_INTERVAL_MS | u64 | 200 |
| DEFAULT_LOG_INTERVAL_SECS | u64 | 30 |
| DEFAULT_OWD_WINDOW_SIZE | usize | 32 |
| EPOCH_ENCRYPTED_SIZE | usize | 24 |
| EPOCH_SIZE | usize | 8 |
| HANDSHAKE_MSG1_SIZE | usize | 106 |
| HANDSHAKE_MSG2_SIZE | usize | 57 |
| JITTER_ALPHA_SHIFT | u32 | 4 |
| MAX_MESSAGE_SIZE | usize | 65535 |
| MIN_SESSION_REPORT_INTERVAL_MS | u64 | 500 |
| MTU_EXCEEDED_SIZE | usize | 36 |
| PATH_MTU_NOTIFICATION_SIZE | usize | 2 |
| PROTOCOL_VERSION | u8 | 1 |
| PUBKEY_SIZE | usize | 33 |
| RECEIVER_REPORT_BODY_SIZE | usize | 67 |
| RECEIVER_REPORT_WIRE_SIZE | usize | 72 |
| REPLAY_WINDOW_SIZE | usize | 2048 |
| RTTVAR_BETA_SHIFT | u32 | 2 |
| SENDER_REPORT_BODY_SIZE | usize | 47 |
| SENDER_REPORT_WIRE_SIZE | usize | 52 |
| SESSION_DATAGRAM_HEADER_SIZE | usize | 36 |
| SESSION_RECEIVER_REPORT_SIZE | usize | 66 |
| SESSION_SENDER_REPORT_SIZE | usize | 46 |
| SRTT_ALPHA_SHIFT | u32 | 3 |
| TAG_SIZE | usize | 16 |
| XK_HANDSHAKE_MSG1_SIZE | usize | 33 |
| XK_HANDSHAKE_MSG2_SIZE | usize | 57 |
| XK_HANDSHAKE_MSG3_SIZE | usize | 73 |
