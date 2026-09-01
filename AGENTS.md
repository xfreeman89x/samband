# AGENTS.md

# Samband — Agent Operating Manual

Samband is an open-source protocol and reference implementation for realtime Push-To-Talk voice communication over opportunistic peer-to-peer mesh networks.

The project is licensed under the Apache License 2.0.

The long-term objective is to create an interoperable radio-like communication network where smartphones and future compatible devices can communicate directly, relay encrypted traffic for one another, and operate without requiring central infrastructure.

The simplest expression of Samband is:

> Press. Talk. Relay. Connect.

---

# 1. PROJECT IDENTITY

Project name:

    Samband

Protocol name:

    Samband Protocol

Suggested abbreviations where useful:

    Samband
    Samband Protocol
    SP

Avoid inventing alternate protocol names without an accepted ADR.

The repository, protocol documentation, applications and tooling should consistently use the Samband identity.

---

# 2. OPEN-SOURCE PRINCIPLE

Samband is designed to be an open protocol.

The project should allow independent developers and manufacturers to eventually create interoperable implementations without depending on the official applications.

The repository must therefore contain enough specification and test material for third parties to implement Samband independently.

The reference applications are implementations of Samband.

They are not the definition of Samband.

The protocol specification is authoritative.

---

# 3. LICENSE

The project uses:

    Apache License 2.0

All new source files and contributions must remain compatible with this license.

Repository root should contain:

    LICENSE
    NOTICE
    CONTRIBUTING.md
    CODE_OF_CONDUCT.md
    SECURITY.md
    GOVERNANCE.md

Do not introduce dependencies with incompatible licensing.

Agents adding dependencies must evaluate their licenses.

---

# 4. PRIMARY PROJECT GOAL

The initial objective is NOT:

- a Web application;
- a SaaS platform;
- a centralized communication backend;
- a cloud service;
- a messaging application.

The initial objective IS:

> Design, specify, simulate and implement a decentralized realtime radio mesh protocol.

The protocol must eventually support:

- direct peer-to-peer communication;
- multi-hop relay;
- opportunistic community relay;
- encrypted private channels;
- realtime PTT audio;
- heterogeneous device capabilities;
- network partitions;
- route recovery;
- future Internet gateways;
- future hardware implementations.

---

# 5. FUNDAMENTAL NETWORK MODEL

Samband separates:

    TRANSPORT NETWORK

from:

    PRIVATE RADIO CHANNELS

The transport mesh may contain devices that do NOT belong to a given radio channel.

Example:

```text
PRIVATE CHANNEL MEMBERS

Alice                               Carol
CH 7                                CH 7
  │                                  │
  │                                  │
  └──── Relay X ─── Relay Y ─────────┘
         no CH 7      no CH 7
```

Relay X and Relay Y transport encrypted traffic.

They must not require access to the channel plaintext.

The transport network is shared.

Channels are private logical overlays.

This distinction is fundamental and must be preserved throughout the architecture.

---

# 6. NETWORK NODE MODEL

Every Samband installation or compatible implementation is a:

    Samband Node

A node may expose capabilities such as:

- endpoint;
- relay;
- gateway;
- audio input;
- audio output;
- direct P2P;
- background relay;
- Internet connectivity;
- battery-aware relay;
- hardware PTT.

Nodes must advertise capabilities.

Avoid hardcoding logic based only on device type.

Prefer:

    capabilities.meshRelay = true

over:

    if device == android

---

# 7. CHANNEL MODEL

A radio channel is a secure logical communication group.

A node may belong to:

- zero channels;
- one channel;
- many channels.

A node does NOT need to belong to a channel in order to relay encrypted Samband traffic.

Channel membership and mesh participation are separate concepts.

---

# 8. AUDIO PRIVACY

Audio MUST be ephemeral.

Never persist:

- raw microphone audio;
- encoded audio frames;
- conversations;
- transcripts;
- voice history.

There is no store-and-forward voice system.

If the destination is unreachable while the speaker is transmitting, the missed audio is lost.

This behavior is intentional.

---

# 9. END-TO-END CONFIDENTIALITY

Samband should be designed so intermediate relays cannot decrypt radio payloads.

Conceptually:

```text
Microphone
    ↓
Opus
    ↓
Channel encryption
    ↓
Encrypted Samband payload
    ↓
Mesh relay
    ↓
Mesh relay
    ↓
Destination
    ↓
Decrypt
    ↓
Opus
    ↓
Speaker
```

Intermediate relay nodes may process only the minimum routing metadata necessary.

Do not claim end-to-end encryption until the actual key architecture is implemented and reviewed.

Never invent cryptographic algorithms.

Security-sensitive protocol design requires Security Agent review.

---

# 10. NO BLOCKCHAIN

Samband does NOT require:

- blockchain;
- cryptocurrency;
- proof of work;
- proof of stake;
- global permanent consensus.

Distributed state should be:

- minimal;
- ephemeral;
- partition tolerant;
- eventually convergent where appropriate.

Possible techniques include:

- gossip;
- signed state;
- TTL-based route advertisements;
- CRDTs only where clearly justified.

Do not add distributed-ledger technology without a compelling protocol requirement and accepted RFC.

---

# 11. TRANSPORT INDEPENDENCE

The Samband Protocol must not depend on a specific physical transport.

Possible transports include:

- Wi-Fi;
- Wi-Fi Direct;
- Wi-Fi Aware;
- Nearby-style APIs;
- Bluetooth;
- BLE;
- Internet;
- Ethernet;
- future radio hardware.

Transport adapters carry Samband packets.

They do not redefine Samband semantics.

---

# 12. CORE ARCHITECTURE

Preferred conceptual architecture:

```text
                    SAMBAND APPLICATION
                           │
                           │
                     SAMBAND CORE
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
     Protocol           Routing           Security
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                     Transport API
                           │
           ┌───────────────┼────────────────┐
           │               │                │
        Android P2P      iOS P2P        Simulator
```

Audio and system integration are above or alongside the core as appropriate.

Transport-specific APIs must not leak into routing or protocol logic.

---

# 13. PREFERRED CORE LANGUAGE

The preferred direction for portable protocol/core logic is:

    Rust

Rust should be evaluated for:

- packet codec;
- identity;
- cryptographic envelope handling;
- routing;
- mesh state;
- duplicate suppression;
- TTL;
- PTT state machines;
- simulation support.

Android reference application:

    Kotlin
    Jetpack Compose

iOS reference application:

    Swift
    SwiftUI

Use FFI or generated bindings only where the shared-core benefit justifies the complexity.

This decision should be confirmed through an ADR and small prototype before excessive implementation.

---

# 14. PROTOCOL SPECIFICATION

The protocol specification must live independently from implementation.

Preferred structure:

```text
/protocol
    /spec
    /schemas
    /test-vectors
    /compatibility
```

The specification must eventually document:

- packet envelope;
- protocol versioning;
- node identity;
- discovery;
- peer authentication;
- capabilities;
- routing;
- relay behavior;
- duplicate suppression;
- TTL;
- channel membership;
- encryption envelope;
- PTT arbitration;
- realtime audio framing;
- error handling;
- version negotiation.

A third party should eventually be capable of building a compatible node from the specification alone.

---

# 15. PACKET MODEL

Keep a strict separation between:

    RELAY ENVELOPE

and:

    ENCRYPTED RADIO PAYLOAD

Conceptually:

```text
┌──────────────────────────────┐
│ Samband Relay Envelope       │
│                              │
│ protocol version             │
│ packet identity              │
│ routing metadata             │
│ TTL                          │
│ traffic class                │
│                              │
│  ┌────────────────────────┐  │
│  │ encrypted payload      │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

Relays should see only what they need to forward traffic.

Metadata privacy is a design goal.

---

# 16. DISCOVERY

Nodes must eventually discover nearby Samband nodes.

Discovery must be independent from channel membership.

Discovery should reveal as little persistent identity information as practical.

Investigate:

- rotating node identifiers;
- ephemeral discovery identifiers;
- authenticated session establishment;
- capability exchange after secure connection.

Avoid permanently broadcasting stable identifiers when unnecessary.

---

# 17. ROUTING

Samband must eventually support:

```text
A ─ B ─ C ─ D
```

where A reaches D through B and C.

Routing must handle:

- neighbor appearance;
- neighbor disappearance;
- route propagation;
- route expiration;
- loops;
- duplicate packets;
- TTL;
- topology changes;
- partitions;
- reconnection;
- latency;
- packet loss;
- battery cost;
- relay willingness.

Do not optimize purely for minimum hop count.

Routing metrics must be observable and tunable.

---

# 18. COMMUNITY RELAY

Samband nodes may optionally relay traffic for other users.

This behavior must be:

- explicit;
- controllable;
- energy aware;
- bandwidth aware;
- abuse resistant.

Possible relay modes:

    DISABLED
    OPPORTUNISTIC
    FULL

Possible gateway policy:

    NEVER
    WIFI_ONLY
    WIFI_AND_MOBILE

Mobile data relay should not be silently enabled.

Community relay must never turn Samband into a generic IP proxy.

Only valid Samband traffic is eligible for relay.

---

# 19. RESOURCE-AWARE ROUTING

Relay availability may depend on:

- battery level;
- charging state;
- thermal state;
- connection quality;
- operating system limitations;
- bandwidth policy;
- user preference.

Example:

```text
battery = 90%
charging = true
relay = preferred
```

versus:

```text
battery = 12%
relay = unavailable
```

This should be expressed as dynamic capabilities/metrics.

---

# 20. NETWORK PARTITIONS

Partitions are normal.

Example:

```text
A ─ B

C ─ D
```

Both partitions should continue operating.

When connectivity returns:

```text
A ─ B ─ C ─ D
```

routing/control state reconverges.

Past audio is never replayed.

---

# 21. DUPLICATE SUPPRESSION

Mesh forwarding may create duplicate routes.

Every forwarded packet must support robust duplicate detection.

Design must address:

- packet IDs;
- sequence numbers;
- replay windows;
- TTL;
- bounded duplicate caches.

Do not allow forwarding loops to cause unbounded resource consumption.

---

# 22. PTT MODEL

Samband is primarily half-duplex.

The logical interaction is:

```text
PTT_REQUEST
      ↓
PTT_GRANTED
      ↓
TRANSMIT
      ↓
PTT_RELEASE
```

Distributed/off-grid arbitration is a protocol problem.

Handle:

- simultaneous PTT requests;
- partitions;
- stale ownership;
- peer disappearance;
- timeout;
- channel busy.

Do not assume a central authority exists.

---

# 23. AUDIO

Preferred codec direction:

    Opus

Audio design priorities:

1. latency;
2. freshness;
3. jitter tolerance;
4. packet-loss tolerance;
5. low bandwidth;
6. energy efficiency.

Stale audio should normally be dropped rather than retransmitted.

Audio reliability semantics are different from control-message semantics.

---

# 24. FIRST TECHNICAL MILESTONE

Do NOT begin with production audio.

The first major milestone is a simulated Samband mesh.

Required proof:

```text
A → B

A → B → C

A → B → C → D
```

Then demonstrate:

- route loss;
- route replacement;
- partition;
- network merge;
- duplicate suppression;
- TTL;
- malicious/malformed packet rejection;
- relay nodes without channel membership.

This simulator is mandatory.

---

# 25. SECOND TECHNICAL MILESTONE

Real Android devices.

Target demo:

```text
Alice          Bob            Carol

CH 7           RELAY          CH 7
 📱              📱             📱
  │              │               │
  └─────────────→├──────────────→│
      encrypted      encrypted
```

Requirements:

- no Internet;
- Alice and Carol share a private channel;
- Bob is not a channel member;
- Bob relays;
- Bob cannot decrypt channel payload;
- Carol receives valid realtime data.

Initially the payload may be synthetic test data rather than audio.

---

# 26. THIRD TECHNICAL MILESTONE

Add realtime encrypted Opus PTT over the proven relay path.

Target demonstration:

> Three phones. No Internet. One foreign relay. Realtime voice.

This is the first iconic Samband demo.

---

# 27. IOS

iOS is a reference platform but must not dictate protocol design.

Document platform limitations explicitly.

If background/community relay is not technically available in some device state, advertise that through capabilities.

Do not simulate capabilities the OS cannot reliably provide.

---

# 28. CROSS-PLATFORM INTEROPERABILITY

A major milestone is:

    Android Samband Node
            ↕
        Samband
            ↕
       iOS Samband Node

The protocol specification, not platform-specific code, must guarantee interoperability.

---

# 29. FUTURE DEVICES

Samband must eventually permit independent implementations for:

- Linux;
- Raspberry Pi;
- embedded Linux;
- automotive;
- watches;
- dedicated handheld radios;
- custom hardware.

Do not build the core around assumptions unique to smartphones.

---

# 30. REPOSITORY STRUCTURE

Preferred initial structure:

```text
/
├── protocol/
│   ├── spec/
│   ├── schemas/
│   ├── test-vectors/
│   └── compatibility/
│
├── core/
│   └── rust/
│
├── simulator/
│
├── apps/
│   ├── android/
│   └── ios/
│
├── bindings/
│   ├── kotlin/
│   └── swift/
│
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── rfc/
│   ├── security/
│   ├── research/
│   └── agents/
│
├── tools/
│
├── LICENSE
├── NOTICE
├── README.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── SECURITY.md
├── GOVERNANCE.md
├── CODE_OF_CONDUCT.md
└── AGENTS.md
```

Modify this only through an architectural decision.

---

# 31. RFC PROCESS

Protocol changes of material significance require an RFC.

Place RFCs under:

    docs/rfc/

Suggested initial RFCs:

    RFC-0001 Samband Network Model
    RFC-0002 Node Identity
    RFC-0003 Channel Identity and Membership
    RFC-0004 Relay Envelope
    RFC-0005 Mesh Routing
    RFC-0006 Encrypted Channel Payload
    RFC-0007 PTT Arbitration
    RFC-0008 Audio Transport

RFC status:

    Draft
    Discussion
    Accepted
    Rejected
    Superseded

Do not silently evolve protocol semantics in implementation PRs.

---

# 32. ADR PROCESS

Implementation architecture decisions belong under:

    docs/adr/

RFC:

    protocol semantics

ADR:

    implementation architecture

Keep the distinction clear.

---

# 33. TEST VECTORS

Protocol interoperability requires canonical test vectors.

Examples:

- packet encode/decode;
- identity derivation;
- signatures;
- encrypted payload envelopes;
- malformed packets;
- duplicate handling;
- version negotiation.

Reference applications must pass the same vectors.

Independent implementations should be able to use them.

---

# 34. SIMULATOR

The simulator is a first-class Samband implementation environment.

It must allow arbitrary networks:

```text
A ─ B ─ C
    │
    D
```

and dynamic changes.

Configurable conditions:

- latency;
- jitter;
- packet loss;
- duplication;
- bandwidth;
- node failure;
- route failure;
- partition;
- recovery;
- malicious nodes.

Simulator behavior must be deterministic when seeded.

---

# 35. OBSERVABILITY

Development builds should expose:

- node identity;
- neighboring nodes;
- capabilities;
- current routes;
- route costs;
- RTT;
- packet loss;
- relay decisions;
- duplicate drops;
- packet TTL;
- current PTT owner;
- battery/relay policy.

Never log plaintext audio.

Avoid unnecessary persistent identity logs.

---

# 36. SECURITY

Create a threat model before freezing Protocol v1.

Threats include:

- impersonation;
- unauthorized channel membership;
- replay;
- route poisoning;
- malicious relay;
- packet injection;
- traffic analysis;
- discovery tracking;
- metadata leakage;
- resource exhaustion;
- denial of service;
- malicious channel member;
- compromised device.

Security review is mandatory for protocol freeze.

---

# 37. CONTRIBUTOR EXPERIENCE

The repository should be easy for external contributors to understand.

Provide:

- architecture overview;
- protocol overview;
- development setup;
- simulator instructions;
- issue templates;
- RFC template;
- ADR template;
- good-first-issue labels;
- contributor guide.

Avoid requiring access to private infrastructure.

A contributor should be able to build and test Samband locally.

---

# 38. AGENT OWNERSHIP

## Agent 0 — Principal Architect / Maintainer

Owns:

    docs/architecture
    docs/adr
    docs/rfc governance
    integration
    package boundaries

---

## Agent 1 — Protocol Specification Engineer

Owns:

    protocol/spec
    protocol/schemas
    protocol/compatibility
    protocol/test-vectors

---

## Agent 2 — Rust Core Engineer

Owns:

    core/rust
    shared protocol/core implementation

---

## Agent 3 — Mesh / Routing Engineer

Owns:

    routing logic
    relay behavior
    simulator routing model

---

## Agent 4 — Security / Cryptography Engineer

Owns:

    docs/security
    cryptographic architecture
    identity
    channel credentials
    encrypted envelope review

---

## Agent 5 — Simulator / Reliability Engineer

Owns:

    simulator
    chaos/network tests
    interoperability test infrastructure

---

## Agent 6 — Android Native Engineer

Owns:

    apps/android
    Android P2P transport
    Android background service
    Android reference UX

---

## Agent 7 — iOS Native Engineer

Owns:

    apps/ios
    iOS transports
    iOS lifecycle
    iOS reference UX

---

## Agent 8 — Audio / PTT Engineer

Owns:

    realtime audio architecture
    Opus integration
    PTT media lifecycle
    latency measurement

---

## Agent 9 — Developer Ecosystem / Interoperability Engineer

Owns:

    bindings
    test-vector runners
    external implementation guidance
    contributor tooling

---

# 39. EXECUTION WAVES

## Wave 0

Start:

    Architect
    Protocol
    Security

Goal:

    Samband v0 architecture and protocol model

---

## Wave 1

Start:

    Rust Core
    Routing
    Simulator

Goal:

    deterministic simulated mesh

---

## Wave 2

Start:

    Android
    Routing
    Security
    Simulator

Goal:

    physical Android direct P2P and relay

---

## Wave 3

Start:

    Audio/PTT
    Android

Goal:

    realtime encrypted PTT through relay

---

## Wave 4

Start:

    iOS
    Interoperability
    Simulator

Goal:

    cross-platform Samband

---

# 40. SHARED CONTRACT RULE

Agents must not independently redefine:

- Samband packet envelope;
- node identity;
- channel identity;
- capabilities;
- relay semantics;
- routing messages;
- encryption envelope;
- PTT state machine.

Changes require RFC/ADR coordination.

---

# 41. HANDOFF FORMAT

Every agent completion report must contain:

    STATUS

    COMPLETED

    FILES CHANGED

    PROTOCOL IMPACT

    PUBLIC API IMPACT

    TESTS

    SECURITY IMPACT

    ASSUMPTIONS

    KNOWN LIMITATIONS

    BLOCKERS

    NEXT RECOMMENDED STEP

---

# 42. DEFINITION OF DONE

A task is not done unless:

- it builds;
- tests pass;
- public behavior is documented;
- protocol implications are documented;
- security implications are considered;
- malformed input is handled;
- no unrelated refactoring was introduced;
- interoperability impact is evaluated.

---

# 43. GUIDING PRINCIPLE

Whenever uncertain, ask:

> Does this make Samband more interoperable, resilient, private and simple to use without coupling it to one device or transport?

If not, reconsider.

The iconic Samband demonstration is:

```text
Alice          Bob             Carol
 📱             📱               📱
 CH 7           relay            CH 7

Alice presses PTT.

Encrypted audio crosses Bob.

Carol hears Alice.

Bob cannot.

No Internet.
```

Everything we build should move Samband toward making that demonstration real.