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

A node reachable over a current one-hop transport attachment. The eventual
authentication and liveness rules remain protocol/security decisions.

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
encoding are unresolved in RFC-0004.

## Protected / encrypted channel payload

Opaque endpoint content carried inside the relay envelope. The term "encrypted"
must not be used as an implementation security claim until the construction,
keys, authentication, and review status are stated.

## PTT

Push-To-Talk: a primarily half-duplex interaction in which channel participants
coordinate a current speaker. The distributed arbitration protocol is
unresolved.

## Traffic class

A protocol-visible category used to apply appropriate forwarding and freshness
semantics. Exact classes and values are unresolved.

## TTL / forwarding lifetime

A bounded forwarding allowance preventing indefinite circulation. Whether the
wire contract uses hop count, time, or another representation is unresolved.

## Duplicate suppression

Bounded recognition and dropping of packets already processed within a defined
window. This is distinct from cryptographic replay protection, though the two
must be coordinated.

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
