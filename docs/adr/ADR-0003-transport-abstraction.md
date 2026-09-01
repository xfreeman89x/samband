---
adr: "0003"
title: Transport Abstraction Boundary
status: Accepted
date: 2026-09-01
deciders:
  - Principal Architect / Maintainer
consulted:
  - Project charter
informed:
  - Protocol, Core, Routing, Simulator, Android, and iOS owners
supersedes: []
superseded_by: null
---

# ADR-0003: Transport Abstraction Boundary

## Context

Samband must operate over heterogeneous present and future links. Letting Wi-Fi,
Bluetooth, platform lifecycle, or simulator types enter routing and protocol
logic would create incompatible Samband variants.

## Decision drivers

- transport-independent protocol semantics;
- simulator and physical implementations must exercise the same core;
- actual runtime capabilities vary by OS, hardware, and policy;
- future transports should not require a protocol redesign.

## Decision

The portable Samband boundary consumes an abstract one-hop transport interface.
Concrete adapters own discovery/connectivity mechanisms, frame movement, link
lifecycle, and measured link properties. Platform types stop at the adapter.

Adapters cannot define routing, identity, channel, envelope, PTT, or audio
semantics. The exact API remains blocked until core and platform experiments
identify ownership, concurrency, MTU, backpressure, and lifecycle needs.

## Consequences

### Positive

- protocol/core logic can run in simulator and on diverse devices;
- platform limitations become explicit capabilities;
- new transports are localized adapters.

### Negative

- the interface must represent asymmetric and changing link behavior without
  collapsing to a lowest-common-denominator fiction;
- asynchronous ownership and backpressure can complicate FFI.

### Neutral or follow-up

- a narrow API prototype is needed alongside ADR-0004;
- transports may still need profile-specific fragmentation below the interface,
  but cannot change protocol semantics silently.

## Alternatives considered

| Alternative | Why not selected |
| --- | --- |
| platform-specific core variants | creates incompatible semantics and duplicated review |
| generic stream/socket abstraction only | may hide discovery, datagram, MTU, lifecycle, and peer properties needed by mesh links |
| transport chosen in routing code | leaks platform concerns and blocks simulator equivalence |

## Validation

The interface must support an in-memory simulator plus at least two materially
different physical transport experiments without core imports of platform APIs.

## Protocol impact

None at this abstraction level. Peer-visible transport capability or negotiation
semantics require RFC review.

## Security and privacy impact

Adapters are untrusted input boundaries and must enforce size/backpressure before
core parsing. Link security cannot be confused with channel payload security.

## Revisit triggers

- experiments show required semantics cannot be expressed without transport-
  specific protocol profiles;
- adapter abstraction creates unacceptable performance or lifecycle loss.

