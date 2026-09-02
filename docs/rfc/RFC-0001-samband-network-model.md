---
rfc: "0001"
title: Samband Network Model
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
supersedes: []
superseded_by: null
---

# RFC-0001: Samband Network Model

## Summary

This RFC proposes the protocol-visible layering, peer/session model, message
taxonomy, and capability representation for Samband Protocol v0.x. A Samband
Node participates in a shared opportunistic mesh while private channels remain
endpoint overlays. Relays process a small outer protocol and do not need to
understand channel, PTT, or audio message bodies.

The proposal is precise enough to align later RFCs and semantic vectors, but it
does not select a wire encoding, routing algorithm, identity construction,
channel credential, cryptographic primitive, PTT arbitration algorithm, or
audio profile.

## Status and authority

Draft and non-normative. The separation between transport network and private
channel, capability-driven roles, opaque foreign relay, transport independence,
and ephemeral audio are inherited project invariants.

This revision records Agent 1's proposed logical protocol model and Agent 4's
initial security requirements. It does not authorize implementation of
security- or routing-sensitive shared contracts. The exact outer metadata set,
peer-session construction, and claim-authentication rules remain subject to
open review gates and [`EXP-007`](../research/experiment-backlog.md).

## Motivation

Every later RFC needs one answer to what a node, link, peer session, relay,
endpoint payload, and capability are. Without an explicit layering and message
model, implementations could accidentally expose channel activity to relays,
make channel membership a prerequisite for forwarding, or treat a platform
label as a permanent role.

## Goals

- define protocol concepts independently from Android, iOS, Rust, and concrete
  transports;
- separate one-hop peer control, mesh control, and opaque endpoint traffic;
- allow a node to combine and dynamically change endpoint and relay behavior;
- treat partitions, merge, and session loss as routine states;
- minimize identity and channel information exposed to non-members;
- provide bounded capability replacement, freshness, and withdrawal semantics;
- give later RFCs one catalog of proposed logical messages.

## Non-goals

- choose node credentials, signatures, authentication, or discovery aliases;
- choose routing algorithms, metrics, addressing schemes, or byte encodings;
- choose channel credentials, encryption, replay protection, PTT arbitration,
  or audio framing;
- define gateway operation in Protocol v0.x;
- provide generic IP forwarding or store-and-forward voice.

## Protocol layering

Samband v0.x is proposed as four semantic layers above a one-hop transport:

```text
one-hop transport attachment
          |
          v
outer Samband envelope and peer/mesh protocol
          |
          +-----------> routing and relay disposition
          |
          v
opaque endpoint payload and future Agent 4-reviewed channel boundary
          |
          v
channel, PTT control, and realtime media semantics
```

The one-hop transport moves bounded frames and reports link state. It does not
define a Samband peer, route, channel, or PTT state.

The outer protocol contains only information needed to negotiate a peer
session, advertise bounded mesh capability, validate/route an eligible packet,
and enforce lifetime and duplicate rules. The endpoint protocol is carried as
an opaque payload through relays.

An endpoint/relay node evaluates local delivery and forwarding independently.
Failure or inability to open an endpoint payload does not by itself prohibit an
otherwise eligible relay action.

## Peer and session model

A **transport adjacency** is a live one-hop attachment to another transport
peer. It is an untrusted input boundary.

A **peer session** is the protocol context produced after exact experimental
compatibility-pair selection and the security/admission checks required by its
protocol profile.
Discovery traffic can propose a session but cannot create authoritative
neighbor, capability, routing, or duplicate state by itself.

A **neighbor** is a peer with a current admitted one-hop session. Agent 4 must
define the authentication and admission evidence; this RFC does not equate a
transport connection with an authenticated node identity.

Peer-session identifiers, discovery handles, routing origin contexts,
long-lived node credentials, channel-member identities, and display names are
distinct concepts. Their binding is owned by RFC-0002 and Agent 4 review.

## Two-level message taxonomy

### Routing-visible outer classes

Only three outer classes are proposed. Exact numeric codes and encoding remain
unselected.

| Outer class | Scope | Relay behavior | Proposed logical types |
| --- | --- | --- | --- |
| `LINK_CONTROL` | current one-hop adjacency or admitted peer session | never forwarded | `DISCOVERY_ADVERTISEMENT`, `SESSION_INIT`, `SESSION_ACCEPT`, `SESSION_REJECT`, `CAPABILITY_SNAPSHOT`, `HEARTBEAT` |
| `MESH_CONTROL` | bounded mesh scope | processed/forwarded only under the selected routing profile | `ROUTE_ADVERTISEMENT` and `ROUTE_WITHDRAWAL` are candidates only; Agent 3 selects the actual types |
| `OPAQUE_ENDPOINT` | endpoint delivery through zero or more relays | payload is not parsed by relays | one opaque endpoint container intended for protection by a future Agent 4-reviewed profile |

`NEIGHBOR_STATE` is local derived state, not a message. It is derived from
transport events, admitted peer-session state, capability snapshots, heartbeat
semantics, and the routing profile.

There is no nested `RELAY_FORWARD` message. Forwarding is an outer-envelope
disposition defined by RFC-0004 and RFC-0005; wrapping an envelope in another
relay message would add metadata and ambiguous lifetime state.

### Endpoint-only inner families

After the Agent 4-defined channel-security boundary accepts and opens an
`OPAQUE_ENDPOINT` payload, an endpoint can encounter these proposed families:

| Inner family | Proposed logical types | Governing RFC |
| --- | --- | --- |
| `CHANNEL` | `SESSION_INIT`, `MEMBERSHIP_PROOF`, `SESSION_ACCEPT`, `SESSION_REJECT`, `MEMBERSHIP_UPDATE`, `SESSION_CLOSE` | RFC-0003 and RFC-0006 |
| `PTT` | `REQUEST`, `GRANT`, `BUSY`, `RELEASE` | RFC-0007 |
| `AUDIO_CONTROL` | `STREAM_START`, `STREAM_END` | RFC-0008 |
| `AUDIO_MEDIA` | `FRAME`; encoded-media content is permitted only under a future Agent 4-reviewed protection profile | RFC-0008 |

Inner family/type names are semantic labels for drafts and vectors, not wire
values. Channel/PTT/audio types must not be exposed in the outer envelope by
default. Any proposed exposure requires a field-by-field justification through
Agent 4 review and EXP-007.

Plaintext or encoded audio bytes are never carried in discovery, mesh-control,
channel-control, PTT-control, stream-start, or stream-end bodies.

## Message identity domains

Identifiers at different layers are not interchangeable:

- a bounded discovery/session exchange identity correlates one link-local
  bootstrap attempt and gains no authority by itself;
- an outer packet identity supports bounded forwarding duplicate suppression;
- a capability generation makes full snapshots replaceable and idempotent;
- a route revision, when selected by RFC-0005, identifies routing state;
- channel operation, PTT request/grant, stream, and media sequence identifiers
  support their own state machines;
- security replay state is defined by Agent 4 and RFC-0006.

Retransmitting the same logical operation can use a new outer packet identity
while retaining the operation identifier. A new packet identity cannot make a
replayed or unauthorized endpoint operation valid.

## Capability representation

Capabilities are session-scoped, dynamic statements, not permanent device
types. The proposed representation is a full replacement snapshot containing:

| Logical item | Proposed rule |
| --- | --- |
| session context | binds the snapshot to exactly one admitted peer session |
| generation | unsigned; replacements strictly increase, identical retries may repeat, and it never wraps |
| validity duration | bounded relative duration measured from acceptance on a local monotonic clock; no sender wall-clock trust |
| entries | bounded set of unique capability identifiers with explicit criticality and bounded typed parameters |

Every capability entry carries an explicit criticality value; absence is
malformed, not an implicit `false`. Any parameter form that can be independently
unknown likewise carries explicit profile-defined criticality. EXP-002 owns the
encoding, not whether that semantic value exists.

When an admitted session has no generation high-water mark, the first valid
snapshot establishes it with any value permitted by the exact profile. A higher
generation then atomically replaces the previous snapshot. While the current
snapshot remains unexpired, an identical generation with identical content is
idempotent and does not refresh its receipt-relative expiry; the same generation
with different content is a state conflict and is not applied. A lower
generation is stale.

"Identical content" means equality of the complete profile-canonical snapshot,
including unknown optional identifiers/parameters and their criticality, not
only the subset interpreted locally. EXP-002 must select the canonical equality
rule. Validity expiry withdraws the entries but retains the session's generation
high-water mark; the expired canonical content need not be retained. After
expiry, every snapshot with `generation <= highWater` is `STALE`, including a
same-generation formerly identical or changed snapshot. Only a higher
generation can establish new capability state. Session closure clears the
high-water mark. Generation exhaustion therefore requires a new admitted
session rather than wrap or rollback. A peer can withdraw earlier by sending a
higher-generation snapshot that omits the capability.

A `HEARTBEAT` updates only the liveness state defined by the selected profile;
it does not silently extend capability validity or resurrect an expired/
withdrawn snapshot.

Unknown non-critical capability identifiers are ignored for behavior and cannot
enable a feature. An unknown capability marked critical, or an unknown critical
parameter on a known capability, rejects the entire atomic snapshot as
`(capability, UNSUPPORTED_CRITICAL_EXTENSION)`. Unknown optional parameters on
a known capability are ignored. Exact critical-field encoding is an EXP-002
decision.

The minimum routing-facing vocabulary is a statement of current relay
willingness and only those optional behaviors already registered by the exact
session profile. A capability cannot change, replace, or renegotiate that
profile; a capability identifier or parameter outside it follows the unknown/
critical rules above. Battery, thermal, mobile-data, platform, and detailed
radio state remain local policy inputs unless RFC-0005 demonstrates that a
bounded, privacy-reviewed wire value is necessary. Capability snapshots never
contain channel identifiers or channel memberships.

Before a snapshot can create authoritative state, its security profile must
bind the complete profile-canonical snapshot to the admitted peer session and
exact compatibility pair. Coverage includes the session context, generation,
validity duration, every entry and parameter, unknown optional content, and
all criticality markers. A peer-session authentication result establishes only
the immediate peer's authority to make its own session-scoped capability
claim; it does not authenticate a forwarded third-party route or capability
claim. Claim origin, delegation, and dissemination admission remain separate
RFC-0005 and Agent 3/4 contracts.

The concrete authentication construction, maximum entry counts, identifier
allocation, validity limits, and first registered capability set remain
blocked on Agent 3/Agent 4 review, EXP-015, EXP-017, and EXP-018.

## Failure and resource bounds

Every experimental profile must set finite limits for transport frame size,
outer header/extensions, payload size, advertised profiles, capability entries
and parameters, peer sessions, routing state, duplicate state, and work caused
by unauthenticated discovery.

Invalid discovery or session proposals create no authoritative neighbor,
capability, routing, channel, or duplicate state. Capability expiry disables
the affected behavior; it does not preserve stale relay willingness for
availability. A partition cannot trigger storage of missed audio for replay.

## Privacy and security considerations

This RFC deliberately defines security interfaces, not security mechanisms.
Agent 4's initial threat-model review requires later profiles to decide and
review:

- node credential, discovery alias, peer-session identity, and routing-origin
  binding;
- authenticated-session admission and complete integrity coverage for session
  and capability messages;
- downgrade resistance for profile negotiation;
- authorization and protection of endpoint payloads;
- security replay state, separately from forwarding duplicate suppression;
- metadata exposure from outer class, traffic treatment, target, length,
  timing, packet identity, capabilities, and extensions.

Every exact-pair offer, selection, rejection-relevant transcript element,
participant role, session-exchange identity, credential identity, freshness
input, and capability claim must be bound according to the selected security
profile. Partial binding or an unauthenticated fallback is not a compatible
mode. The candidate session constructions and identity assurance choices are
catalogued in [`node-identity.md`](../security/node-identity.md); selection and
evidence remain open.

No long-lived node ID, channel credential, signature, cipher, key identifier,
nonce, membership proof, or replay value is selected here. The relay-visible
inventory is tracked in [`relay-security.md`](../security/relay-security.md)
and [`discovery-privacy.md`](../security/discovery-privacy.md). The inner
taxonomy is a visibility target pending SG-001 through the relevant security
gate, not a claim of confidentiality or end-to-end encryption.

## Routing considerations

RFC-0005 must let Agent 3 route through willing non-members, consume only
admitted/session-bound capabilities and protocol-approved outer metadata,
handle snapshot withdrawal, and reconverge after partition/merge. It must not
inspect an `OPAQUE_ENDPOINT` payload or infer a route from channel membership.

The routing review must determine whether `MESH_CONTROL` messages are unicast,
disseminated, or both; what target form is minimally necessary; and which
capabilities or link metrics are local versus shared. These choices cannot add
new outer metadata without reconciling RFC-0004 and EXP-007.

## Wire and versioning impact

RFC-0004 defines the logical envelope, exact-profile negotiation, unknown
field/type handling, packet identity, hop limit, duplicate behavior, and
processing order. EXP-002 selects an encoding only after at least two candidates
exercise the same semantic vectors.

The outer and inner catalogs are registries owned by the protocol. Adding a
peer-visible outer class/type or changing forwarding behavior requires an RFC.
Adding an endpoint-only type still requires an RFC when independent endpoints
observe it, but does not require relays to learn the type.

## Alternatives considered

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| expose channel/PTT/audio as outer packet types | simple relay classification | leaks activity and couples relays to endpoint features | EXP-007 metadata budget; not proposed by default |
| two-level outer/inner taxonomy | relays remain generic and channel-blind | endpoint protection/dispatch boundary must be precise | Agent 4 review plus semantic vectors |
| fixed device roles | simple implementation | false under mobile lifecycle and heterogeneous hosts | platform capability experiments |
| incremental capability deltas | smaller updates | loss/reordering and unbounded history complexity | EXP-015 comparison |
| full replacement capability snapshots | bounded and deterministic | repeated bytes and expiry chatter | EXP-015 comparison |

## Test-vector and interoperability plan

Semantic vectors must cover session-state admission, unsupported exact profiles,
first capability generation, full replacement, identical-generation retry
without expiry refresh, stale/conflicting generations, canonical equality with
unknown optional parameters, expiry with retained high-water mark, identical
and changed same-generation post-expiry retries that remain stale, withdrawal,
unknown optional/critical capability parameters, zero-channel relay, an
endpoint/relay performing local delivery and forwarding, partition, merge, and
a node with several transport attachments.

Vectors use the draft format in
[`../../protocol/test-vectors/FORMAT.md`](../../protocol/test-vectors/FORMAT.md).
No exact-byte vector is canonical until EXP-002 selects an encoding.

## Migration and rollout

Every Protocol v0.x profile is experimental and exactly selected. No
compatibility is inferred from a higher minor number. A node can participate
only in the message catalogs and capability rules of the exact selected
profile. Relays do not translate profiles.

## Open questions

- Which capabilities form the minimal outer registry for the first simulator
  profile? Owner: Agent 1 + Agent 3; EXP-015.
- What authentication/admission result creates a peer session and neighbor?
  Owner: Agent 4; SG-002 and EXP-017.
- What routing-origin context is stable enough to route but private enough to
  avoid a global tracking identifier? Owner: Agent 3 + Agent 4; EXP-005.
- Which outer traffic distinctions are strictly necessary? Owner: Agent 3 +
  Agent 4; EXP-007.
- What maximum snapshot validity and entry bounds fit the v0 operating
  envelope? Owner: Agent 3; EXP-004 and EXP-015.

## Review requirements

- [x] Agent 1 logical layering, taxonomy, capability, and version-boundary
  review recorded in this revision.
- [ ] Agent 3 Routing review of outer classes, capability inputs, and freshness.
- [x] Agent 4 initial threat-model and contract review of session admission,
  visibility, binding, and metadata recorded; construction selection and
  security gates remain open.
- [ ] Capability transition vectors validated against EXP-015 evidence.
- [ ] EXP-007 metadata inventory completed.

## Acceptance blockers

- Agent 3 has not approved routing-visible metadata and capability semantics;
- no peer-session construction, credential assurance policy, capability-claim
  authentication, or complete negotiation-binding profile is selected;
- relay-visible metadata has an initial inventory but no measured privacy
  budget or approved mitigation;
- capability bounds and validity have no EXP-004/EXP-015 evidence;
- no encoding or exact-byte catalog values exist pending EXP-002;
- the initial threat model has not completed maintainer and independent
  security review.

## Decision record

- 2026-09-01: Agent 1 revision proposed the two-level taxonomy, admitted
  peer-session boundary, full replacement capability snapshots, and distinct
  identity domains. RFC remains Draft pending Routing and Security review.
- 2026-09-02: Agent 4 recorded complete negotiation/capability binding,
  immediate-peer versus third-party-claim separation, and metadata/privacy
  requirements. No credential, session protocol, or protection construction
  was selected; RFC remains Draft and all applicable security gates stay open.

## References

- [`network-model.md`](../architecture/network-model.md)
- [`shared-contracts.md`](../architecture/shared-contracts.md)
- [`RFC-0002`](RFC-0002-node-identity.md)
- [`RFC-0004`](RFC-0004-relay-envelope.md)
- [`RFC-0005`](RFC-0005-mesh-routing.md)
- [`node identity security`](../security/node-identity.md)
- [`discovery privacy`](../security/discovery-privacy.md)
- [`relay security`](../security/relay-security.md)
- [`experiment-backlog.md`](../research/experiment-backlog.md)
