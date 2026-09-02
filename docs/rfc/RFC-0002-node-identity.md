---
rfc: "0002"
title: Node Identity
status: Draft
authors:
  - Samband contributors
created: 2026-09-01
updated: 2026-09-02
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

## Agent 4 candidate architecture

The Wave 0 security review requires distinct per-device credentials,
channel-scoped membership identity, rotating discovery handles, session-local
contexts, and routing pseudonyms scoped to the minimum lifetime Agent 3 can
justify. A stable credential is not broadcast in discovery or copied into the
generic relay envelope by default. This is a required separation of security
contexts, not a selected credential format or primitive.

Credential/trust candidates are self-issued per-device credentials verified by
an out-of-band fingerprint or invitation, channel-scoped member credentials, a
locally rooted standard device-certificate hierarchy, and optional externally
certified deployment credentials. First-use continuity is an explicitly weaker
option whose initial encounter can be impersonated and which cannot grant
channel membership by itself.

Peer-session candidates for EXP-017 are EDHOC (RFC 9528), mutually
authenticated TLS/DTLS 1.3 profiles, and a fully specified Noise pattern.
HPKE is not an interactive peer-session protocol and MLS is not a one-hop
session replacement. No candidate or cipher suite is selected.

EXP-017 must compare complete session profiles, including standard post-
handshake record protection. EDHOC exports keying material but does not itself
define a generic Samband record layer; Samband must not invent exporter-plus-
AEAD framing, nonce, sequence, replay, update, or closure rules. Every candidate
must identify an established record construction and pin its framing,
direction/key separation, replay/loss/reordering, exhaustion/update,
restart/rollback, and resource semantics.

The full goals, assumptions, disclosure, partition, compromise, revocation, and
open-question analysis is in
[`node-identity.md`](../security/node-identity.md). Discovery-specific analysis
is in [`discovery-privacy.md`](../security/discovery-privacy.md).

## Protocol-facing identity contract

Protocol v0.x distinguishes opaque identity contexts without selecting their
construction:

| Context | Required protocol property | Explicitly not implied |
| --- | --- | --- |
| discovery handle | bounded, short-lived value usable only during one-hop discovery/bootstrap | node authentication, routing reachability, or channel membership |
| peer-session context | scoped to one admitted one-hop session and invalid after closure | long-lived node identity or trust in route claims |
| origin routing context | scoped/stable only as long as the selected routing profile requires | source route, human identity, channel identity, or global persistence |
| authenticated channel principal context | available only after future Agent 4-defined security processing accepts an opaque endpoint payload | relay-visible identity, node-wide identity, or automatic authority over every action subject |
| action subject/owner reference | decoded protected semantic value evaluated against the authenticated principal and current state | proof that the subject sent or authorized the action |
| display label | local presentation metadata | any protocol authorization |

Every selected profile must define the scope, equality, maximum encoded size,
creation/expiry event, and permissible correlation of each context it uses.
Bindings among contexts require an Agent 4 security verdict; an implementation
cannot infer them from equal bytes or application labels. The authenticated
principal, affected membership subject, PTT decision issuer, grant owner, and
media sender can be different roles and must not share one ambiguous `actor`
field or context.

The RFC-0004 packet identity is a forwarding duplicate-correlation token, not
an identity context or proof of origin. Capability claims and routing messages
also grant no identity or authorization by themselves.

Before Agent 4 defines peer admission, discovery/session messages can be used
only as bounded experimental negotiation inputs. They cannot create
authoritative neighbor, capability, route, duplicate, membership, PTT, or media
state. Simulator vectors may inject a synthetic admission disposition, clearly
marked non-cryptographic and non-production.

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

Agent 4 exclusively owns credential/key type and generation, proof of
possession or signatures, trust bootstrap, secure storage, rotation, recovery,
revocation/partition limits, compromise behavior, multi-device semantics,
discovery-alias derivation/unlinkability, alias-to-session binding, and the
authentication of routing origins/targets. Agent 1 will not add placeholder
keys, signature fields, algorithm identifiers, or derivations to complete a
schema.

## Routing considerations

Routing may need a stable-enough target or authenticated control origin, but
that need must not automatically force a globally visible persistent identity.
Agent 3 must state routing lifetime and correlation requirements in RFC-0005,
including the exact local-delivery predicate and when a routing context rotates
or expires. EXP-005 must test discovery/session/routing binding under reconnect
and partition before a representation is selected.

## Wire and versioning impact

Future messages may carry discovery aliases, session authentication material,
key/algorithm identifiers, and rotation proofs. Exact formats, canonicalization,
negotiation, and downgrade handling remain unresolved.

RFC-0004's exact-profile negotiation applies before an admitted peer session.
Unknown security-critical identity/authentication extensions fail closed; they
cannot be treated as optional fields. The selected peer-session profile must
bind the complete most-recent offered exact-pair set, selected pair and echo,
both roles, session-exchange identity, credential evidence, fresh handshake
context, methods/suites/security-critical extensions, and Samband application
context into one authenticated transcript with key confirmation. Every later
link-control packet must match the admitted exact pair and session before state
mutation. EXP-002 establishes the required canonicalization/preservation
properties and EXP-017 compares standard constructions.

## Alternatives considered

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| one long-lived public identifier everywhere | simple correlation and routing | pervasive tracking; compromise linkage | privacy analysis; likely unacceptable |
| long-lived credential with rotating discovery aliases | balances authentication and discovery privacy | rotation/linking protocol complexity | unlinkability and session-binding analysis |
| pairwise identifiers | identifier-level cross-peer separation; no overall unlinkability claim | discovery and multi-hop routing complexity; collusion, timing, and lower-layer correlation remain | routing/privacy feasibility experiment |
| externally certified identity | easier trust bootstrap in some deployments | central dependency and exclusion risk | optional-profile analysis only |
| EDHOC peer session | compact standard AKE with transcript and credential hooks | CBOR/COSE profile, identity method, errors, and library fit unresolved | EXP-017 |
| TLS/DTLS 1.3 peer session | mature standard implementations and transcript protection | mutual-peer role, framing, overhead, resumption, and credential profile unresolved | EXP-017 |
| fixed Noise peer-session pattern | compact established framework and identity-hiding choices | pattern/prologue/suite/negotiation must be profiled; framework status and libraries need review | EXP-017 |

No alternative is selected.

## Test-vector and interoperability plan

After algorithm selection, vectors must cover deterministic public derivations,
valid and invalid proofs, rotation/session binding, replay, wrong context,
unknown algorithms, corrupted keys, and cross-version behavior. Fixtures use
published synthetic keys only.

Before algorithm selection, semantic vectors cover scope separation, expiry,
unbound-context rejection, and the rule that unadmitted discovery input creates
no authoritative state. Such vectors inject a named synthetic security verdict
and do not claim authentication.

## Migration and rollout

No identity/security profile exists to migrate today. Any future v0.x change to
credential, handle scope, binding, authentication, rotation, recovery, or
failure behavior uses a new exact protocol/security profile and vector pin.
Peers never fall back from an unknown security-critical identity mechanism to
an unauthenticated or older interpretation. Cross-profile identity migration
requires explicit Agent 4-reviewed semantics; equal-looking identifiers do not
bridge profiles automatically.

## Open questions

- What is the root node credential and how is it generated and stored?
- Can discovery aliases be unlinkable to passive observers yet bind safely to a
  subsequent authenticated session?
- What identity does multi-hop routing target and for how long is it stable?
- How do users verify peers or channels without central service availability?
- What recovery and revocation claims are realistic during partitions?
- Is multi-device identity shared, delegated, or intentionally distinct?

## Review requirements

- [x] Agent 4 initial threat-model, identity/session candidate, lifecycle,
  privacy, and partition review recorded in this revision.
- [ ] Agent 4 selection review and SG-002 closure after EXP-005/EXP-017.
- [x] Agent 1 identity-context, wire-boundary, versioning, and synthetic-vector
  review recorded in this revision.
- [ ] Agent 3 routing identity requirements supplied.
- [ ] Privacy/unlinkability experiment designed.
- [ ] Canonical identity vector plan reviewed.

## Acceptance blockers

- the initial threat model is documented but SG-001 remains open pending
  independent acceptance/review;
- no standard construction or credential lifecycle is selected;
- discovery privacy and routing identity needs are not reconciled;
- recovery/revocation semantics and rollback-safe storage are unresolved;
- EXP-005, EXP-017, and EXP-019 evidence does not exist.

## Decision record

- 2026-09-01: Agent 1 revision separated discovery, peer-session, routing,
  channel-member/action-subject, packet, and display contexts and defined their protocol-facing
  bounds without choosing credentials or cryptography. RFC remains Draft for
  Agent 3/Agent 4 review and EXP-005.
- 2026-09-02: Agent 4 required distinct principal/subject roles, private stable
  credentials, mandatory complete negotiation binding, and standard
  peer-session/credential candidates. No construction was selected; SG-002
  remains open for EXP-005/017/019 and independent review.

## References

- [`network-model.md`](../architecture/network-model.md)
- [`threat-model.md`](../security/threat-model.md)
- [`node-identity.md`](../security/node-identity.md)
- [`discovery-privacy.md`](../security/discovery-privacy.md)
- [`experiment-backlog.md`](../research/experiment-backlog.md)
