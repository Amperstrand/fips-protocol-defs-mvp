# Profile: fips-v1-xx-draft

> AUTO-GENERATED FILE. DO NOT EDIT BY HAND.
> Regenerate with: `python3 tools/render_all.py`
> Generator: `tools/render_markdown.py`

- **Status:** draft-future
- **Description:** future/draft FIPS profile for FMP v1 using Noise XX three-message handshake.

## Upstream provenance

| Field | Value |
| --- | --- |
| Repo | https://github.com/jmcorgan/fips.git |
| Ref | next |
| Commit | 81baeebf2247cc26e13ca631066b7ee6bc6380ca |
| Source | extraction-fed from canonical jmcorgan/fips@next (FMP v1 / Noise XX; draft, do not enable until upstream ships v0.5.0) |

> This profile is downstream experimental tooling. It is NOT the canonical
> FIPS protocol specification. Upstream `jmcorgan/fips` remains the authority.

## Intended consumers

- Amperstrand/microfips
- Amperstrand/fips-lab
- Wireshark Lua experiments

## Compatibility

- **microfips PR:** #132
- **fips-lab:** future capture decoding profile once upstream and microfips agree on FMP v1/XX
- **Upstream requirement:** do not enable until upstream FIPS ships compatible FMP v1 / Noise XX behavior

## FMP

- **Version:** 1
- **Handshake pattern:** XX
- **Common prefix size:** 4 bytes
- **Established header size:** 16 bytes
- **Inner header size:** 5 bytes

### Messages

| Message | Present | Role | Wire size | Payload pattern | Summary |
| --- | --- | --- | --- | --- | --- |
| msg1 | yes | initiator_to_responder | 33 bytes | e | Noise XX message 1: ephemeral key only |
| msg2 | yes | responder_to_initiator | 106 bytes | e,ee,s,es,epoch | Noise XX message 2: responder ephemeral/static encrypted material and epoch |
| msg3 | yes | initiator_to_responder | 73 bytes | s,se,epoch | Noise XX message 3: initiator static encrypted material and epoch |

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

- This profile is draft only.
- Do not use as default for microfips main.
- Keep PR #132 gated until upstream FIPS ships compatible FMP v1 / Noise XX.
- Add golden vectors before making this profile stable.

## Extracted constants (canonical upstream)

| Constant | Type | Value |
| --- | --- | --- |
| COORDS_REQUIRED_SIZE | usize | 34 |
| ENCRYPTED_MIN_SIZE | usize | 32 |
| EPOCH_ENCRYPTED_SIZE | usize | 24 |
| EPOCH_SIZE | usize | 8 |
| HANDSHAKE_MSG1_SIZE | usize | 33 |
| HANDSHAKE_MSG2_SIZE | usize | 106 |
| HANDSHAKE_MSG3_SIZE | usize | 73 |
| MAX_MESSAGE_SIZE | usize | 65535 |
| MSG1_WIRE_SIZE | usize | 41 |
| MSG2_WIRE_SIZE | usize | 118 |
| MSG3_WIRE_SIZE | usize | 85 |
| MTU_EXCEEDED_SIZE | usize | 36 |
| NEGOTIATION_HEADER_SIZE | usize | 10 |
| PATH_MTU_NOTIFICATION_SIZE | usize | 2 |
| PUBKEY_SIZE | usize | 33 |
| RECEIVER_REPORT_SIZE | usize | 54 |
| REPLAY_WINDOW_SIZE | usize | 2048 |
| SENDER_REPORT_SIZE | usize | 20 |
| SESSION_DATAGRAM_HEADER_SIZE | usize | 36 |
| SESSION_RECEIVER_REPORT_SIZE | usize | 53 |
| SESSION_SENDER_REPORT_SIZE | usize | 19 |
| TAG_SIZE | usize | 16 |
