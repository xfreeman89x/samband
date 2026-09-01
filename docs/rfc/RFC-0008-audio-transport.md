---
rfc: "0008"
title: Audio Transport
status: Draft
authors:
  - Samband contributors
created: 2026-09-01
updated: 2026-09-01
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
microphone -> codec -> channel protection -> Samband relay -> open -> codec -> speaker
```

Relays process only the relay envelope and opaque protected payload. Endpoints
own capture, codec, jitter handling, and playback. Diagnostics may record safe
metrics but not audio bytes or reconstructable voice content.

## Semantics to define

The accepted RFC must define codec/profile negotiation, stream identity and
binding to PTT ownership, sequence and timestamp domain, frame duration and
aggregation, start/end/discontinuity, route change, stale threshold, loss
concealment signaling, optional redundancy/FEC, payload size, jitter buffer
expectations, and unsupported-profile behavior.

## Failure and resource bounds

Receivers must bound jitter buffers, decoder input, sequence gaps, stream count,
and unauthenticated work. Invalid, late, duplicate, replayed, oversized, or
wrong-stream frames are dropped safely. Audio frames cannot accumulate across
partitions or app suspension for later playback.

## Privacy and security considerations

Frame cadence, size, codec mode, start/end, and speaker context can reveal
activity even when content is protected. Payloads must authenticate stream and
channel context and coordinate replay behavior with RFC-0006. Debugging and
crash artifacts must not contain raw or encoded audio. Agent 4 review is required.

## Routing considerations

The audio profile must fit forwarding sizes and freshness semantics from
RFC-0004/RFC-0005. Route changes can reorder or delay frames; routing must not
reliably retransmit media in a way that violates the stale threshold. The
latency budget must allocate capture, encode, queue, per-hop forwarding, jitter,
decode, and playback components.

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

## Review requirements

- [ ] Agent 1 media framing/versioning review.
- [ ] Agent 4 context binding, replay, metadata, and artifact review.
- [ ] Agent 3 freshness/routing assumption review.
- [ ] Agent 8 codec/profile/latency review after M4 prerequisites.
- [ ] Physical cross-platform measurements completed before acceptance.

## Acceptance blockers

- protected payload and PTT contracts are unresolved;
- codec/profile and latency budget lack evidence;
- freshness/FEC/jitter behavior is unresolved;
- no physical or cross-platform audio measurements exist;
- security and non-persistence audit is incomplete.

## References

- [`RFC-0006`](RFC-0006-encrypted-channel-payload.md)
- [`RFC-0007`](RFC-0007-ptt-arbitration.md)
- [`milestone-acceptance.md`](../architecture/milestone-acceptance.md)
