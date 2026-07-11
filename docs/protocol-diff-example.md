# Protocol Diff Example

> This repository is **experimental downstream tooling**. The diff below
> describes a hand-authored draft profile, not a confirmed upstream change.

Running:

```bash
python3 tools/diff_profiles.py profiles/fips-v0-ik-xk.json profiles/fips-v1-xx-draft.json
```

currently produces output equivalent to:

```text
PROFILE_NAME: fips-v0-ik-xk -> fips-v1-xx-draft
STATUS: current-compatible -> draft-future
UPSTREAM_REF: v0.4.0 -> upstream-future
UPSTREAM_COMMIT: 780dbadea096 -> None
FMP_VERSION: 0 -> 1
HANDSHAKE_PATTERN: IK_XK -> XX
UPSTREAM_COMMIT value differs as above; see actual tool output for exact line
MSG1.PAYLOAD_PATTERN: <none> -> e
MSG2.PAYLOAD_PATTERN: <none> -> e,ee,s,es,epoch
MSG3: added
```

The canonical, minimal reviewable summary is:

```text
FMP_VERSION: 0 -> 1
HANDSHAKE_PATTERN: IK_XK -> XX
MSG3: added
```

## Why this matters

This makes `microfips` PR [#132](https://github.com/Amperstrand/microfips/pull/132)
reviewable: reviewers can see at a glance that the draft FMP v1 / Noise XX
profile:

- bumps the FMP version (`0 -> 1`),
- changes the handshake pattern (`IK_XK -> XX`),
- adds a third handshake message (`MSG3: added`),
- and carries per-message Noise payload patterns (`e`, `e,ee,s,es,epoch`,
  `s,se,epoch`).

Because the v1 profile is anchored to `upstream-future` with `commit: null`
and `status: draft-future`, this diff also makes it obvious that PR #132 must
stay **gated** until upstream `jmcorgan/fips` ships compatible FMP v1 / Noise
XX behavior.

> Note: `tools/diff_profiles.py` prints every field that changed. The exact
> set of lines depends on the two profiles being compared; the tool always
> exits 0 when inputs are valid, even when differences exist.
