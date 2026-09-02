---
rfc: "0007"
title: PTT Arbitration
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

# RFC-0007: PTT Arbitration

## Summary

This RFC will define half-duplex Push-To-Talk floor control without assuming a
central authority. It must handle simultaneous requests, partitions, merge,
stale ownership, loss, delay, and malicious participants. No arbitration
algorithm, clock model, or message encoding is selected here.

## Status and authority

Draft and non-normative. `REQUEST`, `GRANT`, `BUSY`, and `RELEASE` are
conceptual interactions, not frozen message names or a guaranteed sequence.

## Motivation

Users need predictable feedback about who may transmit. In an opportunistic
mesh, nodes can see different channel partitions and event orders. A design that
assumes a reachable coordinator fails the off-grid goal, while an unbounded
distributed consensus protocol conflicts with realtime latency and partitions.

## Goals

- primarily half-duplex channel behavior without permanent central authority;
- deterministic resolution for concurrent requests within a connected view;
- bounded stale ownership and recovery after speaker disappearance;
- explicit partition and merge behavior;
- authentication and authorization of floor-control actions;
- low acquisition latency and bounded control overhead;
- observable state suitable for deterministic simulation.

## Non-goals

- guarantee one global speaker across disconnected partitions;
- create permanent consensus or a blockchain;
- define audio codec or channel-key management;
- persist or replay audio missed while a request was unresolved;
- assume synchronized trustworthy wall clocks.

## Protocol-facing PTT boundary

PTT is an endpoint-only inner family inside RFC-0004's `OPAQUE_ENDPOINT`
payload. Relays see neither the PTT subtype nor channel, authenticated
principal, action subject, request, grant, term, or speaker context by default.
A PTT message reaches the state machine
only after RFC-0006 channel open/security-replay processing and channel action
authorization accept it.

The proposed catalog and minimum logical content are:

| Type | Minimum semantic content | Required effect |
| --- | --- | --- |
| `REQUEST` | request identity, request-subject reference or profile-pinned derivation, plus optional bounded policy input | creates/replaces one pending request idempotently |
| `GRANT` | request identity, grant identity, grant-owner action subject, arbitration term/context, bounded validity | is the only control action that can authorize transmit state |
| `BUSY` | request identity plus bounded decision/reference context | rejects/defers that request; never grants ownership |
| `RELEASE` | exactly one pending-request or grant reference plus bounded reason | cancels a request or releases only the referenced grant idempotently |

Message names and fields are logical, not wire codes. The selected arbitration
model can refine the decision/term context through this RFC, but it cannot use
outer packet identity as a request, grant, owner, or replay identity.

The selected profile must state whether a request subject is carried as a
protected semantic reference or derived from the authenticated principal. Any
derivation is an exact authorization rule bound to the channel epoch and
current state; equal-looking identifiers or omission never imply principal/
subject equality. The same rule identifies the grant-owner subject referenced
by a later `GRANT`.

## Proposed abstract state machine

The following state machine constrains externally observable behavior without
selecting who grants the floor or how contenders are ordered:

| State | Entry | Permitted transitions |
| --- | --- | --- |
| `IDLE` | no current local request or accepted grant | local press -> `REQUESTING`; accepted grant to another -> `RECEIVING` |
| `REQUESTING` | one bounded local request is pending | matching accepted grant -> `TRANSMIT_GRANTED`; matching busy/release/cancel/expiry -> `IDLE`; other accepted grant -> `RECEIVING` |
| `TRANSMIT_GRANTED` | one accepted unexpired grant names the local action subject | local release/grant expiry/revocation/session loss -> `RELEASING` or `RECOVERING`; newer accepted conflicting decision -> profile-defined recovery |
| `RECEIVING` | an accepted grant names another action subject in the local connected view | matching release/expiry -> `IDLE`; conflict/merge -> `RECOVERING` |
| `RELEASING` | the local node has emitted an idempotent release/cancel | accepted completion or bounded timeout -> `IDLE` |
| `RECOVERING` | ownership is stale, conflicting, or lacks required session state | selected arbitration recovery completes -> `IDLE`, `RECEIVING`, or `TRANSMIT_GRANTED` |

Only `TRANSMIT_GRANTED` permits a local audio stream start. A request, timeout,
silence, media packet, optimistic UI, or locally guessed owner never creates a
grant. A profile that permits optimistic/partition-local transmission must name
that behavior as a separate experimental state and user-visible condition; it
cannot present it as a globally confirmed grant.

The state machine uses an abstract locally monotonic timer and/or logical
arbitration term. It never assumes synchronized or trustworthy wall clocks.
EXP-008 must select authority, term/lease representation, tie-break, timeouts,
retransmission, fairness/priority, cancellation, recovery, and merge behavior.

## Identifier, retransmission, and idempotence rules

- Request identities are unique within the Agent 4-validated channel,
  authenticated-principal, and arbitration context for the profile-defined
  retention window.
- Grant identities/terms identify one ownership decision and cannot be reused
  to grant a different action subject/request.
- A retry preserves the inner request/grant/release identity but normally uses
  a new outer packet identity.
- Repeated identical `REQUEST`, `GRANT`, `BUSY`, or `RELEASE` operations are
  idempotent and do not extend a lease/validity window merely by duplication.
- A `RELEASE` cannot cancel a different request or release a newer/different
  grant. Unknown or stale references produce no ownership transition.
- Re-encapsulating an old action in a new packet does not bypass Agent 4 replay
  checks or make it current.
- AUDIO messages never establish, extend, or transfer PTT ownership.

Identifier syntax, generation, collision/linkability, authenticated-principal/
action-subject binding, replay windows, and logging are Agent 4 dependencies.
Agent 1 defines
only scope, equality, references, idempotence, and bounded lifetime here.

## Partition and merge contract

Protocol v0.x cannot guarantee one global speaker across disconnected
partitions. Every selected model must state whether each component can issue a
partition-local grant, how that state is shown to users, and what happens when
conflicting current grants meet after merge.

Merge resolution applies only to current control state. It never replays audio
missed during the partition and never makes an old grant retroactively valid.
Conflicting media received before an accepted merge decision is dropped or
handled only according to the explicit selected profile.

## Failure and resource bounds

Requests, retries, ownership records, and deduplication state must expire and be
bounded. Lost release, node disappearance, delayed grants, reordered messages,
clock skew, duplicate requests, request floods, and conflicting partition owners
must not cause permanent lockout or unbounded control traffic.

Every profile must bound concurrent pending requests, retained request/grant
identities, retry count/rate, grant validity, recovery time, and emitted control
messages per event. Resource saturation can reject new requests but cannot
evict/replace a current authorized grant ambiguously.

## Privacy and security considerations

Floor-control messages can reveal channel activity, speaker identity, timing,
and membership. A malicious member can monopolize or jam the floor, forge
release, replay grants, or exhaust request state. Agent 4's initial threat and
boundary review requires exact authorization, replay, privacy, and abuse limits;
cryptography cannot force a malicious member to transmit fairly.

Agent 4 exclusively owns principal/subject/channel authentication and authorization,
grantor/decision authority, replay protection, request/grant identity binding,
speaker privacy, malicious-member abuse limits, and any security epoch. PTT
subtypes/identifiers remain protected-inner metadata by default; EXP-007 must
justify any outer exposure. No signature, credential, key, nonce, priority
authority, or anti-replay construction is selected here.

The authenticated sending principal, arbitration decision issuer, request
subject, grant owner, and releasing principal are distinct roles. A selected
profile must authorize the complete decoded action against the current channel
epoch, principal role, referenced subject/owner, operation/request/grant/term,
state revision, and bounded authorization validity. That verdict establishes
permission and principal/subject binding, not that the referenced PTT/grant/
stream semantic preconditions currently hold. The state machine checks those
next against the same revision; authorization, precondition check, and guarded
transition are atomic or revision-bound so a verdict cannot be reused after
state changes. An authorized but missing/stale grant can therefore produce
`STATE_CONFLICT` rather than `POLICY_REJECTED`.

Security replay is scoped independently from packet duplicate and PTT
idempotence. Rewrapping an old grant under a new packet ID or protected record
does not extend it. Once an authenticated record consumes replay state, a later
PTT state conflict does not roll that security state back under the proposed
RFC-0006 model. Exact replay windows, grant authority, partition-local status,
and member request/rate limits remain EXP-006/008 decisions.

## Routing considerations

Arbitration latency and consistency depend on propagation and topology. Agent 3
must characterize whether control uses unicast, dissemination, a selected
coordinator, or another pattern, and how route changes affect ownership. PTT
must not assume delivery guarantees unavailable from RFC-0005.

The selected model must state what constitutes a connected arbitration view,
how route loss affects a pending request/current grant, and which bounded
control retries are permitted. RFC-0004 hop limit is not a grant lifetime, and
routing duplicate suppression is not PTT idempotence or security replay.

## Alternatives to evaluate

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| deterministic distributed contention with bounded lease | no fixed coordinator | clock/partition conflicts and fairness | seeded loss/skew/concurrency simulation |
| dynamically elected reachable coordinator | simple decisions while reachable | election latency and partition leaders | churn and merge experiments |
| circulating token/permission artifact | explicit ownership | token loss/recovery and path dependency | loss/partition simulation |
| optimistic local transmit with conflict suppression | low perceived latency | overlapping speech and inconsistent feedback | UX/latency/conflict measurements |

No alternative is selected.

## Wire and versioning impact

Future semantics may require request IDs, participant or sender context,
ownership generation, priority/policy, expiry or logical ordering, decisions,
and release/recovery signals. Exact fields, confidentiality, and encoding remain
unresolved.

All proposed PTT fields remain inside the endpoint payload by default. Unknown
PTT types are rejected as `(ptt, UNSUPPORTED_MESSAGE)`. Unknown optional
semantic fields/extensions in a known PTT type are ignored locally; unknown
critical semantic fields/extensions reject as
`(ptt, UNSUPPORTED_CRITICAL_EXTENSION)` before authorization or state mutation.
An optional element cannot affect identity, authority, context,
authorization, replay/freshness, PTT state preconditions, or emitted actions;
Agent 4 must protect its presence and criticality.
All of those decisions occur only after successful channel-open and
security-replay processing; security-profile fields remain Agent 4-owned at the
`channel-security` boundary. Relays continue treating the outer payload as
opaque. Exact-profile negotiation must prevent an endpoint from assuming
unsupported arbitration semantics, and Agent 4 must bind/downgrade-protect that
negotiation.

## Test-vector and interoperability plan

Deterministic vectors must cover single request, concurrent requests with every
event ordering, loss/duplication/reordering, delayed request/grant/release,
speaker disappearance, timeout, partition-local speakers, merge, stale messages,
unauthorized actions, monopolization limits, and version mismatch.

Vectors also cover retry with a new packet identity and stable request identity,
duplicate grant without validity extension, release of the wrong/newer grant,
media before grant, media that cannot create ownership, bounded request floods,
and rejection before any state mutation. Until Agent 4 review, security verdicts
and principal/subject/channel contexts are synthetic non-production inputs.

## Migration and rollout

Each v0.x arbitration model is an exact endpoint profile. Endpoints do not mix
request/grant/term semantics across profiles or infer compatibility from message
names. Profile/session change expires pending requests, grants, and recovery
state according to an explicit bounded rule; it never replays missed audio or
converts an optimistic/partition-local state into a confirmed grant. Security-
critical negotiation/downgrade behavior remains Agent 4-owned.

## Open questions

- Is a partition-local speaker allowed, and how is that presented to users?
- What fairness or priority policy belongs in Protocol v0?
- Can arbitration use logical time without synchronized clocks?
- What acquisition latency budget is realistic over several hops?
- Which party grants the floor in a fully decentralized channel?
- How are conflicting owners resolved after merge without replaying audio?
- What abuse controls are enforceable against an authorized malicious member?

## Review requirements

- [x] Agent 1 inner-message catalog, abstract state machine, identity,
  idempotence, partition, wire-boundary, and vector review recorded here.
- [ ] Agent 3 propagation/partition review.
- [x] Agent 4 initial principal/subject, authorization, privacy, replay, and
  malicious-member abuse requirements recorded.
- [ ] Agent 4 review of the selected arbitration/security profile and SG-007.
- [ ] Deterministic arbitration comparison completed.
- [ ] User-visible ambiguity documented.

## Acceptance blockers

- arbitration alternative and clock model are unresolved;
- routing delivery assumptions and latency budget are unknown;
- partition/merge semantics are unresolved;
- authorization and abuse requirements are reviewed initially, but authority,
  construction, replay bounds, and enforceable policy remain unresolved.

## Decision record

- 2026-09-01: Agent 1 revision defined an endpoint-only PTT catalog, abstract
  states, operation identities/idempotence, grant-gated media boundary, and
  explicit partition contract without selecting arbitration authority or
  algorithm. RFC remains Draft pending EXP-008 and Agent 3/Agent 4 review.
- 2026-09-02: Agent 4 separated authenticated principals from decision issuers
  and grant subjects, required revision-bound action authorization and distinct
  replay consumption, and documented malicious-member/privacy limits. No PTT
  authority or security construction was selected.

## References

- [`RFC-0003`](RFC-0003-channel-identity-and-membership.md)
- [`RFC-0005`](RFC-0005-mesh-routing.md)
- [`RFC-0008`](RFC-0008-audio-transport.md)
- [`channel-security.md`](../security/channel-security.md)
- [`threat-model.md`](../security/threat-model.md)
