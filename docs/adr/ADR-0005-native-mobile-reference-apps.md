---
adr: "0005"
title: Native Android and iOS Reference Apps
status: Proposed
date: 2026-09-01
deciders:
  - Principal Architect / Maintainer
consulted: []
informed:
  - Android, iOS, Core, and Ecosystem owners
supersedes: []
superseded_by: null
---

# ADR-0005: Native Android and iOS Reference Apps

## Context

The reference apps need direct access to peer connectivity, permissions,
background lifecycle, audio, system PTT integration, diagnostics, and battery
policy. Platform behavior is central to honest capability advertisement. The
project prefers Kotlin/Jetpack Compose and Swift/SwiftUI, but has not yet
completed platform feasibility experiments.

## Decision drivers

- complete access to official platform networking and audio APIs;
- truthful foreground/background and relay behavior;
- maintainable platform diagnostics and permission UX;
- clear boundary to a possible portable Rust core;
- no protocol design dictated by UI framework convenience.

## Proposed decision

Use native Android (Kotlin, with Jetpack Compose for reference UX) and native iOS
(Swift, with SwiftUI for reference UX) applications, subject to focused
transport, lifecycle, and shared-core integration experiments.

The decision concerns reference apps only. Independent implementations may use
other compatible stacks. Protocol and routing semantics remain in authoritative
spec/core boundaries, not in view or platform adapter code.

## Consequences if accepted

### Positive

- direct access to current official platform capabilities and diagnostics;
- platform lifecycle limitations can be represented accurately;
- native audio and permission UX remain supportable.

### Negative

- two app codebases and toolchains require maintenance;
- shared-core bindings and async/lifecycle integration add complexity;
- UI behavior cannot be shared by default.

### Neutral or follow-up

- the first UI is diagnostic and proof-oriented, not product polish;
- platform stacks do not imply permanent relay availability.

## Alternatives considered

| Alternative | Why not selected yet |
| --- | --- |
| one cross-platform UI/runtime | may simplify UI but could lag or abstract critical P2P/background/audio APIs |
| Android-only reference project | useful for early physical proof but insufficient for protocol neutrality and cross-platform milestone |
| no official apps | weakens real-device proof and contributor diagnostics |

Experiments must compare platform access and maintenance cost before acceptance.

## Validation required for acceptance

- official-API transport and lifecycle spike on supported Android/iOS versions;
- capability matrix for discovery, direct links, foreground/background receive,
  relay, audio, and suspension;
- Rust/core integration evidence if ADR-0004 is accepted;
- reproducible public builds without private infrastructure;
- dependency license and supply-chain review.

## Protocol impact

None. Platform constraints become capabilities; they do not silently change
Samband semantics.

## Security and privacy impact

Apps own permissions, local credential storage integration, audio devices, and
diagnostic privacy. Agent 4 must review those boundaries before protected-channel
claims.

## Revisit triggers

- a cross-platform stack proves equivalent platform access with materially lower
  maintenance cost;
- official APIs cannot meet required physical milestones;
- platform policy changes make the proposed reference role infeasible.

