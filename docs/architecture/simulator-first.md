# Simulator-First Development Strategy

## Decision

[`ADR-0002`](../adr/ADR-0002-simulator-first-development.md) makes deterministic
simulation the first implementation environment. No production audio or mobile
mesh implementation should precede the contracts needed to prove generic
multi-hop relay.

## Why simulation comes first

Mobile transport APIs combine protocol questions with permissions, radios,
background suspension, device compatibility, and nondeterministic timing. A
deterministic simulator isolates Samband semantics so route, relay, lifetime,
duplicate, partition, and failure behavior can be reproduced before physical
constraints are added.

The simulator also creates shared evidence for Protocol, Routing, Security, and
Core reviewers.

## Required architecture

The simulator should compose:

- virtual Samband Nodes using the same portable contracts as physical nodes;
- an in-memory transport adapter with bounded frames;
- virtual monotonic time;
- seeded pseudo-randomness supplied through an explicit interface;
- a topology/event scheduler;
- configurable latency, jitter, loss, duplication, bandwidth, and failure;
- safe metrics and trace output that contains no secrets or audio;
- scenario definitions suitable for canonical test vectors.

The simulator must not depend on wall-clock sleeps for semantic tests.

## Baseline scenarios

1. direct `A -> B` delivery;
2. two-hop `A -> B -> C` delivery;
3. three-hop `A -> B -> C -> D` delivery through two relays;
4. relay with zero channel memberships;
5. alternate-path selection after route loss;
6. node disappearance and route expiration;
7. partition with continued local operation;
8. merge and bounded reconvergence without past-audio replay;
9. duplicate injection and bounded suppression;
10. lifetime exhaustion and loop prevention;
11. malformed and malicious packet rejection;
12. dynamic relay withdrawal due to policy/resource capability.

## Determinism contract

For a fixed simulator version, protocol profile, scenario, and seed, the ordered
semantic event log and asserted outcomes must be identical. Performance timing
from the host is reported separately and cannot alter correctness.

Any nondeterminism source must be injected or recorded. Scenario failures must
print enough topology, seed, and event context to reproduce them.

## Measurements

The first routing evaluation should measure convergence event count and virtual
time, delivery ratio, path changes, bytes and packets forwarded per delivered
payload, duplicate drop rate, route churn, bounded-state high-water marks, and
effects of relay willingness.

Absolute mobile energy and radio latency are not inferred from simulation; they
require physical experiments.

## Anti-shortcut rules

- The simulator cannot access channel plaintext at relay nodes.
- It cannot call routing internals that a real transport would bypass.
- It consumes the same packet validation and vector contracts as other nodes.
- A synthetic security adapter must be visibly non-production and cannot create
  security claims.
- Scenario-only behavior must not leak into the protocol.

## Exit gate

The simulator milestone passes only when all baseline scenarios are automated,
seed-reproducible, bounded, and traceable to accepted or explicitly experimental
contracts in the shared-contract registry.
