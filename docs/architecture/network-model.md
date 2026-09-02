# Samband Network Model

## Status and authority

This document defines stable architectural vocabulary and separation rules.
Protocol-visible identifiers, messages, algorithms, and encodings remain Draft
RFC work, beginning with
[`RFC-0001`](../rfc/RFC-0001-samband-network-model.md).

## Two distinct layers

### Samband transport network

The transport network is the changing graph of Samband Nodes and one-hop links
that can carry Samband frames. Participation in this graph does not imply
membership in any private channel.

### Private radio channels

A private channel is a logical security and communication overlay whose
authorized endpoints can participate in channel traffic. It is not a physical
network, link, SSID, backend room, or routing domain by definition.

The invariant is:

```text
transport network != private channel
```

A relay between channel members can be outside the channel. Routing must not
require plaintext channel identity or payload access unless a future accepted
RFC demonstrates an unavoidable and reviewed need.

## Samband Node

A Samband Node is a running compatible protocol participant. It may expose zero
or more dynamic capabilities. A single node can combine roles, and its available
roles can change with operating-system state, user policy, battery, thermal
state, connectivity, or hardware.

The node is the protocol concept. A phone, process, embedded device, vehicle,
or dedicated radio is a host for a node, not a protocol role by itself.

## Capability-based roles

### Endpoint

An endpoint originates or consumes protected channel traffic. It may have audio
input/output, but endpoint capability does not imply relay capability.

### Community relay

A community relay is a node that explicitly offers to forward eligible Samband
traffic for other nodes. It may belong to no private channel. Relay willingness
is dynamic, policy-controlled, energy-aware, bandwidth-aware, and
abuse-resistant.

Relay participation must never silently enable mobile-data forwarding or turn
the node into a generic IP proxy.

### Future gateway

A gateway is a future node capability that bridges Samband traffic between
otherwise separate Samband transports or across an Internet path. A gateway is
not a central authority and does not terminate channel protection merely because
it changes transports. Gateway semantics are not part of the initial milestone
and require a future RFC.

### Transport attachment

A transport attachment is one local one-hop adapter instance, such as a Wi-Fi,
Bluetooth, Ethernet, Internet, simulator, or future radio link. It moves
Samband frames but does not define channel or routing semantics.

## Membership and participation matrix

| Node behavior | Mesh participation | Channel membership required | Plaintext required |
| --- | --- | --- | --- |
| discover/connect neighbor | yes | no | no |
| relay eligible Samband traffic | yes | no | no |
| originate channel payload | yes | yes | only at originating endpoint |
| consume channel payload | yes | yes | only at receiving endpoint |
| future gateway transport bridge | yes | no by default | no by default |

The exact proofs, metadata, and authentication are unresolved security and
protocol decisions.

## Partitions and convergence

Partitions are normal, not exceptional. Each connected component continues to
operate with the state and members it can reach. When links return, bounded
control state reconverges according to the accepted routing RFC. Past audio is
not replayed after a merge.

## Traffic classes

The architecture anticipates different delivery semantics for control traffic
and fresh media. This does not yet establish wire traffic-class values.

- Control information may require acknowledgement, replacement, or bounded
  retransmission depending on its eventual specification.
- Realtime audio prioritizes freshness and should normally drop stale frames.
- Relay and abuse controls must bound both classes.

## Identity layers

The architecture distinguishes at least the following questions without yet
choosing their representation:

- persistent node accountability or authentication identity;
- privacy-preserving discovery identifiers;
- connection/session peer identity;
- private-channel membership identity;
- human-facing display names.

Collapsing these into one stable broadcast identifier is not assumed. Agent 4
Security review and Agent 1 Protocol review are required by
[`RFC-0002`](../rfc/RFC-0002-node-identity.md).

The authoritative semantic domains, lifetimes, audiences, and permitted
bindings are defined in [`identity-domains.md`](identity-domains.md). That
architecture establishes separation only; concrete representations remain RFC,
Routing, and Security work.

## Non-goals

The network model does not require blockchain, cryptocurrency, permanent global
consensus, a globally connected topology, a central channel server, or
store-and-forward voice.
