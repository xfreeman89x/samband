---
adr: "0002"
title: Simulator-First Development
status: Accepted
date: 2026-09-01
deciders:
  - Principal Architect / Maintainer
consulted:
  - Project charter
informed:
  - Core, Routing, Simulator, Platform, and Audio owners
supersedes: []
superseded_by: null
---

# ADR-0002: Simulator-First Development

## Context

The core protocol problems—multi-hop relay, topology changes, partitions,
duplicates, lifetime, malformed traffic, and foreign relays—must be understood
independently from mobile radio APIs and realtime audio. Physical systems are
hard to reproduce and combine several sources of nondeterminism.

## Decision drivers

- deterministic reproduction of network behavior;
- fast exploration of protocol and routing alternatives;
- shared evidence for multiple domain reviewers;
- no dependence on private infrastructure or mobile SDK for contributors;
- avoid optimizing audio before generic relay works.

## Decision

The first Samband implementation environment is a deterministic simulator that
uses the same portable contracts and canonical vectors intended for physical
nodes. Production audio and mobile multi-hop work wait until simulator contracts
and generic protected relay prerequisites pass their gates.

The detailed strategy is in
[`../architecture/simulator-first.md`](../architecture/simulator-first.md).

## Consequences

### Positive

- failures are seed-reproducible and can cover partitions and malicious input;
- routing candidates can be compared with identical scenarios;
- contributors can validate core behavior without devices.

### Negative

- simulated radios cannot prove mobile lifecycle, energy, RF, or physical audio
  behavior;
- deliberate effort is required to prevent simulator-only shortcuts.

### Neutral or follow-up

- physical experiments remain mandatory at later gates;
- virtual time, randomness, transport, and metrics interfaces need design after
  relevant RFCs are accepted.

## Alternatives considered

| Alternative | Why not selected |
| --- | --- |
| start with Android direct networking | entangles protocol with permissions, radios, lifecycle, and device APIs |
| start with audio | optimizes a media pipeline before relay and channel protection are proven |
| rely only on unit tests | cannot model topology/event interactions and convergence evidence cohesively |

## Validation

M2 criteria require deterministic direct/multi-hop/foreign-relay, route loss,
partition/merge, duplicate, lifetime, and malicious-input scenarios with bounded
state and observable metrics.

## Protocol impact

None. The simulator implements accepted or explicitly experimental protocol
profiles; it does not define them.

## Security and privacy impact

The simulator enables adversarial testing but cannot validate real cryptographic
side channels or platform secret storage. It must not log real secrets or audio.

## Revisit triggers

- the simulator cannot reuse physical-node contracts;
- deterministic modeling demonstrably hides a critical class of required behavior.
