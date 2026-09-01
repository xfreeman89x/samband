# Component Model

## Purpose

This model defines responsibilities and ownership boundaries before packages
or public APIs are created. Names below are conceptual components, not frozen
crate, module, or wire names.

## Protocol artifacts

Location: [`../../protocol/`](../../protocol/README.md).

Responsibilities:

- implementation-independent normative specification;
- schemas derived from accepted semantics;
- canonical positive and negative test vectors;
- version and compatibility rules;
- independent implementation guidance.

Protocol artifacts must not depend on reference-implementation internals.

## Portable core boundary

Location: [`../../core/`](../../core/README.md).

Candidate responsibilities, subject to accepted RFCs and ADRs:

- protocol encode/decode and validation;
- bounded packet lifetime and duplicate handling;
- capability and mesh state models;
- routing primitives;
- interfaces to reviewed identity and channel protection;
- deterministic clocks and randomness injection for tests;
- PTT state primitives after RFC acceptance.

The core must not depend on UI frameworks, mobile lifecycle APIs, physical
transport APIs, application databases, or audio persistence.

## Security boundary

Responsibilities:

- standard cryptographic primitive integration after review;
- identity/session/channel authorization interfaces;
- protected payload envelope processing;
- key lifecycle and replay protection after RFC acceptance;
- secret zeroization and safe diagnostic boundaries where supported.

Routing cannot request channel plaintext or secret keys. Security code cannot
invent topology or transport semantics. No concrete design is accepted during
this bootstrap.

## Routing and relay boundary

Responsibilities:

- neighbor and route state;
- route selection and expiration;
- relay eligibility and willingness;
- forwarding lifetime and duplicate decisions;
- partition/merge behavior and observable metrics.

Routing may consume only protocol-approved relay metadata, dynamic capabilities,
and abstract link metrics. It must not inspect channel plaintext or platform
types. Algorithm selection remains under
[`RFC-0005`](../rfc/RFC-0005-mesh-routing.md).

## Transport interface and adapters

The transport interface presents one-hop links to the core. An adapter may:

- discover or accept peers according to platform capabilities;
- establish, close, and report one-hop link state;
- send and receive bounded Samband frames;
- report measured link and lifecycle properties;
- surface changes in availability.

An adapter may not define packet semantics, channel membership, route selection,
or PTT ownership. Platform-specific objects stop at the adapter boundary.

## Simulator

Location: [`../../simulator/`](../../simulator/README.md).

The simulator composes the same portable core contracts with a deterministic
virtual transport, controllable clock, seeded randomness, topology scheduler,
and safe metrics. It is a first-class implementation environment, not a toy
mock of different semantics.

## Native reference applications

Location: [`../../apps/`](../../apps/README.md).

Applications own user policy, permissions, platform lifecycle, diagnostics,
audio device access, and presentation. They consume core and adapter APIs. They
must not reimplement protocol semantics to work around platform limitations;
limitations become capabilities or explicit incompatibilities.

## Audio/PTT boundary

Endpoint applications own microphone capture, codec integration, jitter
handling, and playback. The core may eventually own transport-independent PTT
and media framing semantics. Audio bytes remain ephemeral and must not be stored
by applications, the core, simulator output, diagnostics, or relays.

## Bindings

Location: [`../../bindings/`](../../bindings/README.md).

Bindings expose deliberately narrow, reviewed interfaces to a portable core.
They should translate ownership and error semantics without creating a second
source of protocol truth. No FFI surface is accepted until the shared-core
experiment has established a worthwhile boundary.

## Future gateways

A gateway is a transport/relay capability within Samband. It is not a backend,
channel authority, generic proxy, or implicit decryption point. Gateway support
requires an RFC and threat-model update.

