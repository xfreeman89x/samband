---
rfc: "0002"
title: Node Identity
status: Draft
authors:
  - Samband contributors
created: 2026-09-01
updated: 2026-09-01
target: Protocol v0.x
requires:
  - Agent 1 Protocol review
  - Agent 3 Routing review
  - Agent 4 Security review
supersedes: []
superseded_by: null
---

# RFC-0002: Node Identity

## Summary

This RFC will define how Samband peers authenticate nodes while minimizing
tracking during discovery and keeping node identity distinct from channel
membership and human-facing names. It deliberately does not choose algorithms,
key formats, or identifier derivations in this draft.

## Status and authority

Draft and non-normative. All cryptographic and wire-visible decisions require
Agent 4 Security and Agent 1 Protocol review.

## Motivation

Samband needs sufficient peer accountability to resist impersonation, replay,
and route injection, yet permanently broadcasting a stable identifier would
enable tracking. One identifier cannot be assumed to safely serve discovery,
authenticated sessions, routing, channel authorization, and user display.

## Goals

- authenticate peers without a mandatory central online service;
- support offline and partitioned operation;
- minimize stable identity exposure during discovery;
- define explicit relationships among node, discovery, session, channel, and
  display identities;
- support rotation, compromise recovery, and future versioning;
- provide independently testable derivation/verification behavior.

## Non-goals

- choose channel membership or group-key management;
- create a global human identity or public directory;
- require legal identity, phone number, or email address;
- design custom cryptographic primitives;
- define routing trust from identity alone.

## Candidate identity layers

The design should evaluate at least:

- a longer-lived node authentication credential;
- unlinkable or rotating discovery identifiers;
- connection/session-bound peer identifiers;
- channel-specific authorization identity or proof;
- optional local human-readable labels outside protocol authority.

Whether these are derived, independent, certified, or pairwise is unresolved.

## Lifecycle questions

The accepted design must specify creation, secure storage, proof of possession,
rotation, recovery, multi-device behavior, compromise, revocation limits while
offline, and how peers treat an identity they have never seen before.

## Failure and resource bounds

Unauthenticated discovery traffic and invalid proofs must have strict size,
rate, and computation bounds. Failure cannot reveal secret material or create
unbounded identity caches. Clock dependence must be explicit because offline
nodes may have skewed clocks.

## Privacy and security considerations

Threats include impersonation, Sybil/resource attacks, correlation of rotating
identifiers, malicious peers, stolen device credentials, downgrade, replay,
and identity recovery that re-links past observations. Agent 4 must produce the
threat-model context before an alternative is selected.

## Routing considerations

Routing may need a stable-enough target or authenticated control origin, but
that need must not automatically force a globally visible persistent identity.
Agent 3 should state routing lifetime and correlation requirements in RFC-0005.

## Wire and versioning impact

Future messages may carry discovery aliases, session authentication material,
key/algorithm identifiers, and rotation proofs. Exact formats, canonicalization,
negotiation, and downgrade handling remain unresolved.

## Alternatives considered

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| one long-lived public identifier everywhere | simple correlation and routing | pervasive tracking; compromise linkage | privacy analysis; likely unacceptable |
| long-lived credential with rotating discovery aliases | balances authentication and discovery privacy | rotation/linking protocol complexity | unlinkability and session-binding analysis |
| pairwise identifiers | strong cross-peer unlinkability | discovery and multi-hop routing complexity | routing feasibility experiment |
| externally certified identity | easier trust bootstrap in some deployments | central dependency and exclusion risk | optional-profile analysis only |

No alternative is selected.

## Test-vector and interoperability plan

After algorithm selection, vectors must cover deterministic public derivations,
valid and invalid proofs, rotation/session binding, replay, wrong context,
unknown algorithms, corrupted keys, and cross-version behavior. Fixtures use
published synthetic keys only.

## Open questions

- What is the root node credential and how is it generated and stored?
- Can discovery aliases be unlinkable to passive observers yet bind safely to a
  subsequent authenticated session?
- What identity does multi-hop routing target and for how long is it stable?
- How do users verify peers or channels without central service availability?
- What recovery and revocation claims are realistic during partitions?
- Is multi-device identity shared, delegated, or intentionally distinct?

## Review requirements

- [ ] Agent 4 threat-model and cryptographic architecture review.
- [ ] Agent 1 wire/versioning review.
- [ ] Agent 3 routing identity requirements supplied.
- [ ] Privacy/unlinkability experiment designed.
- [ ] Canonical identity vector plan reviewed.

## Acceptance blockers

- threat model is not complete;
- no standard construction or credential lifecycle is selected;
- discovery privacy and routing identity needs are not reconciled;
- recovery/revocation semantics are unresolved.

## References

- [`network-model.md`](../architecture/network-model.md)
- [`threat-model.md`](../security/threat-model.md)
- [`experiment-backlog.md`](../research/experiment-backlog.md)
