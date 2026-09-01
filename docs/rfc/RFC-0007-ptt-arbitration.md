---
rfc: "0007"
title: PTT Arbitration
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

# RFC-0007: PTT Arbitration

## Summary

This RFC will define half-duplex Push-To-Talk floor control without assuming a
central authority. It must handle simultaneous requests, partitions, merge,
stale ownership, loss, delay, and malicious participants. No arbitration
algorithm, clock model, or message encoding is selected here.

## Status and authority

Draft and non-normative. `REQUEST`, `GRANTED`, `BUSY`, and `RELEASE` are
conceptual interactions, not frozen message names or a guaranteed sequence.

## Motivation

Users need predictable feedback about who may transmit. In an opportunistic
mesh, nodes can see different channel partitions and event orders. A design that
assumes a reachable coordinator fails the off-grid goal, while an unbounded
distributed consensus protocol conflicts with realtime latency and partitions.

## Goals

- primarily half-duplex channel behavior without permanent central authority;
- deterministic resolution for concurrent requests within a connected view;
- bounded stale ownership and recovery after speaker disappearance;
- explicit partition and merge behavior;
- authentication and authorization of floor-control actions;
- low acquisition latency and bounded control overhead;
- observable state suitable for deterministic simulation.

## Non-goals

- guarantee one global speaker across disconnected partitions;
- create permanent consensus or a blockchain;
- define audio codec or channel-key management;
- persist or replay audio missed while a request was unresolved;
- assume synchronized trustworthy wall clocks.

## State model to define

The accepted design must define local states such as idle, requesting,
transmitting, receiving/busy, releasing, and recovery; the authoritative event
inputs; request identity; ownership term/epoch or equivalent; tie-breaking;
timeouts; retransmission/replacement; cancellation; and merge behavior.

User-visible state should distinguish confirmed permission from optimistic or
partition-local behavior if both exist.

## Failure and resource bounds

Requests, retries, ownership records, and deduplication state must expire and be
bounded. Lost release, node disappearance, delayed grants, reordered messages,
clock skew, duplicate requests, request floods, and conflicting partition owners
must not cause permanent lockout or unbounded control traffic.

## Privacy and security considerations

Floor-control messages can reveal channel activity, speaker identity, timing,
and membership. A malicious member can monopolize or jam the floor, forge
release, replay grants, or exhaust request state. Agent 4 must review authorization,
replay, privacy, and abuse limits; cryptography cannot force a malicious member
to transmit fairly.

## Routing considerations

Arbitration latency and consistency depend on propagation and topology. Agent 3
must characterize whether control uses unicast, dissemination, a selected
coordinator, or another pattern, and how route changes affect ownership. PTT
must not assume delivery guarantees unavailable from RFC-0005.

## Alternatives to evaluate

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| deterministic distributed contention with bounded lease | no fixed coordinator | clock/partition conflicts and fairness | seeded loss/skew/concurrency simulation |
| dynamically elected reachable coordinator | simple decisions while reachable | election latency and partition leaders | churn and merge experiments |
| circulating token/permission artifact | explicit ownership | token loss/recovery and path dependency | loss/partition simulation |
| optimistic local transmit with conflict suppression | low perceived latency | overlapping speech and inconsistent feedback | UX/latency/conflict measurements |

No alternative is selected.

## Wire and versioning impact

Future semantics may require request IDs, participant or sender context,
ownership generation, priority/policy, expiry or logical ordering, decisions,
and release/recovery signals. Exact fields, confidentiality, and encoding remain
unresolved.

## Test-vector and interoperability plan

Deterministic vectors must cover single request, concurrent requests with every
event ordering, loss/duplication/reordering, delayed request/grant/release,
speaker disappearance, timeout, partition-local speakers, merge, stale messages,
unauthorized actions, monopolization limits, and version mismatch.

## Open questions

- Is a partition-local speaker allowed, and how is that presented to users?
- What fairness or priority policy belongs in Protocol v0?
- Can arbitration use logical time without synchronized clocks?
- What acquisition latency budget is realistic over several hops?
- Which party grants the floor in a fully decentralized channel?
- How are conflicting owners resolved after merge without replaying audio?
- What abuse controls are enforceable against an authorized malicious member?

## Review requirements

- [ ] Agent 1 state-machine and wire review.
- [ ] Agent 3 propagation/partition review.
- [ ] Agent 4 authorization, privacy, replay, and abuse review.
- [ ] Deterministic arbitration comparison completed.
- [ ] User-visible ambiguity documented.

## Acceptance blockers

- arbitration alternative and clock model are unresolved;
- routing delivery assumptions and latency budget are unknown;
- partition/merge semantics are unresolved;
- authorization and abuse model is unreviewed.

## References

- [`RFC-0003`](RFC-0003-channel-identity-and-membership.md)
- [`RFC-0005`](RFC-0005-mesh-routing.md)
- [`RFC-0008`](RFC-0008-audio-transport.md)

