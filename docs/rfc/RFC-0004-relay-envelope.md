---
rfc: "0004"
title: Relay Envelope
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
supersedes: []
superseded_by: null
---

# RFC-0004: Relay Envelope

## Summary

This RFC will define the forwardable Samband relay envelope that separates
minimal routing/validation metadata from an opaque protected payload. It lists
required semantic questions but deliberately leaves field set, encoding,
authentication, addressing, and lifetime representation unresolved.

## Status and authority

Draft and non-normative. The relay-envelope/protected-payload separation is an
architectural invariant. No example field name, order, type, or diagram in this
draft is a wire contract.

## Motivation

Relays need enough information to reject malformed or exhausted traffic,
suppress duplicates, apply policy, and move a packet. Excess metadata weakens
privacy; insufficient authenticated metadata enables loops, injection, and
resource abuse. All implementations need one reviewed boundary.

## Goals

- carry opaque endpoint payloads through non-member relays;
- bound packet size, lifetime, duplication, parsing, and forwarding work;
- support protocol versioning and controlled extensibility;
- expose only routing and policy metadata demonstrated necessary;
- define deterministic processing and rejection order;
- support control and fresh media semantics without conflating them.

## Non-goals

- choose the routing algorithm or channel encryption construction;
- define audio frame contents;
- expose private-channel labels for relay convenience;
- provide generic arbitrary-protocol tunneling;
- freeze a byte encoding before measurement and security review.

## Candidate semantic information

The evaluation must determine whether and how an envelope represents protocol
version/profile, message family, packet identity, forwarding lifetime, routing
target/context, traffic/freshness class, payload length, extension information,
and integrity/authentication context.

This is a question list, not a proposed fixed field set. Each item needs an
owner, visibility justification, maximum size, validation rule, and versioning
behavior.

## Processing model to define

An accepted RFC must order framing/size checks, version negotiation, structural
validation, authentication appropriate to the layer, lifetime check, duplicate
or replay handling, policy/routing lookup, local delivery, and forwarding. It
must state which failure is observable and what state, if any, is updated.

## Failure and resource bounds

The decoder must reject truncation, overflow, impossible lengths, unsupported
critical extensions, excessive allocation, and invalid lifetime without panic
or unbounded work. Duplicate and replay state must be bounded. Maximum frame and
payload sizes require transport and simulator evidence.

## Privacy and security considerations

Packet IDs, routing targets, traffic class, length, timing, and stable extension
patterns can reveal relationships. Authentication fields may themselves create
linkability. Agent 4 must produce a field-by-field metadata budget and analyze
injection, modification, downgrade, replay, amplification, and parsing attacks.

## Routing considerations

Agent 3 must specify the minimum information needed for candidate routing
strategies, lifetime semantics, loop handling, local delivery, and multi-link
forwarding. Routing convenience alone does not justify channel metadata.

## Encoding and versioning alternatives

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| compact fixed binary header | predictable and efficient | rigid evolution; optional-field pressure | size and versioning prototype |
| length-delimited TLV envelope | extensible and skippable | parsing/canonicalization complexity and overhead | fuzzing/overhead prototype |
| established schema encoding | tooling and multi-language support | dependency, canonicalization, unknown-field semantics | library/license/interoperability study |
| small fixed prefix plus bounded extensions | balances fast rejection and evolution | two-layer complexity | decoder prototype and negative corpus |

No encoding is selected.

## Test-vector and interoperability plan

Vectors must cover minimum/maximum valid frames, exact bytes, unknown versions
and extensions, truncation at every boundary, length overflow, lifetime
exhaustion, duplicate identity, tampering, invalid authentication, payload
opacity, and stable error categories. Decoder fuzzing is required before freeze.

## Open questions

- What addressing or routing target is visible at each hop?
- What packet identity provides bounded duplicate handling without excessive
  tracking or collision risk?
- Is lifetime hop-based, time-based, or combined?
- Which metadata is authenticated end-to-end, hop-by-hop, or both?
- How are unknown optional and critical extensions distinguished?
- What maximum sizes work across candidate transports without hidden fragmentation?
- Can control and media share one envelope without unnecessary metadata?

## Review requirements

- [ ] Agent 1 field, encoding, processing, and versioning review.
- [ ] Agent 3 minimum routing metadata and lifetime review.
- [ ] Agent 4 metadata budget and attack-surface review.
- [ ] Cross-language decoder prototype and benchmarks.
- [ ] Negative corpus and fuzz plan reviewed.

## Acceptance blockers

- routing information requirements are unknown;
- identity/authentication and replay relationships are unknown;
- encoding and size limits lack evidence;
- metadata/privacy analysis is absent;
- processing order and versioning are unresolved.

## References

- [`RFC-0001`](RFC-0001-samband-network-model.md)
- [`RFC-0005`](RFC-0005-mesh-routing.md)
- [`RFC-0006`](RFC-0006-encrypted-channel-payload.md)
