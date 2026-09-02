---
rfc: "0008"
title: Audio Transport
status: Draft
authors:
  - Samband contributors
created: 2026-09-01
updated: 2026-09-02
target: Protocol v0.x
requires:
  - Agent 1 Protocol review
  - Agent 3 Routing review
  - Agent 4 Security review
  - Agent 8 Audio review before implementation
supersedes: []
superseded_by: null
---

# RFC-0008: Audio Transport

## Summary

This RFC will define freshness-oriented realtime audio framing and stream
lifecycle over an established Samband channel and PTT grant. Opus is the
preferred codec direction for evaluation, not an accepted profile. Production
audio begins only after generic protected multi-hop relay is proven.

## Status and authority

Draft and non-normative. This document establishes privacy and evidence
requirements but no codec settings, frame duration, byte layout, retransmission,
forward-error-correction, or jitter policy.

## Motivation

Realtime voice differs from control traffic: old frames quickly lose value, and
retransmission can increase latency more than intelligibility. Multi-hop mesh
loss, jitter, MTU variation, route changes, and device energy require an explicit
media contract shared across independent implementations.

## Goals

- prioritize latency and freshness over eventual delivery;
- support interoperable realtime voice with measured loss/jitter behavior;
- bind frames to an authorized PTT stream and protected channel context;
- define sequence/timing, start/end, codec negotiation, and stale-frame rules;
- avoid hidden transport fragmentation assumptions;
- ensure audio and transcripts are never persisted.

## Non-goals

- begin audio implementation before protected synthetic relay works;
- store-and-forward voice, voicemail, recording, or transcription;
- retransmit stale voice by default;
- select platform audio APIs in the protocol;
- claim quality or latency without physical measurements.

## Pipeline boundary

```text
microphone -> codec -> future reviewed channel boundary -> Samband relay -> open -> codec -> speaker
```

Relays process only the relay envelope and an opaque endpoint payload intended
for protection by a future Agent 4-reviewed profile. Endpoints own capture,
codec, jitter handling, and playback. Diagnostics may record safe metrics but
not audio bytes or reconstructable voice content.

## Control-plane and media-plane boundary

Audio uses two endpoint-only inner families inside RFC-0004's
`OPAQUE_ENDPOINT` payload:

| Inner family/type | Minimum semantic content | Audio bytes allowed |
| --- | --- | --- |
| `AUDIO_CONTROL.STREAM_START` | stream identity, accepted PTT grant reference, stream-owner action-subject reference or profile-pinned derivation, negotiated media profile, sequence/media-time origin, bounded stream parameters | no |
| `AUDIO_MEDIA.FRAME` | protected-record authenticated-principal/frame-sender binding, stream identity, media sequence, stream-relative media timestamp/duration, bounded frame flags, future-protected encoded-media content | yes, only under a future Agent 4-reviewed protection profile |
| `AUDIO_CONTROL.STREAM_END` | stream identity, final sequence/reference when known, bounded reason/discontinuity context | no |

Channel, authenticated principal, action subject, grant, stream, codec/profile,
sequence, timestamp, and audio
subtype remain inside the endpoint payload by default. Relays receive only the
coarse RFC-0004 traffic treatment justified by the routing profile. EXP-007 and
Agent 4 review are required before exposing any additional media metadata.

Encoded or plaintext audio is never embedded in discovery, mesh-control,
channel-control, PTT-control, `STREAM_START`, or `STREAM_END` messages.

The selected media profile must state whether the stream-owner subject is
carried in protected `STREAM_START` semantics or derived from the accepted
grant owner. The frame sender comes from the authenticated protected-record
principal unless an explicit protected sender reference is separately
authorized. Neither role is derived from packet identity, routing origin,
stream identity, or equal-looking bytes; every frame authorization binds the
principal, stream owner, grant, channel epoch, and current stream state.

## Proposed stream semantics

1. An endpoint can emit `STREAM_START` only while it holds an accepted,
   unexpired RFC-0007 grant in the same Agent 4-validated
   channel/principal/subject context.
2. A stream identity is unique within that channel/grant context for the
   profile-defined retention window and is distinct from packet, request, and
   grant identities.
3. `STREAM_START` binds exactly one negotiated media profile and initializes a
   stream-relative sequence/media-time domain. It does not create or extend a
   PTT grant.
4. `FRAME` is valid only for an accepted active stream and matching current PTT
   grant/security context. Media cannot establish or transfer ownership.
5. Media sequence and media timestamp are stream-relative. They are not trusted
   wall-clock time, forwarding TTL, packet identity, security replay state, or
   a nonce unless Agent 4 later defines and reviews an explicit relationship.
6. `STREAM_END` closes only the referenced stream. It does not substitute for
   PTT `RELEASE` and cannot close a newer/different stream.
7. Duplicate/reordered start/end operations are idempotent under their inner
   identities and cannot extend freshness or grant validity.
8. Missing `STREAM_END`, grant expiry, loss/expiry of the bound channel,
   arbitration, or security context, route recovery failure, or suspension
   closes the stream through bounded local expiry. Loss of one peer session is
   a routing event and does not by itself close the stream while bounded
   profile-defined recovery preserves the required endpoint context. No audio
   is retained for later completion or playback.

The codec/profile catalog, frame duration, bitrate, aggregation, sequence width
and wrap, media clock, flags, optional FEC/redundancy, and stream timeout remain
Agent 8/Agent 3/Agent 4-reviewed decisions informed by EXP-013.

## Semantics to define

The accepted RFC must define codec/profile negotiation, stream identity and
binding to PTT ownership, sequence and timestamp domain, frame duration and
aggregation, start/end/discontinuity, route change, stale threshold, loss
concealment signaling, optional redundancy/FEC, payload size, jitter buffer
expectations, and unsupported-profile behavior.

The selected experimental media profile must also define maximum concurrent
streams, maximum frame/media bytes, sequence/reorder window, local queue dwell,
receiver stale threshold, jitter-buffer duration/bytes, discontinuity handling,
and the exact relationship between PTT grant expiry and stream termination.

After successful channel-open and security-replay admission, an unknown
optional semantic field/extension in a known AUDIO_CONTROL or AUDIO_MEDIA type
may be ignored only if it cannot affect identity, stream/grant/channel/security
context, authority, authorization, replay/freshness, state preconditions, or
emitted actions. Unknown critical semantic elements reject locally as
`(audio, UNSUPPORTED_CRITICAL_EXTENSION)` before authorization/state mutation.
Agent 4 must protect element presence and criticality; protection-format and
security-profile fields remain `channel-security`-owned.

## Failure and resource bounds

Receivers must bound jitter buffers, decoder input, sequence gaps, stream count,
and unauthenticated work. Invalid, late, duplicate, replayed, oversized, or
wrong-stream frames are dropped safely. Audio frames cannot accumulate across
partitions or app suspension for later playback.

Routing duplicate suppression, security replay, media-sequence duplicate, and
receiver staleness are separate checks. A frame can have a fresh outer packet
identity yet still be a replayed, duplicate, or stale media operation. No one of
these checks substitutes for another.

The baseline permits no protocol-level retransmission of media after the
profile's freshness deadline. Control retries and optional FEC/redundancy must
be explicit, bounded, and measured; they cannot become hidden store-and-forward
voice.

## Privacy and security considerations

Frame cadence, size, codec mode, start/end, and speaker context can reveal
activity even if a future profile protects content. That profile must
authenticate stream/channel context and coordinate replay behavior with
RFC-0006. Debugging and crash artifacts must not contain raw or encoded audio.
Agent 4's initial boundary review is recorded, but the construction remains
unselected.

Agent 4 exclusively owns channel/principal/subject/grant/stream cryptographic binding,
security replay, any sequence/nonce relationship, media-profile negotiation
downgrade protection, sender/epoch context, failure oracles, and artifact audit.
This RFC chooses no key, nonce, signature, cipher, tag, epoch, or algorithm.
Until SG-008, the stream model is an interface for synthetic semantic vectors,
not a reviewed protected-audio claim.

The protected-record authenticated principal, PTT grant owner, stream owner,
and frame sender must be related by one exact authorization rule; equal-looking
IDs do not establish that relationship. Codec or playback processing occurs
only after protected-record authentication, security-replay acceptance, bounded
inner decode, action authorization, current-grant validation, stream binding,
and media freshness checks. A fresh packet ID or media sequence cannot revive
an old grant/security record.

SFrame RFC 9605 is a possible later framing candidate, not a complete Samband
security model: it delegates key management and receiver anti-replay, exposes
KID/counter metadata if outside the opaque boundary, and does not authenticate
one sender against other holders of the same symmetric key. Any SFrame header
stays inside `OPAQUE_ENDPOINT` by default and requires the RFC-0003/0006
membership, per-sender key, authorization, and replay contract.

Non-persistence applies to jitter/reorder buffers, logs, telemetry, crash dumps,
backups, swap/temporary files, test artifacts, and OS integrations as well as
application history. It cannot prevent an authorized recipient or compromised
endpoint from recording audio outside Samband.

## Routing considerations

The audio profile must fit forwarding sizes and freshness semantics from
RFC-0004/RFC-0005. Route changes can reorder or delay frames; routing must not
reliably retransmit media in a way that violates the stale threshold. The
latency budget must allocate capture, encode, queue, per-hop forwarding, jitter,
decode, and playback components.

RFC-0004 hop limit bounds forwarding distance but is not media age. Relays apply
bounded local queue policy; endpoints apply stream-relative sequence/reorder and
staleness rules after channel security. Media is never queued across a
partition or reconnection. Agent 3 must review whether the coarse visible
realtime treatment is sufficient and prevent control starvation under media
load.

Peer-session churn, route loss, endpoint channel-session closure, arbitration-
context invalidation, and protected-media security-context invalidation are
distinct events. A selected profile must define the bounded route-recovery
interval during which fresh media may continue over an alternate admitted path,
the queue/staleness limits during that interval, and the exact terminal event.
Recovery cannot extend the PTT grant, retain stale frames, or replay media.

## Alternatives to evaluate

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| fixed mandatory Opus baseline profile | simple interoperability | may not fit all devices/links | device/mesh latency and energy measurements |
| small negotiated set of Opus profiles | adaptability | negotiation and downgrade complexity | cross-platform compatibility prototype |
| application-selected arbitrary codec | flexibility | weak interoperability and attack surface | inconsistent with initial protocol goal |
| no retransmission with codec loss concealment | low latency | quality loss under bursts | seeded and physical loss tests |
| bounded redundancy/FEC | improved loss tolerance | bandwidth/latency/energy overhead | multi-hop comparison |

No alternative is selected.

## Test-vector and interoperability plan

After profile selection, vectors cover exact frame encoding, sequence/timestamp
wrap, start/end, missing/duplicate/reordered/late frames, route discontinuity,
unsupported profile, tampering, wrong PTT owner, bounded jitter, and codec
reference input/output tolerances where exact PCM output is not portable.
Synthetic tones or published non-personal fixtures must replace real recordings.

Protocol-semantic vectors precede codec vectors and cover start without grant,
matching start/frame/end, frame before start, wrong/expired grant, wrong stream,
duplicate start/end without extension, sequence gap/reorder/duplicate, stale
frame with fresh packet identity, missing end timeout, route discontinuity,
unsupported exact media profile, bounded concurrent streams/jitter state, and
no media retention across partition/merge. Until Agent 4 review, channel/open,
replay, and authorization verdicts are named synthetic non-production inputs.

## Migration and rollout

Each v0.x media profile is exact and pinned by the endpoint protocol profile.
Unknown profiles fail locally after the reviewed security boundary; relays do
not transcode or translate. An endpoint protocol/media-profile change, endpoint
channel-session closure, loss of the required arbitration/security context
after bounded profile-defined recovery, or grant invalidation terminates
affected streams and drops queued/stale media. Loss of one peer session alone
is only a routing event. No transition reinterprets frames under another codec/
security profile or stores them for later migration. Negotiation downgrade
protection remains Agent 4-owned.

## Measurements required

Report PTT acquisition, capture/encode, packetization, queue/per-hop, jitter,
decode/playback, and end-to-end latency separately. Report loss, burst loss,
reordering, bandwidth, CPU, battery, thermal behavior, and intelligibility/quality
method. Simulator results cannot substitute for physical audio measurements.

## Open questions

- Which Opus profiles, frame durations, bitrates, and channel modes are mandatory?
- What is the end-to-end and per-stage latency budget?
- How is codec/profile negotiation protected from downgrade?
- When do FEC or redundancy improve quality enough to justify overhead?
- How are timestamp clocks mapped without global synchronization?
- What safe diagnostics permit audio debugging without retaining voice?
- How do mobile suspension and route changes terminate or resume streams?
- What bounded alternate-route recovery survives peer-session churn without
  extending grant validity or retaining stale media?

## Review requirements

- [x] Agent 1 control/media split, stream/PTT binding, identity, processing,
  versioning, failure, and semantic-vector review recorded in this revision.
- [x] Agent 4 initial context/principal/grant/stream binding, replay, metadata,
  SFrame-boundary, and non-persistence requirements recorded.
- [ ] Agent 4 review of the selected protected media profile and SG-008 audit.
- [ ] Agent 3 freshness/routing assumption review.
- [ ] Agent 8 codec/profile/latency review after M4 prerequisites.
- [ ] Physical cross-platform measurements completed before acceptance.

## Acceptance blockers

- protected payload and PTT contracts are unresolved;
- codec/profile and latency budget lack evidence;
- freshness/FEC/jitter behavior is unresolved;
- no physical or cross-platform audio measurements exist;
- security construction and non-persistence implementation audit remain
  incomplete after the initial architecture review.

## Decision record

- 2026-09-01: Agent 1 revision separated opaque stream control from
  future-protected media frames, bound streams to accepted PTT grants, separated hop/replay/
  sequence/staleness domains, and prohibited control-plane audio bytes. RFC
  remains Draft pending protected payload, routing, security, codec, and physical
  evidence.
- 2026-09-02: Agent 4 required principal/grant/stream authorization before codec
  use, kept SFrame metadata inside the opaque boundary by default, and expanded
  non-persistence to runtime/platform artifacts. No media security construction
  or audio implementation was selected.
- 2026-09-02: Wave 0 integration review distinguished peer-session churn from
  loss of endpoint channel/arbitration/security context and required bounded,
  freshness-preserving route recovery before stream teardown. No recovery,
  media, routing, or security profile was selected; RFC remains Draft.

## References

- [`RFC-0006`](RFC-0006-encrypted-channel-payload.md)
- [`RFC-0007`](RFC-0007-ptt-arbitration.md)
- [`channel-security.md`](../security/channel-security.md)
- [`relay-security.md`](../security/relay-security.md)
- [`milestone-acceptance.md`](../architecture/milestone-acceptance.md)
