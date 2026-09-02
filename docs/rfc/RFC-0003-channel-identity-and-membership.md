---
rfc: "0003"
title: Channel Identity and Membership
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

# RFC-0003: Channel Identity and Membership

## Summary

This RFC will define private-channel identity, authorization, membership proof,
membership changes, and offline operation. It keeps channel membership separate
from mesh participation and leaves credential and group-key choices unresolved.

## Status and authority

Draft and non-normative. A channel is an architectural concept, not yet a wire
identifier or cryptographic construction. Agent 4 review is mandatory.

## Motivation

Authorized endpoints must recognize channel traffic and one another without
requiring relays to join the channel. Adding and removing members through
partitions creates difficult authorization and key-rotation questions that
cannot be hidden in application state.

## Goals

- support zero, one, or many channel memberships per node;
- operate without a continuously available central authority;
- keep relays outside channel authorization and plaintext;
- define join, add, remove, leave, compromise, and rekey semantics;
- minimize channel-identifying metadata visible to non-members;
- support deterministic conformance tests.

## Non-goals

- choose a user directory or social graph;
- make human channel labels globally unique;
- select a group-key algorithm in this draft;
- define PTT arbitration or audio frames;
- promise instant revocation across disconnected partitions.

## Conceptual model

The design should distinguish a channel identifier or context, an authorization
state, a membership proof, payload-protection key state, membership epochs, and
local presentation metadata. Whether these are combined in one artifact is an
open security decision.

A relaying node receives no membership merely by forwarding channel traffic.
Human-visible labels such as "Channel 7" are not authorization evidence.

## Protocol-facing channel boundary

CHANNEL is an endpoint-only inner family carried inside RFC-0004's
`OPAQUE_ENDPOINT` payload. Relays do not parse channel messages and the outer
envelope does not expose a channel identifier, member, authenticated principal,
action subject, membership proof,
epoch, or operation subtype by default.

The protocol requires an Agent 4-defined channel-security boundary with three
logically distinct results:

1. protected-record authentication/open disposition and provisional security
   context;
2. security-replay disposition for that authenticated record;
3. authorization of the complete decoded channel action in the returned
   channel, authenticated-principal, subject, epoch, and current-state context.

These results need not be separate function calls or prescribe a standard
construction's internal order, but no plaintext or context leaves the security
boundary and no channel state changes until authentication and replay both
accept. Action authorization follows bounded decode and distinguishes the
authenticated sender/principal from an affected member or other action
subject. A successful outer peer/session or relay-envelope admission is
insufficient. A relay never invokes the channel boundary and needs no channel
credential.

The proposed logical CHANNEL catalog is:

| Type | Protocol purpose | Security-owned content |
| --- | --- | --- |
| `SESSION_INIT` | propose an endpoint channel session | channel context/bootstrap and initiator evidence |
| `MEMBERSHIP_PROOF` | present authorization evidence | proof construction, authenticated-principal/subject binding, freshness/replay data |
| `SESSION_ACCEPT` / `SESSION_REJECT` | conclude the bounded establishment attempt | authenticated decision and permitted failure detail |
| `MEMBERSHIP_UPDATE` | represent an add/remove/leave or other reviewed state transition | authority, epoch/key transition, conflict rules |
| `SESSION_CLOSE` | end the endpoint channel-session context | authorization and stale-message behavior |

These names define a reviewable state-machine surface, not wire codes or a
promise that every security construction uses separate messages. Agent 4 can
propose a smaller/different catalog through this RFC if a standard construction
requires it.

Every channel operation needs its own bounded operation identity and
idempotence/conflict rule. That identity is distinct from RFC-0004 packet
identity and cannot bypass security replay protection when the operation is
re-encapsulated in a new outer packet.

## Membership lifecycle

The accepted design must define channel creation, invitation/bootstrap,
authentication of existing and joining members, concurrent changes, removal,
leave, device loss, compromise, epoch transition, stale member behavior, and
partition merge. Availability and immediate revocation may conflict; the RFC
must state the chosen tradeoffs.

Agent 1 deliberately does not define the channel identifier, invitation or
credential, membership proof, authority/delegation, epoch/key state, add/remove
conflict rule, compromise/revocation guarantee, or recipient-selection tag.
Agent 4's Wave 0 candidate analysis is below and in
[`channel-security.md`](../security/channel-security.md); selection remains
informed by EXP-006. A real v0.x endpoint profile cannot accept
CHANNEL/PTT/AUDIO actions until that reviewed contract exists.

## Agent 4 candidate security model

The channel context is an internal collision-resistant group context generated
under the selected standard and is independent from a human label, discovery
handle, routing target, or stable public node identifier. It, the roster,
membership credentials, authenticated principal, action subjects, epoch, and
proofs remain inside the opaque endpoint boundary by default.

RFC-0003 must select an application authorization policy because group
authentication alone does not state who may add or remove a member. Candidates
include one administrator, an explicit administrator set, multiple ordinary
approvals over one canonical transition, and broader member authority. Each has
different compromise and partition availability. Samband will not invent a
threshold-signature construction.

MLS (RFC 9420 with RFC 9750) is the leading standardized EXP-006 candidate for
authenticated epochs, add/remove/update, Welcome delivery, forward-secrecy and
post-compromise mechanisms. It is not selected: Samband must still define its
Authentication and Delivery Service realizations, credentials, application
authorization, required extensions/suite, limits, private/public message
policy, concurrent-commit tie-break, partition reinitialization, resync,
recipient selection, and metadata budget.

Pairwise HPKE fan-out is a cost/scale comparator and possible standard
bootstrap component, not a group-membership protocol. HPKE alone supplies no
roster, authority, canonical epoch, replay, removal convergence, or
post-compromise recovery. Static group secrets and a home-grown combination of
HPKE, AEAD, and sender keys are not viable general-profile choices.

Every selected profile must also define bounded candidate channel/key trials,
ambiguous selector behavior, security replay state, and restart/rollback
recovery. Any relay-visible recipient selector remains blocked on EXP-007.

## Failure and resource bounds

Invalid proofs, oversized membership state, change floods, and divergent epoch
histories must fail within bounded work. Nodes cannot persist voice content to
repair a membership partition.

## Privacy and security considerations

Threats include unauthorized join, malicious inviter, removed member access,
compromised member, member enumeration, channel correlation, rollback, forked
membership state, replay, and denial of service. Security analysis must
distinguish confidentiality from authenticity and forward/post-compromise
properties rather than implying them.

## Routing considerations

Routing should not require plaintext channel identity. The RFC must specify how
an endpoint recognizes relevant protected traffic without exposing more channel
metadata to relays than necessary. Any multicast/dissemination implication must
be coordinated with RFC-0005.

RFC-0005 must define a routing target independently from a channel credential.
Any recipient-selection value visible to relays requires EXP-007 and Agent 4
approval; it cannot be added implicitly as a plaintext channel ID.

## Wire and versioning impact

Future artifacts may include channel contexts, invitation/bootstrap data,
membership changes, proofs, epochs, and algorithm/version identifiers. No field,
encoding, or transport is chosen.

These artifacts remain inside the endpoint payload by default. Unknown
security-critical channel versions, algorithms, or extensions fail closed
after channel security processing; they are never skipped as ordinary optional
fields. Exact encoding and authenticated canonicalization remain joint
Agent 1/Agent 4 work after EXP-002 and EXP-006.

After successful channel-open and security-replay admission, optional semantic
fields/extensions in a known CHANNEL type may be ignored only when they cannot
affect identity, membership, authority, channel/principal/subject/security context,
authorization, replay/freshness, state preconditions, or emitted actions.
Unknown critical semantic elements reject locally as
`(channel, UNSUPPORTED_CRITICAL_EXTENSION)` before authorization/state mutation.
Agent 4 must protect presence and criticality against injection, stripping, or
downgrade; protected-container/security-profile fields remain
`channel-security`-owned.

## Alternatives considered

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| pre-provisioned static group secret | simple offline bootstrap | poor removal, compromise, and scale properties | limited-profile threat analysis |
| signed membership state plus epoch keys | explicit audit/state | conflict and key-distribution complexity | partition/merge model |
| MLS RFC 9420/9750 application profile | standardized epochs, membership operations, group authentication, FS/PCS mechanisms | linear-epoch conflict, AS/DS realization, metadata, state/resource and partition fit unresolved | EXP-006 bounded standards prototype |
| pairwise HPKE fan-out with separate standardized group state | simple recipient isolation and useful bootstrap comparator | linear bandwidth; HPKE alone lacks membership, replay, FS/PCS, and convergence | EXP-006 scale/security comparison |
| sender-key construction supplied by a reviewed standard | efficient multi-sender media | distribution, sender attribution, replay, removal, and PCS fit | identify a complete standard before prototyping |

No alternative is selected.

## Test-vector and interoperability plan

Semantic vectors must cover create, add, reject, remove, leave, concurrent
changes, stale epoch, partition, merge, compromise assumptions, and unauthorized
payload. Cryptographic vectors follow only after standard construction review.

Pre-security semantic vectors may inject synthetic channel-open and action-
authorization dispositions to exercise message ordering and bounded state. They
must label the adapter non-cryptographic/non-production and contain no invented
keys, signatures, nonces, tags, or membership proofs.

## Migration and rollout

No channel-security or membership profile exists to migrate today. A future
change to channel identity, authority, membership proof, epoch/key lifecycle,
operation ordering, or partition behavior creates a new exact profile and
vector pin. Endpoints never reinterpret an unknown security-critical channel
artifact under an older profile or fall back to a static/plaintext credential.
Cross-profile membership/epoch migration requires its own reviewed transition;
relays do not translate it.

## Open questions

- What makes a channel identity stable, private, and collision-resistant?
- Who may add or remove members, and how is that authority delegated?
- How are concurrent offline membership changes reconciled or rejected?
- What confidentiality can be promised after removal or device compromise?
- How does an endpoint select relevant opaque payloads without exposing channel
  membership to every relay?
- What usability ceremony is acceptable for offline channel bootstrap?

## Review requirements

- [x] Agent 4 initial threat, authority, lifecycle, standard-candidate,
  partition, compromise, and metadata review recorded in this revision.
- [ ] Agent 4 construction/policy selection and SG-003 closure after EXP-006.
- [x] Agent 1 protected-inner-family, operation identity, state/wire boundary,
  failure, and synthetic-vector review recorded in this revision.
- [ ] Agent 3 dissemination metadata review.
- [ ] Partition/merge membership model tested.
- [ ] Positive and adversarial vector plan reviewed.

## Acceptance blockers

- channel identity representation and authorization policy remain unresolved;
- group-key/membership-change construction is unresolved; MLS is a candidate,
  not a selected profile;
- offline conflict and removal semantics are unresolved;
- metadata exposure has an initial budget but no measured mitigation;
- EXP-006, EXP-007, and EXP-019 evidence does not exist.

## Decision record

- 2026-09-01: Agent 1 revision placed CHANNEL operations behind a distinct
  endpoint security/replay and authorization boundary, kept them opaque to
  relays, and separated operation identity from packet identity. RFC remains
  Draft pending Agent 4 construction/lifecycle work and Agent 3 metadata review.
- 2026-09-02: Agent 4 documented membership authority choices, MLS as the lead
  standards experiment, incomplete alternatives, partition/removal limits,
  principal/subject separation, and bounded key-selection/replay requirements.
  No construction or policy was selected; RFC remains Draft.

## References

- [`RFC-0001`](RFC-0001-samband-network-model.md)
- [`RFC-0002`](RFC-0002-node-identity.md)
- [`RFC-0006`](RFC-0006-encrypted-channel-payload.md)
- [`channel-security.md`](../security/channel-security.md)
- [`threat-model.md`](../security/threat-model.md)
