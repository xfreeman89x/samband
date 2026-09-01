---
rfc: "0001"
title: Samband Network Model
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

# RFC-0001: Samband Network Model

## Summary

This RFC will define the protocol-visible model for Samband Nodes participating
in a shared, opportunistic transport mesh while private radio channels remain
separate protected overlays. It establishes the problem space for capabilities,
neighbors, relays, partitions, and future gateways without selecting wire
messages or algorithms yet.

## Status and authority

Draft and non-normative. The separation between transport network and private
channel, capability-driven roles, opaque foreign relay, transport independence,
and ephemeral audio are inherited project invariants. Their exact protocol
representation is unresolved.

## Motivation

Every later RFC needs a common answer to what a node, link, relay, endpoint, and
channel are. Without it, platform or routing implementations could accidentally
make channel membership a prerequisite for mesh participation or treat a device
type as a permanent capability.

## Goals

- define protocol concepts independently from Android, iOS, Rust, and transports;
- allow a node to combine and dynamically change endpoint, relay, and future
  gateway capabilities;
- treat partitions and merge as routine states;
- minimize identity and channel information exposed to non-members;
- bound community relay to eligible Samband traffic.

## Non-goals

- choose node identity or discovery identifiers;
- choose routing algorithms, metrics, or message encodings;
- choose channel credentials, cryptography, PTT, or audio framing;
- define gateway operation in Protocol v0;
- provide generic IP forwarding.

## Proposed conceptual model

A Samband Node participates through one or more transport attachments. A current
one-hop authenticated participant is a neighbor. The mesh forms from these
links and carries Samband relay/control traffic.

Private channels are logical overlays authorized independently from the mesh.
An endpoint may originate or consume channel payloads. A relay may forward an
opaque payload regardless of its channel memberships. Capabilities describe
current availability and willingness, not permanent device categories.

Capability state needs freshness and withdrawal semantics, but no representation
or timer is proposed in this draft.

Candidate local relay policies include disabled, opportunistic, and full relay;
candidate future gateway data policies include never, Wi-Fi only, and explicitly
enabled mobile data. These are evaluation concepts, not wire values or accepted
defaults. Mobile-data relay must never be enabled silently.

## Failure and resource bounds

The eventual protocol must bound capability state, neighbor state, forwarding
lifetime, duplicate state, control propagation, and work caused by unauthenticated
peers. A partition cannot trigger storage of missed audio for later replay.

## Privacy and security considerations

Discovery and capability advertisements may permit tracking or device
fingerprinting. Stable node identity may need separation from discovery and
session identifiers. Relays should learn only the metadata required for safe
forwarding. Agent 4 review is required before this model can enter Discussion.

## Routing considerations

The model must let Agent 3 define routes through willing non-members, handle
capability withdrawal, and reconverge after partition/merge. Whether the network
uses destination routing, controlled dissemination, or a hybrid is unresolved.

## Wire and versioning impact

Expected future families include discovery/session establishment, capability
exchange, mesh control, and relay traffic. Names, fields, authentication,
ordering, and encoding require Agent 1 review and later RFCs.

## Alternatives considered

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| channel-scoped transport meshes | simpler channel routing | excludes foreign relays; exposes membership; duplicates infrastructure | not aligned with project invariant |
| fixed device roles | simple implementation | false under mobile lifecycle; blocks heterogeneous nodes | platform capability experiments |
| capability-based shared mesh | composable and transport-independent | freshness and abuse complexity | simulator and platform evidence |

## Test-vector and interoperability plan

Semantic scenarios must cover zero-channel relay, multiple channel memberships,
dynamic relay withdrawal, partitioned operation, merge, and a node with several
transport attachments. Negative cases must cover unknown/stale/inconsistent
capabilities once their semantics exist.

## Open questions

- What minimum capability vocabulary is mandatory in Protocol v0?
- Which capabilities are authenticated, negotiated, or locally observed?
- What constitutes a neighbor before and after peer authentication?
- Does a Samband mesh need an explicit network-scope identifier?
- How are capability freshness and withdrawal represented without excess chatter?
- Which gateway concepts, if any, must be reserved for version negotiation?

## Review requirements

- [ ] Agent 1 Protocol review.
- [ ] Agent 3 Routing review.
- [ ] Agent 4 Security review.
- [ ] Capability transition vectors designed.
- [ ] Metadata inventory completed.

## Acceptance blockers

- identity and neighbor-authentication model is unresolved;
- capability vocabulary/freshness is unresolved;
- routing and metadata requirements have not been reconciled;
- no threat-model review exists.

## References

- [`network-model.md`](../architecture/network-model.md)
- [`RFC-0002`](RFC-0002-node-identity.md)
- [`RFC-0005`](RFC-0005-mesh-routing.md)
