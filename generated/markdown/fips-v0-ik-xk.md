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
| Commit | 780dbadea096 |
| Source | hand-authored MVP profile based on current microfips/fips-lab compatibility notes |

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
| msg1 | yes | initiator_to_responder | unknown | — | initial FMP handshake message for v0-compatible profile |
| msg2 | yes | responder_to_initiator | unknown | — | response FMP handshake message for v0-compatible profile |

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
