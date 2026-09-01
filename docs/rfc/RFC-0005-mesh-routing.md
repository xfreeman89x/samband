---
rfc: "0005"
title: Mesh Routing
status: Draft
authors:
  - Samband contributors
created: 2026-09-01
updated: 2026-09-01
target: Protocol v0.x
requires:
  - Agent 3 Routing review
  - Agent 1 Protocol review
  - Agent 4 Security review
supersedes: []
superseded_by: null
---

# RFC-0005: Mesh Routing

## Summary

This RFC will define how Samband traffic reaches endpoints through changing
multi-hop paths, including willing relays that are not private-channel members.
It establishes evaluation requirements but does not select distance-vector,
link-state, gossip, on-demand, or hybrid routing in this draft.

## Status and authority

Draft and non-normative. Agent 3 owns algorithm evaluation; Agent 1 owns wire
semantics; Agent 4 reviews routing authentication, metadata, and abuse.

## Motivation

Samband must operate across appearance/disappearance, alternate paths,
partitions, merge, unstable radios, and dynamic relay willingness. Minimum hop
count alone does not capture latency, loss, energy, thermal state, bandwidth,
or operating-system availability.

## Goals

- deliver through one or more willing relays without channel membership;
- converge predictably after link and capability changes;
- prevent loops and bound duplicate propagation and state;
- support partitions without central authority and reconverge after merge;
- incorporate observable, tunable resource/link metrics;
- allow a relay to withdraw promptly when policy or resources change;
- minimize routing metadata and control overhead.

## Non-goals

- route generic IP traffic;
- optimize for Internet-scale stable networks without Samband evidence;
- expose plaintext channels as routing domains by default;
- guarantee delivery of stale realtime audio;
- select cryptographic protection before security review.

## Required model

An accepted RFC must define neighbor state, reachability or route state,
advertisement/discovery events, withdrawal/expiration, metric composition,
tie-breaking, lifetime, local delivery, forwarding, duplicate interaction,
reconvergence, and observable reason codes.

Dynamic inputs may include measured link quality, RTT, loss, available bandwidth,
relay willingness, charging/battery state, thermal pressure, data policy, and OS
lifecycle. The protocol must decide which are shared, quantized, locally used,
or omitted for privacy and stability.

## Failure and resource bounds

Route and neighbor state, advertisements, path history, duplicate caches, and
retries must be bounded. The design must address count-to-infinity, loops,
oscillation, metric manipulation, stale state, control storms, and malicious
topology churn. Past audio is never buffered for partition recovery.

## Privacy and security considerations

Route advertisements can reveal topology, stable identities, capabilities,
location correlation, and communicating peers. Malicious nodes can poison,
blackhole, wormhole, selectively forward, flood, or falsify resource metrics.
Agent 4 must review authentication, trust limits, metadata, and safe degradation;
cryptographic authentication alone does not make advertised routes truthful.

## Relay-envelope considerations

Agent 3 must identify the minimum routing target, packet identity, lifetime, and
traffic information needed by each candidate. RFC-0004 then decides their
protocol representation. No candidate may assume channel plaintext.

## Alternatives to evaluate

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| proactive distance vector | simple next-hop state; low forwarding work | count-to-infinity, churn chatter, poisoning | seeded churn/scale simulations |
| link state | richer path selection and convergence analysis | topology metadata and control/state cost | overhead/privacy/scale simulations |
| on-demand route discovery | less idle state | setup latency and discovery flooding | PTT acquisition and partition tests |
| controlled gossip/flooding | robust in small dynamic meshes | duplicates, bandwidth, poor scale | suppression and density benchmarks |
| hybrid strategy | can balance setup and steady state | complexity and more protocol states | only after simpler candidates fail criteria |

No algorithm is selected. The simplest candidate satisfying measured Samband
conditions should be preferred.

## Simulator evaluation plan

Candidate strategies use identical seeded scenarios and compare virtual
convergence time, delivery ratio, forwarding/control bytes, duplicate rate,
state high-water marks, route churn, latency, path stability, and relay energy
proxies. Scenarios include chains, grids, alternate paths, partitions, merge,
loss/jitter, relay withdrawal, dishonest metrics, and malformed control traffic.

## Test-vector and interoperability plan

Semantic vectors must define exact event order and expected route/forwarding
decisions without depending on map iteration order or wall-clock time. Negative
vectors cover stale/looping advertisements, invalid metrics, exhausted lifetime,
duplicate messages, unknown capability transitions, and bounded overflow.

## Open questions

- What network sizes, densities, churn, and radio ranges define the initial
  Samband operating envelope?
- Is routing destination-oriented, dissemination-oriented, or mixed for channel
  traffic?
- Which metrics are safe and stable enough to exchange?
- What prevents oscillation when relay willingness or battery changes rapidly?
- How does authenticated identity interact with privacy-preserving routing IDs?
- What freshness/convergence target is needed for acceptable PTT acquisition?
- Which misbehavior can be detected locally without global trust?

## Review requirements

- [ ] Agent 3 candidate analysis and recommendation.
- [ ] Agent 1 message/processing/versioning review.
- [ ] Agent 4 poisoning, metadata, and DoS review.
- [ ] RFC-0004 metadata requirements reconciled.
- [ ] Deterministic comparison results published.

## Acceptance blockers

- target operating envelope and metrics are not defined;
- candidate algorithms have not been compared;
- identity and envelope dependencies are unresolved;
- poisoning/metadata analysis is absent;
- convergence and resource budgets are unset.

## References

- [`simulator-first.md`](../architecture/simulator-first.md)
- [`RFC-0004`](RFC-0004-relay-envelope.md)
- [`experiment-backlog.md`](../research/experiment-backlog.md)

