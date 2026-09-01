---
rfc: "0003"
title: Channel Identity and Membership
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

# RFC-0003: Channel Identity and Membership

## Summary

This RFC will define private-channel identity, authorization, membership proof,
membership changes, and offline operation. It keeps channel membership separate
from mesh participation and leaves credential and group-key choices unresolved.

## Status and authority

Draft and non-normative. A channel is an architectural concept, not yet a wire
identifier or cryptographic construction. Agent 4 review is mandatory.

## Motivation

Authorized endpoints must recognize channel traffic and one another without
requiring relays to join the channel. Adding and removing members through
partitions creates difficult authorization and key-rotation questions that
cannot be hidden in application state.

## Goals

- support zero, one, or many channel memberships per node;
- operate without a continuously available central authority;
- keep relays outside channel authorization and plaintext;
- define join, add, remove, leave, compromise, and rekey semantics;
- minimize channel-identifying metadata visible to non-members;
- support deterministic conformance tests.

## Non-goals

- choose a user directory or social graph;
- make human channel labels globally unique;
- select a group-key algorithm in this draft;
- define PTT arbitration or audio frames;
- promise instant revocation across disconnected partitions.

## Conceptual model

The design should distinguish a channel identifier or context, an authorization
state, a membership proof, payload-protection key state, membership epochs, and
local presentation metadata. Whether these are combined in one artifact is an
open security decision.

A relaying node receives no membership merely by forwarding channel traffic.
Human-visible labels such as "Channel 7" are not authorization evidence.

## Membership lifecycle

The accepted design must define channel creation, invitation/bootstrap,
authentication of existing and joining members, concurrent changes, removal,
leave, device loss, compromise, epoch transition, stale member behavior, and
partition merge. Availability and immediate revocation may conflict; the RFC
must state the chosen tradeoffs.

## Failure and resource bounds

Invalid proofs, oversized membership state, change floods, and divergent epoch
histories must fail within bounded work. Nodes cannot persist voice content to
repair a membership partition.

## Privacy and security considerations

Threats include unauthorized join, malicious inviter, removed member access,
compromised member, member enumeration, channel correlation, rollback, forked
membership state, replay, and denial of service. Security analysis must
distinguish confidentiality from authenticity and forward/post-compromise
properties rather than implying them.

## Routing considerations

Routing should not require plaintext channel identity. The RFC must specify how
an endpoint recognizes relevant protected traffic without exposing more channel
metadata to relays than necessary. Any multicast/dissemination implication must
be coordinated with RFC-0005.

## Wire and versioning impact

Future artifacts may include channel contexts, invitation/bootstrap data,
membership changes, proofs, epochs, and algorithm/version identifiers. No field,
encoding, or transport is chosen.

## Alternatives considered

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| pre-provisioned static group secret | simple offline bootstrap | poor removal, compromise, and scale properties | limited-profile threat analysis |
| signed membership state plus epoch keys | explicit audit/state | conflict and key-distribution complexity | partition/merge model |
| standardized group messaging construction | reviewed semantics and updates | implementation and resource complexity; fit unknown | Agent 4 standards evaluation/prototype |
| pairwise fan-out | simple pairwise security concepts | bandwidth and group consistency cost | scale/routing simulation |

No alternative is selected.

## Test-vector and interoperability plan

Semantic vectors must cover create, add, reject, remove, leave, concurrent
changes, stale epoch, partition, merge, compromise assumptions, and unauthorized
payload. Cryptographic vectors follow only after standard construction review.

## Open questions

- What makes a channel identity stable, private, and collision-resistant?
- Who may add or remove members, and how is that authority delegated?
- How are concurrent offline membership changes reconciled or rejected?
- What confidentiality can be promised after removal or device compromise?
- How does an endpoint select relevant opaque payloads without exposing channel
  membership to every relay?
- What usability ceremony is acceptable for offline channel bootstrap?

## Review requirements

- [ ] Agent 4 threat-model and group-key review.
- [ ] Agent 1 protocol state/wire review.
- [ ] Agent 3 dissemination metadata review.
- [ ] Partition/merge membership model tested.
- [ ] Positive and adversarial vector plan reviewed.

## Acceptance blockers

- channel identity and authorization model is unresolved;
- group-key/membership-change construction is unresolved;
- offline conflict and removal semantics are unresolved;
- metadata exposure is not analyzed.

## References

- [`RFC-0001`](RFC-0001-samband-network-model.md)
- [`RFC-0002`](RFC-0002-node-identity.md)
- [`RFC-0006`](RFC-0006-encrypted-channel-payload.md)
