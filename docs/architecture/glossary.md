# Samband Glossary

Terms in this glossary are architectural vocabulary. Exact wire names and
representations require accepted RFCs.

## Samband

The open protocol project, specification, compatibility material, and reference
implementations described by this repository.

## Samband Protocol (SP)

The implementation-independent set of accepted semantics, encodings,
versioning rules, and test vectors that compatible nodes implement. Reference
application behavior is not automatically protocol behavior.

## Samband Node

A running compatible protocol participant. A node may be hosted by a phone,
desktop, embedded system, vehicle, dedicated radio, or another device. Its roles
are expressed through dynamic capabilities.

## Transport network / Samband mesh

The changing graph of Samband Nodes and one-hop links available to carry
Samband traffic. It is shared infrastructure and is not the same as a private
channel.

## Neighbor

A peer reachable over a current one-hop transport attachment and admitted under
the selected Samband peer-session profile. RFC-0001 distinguishes untrusted
transport adjacency from authoritative neighbor/session state. Exact
authentication, admission, and liveness rules remain Protocol/Security
decisions.

## Transport adjacency

A live one-hop transport relationship before Samband peer-session admission. It
is an untrusted input boundary and does not by itself create neighbor,
capability, route, duplicate, channel, PTT, or media state.

## Peer session

The one-hop Samband context after exact experimental `(envelope format,
protocol profile)` pair selection and the admission/security checks required by
that protocol profile. The concrete authentication and identity binding remain
Agent 4 work.

## Discovery handle

A short-lived, transport-visible value used only to correlate the minimum
link-local discovery exchange needed to attempt a peer session. It is not a
node identity, credential, routing origin, channel identifier, membership
proof, or authorization result. Rotation and linkability rules remain under
Agent 4 review.

## Credential identity

The identifier or public-key reference evaluated by a selected security
profile. A credential identity is not automatically a human identity, display
name, routing origin, channel identity, or authorization decision.

## Authenticated principal

The security-profile result naming the party whose credential or session key
authenticated a particular claim or protected record. An immediate-peer
principal authenticates only that peer's link/session claim unless another
reviewed protocol explicitly proves delegation or end-origin authority.

## Action subject

The node, channel member, membership target, speaker, stream owner, or other
entity about which an authenticated message requests a state change. The
authenticated principal and action subject may differ only when the governing
authorization rule explicitly permits it; equality must never be inferred from
one ambiguous `actor` field.

## Transport

A mechanism that establishes one-hop connectivity and carries bounded Samband
frames, such as a simulator link, Wi-Fi technology, Bluetooth technology,
Ethernet, Internet, or future radio hardware. A transport does not redefine
Samband semantics.

## Transport adapter

Platform-specific code implementing the Samband transport interface. It reports
actual link and lifecycle capabilities and keeps platform types outside the
core.

## Endpoint

A node capability that originates or consumes protected private-channel
traffic. An endpoint can also relay if it separately advertises and enables that
capability.

## Relay

A node capability that validates forwarding eligibility and carries Samband
traffic toward other nodes. A relay does not require private-channel membership
or access to channel plaintext.

## Community relay

A relay offered by a user or operator to assist other Samband participants. It
is explicit, controllable, resource-aware, and limited to valid Samband traffic.

## Gateway

A future capability that bridges Samband traffic across transports or an
Internet path. It is not inherently a trusted authority or decryption endpoint
and must not become a generic IP proxy. Gateway semantics require a future RFC.

## Capability

An advertised, potentially dynamic statement about what a node can currently
do or is willing to do, such as relay availability, audio input, or a supported
transport. Capabilities may change with policy and runtime conditions.

## Private radio channel / private channel

A logical security and communication overlay for authorized endpoints. It is
separate from the transport network. Identity, membership, authorization, and
key management remain under RFC and security review.

## Channel member

An endpoint authorized according to the accepted channel-membership protocol.
Possessing a human-visible channel label alone cannot establish membership.

## Relay envelope

The forwardable Samband structure containing only protocol-approved metadata
needed to validate, bound, classify, and route an opaque payload. Its fields and
encoding are proposed but unresolved in RFC-0004.

## Origin routing context

An opaque routing/duplicate scope proposed by RFC-0004. It is not automatically
a long-lived node identity, source route, channel identity, or human identity.
Its stability, construction, binding, and privacy remain Routing/Security work.

## Packet identity

An opaque token assigned once to a forwarding instance and preserved across
relays and transport copies. It supports mesh duplicate suppression only; it is
scoped for that purpose by the exact envelope-format/protocol-profile pair and
origin routing context. It is not proof of origin, operation identity,
acknowledgement, ordering, or security replay protection.

## Opaque endpoint payload

Endpoint bytes carried unchanged by the relay layer and not parsed by relays.
"Opaque" describes a protocol boundary, not a claim of encryption, anonymity,
unlinkability, authentication, or metadata privacy.

## Protected / encrypted channel payload

Opaque endpoint content carried inside the relay envelope. The term "encrypted"
must not be used as an implementation security claim until the construction,
keys, authentication, and review status are stated.

## Protected record

One authenticated security-protocol record inside the opaque endpoint
container, interpreted under an exact security profile and channel epoch. Its
canonical associated context, sender/principal binding, replay identifier,
recipient selection, and failure behavior remain RFC-0006 decisions.

## Channel epoch

A monotonically ordered channel-security state generation under a selected
group-key protocol. It is not wall-clock time, hop limit, packet identity,
capability generation, route revision, PTT request identity, stream identity,
or media sequence. Epoch transition and partition behavior remain under
security review.

## PTT

Push-To-Talk: a primarily half-duplex interaction in which channel participants
coordinate a current speaker. The distributed arbitration protocol is
unresolved.

## Traffic treatment / traffic class

A protocol-visible category used to apply appropriate forwarding and freshness
semantics. RFC-0004 proposes the coarse Draft labels `BOUNDED_CONTROL` and
`FRESH_MEDIA`; their need, visibility, values, and encoding remain under
Routing/Security review.

## TTL / forwarding lifetime

A bounded forwarding allowance preventing indefinite circulation. Whether the
wire contract uses hop count, time, or another representation is unresolved.
RFC-0004 proposes a v0.x hop-limit baseline in which local delivery is possible
at one and forwarding decrements values greater than one.

## Duplicate suppression

Bounded recognition and dropping of packets already processed within a defined
window. This is distinct from cryptographic replay protection, though the two
must be coordinated.

## Security replay protection

The security-profile mechanism and bounded state that reject reuse of an
already authenticated protected record in its defined sender/channel/epoch
domain. It is independent from outer duplicate suppression and from PTT or
media freshness. Whether authenticated stale/replayed records consume state,
and how crash or rollback recovery behaves, must be explicit in the selected
security profile.

## Partition

A state in which the mesh is split into disconnected components. Partitions are
normal; connected components continue operating without replaying missed audio.

## Canonical test vector

A versioned, deterministic fixture with defined input, expected output or
failure, provenance, and protocol scope. All compatible implementations should
be able to consume the same semantic vectors.

## Reference implementation

An official implementation used to prove and exercise the specification. It is
not authoritative when it disagrees with accepted protocol documents.
