---
rfc: "0006"
title: Encrypted Channel Payload
status: Draft
authors:
  - Samband contributors
created: 2026-09-01
updated: 2026-09-01
target: Protocol v0.x
requires:
  - Agent 4 Security review
  - Agent 1 Protocol review
supersedes: []
superseded_by: null
---

# RFC-0006: Encrypted Channel Payload

## Summary

This RFC will define how authorized endpoints protect private-channel payloads
so non-member relays cannot recover or undetectably modify their content. It
separates payload protection from transport security, peer authentication, and
channel authorization. No cryptographic construction is selected here.

## Status and authority

Draft and non-normative. The project intends end-to-end confidentiality, but no
implementation may claim end-to-end encryption until Agent 4 has approved the
identity, membership, key, algorithm, nonce, authentication, and replay design.

## Motivation

The iconic Samband path crosses a foreign relay. Link encryption alone ends at
that relay and is insufficient. A protected payload must remain opaque across
multiple transports while binding the right channel context, sender/epoch state,
freshness, and relevant relay-envelope metadata without leaking unnecessary
information.

## Goals

- protect channel payload confidentiality and integrity between authorized
  endpoints across foreign relays;
- use standard, reviewed cryptographic constructions;
- coordinate keys with channel membership changes and compromise assumptions;
- prevent nonce misuse, replay, cross-channel substitution, and downgrade;
- make failure behavior and metadata exposure explicit;
- support streaming/fresh media without persisting content.

## Non-goals

- invent cryptographic primitives;
- treat transport security as channel security;
- hide all traffic timing, size, or topology by unsubstantiated claim;
- solve membership authorization independently from RFC-0003;
- define audio codec/framing or PTT arbitration.

## Security-layer separation

The accepted specification must distinguish:

1. transport/link protection, if any;
2. node/session authentication;
3. channel membership and authorization;
4. end-to-end payload confidentiality/integrity;
5. replay protection and duplicate suppression;
6. optional metadata-protection techniques.

Success in one layer cannot be cited as success in another.

## Required construction properties

Agent 4 must define algorithm agility without downgrade, key identifiers or
epochs, sender/context binding, nonce strategy, authenticated associated data,
payload length limits, replay windows, rekey/rotation, member removal behavior,
compromise limits, secret storage, and erasure expectations.

Whether relays can validate any outer authentication before forwarding, and
which envelope fields are end-to-end authenticated, remain open questions.

## Failure and resource bounds

Invalid tags, unknown algorithms/epochs, replay, truncated payloads, excessive
lengths, missing keys, and state rollback must fail safely and within bounded
work. Authentication failure must not expose partial plaintext or detailed
oracle behavior to untrusted peers.

## Privacy and metadata considerations

Encryption does not hide packet size, timing, route, traffic class, or all key
and epoch correlations. Padding, batching, aliasing, and cover traffic have
energy/latency costs and are not assumed. Agent 4 must state the metadata budget
and residual traffic-analysis exposure.

## Alternatives to evaluate

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| shared channel epoch key | efficient group media | sender attribution, removal, compromise, nonce coordination complexity | threat model and multi-sender prototype |
| per-sender keys within channel epochs | clearer sender state and nonce domains | distribution and membership-change overhead | scale and key-update model |
| standardized group messaging protocol/construction | reviewed membership/key semantics | realtime/offline/resource fit may be complex | Agent 4 standards analysis and prototype |
| pairwise encryption fan-out | familiar pairwise properties | bandwidth grows with members; relay/routing overhead | group-size simulation |

No alternative or primitive is selected.

## Wire and versioning impact

The protected payload may need version/algorithm context, epoch/sender context,
nonce or sequence information, ciphertext, and authentication data. Whether
these live inside or alongside the opaque relay payload, and which are visible,
requires joint Agent 1/Agent 4 design.

## Test-vector and interoperability plan

After construction selection, use published synthetic keys to cover valid
protection/opening, wrong channel/sender/epoch/context, nonce boundaries,
replay, tampering at every field, truncation, unknown algorithms, removal/rekey,
and deterministic standard vectors where safe. Randomized encryption vectors
must fix all randomness explicitly.

## Open questions

- Which standard construction meets offline group PTT requirements?
- What forward secrecy, post-compromise security, and removal guarantees are
  feasible without continuous connectivity?
- How are multi-sender nonce domains made misuse-resistant?
- Which relay-envelope fields are authenticated end to end?
- What channel/epoch metadata must be visible for recipient selection?
- How are lost key updates handled without storing missed audio?
- What padding or size-hiding policy is justified by measured costs?

## Review requirements

- [ ] Agent 4 construction, keys, threat, and metadata review.
- [ ] Agent 1 payload/wire/versioning review.
- [ ] RFC-0003 membership lifecycle reconciled.
- [ ] RFC-0004 associated metadata reconciled.
- [ ] Standard vectors and negative cases reviewed.

## Acceptance blockers

- threat model and membership/key architecture are incomplete;
- no standard construction is selected or analyzed;
- nonce/replay/epoch behavior is unresolved;
- metadata exposure and failure oracles are unreviewed.

## References

- [`RFC-0003`](RFC-0003-channel-identity-and-membership.md)
- [`RFC-0004`](RFC-0004-relay-envelope.md)
- [`review-gates.md`](../security/review-gates.md)

