# Samband Roadmap

This roadmap defines outcome gates, not calendar promises. A milestone advances
only when its measurable acceptance criteria are met. Pre-v1 releases may make
incompatible changes when those changes are documented.

## M0 — Authoritative project foundation

Target release: architecture bootstrap.

Acceptance criteria:

- the Apache-2.0 license and public governance files exist;
- the canonical repository structure and dependency rules are documented;
- RFC and ADR workflows, templates, and indexes exist;
- initial RFCs 0001 through 0008 are Draft and expose unresolved decisions;
- shared-contract ownership and required review gates are explicit;
- security, routing, and wire-format decisions are not presented as frozen;
- a cross-platform repository validator passes.

M0 does not produce a Samband implementation.

## M1 — Protocol v0 architecture

Target release: v0.1.

Acceptance criteria:

- Agent 1 has produced an internally consistent Protocol v0.x specification;
- Agent 4 has completed an initial threat model and reviewed identity, channel
  authorization, replay, and relay metadata exposure;
- Agent 3 has reviewed routing assumptions and envelope requirements;
- each shared contract needed by the simulator is accepted or explicitly
  versioned as experimental;
- canonical positive and negative test-vector formats are defined;
- no cryptographic primitive or wire encoding remains implicit.

This gate does not freeze Protocol v1 compatibility.

## M2 — Deterministic simulated mesh

Target release: v0.2.

Acceptance criteria:

- a seed reproduces identical topology events and packet outcomes;
- scenarios prove one-hop `A -> B`, two-hop `A -> B -> C`, and three-hop
  `A -> B -> C -> D` delivery;
- a relay without channel membership forwards an opaque payload;
- route loss, alternate route, partition, merge, duplicate suppression, and TTL
  expiration have automated tests;
- malformed and unsupported packets are rejected without unbounded work;
- convergence time, forwarding overhead, duplicate drops, and route churn are
  observable in test output;
- the simulator consumes the same contracts and vectors intended for physical
  implementations.

Production audio is out of scope for M2.

## M3 — Native direct transport experiments

Target release: v0.3.

Acceptance criteria:

- two physical Android nodes exchange generic Samband packets without Internet;
- the adapter exposes measured link and lifecycle capabilities rather than
  device-type assumptions;
- transport-specific types do not leak into protocol or routing code;
- background, battery, permission, and discovery limitations are documented;
- the experiment can be reproduced from public instructions.

The equivalent iOS feasibility experiments may run in parallel only after M1
defines the contracts they exercise.

## M4 — Physical multi-hop community relay

Target releases: v0.4 and v0.5.

Acceptance criteria:

- Alice reaches Carol through Bob with no Internet and no direct Alice-Carol
  link;
- Bob is not a member of Alice and Carol's private channel;
- relay participation is explicit and dynamically advertised;
- Bob cannot obtain the protected synthetic payload plaintext;
- route loss and relay withdrawal recover according to documented semantics;
- mobile data is not silently used;
- relevant security and abuse-resistance tests pass.

The payload may remain synthetic. This gate is not yet the audio demo.

## M5 — Realtime PTT through a foreign relay

Target release: v0.6.

Acceptance criteria:

- reviewed channel protection is used end to end;
- Alice's live Opus audio reaches Carol through Bob without Internet;
- Bob cannot decrypt channel audio;
- raw audio, encoded frames, transcripts, and voice history are never persisted;
- PTT acquisition and end-to-end latency are reported against an agreed budget;
- stale audio is dropped and loss/jitter behavior is measured;
- simultaneous PTT, stale ownership, and participant loss have deterministic
  tests.

## M6 — Cross-platform reference interoperability

Target releases: v0.7 and v0.8.

Acceptance criteria:

- Android and iOS reference nodes pass the same canonical vectors;
- they exchange Samband traffic using documented protocol semantics;
- platform lifecycle limitations are truthfully advertised as capabilities;
- no platform-specific workaround silently changes the protocol;
- an independent test harness can distinguish compatible from incompatible
  behavior.

## M7 — Protocol v1.0 and relay hardening

Target releases: v0.9 and v1.0.

Acceptance criteria:

- the complete threat model and external security review have no unresolved
  release blockers;
- compatibility, version negotiation, deprecation, and extension rules are
  normative;
- canonical vectors cover every mandatory message and malformed-input class;
- at least two independent implementations interoperate against the published
  specification;
- community relay energy, bandwidth, abuse, and metadata risks have measured
  mitigations;
- all v1 shared contracts are frozen through accepted RFCs.

No compatibility promise is made before this gate unless a release explicitly
documents a narrower promise.
