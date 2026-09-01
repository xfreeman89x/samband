# System Overview

## Status

Architecture bootstrap. This document records project scope and boundaries; it
does not define a wire-compatible protocol.

## Mission

Samband is an open, transport-independent protocol for realtime radio-like
communication across opportunistic peer-to-peer paths. The intended system can
operate through direct links, willing community relays, partitions, and future
gateways without making a central service authoritative.

The reference implementations exist to prove the specification. They are not
the definition of Samband.

## Architectural principles

1. **Protocol authority** — independent specification and canonical test
   vectors define observable behavior.
2. **Layer separation** — the transport network is distinct from private radio
   channels.
3. **Capability-driven behavior** — a node advertises what it can do now; code
   does not infer capability from platform labels.
4. **Opaque relaying** — relays require only the metadata necessary to validate
   and forward traffic, not channel plaintext or membership.
5. **Transport independence** — Wi-Fi, Bluetooth, Internet, Ethernet, simulator,
   and future radio links are adapters below Samband semantics.
6. **Partition tolerance** — disconnection and reconnection are normal states.
7. **Ephemeral audio** — live audio is neither store-and-forward nor historical
   content.
8. **Evidence before commitment** — platform feasibility, routing scale,
   cryptographic architecture, and latency claims require experiments.
9. **Bounded work** — malformed, duplicated, replayed, or looping traffic must
   not create unbounded memory, CPU, bandwidth, or storage use.
10. **Open implementation** — public material must be sufficient for an
    independent compatible node.

## Conceptual system

```text
                          Samband application
                    PTT UX, policy, diagnostics
                                  |
                        node orchestration
                                  |
          +-----------------------+-----------------------+
          |                       |                       |
     protocol codec          routing/relay        channel security
          |                       |                       |
          +-----------------------+-----------------------+
                                  |
                         transport interface
                                  |
             +--------------------+--------------------+
             |                    |                    |
        native adapter       simulator adapter     future adapter
```

Audio capture/encode and playback/decode sit at the endpoint boundary. Protected
audio frames cross the core only as ephemeral channel payloads. Platform and
transport types remain outside protocol, routing, and security semantics.

## Planes

Samband separates concerns into conceptual planes without requiring that each
be a separate process or package:

- **link/transport plane**: discovers or connects peers and moves bounded byte
  frames over one hop;
- **mesh control plane**: exchanges capability and reachability information and
  reacts to topology changes;
- **relay data plane**: validates forwarding eligibility, applies duplicate and
  lifetime rules, and forwards opaque payloads;
- **channel plane**: authorizes private-channel participation and protects
  endpoint payloads;
- **media/PTT plane**: arbitrates half-duplex transmission and carries fresh
  realtime audio;
- **observability plane**: exposes safe development metrics without plaintext
  audio, secrets, or unnecessary stable identity logs.

The exact messages and algorithms for these planes remain RFC work.

## Initial scope

The first technical proof is a deterministic simulated mesh with direct and
multi-hop delivery, foreign relay, route changes, partitions, merge, duplicate
suppression, TTL behavior, and malformed-packet rejection.

Explicitly out of scope for the bootstrap are:

- production Android or iOS applications;
- realtime audio implementation;
- a centralized backend or Web application;
- a generic Internet proxy;
- final identity, cryptography, routing, wire encoding, or PTT arbitration;
- claims of production security or v1 compatibility.

## Future implementation horizon

The protocol must remain implementable beyond smartphones. Anticipated future
hosts include Linux, Raspberry Pi, embedded Linux, vehicles, watches, dedicated
handheld radios, and custom hardware. These are compatibility horizons, not
committed platform milestones, and must not introduce smartphone-only core
assumptions.

## Development observability

Development builds should expose safe, bounded diagnostics for local node/session
identity, neighbors, current capabilities, routes and costs, RTT/loss, relay
decisions, duplicate drops, forwarding lifetime, PTT owner, and resource/relay
policy. Exact schemas are not yet defined. Diagnostics must not retain plaintext
audio, channel secrets, protected payloads, or unnecessary persistent identity.

## Success test

Every major decision should advance the following outcome without coupling the
protocol to a platform:

```text
Alice (channel member) -> Bob (relay only) -> Carol (channel member)
```

There is no Internet or direct Alice-Carol link. Bob relays valid Samband
traffic, cannot recover the channel payload, and Carol receives fresh realtime
audio once the audio milestone is reached.
