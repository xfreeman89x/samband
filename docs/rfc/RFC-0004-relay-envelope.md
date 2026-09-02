---
rfc: "0004"
title: Relay Envelope
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

# RFC-0004: Relay Envelope

## Summary

This RFC proposes the logical Samband v0.x outer envelope, exact experimental
profile negotiation, processing order, hop lifetime, packet identity, duplicate
handling, unknown extension/type behavior, and routing/security interfaces.

The envelope separates minimal routing-visible state from an opaque endpoint
payload. The proposal intentionally does not select bytes, a schema language,
an addressing/routing algorithm, an authentication construction, or a channel
protection construction.

## Status and authority

Draft and non-normative. The relay-envelope/opaque-payload separation is an
architectural invariant. Field names in this RFC and semantic vectors are
logical names, not stable wire names or assigned numbers.

Agent 1 review establishes a coherent proposed v0.x processing contract. Agent
4's initial review defines the required admission, coverage, replay, malicious-
relay, and privacy boundaries but selects no construction. Exact encoding
remains blocked on EXP-002 and EXP-014. Routing target semantics, numeric
limits, outer authentication, mutable-field protection, and measured metadata
visibility remain blocked on Agent 3, EXP-007/018, and later security review.

## Motivation

Relays need enough information to reject malformed or exhausted traffic,
suppress forwarding duplicates, apply bounded policy, and move opaque payloads.
Excess metadata weakens privacy; insufficient validated metadata enables loops,
injection, cache poisoning, and unbounded work. Independent implementations
need deterministic rules before an encoding prototype can be compared fairly.

## Goals

- carry opaque endpoint payloads through non-member relays;
- bound frame, parsing, extension, payload, lifetime, duplicate, and forwarding
  work;
- distinguish exact profile semantics from envelope syntax evolution;
- define deterministic processing and local failure categories;
- preserve unknown optional extensions across forwarding;
- keep packet duplicate identity distinct from security replay and operation
  identities;
- separate local delivery from forwarding eligibility.

## Non-goals

- choose a routing algorithm, route metric, target kind, or next-hop encoding;
- choose identity, signature, authentication, encryption, key, nonce, or replay
  mechanisms;
- define channel, PTT, codec, or audio-frame bodies in the outer envelope;
- expose private-channel labels for relay convenience;
- provide arbitrary-protocol tunneling or store-and-forward delivery;
- freeze Protocol v1 or a byte encoding.

## Terminology

**Envelope format** identifies the parser/framing generation needed to recover
bounded outer fields.

**Protocol profile** identifies one exact experimental set of field, message,
processing, routing, and limit semantics.

**Packet identity** is an opaque forwarding duplicate-correlation token scoped
by the selected compatibility pair and an origin routing context. It is not
proof of identity, authenticity, authorization, collision resistance, or
security replay protection.

**Hop limit** is the proposed Protocol v0.x TTL semantic: an
origin-selected, inclusive forwarding-distance/path-hop budget, not a count of
future transmissions from the current receiver, wall-clock age, media
freshness, or replay state.

## Proposed logical envelope

The exact selected encoding must represent the following logical items. Field
presence is class/profile-dependent.

| Logical item | Purpose | Proposed v0.x rule |
| --- | --- | --- |
| envelope format | bounded parser selection | exact supported format required; no parser guessing |
| protocol profile | peer and multi-hop semantics | exact pre-v1 profile match; no numeric compatibility inference |
| outer class/type | link control, mesh control, or opaque endpoint data | registry from RFC-0001; unknown forwarding semantics fail closed |
| packet identity | forwarding duplicate correlation | mandatory and immutable for forwardable packets |
| origin routing context | scopes packet identity and routing origin | opaque; not a long-lived node credential or source route |
| routing directive | local-delivery/forwarding input | optional profile-defined scope plus opaque target; never a next-hop or path list |
| hop limit | origin-selected forwarding-distance limit | mandatory for forwardable packets; inclusive path-budget semantics below |
| traffic treatment | untrusted bounded control or freshness-oriented scheduling hint | coarse profile registry; not authorization, inner-type proof, or delivery guarantee |
| payload length | bound opaque payload parsing/allocation | must agree exactly with framing |
| extensions | bounded evolution surface | every extension declares critical or optional handling |
| payload | outer control body or opaque endpoint container | `OPAQUE_ENDPOINT` bytes are preserved; known control bodies are processed only under their selected profile |

`LINK_CONTROL` packets are never forwarded and do not carry a mesh routing
directive. `MESH_CONTROL` packets use only types and propagation rules selected
by the routing profile. `OPAQUE_ENDPOINT` packets expose no channel, PTT, audio,
authenticated principal, action subject, request, grant, stream, codec, sender,
or epoch subtype by default.

The routing directive contract for every admitted target kind must define its
syntax/equality, scope/stability, local-delivery predicate, forwarding scope,
maximum fanout, no-route behavior, whether delivery terminates forwarding,
metadata exposure, and required security binding. RFC-0005 and Agent 3 own the
first target kinds. A channel identifier is not a routing target by default.

The next hop and concrete transport attachment are local decisions and never
generic envelope fields. Protocol v0.x does not carry a full path or source
route.

## Proposed traffic-treatment registry

The logical v0.x proposal has two coarse values, both still subject to EXP-007
and Agent 3/Agent 4 review:

| Treatment | Semantics | Not implied |
| --- | --- | --- |
| `BOUNDED_CONTROL` | bounded control queue/retry/replacement behavior only when the governing message/profile defines it | authorization, guaranteed delivery, global priority, or indefinite retention |
| `FRESH_MEDIA` | freshness-oriented queueing; stale or partition-retained work is dropped | audio subtype, permission to speak, security validity, or a fixed codec |

`LINK_CONTROL` and `MESH_CONTROL` use `BOUNDED_CONTROL`. An
`OPAQUE_ENDPOINT` packet can use either value without revealing its inner
subtype. Relays treat the value only as an untrusted, bounded scheduling input.
The future Agent 4-reviewed endpoint protection profile must bind it to the
opaque payload and the receiving endpoint must reject a mismatch with the
selected inner semantics as `STATE_CONFLICT`; a false value cannot change
authorization or make stale content valid. Unknown values fail closed.

## Protocol v0.x versioning and negotiation

Versioning has two independent axes:

1. the envelope format determines whether bounded outer parsing is possible;
2. the protocol profile determines exact field, catalog, processing, routing,
   extension, and limit semantics.

The exact compatibility selection is the ordered pair `(envelope format,
protocol profile)`. Neither identifier contains or implies the other. A
released vector set and conformance claim pin both members explicitly.

Pre-session `DISCOVERY_ADVERTISEMENT` is the only packet without a selected
protocol profile. It uses the bounded bootstrap grammar of an envelope format
the receiver already supports and advertises a bounded list of exact
`(envelope format, protocol profile)` pairs. The initiator selects exactly one
pair from the most recent offer using local policy and binds the selection to
one link-local session-exchange identity in `SESSION_INIT`. A responder either
echoes that exact pair and exchange identity in `SESSION_ACCEPT` or rejects; it
never substitutes another pair. The session becomes authoritative only after
both roles have confirmed the same pair and the profile-required Agent 4
admission succeeds. Profile identifiers are opaque for selection: neither side
infers compatibility or preference from numeric ordering. If no exact pair
intersects, the session is not admitted. Simultaneous initiation, retry, stale
offer, and collision behavior remain part of the exact bootstrap profile and
EXP-002; the grammar cannot fall back to parser guessing.

The selected Agent 4-reviewed peer-session profile must bind the complete
most-recent offered exact-pair set, selected pair and responder echo/rejection,
both initiator/responder roles, session-exchange identity, presented credential
evidence, fresh handshake/session context, security method/suite/critical
extensions, Samband application context, and relevant discovery/adjacency
context into the same authenticated transcript with required key confirmation.
Every post-bootstrap `LINK_CONTROL`, `MESH_CONTROL`, and `OPAQUE_ENDPOINT`
packet's pair must exactly match its admitted ingress session before duplicate
lookup, state mutation, local dispatch, or forwarding. A supported but
session-mismatched pair is rejected locally without a network response; the
exact `(layer, result)` mapping remains an Agent 1/4 failure-oracle decision for
the selected profile. Before construction selection and EXP-002/017, discovery
remains an untrusted negotiation hint and cannot create authoritative peer,
capability, route, or duplicate state.

Every forwardable packet is processed under one exact selected pair, and each
ordinary egress session used for it must be admitted under that same pair. A relay
cannot transcode to a different envelope format, reinterpret the packet under a
different protocol profile, or forward under a pair whose lifetime, target,
critical-extension, duplicate, or format rules it does not implement. A relay
does reserialize the same envelope format when applying permitted mutable
forwarding fields such as hop limit; that is not format translation. A change
to either pre-v1 member can be incompatible and requires a new pair/vector-set
pin.

Protocol v1 major/minor compatibility is deliberately not frozen by this RFC.

## Unknown field, extension, and message behavior

- An unsupported envelope format is dropped after only the bounded prefix
  parse; the payload is not parsed or forwarded.
- An unsupported exact protocol profile is dropped and not translated.
- An unknown outer class, forwarding scope, routing target kind, or traffic
  treatment is dropped as `UNSUPPORTED_OUTER_SEMANTICS` because forwarding
  semantics are unknown. An unknown critical extension is dropped as
  `UNSUPPORTED_CRITICAL_EXTENSION`.
- An unknown optional envelope extension is ignored for local behavior and
  preserved unchanged when forwarding.
- Unknown optional fields inside a known outer message are ignored for local
  behavior and preserved when that message is forwarded. An unknown critical
  field rejects that message as `(outer, UNSUPPORTED_CRITICAL_EXTENSION)`.
- Unknown `LINK_CONTROL` or `MESH_CONTROL` message types are dropped as
  `(outer, UNSUPPORTED_MESSAGE)` and are not forwarded.
- Relays do not inspect the inner type of an `OPAQUE_ENDPOINT` payload. An
  endpoint that accepts/opens the payload but does not implement its inner
  family/profile drops it locally as `(endpoint, UNSUPPORTED_MESSAGE)`; an
  unknown type inside a known family uses that family's layer. Foreign relay
  eligibility is unchanged.
- After successful Agent 4-defined channel-open and security-replay admission,
  an unknown optional semantic field/extension in a known CHANNEL, PTT,
  AUDIO_CONTROL, or AUDIO_MEDIA message is ignored for local behavior. An
  unknown critical semantic field/extension rejects before action authorization
  or inner state mutation as `(channel, UNSUPPORTED_CRITICAL_EXTENSION)`,
  `(ptt, UNSUPPORTED_CRITICAL_EXTENSION)`, or
  `(audio, UNSUPPORTED_CRITICAL_EXTENSION)` according to the known family.
  Unknown protection-format, algorithm, credential, authentication, replay, or
  other security-critical material remains Agent 4-owned and fails at the
  `channel-security` boundary instead; no Draft rule reclassifies it as
  optional.
- An optional inner semantic element cannot affect identity, channel/principal/subject/
  security context, authority, authorization, replay/freshness, state-machine
  preconditions, or emitted actions. Anything that can must be critical or
  Agent 4-owned. Agent 4 must bind presence and criticality under future
  integrity coverage; this RFC selects no mechanism.
- Duplicate singular fields, impossible lengths, truncated values, illegal
  criticality, and representations with multiple interpretations are
  `MALFORMED`.

EXP-002 must prove that the selected encoding can bound, distinguish, skip, and
preserve extensions without ambiguous canonicalization. Agent 4 must approve
the classification and authenticated coverage of security-critical extensions.

Every field/extension registration must also declare its scope (link-local,
forwarding-immutable, hop-mutable, or transport-local), issuer, repeatability,
preservation/canonicalization, permitted mutation, security coverage, privacy
lifetime/audience, and failure outcome. Identifier, criticality, length, and
value cannot be stripped or rewritten at a scope where they affect behavior.
Cheap pre-authentication structural rejection remains allowed but cannot mutate
authoritative state or produce an oracle/amplifying response.

## Hop-limit semantics (Protocol v0.x TTL)

The proposed baseline uses a bounded unsigned hop limit because it requires no
shared wall clock:

1. an origin emits a forwardable packet with `hopLimit >= 1` and no greater
   than the profile maximum;
2. a receiver may deliver a locally eligible packet with `hopLimit == 1`;
3. a relay may forward only when `hopLimit > 1`;
4. every one-hop forwarded copy carries exactly `hopLimit - 1`;
5. every fanout/multipath copy from the same processing event carries the same
   decremented value;
6. local delivery does not decrement the value;
7. no relay may increase, reset, or replace hop limit by re-encapsulating the
   same packet identity;
8. a non-local packet at `hopLimit == 1` is dropped as
   `LIFETIME_EXHAUSTED`;
9. a relay copy changes only hop limit and transport framing; it preserves the
   envelope format/profile, class/type, origin context, packet identity,
   routing directive, traffic treatment, payload length, extensions, and
   payload exactly under the selected encoding.

Hop limit is excluded from packet duplicate identity because it changes at
every forwarding step. The selected security profile must state how the
received value is admitted, what immutable origin context or initial bound (if
any) is authenticated, how an outgoing decrement is authorized/re-protected,
and which exact fields can change without invalidating origin/content
authentication. One-hop session integrity can show only that the immediate
neighbor sent a value; it cannot prove an admitted malicious relay decremented
honestly. An immutable origin budget plus remaining value and stronger path/
hop attestations are EXP-018 alternatives requiring Agent 1 review if they
change fields. No hash/signature chain or other construction is invented here.

Until a construction is selected, the rule is an honest-node interoperability
requirement plus a syntactic maximum, not a claim that malicious relays cannot
reset, over-decrement, re-originate, or drop traffic.

Hop limit does not express wall-clock age, queue residence, media staleness,
security replay, grant expiry, or stream sequence. Local queues are bounded;
RFC-0008 separately defines realtime freshness. The initial/default hop limit
and maximum remain Agent 3 decisions informed by EXP-003 and EXP-004.

Time-based or combined forwarding lifetime remains a documented alternative,
not a hidden implementation option. An absolute timestamp depends on clock
trust/skew and reveals timing; a decrementing duration needs defined per-hop
residence accounting and mutable-field protection. Agent 3 can replace the
hop-only proposal through RFC review if EXP-003/EXP-004 shows hop count cannot
bound the target operating envelope.

## Packet identity and duplicate suppression

Every forwardable packet MUST contain an origin routing context and packet
identity. Absence of either is `MALFORMED`. The duplicate key is the tuple:

```text
(envelope format, protocol profile, origin routing context, packet identity)
```

The origin assigns the packet identity. All transport retransmissions,
multi-path copies, and relays preserve it. A relay never creates a new identity
for the same forwarding instance. Routing revisions, capability generations,
channel operations, PTT requests/grants, streams, and media sequence numbers
use separate identifiers.

Packet identity generation, width, entropy/counter construction, collision
risk, restart/session rollover, origin binding, and linkability require joint
Agent 3/Agent 4 review. Packet identity alone grants no trust and cannot satisfy
cryptographic replay protection.

Candidate generation strategies remain unselected:

| Candidate | Benefit | Risk/evidence needed |
| --- | --- | --- |
| session-local counter | compact and deterministic | restart reuse and linkability; EXP-005/EXP-016 |
| bounded random value | avoids obvious sequencing | entropy/collision and test determinism; Agent 4/EXP-016 |
| session prefix plus counter | explicit duplicate domain | alias/session correlation and prefix binding; EXP-005/EXP-007/EXP-016 |

An encoding candidate must support the eventual chosen size without excessive
overhead, but EXP-002 cannot choose the security/privacy construction by codec
convenience.

For the proposed first-seen policy, an occurrence admitted under the profile's
outer/session security requirements can become the first committed result under
the processing rules below. Only later occurrences that match committed
duplicate state produce neither local nor forwarding effect, do not refresh
cache retention, and are dropped as `DUPLICATE`, even if they arrive over
another link or carry a higher remaining hop limit. If a reviewed security
profile detects different authenticated immutable content against a committed
key, the later occurrence remains dropped and can produce a local
`PACKET_ID_CONFLICT` diagnostic without a network response. A post-admission
no-effect occurrence that the exact routing profile deliberately does not
commit does not suppress a later occurrence merely by having been observed.

Every exact profile declares a `minimumDuplicateCapacity` conformance floor and
an exact `duplicateRetention` semantic duration covering its maximum expected
packet residence/retransmission window. Each implementation declares a finite
`configuredDuplicateCapacity` at or above the floor. Saturation vectors use the
declared configured capacity; an implementation can sacrifice availability but
cannot retain more keys than it declared. Larger conforming capacities may
improve availability but do not change first-seen behavior or retention.
Numeric values and overload/no-effect interaction remain review items for
RFC-0005, EXP-003, and EXP-016.

Admission does not make an origin benign. Profiles also need finite global and
appropriate per-attachment, session, scoped-origin, and target quotas for
unique packet identities. Rotating an origin context cannot silently reset all
abuse budgets. Any unauthenticated negative cache is separate, bounded, and
cannot suppress an admitted occurrence.

## Processing model

An implementation presents the following ordered semantic stages. Cheap
stateless rejection can precede expensive security work, but untrusted fields
cannot mutate authoritative protocol state.

1. **Transport admission** — enforce one-hop frame size, ingress policy,
   backpressure, and bounded buffering before parsing.
2. **Bounded prefix parse** — recover only enough framing to select the
   envelope format and validate declared lengths without payload allocation.
3. **Format/profile validation** — reject unsupported format/profile and
   impossible, truncated, overflowing, or excessive lengths.
4. **Structural validation** — validate required fields, class/type, extension
   criticality, routing-target kind, traffic treatment, payload length, and hop
   range. No authoritative state changes.
5. **Session, outer, and applicable claim security admission** — obtain
   logically distinct verdicts for the admitted peer session, exact outer
   packet/context, and, for routing-relevant capability or mesh-control input,
   the issuer's authorization and security freshness/replay. A selected profile
   can implement these in one component but cannot conflate their guarantees.
   Immediate-peer authentication does not authorize arbitrary third-party
   route/capability claims. Each verdict binds the exact pair, session, ingress,
   content, issuer scope, and declared mutable fields. Agent 4 owns mechanism,
   coverage, failure behavior, and any pre-admission response. Synthetic
   simulator verdicts are explicitly non-cryptographic and non-production.
6. **Duplicate lookup** — query bounded duplicate state only after every
   admission required for that packet/claim. An unauthenticated or unauthorized
   packet ID cannot poison the authoritative cache.
7. **Independent dispositions** — compute `eligibleForLocalDelivery` and
   `eligibleForForwarding` separately from approved outer metadata, current
   routing state, hop limit, relay capability, and local policy. Both can be
   true. Inner-payload readability is not a relay predicate.
8. **Resource reservation** — reserve bounded duplicate, local-dispatch, and/or
   forwarding work. Failure cannot grow state and yields a local drop reason.
9. **Duplicate insertion** — insert the key before observable local-delivery or
   forwarding side effects. The committed actions form the first-seen result.
10. **Local and/or relay action** — dispatch a locally eligible opaque endpoint
    payload only to the Agent 4-defined channel open/replay boundary; independently
    emit each approved forwarding copy with decremented hop limit and all other
    envelope semantics preserved. A profile-generated control
    update is a new semantic packet with its own packet identity, not a relay
    copy or a way to reset endpoint-data lifetime.
11. **Inner authorization** — only a local endpoint that receives an accepted
    channel-security/replay verdict may decode and authorize a CHANNEL, PTT, or
    AUDIO action and mutate its state.
12. **Bounded observability** — record a safe local reason/metric without
    plaintext payload, secrets, audio, or unnecessary stable identity.

Stages 6 through 10 MUST be serialized atomically for one duplicate key: no
concurrent occurrence can observe or commit an inconsistent first-seen result.
Packets with no local-delivery or forwarding disposition produce no such
effect. Every exact routing profile must define whether duplicate state is
committed for each post-admission no-effect result, including
`LIFETIME_EXHAUSTED`, `POLICY_REJECTED`, `NO_ROUTE`, `RESOURCE_LIMIT`, partial
fanout, and enqueue failure. It must also define which reserved actions form the
atomic first-seen result when only some fanout reservations succeed. These are
explicit Agent 3/Agent 4 and EXP-016 review questions, not implementation
choices.

Stage 5 claim-freshness/replay checks are provisional if they require mutable
authoritative state. Every exact profile must define the claim replay key and
window, the commit point, its atomic relationship to duplicate insertion and
route/capability state transition, and a consumption matrix for every later
duplicate, stale/conflict, no-route, resource, and partial-action outcome.
Unauthenticated input never advances claim state, and an observable accepted
effect cannot later roll it back. This RFC does not select consume-on-
authentication versus consume-on-application for routing/capability claims;
EXP-018 and canonical concurrency/failure vectors must resolve it.

## Layered local outcomes and network errors

Semantic vectors use `(layer, result)` observations rather than one acceptance
flag or implementation error string. Outer success is one of
`OUTER_DISPATCHED_LOCAL`, `OUTER_FORWARDED`, or
`OUTER_DISPATCHED_LOCAL_AND_FORWARDED`; it says nothing about endpoint security
or inner-action acceptance. A later endpoint stage can independently report
`INNER_ACTION_APPLIED`, `IDEMPOTENT_NO_CHANGE`, or a failure category. A
successful session, capability, or routing state transition reports
`STATE_APPLIED` at its corresponding layer.

Stable failure categories are:

`FRAME_TOO_LARGE`, `MALFORMED`, `UNSUPPORTED_ENVELOPE`,
`UNSUPPORTED_PROFILE`, `UNSUPPORTED_OUTER_SEMANTICS`,
`UNSUPPORTED_CRITICAL_EXTENSION`,
`UNSUPPORTED_MESSAGE`, `SECURITY_REJECTED`, `LIFETIME_EXHAUSTED`,
`DUPLICATE`, `PACKET_ID_CONFLICT`, `STALE`, `POLICY_REJECTED`, `NO_ROUTE`,
`RESOURCE_LIMIT`, and `STATE_CONFLICT`.

Layers are `outer`, `session`, `capability`, `routing`, `channel-security`,
`endpoint`, `channel`, `ptt`, `audio`, `wire`, `security`, and `scenario`. Multiple
observations can therefore report successful outer forwarding and a local
`UNSUPPORTED_MESSAGE` at the channel layer without contradiction.
`OUTER_*` success results and `UNSUPPORTED_OUTER_SEMANTICS` are outer-only;
`STATE_APPLIED` is session/capability/routing-only; `INNER_ACTION_APPLIED` is
channel/PTT/audio-only.

The baseline sends no network error for invalid transit traffic, duplicates,
unsupported versions, authentication failures, exhausted lifetime, no route,
or resource pressure. Any future error response requires explicit scope,
authentication, rate/amplification bound, non-recursion rule, and Agent 4
failure-oracle review.

Every exact profile maps rejection at each of the six logical security
dispositions to one stable `(layer, result)`, state-consumption rule, peer-
response rule, and redacted diagnostic category. `SECURITY_REJECTED` denotes a
required authentication, integrity, context, or replay admission failure (or a
profile-pinned generic coalescing needed to avoid an oracle).
`POLICY_REJECTED` denotes an otherwise admitted/authenticated claim or action
declined solely by an explicit authorization or local policy. A profile that
coalesces those cases must say so and cannot expose the distinction elsewhere.

## Security interface and dependencies

The security architecture requires six logically distinct dispositions rather
than one ambiguous "authentication" step:

1. link/session admission and negotiation-transcript binding;
2. outer-envelope admission and integrity/authenticity coverage;
3. routing/capability claim authorization plus security-freshness/replay
   admission before authoritative route/capability mutation;
4. local protected-record authentication/open;
5. security-replay admission and atomic replay-state commit;
6. authorization of the complete decoded channel/PTT/audio action with
   authenticated-principal/action-subject separation.

One selected component may provide multiple verdicts, but none is transferable
across a different pair, session, ingress, content, issuer, or state revision.
Authentication of an immediate peer does not authenticate a claimed multi-hop
origin and does not make a route, metric, or capability truthful.

The encoding experiment must expose exact immutable bytes or normalized
semantic context to the future security profile and identify every mutable
relay field. Every exact profile classifies every outer element as link-local,
forwarding-immutable, hop-mutable, or transport-local and identifies who may
assert/change it, its security coverage, and the attacker covered. The future
endpoint protection or a separate origin proof must bind all immutable outer
semantics whose substitution affects delivery, duplicates, scheduling,
interpretation, or authorization, including the exact pair, class/type, origin,
packet identity, routing directive, traffic treatment, payload length/content,
and applicable extension identifiers/criticality/values. The endpoint provides
an endpoint-visible treatment mismatch verdict. Exact coverage and retry-under-
new-packet-ID behavior require joint Agent 1/4 and EXP-002 review.

This RFC does not add a signature, tag, nonce, key, algorithm ID, channel
selector, epoch, authenticated origin budget, or sender ID merely to complete a
schema.

Duplicate suppression, cryptographic replay rejection, and media/application
staleness remain three independent results in specifications and vectors.

## Privacy and metadata considerations

Envelope format/profile, outer class/type, packet identity, routing origin and
target, hop limit, traffic treatment, length, timing, capability state, and
extension patterns can enable correlation. An opaque payload is not a claim of
anonymity, unlinkability, or metadata privacy.

The initial observer-by-field budget is in
[`relay-security.md`](../security/relay-security.md). EXP-007 must justify every
visible field against colluding relays and assess whether a coarse traffic
treatment is necessary. Origin/target/packet contexts must not be raw stable
credentials and require minimum scope/rotation rules. Channel selector,
member/sender identity, PTT request/grant, stream ID, codec, key epoch, and
inner subtype remain inside the opaque endpoint payload by default.

## Routing considerations

Agent 3 must define target kinds, local-delivery predicates, propagation and
fanout, routing-control types, no-route behavior, retry/queue semantics,
numeric hop and cache bounds, and loops beyond hop limit/duplicate suppression.

Routing consumes only validated outer metadata, admitted capabilities, abstract
link metrics, and local policy. It cannot inspect endpoint payloads or infer a
channel routing domain. Relay service is best effort and current capability is
willingness, not a delivery promise. Fresh media is never queued across a
partition or reconnection.

## Encoding alternatives

| Alternative | Benefits | Costs/risks | Evidence needed |
| --- | --- | --- | --- |
| compact fixed binary header | predictable and efficient | rigid evolution and optional-field pressure | EXP-002 size/version prototype |
| length-delimited TLV envelope | explicit criticality and preservation | parser/canonicalization complexity and overhead | EXP-002 fuzz/overhead prototype |
| established schema encoding | multi-language tooling | dependency, canonicalization, unknown-field variance | EXP-002 license/interoperability study |
| fixed bounded prefix plus extensions | early rejection plus evolution | two-layer complexity and mutable-field coverage | EXP-002 and Agent 4 review |

No encoding is selected. EXP-014 supplies the transport-size/fragmentation
evidence needed for frame and payload maxima.

## Test-vector and interoperability plan

Semantic vectors must cover exact-profile offer/selection/echo and failure,
direct delivery at hop limit 1, forwarding from 2 to 1, fanout decrement, no
increase/reset, first-seen duplicate behavior, concurrent/higher-hop duplicate
arrival, declared-capacity saturation, atomic no-effect/partial-fanout policy,
unknown optional preservation, unknown critical and unknown outer-semantic
rejection, malformed lengths, independent local/forward dispositions,
link-control non-forwarding, no-route, resource failure, traffic-treatment
mismatch, inner-unknown forwarding opacity, unknown inner family/type, and
optional/critical semantic elements after both channel-security gates.

The draft vector format is
[`../../protocol/test-vectors/FORMAT.md`](../../protocol/test-vectors/FORMAT.md).
Exact-byte, truncation-at-every-boundary, canonicalization, and parser fuzz
vectors follow only after EXP-002 selects an encoding. Security vectors wait
for Agent 4 and use public synthetic fixtures only.

## Migration and rollout

The v0.x proposal becomes an exact experimental compatibility selection only
when both its envelope-format and protocol-profile identifiers, numeric limits,
and vector-set pin exist. A change that alters either format bytes/parsing or
profile field requirements, processing order, failure disposition, hop/
duplicate rule, extension criticality, or catalog value uses a new applicable
identifier and pair/vector-set pin. Released vectors are never rewritten.

## Open questions

- Which target kinds and propagation semantics does the first routing profile
  require? Owner: Agent 3; EXP-003.
- What are the hop-limit maximum, `minimumDuplicateCapacity`, configured-capacity
  declaration rules, and `duplicateRetention` values? Owner: Agent 3;
  EXP-003/EXP-004/EXP-016.
- How are packet identity and origin routing context generated, bound, rotated,
  and protected from tracking/cache poisoning? Owner: Agent 4 + Agent 3;
  EXP-005/EXP-007/EXP-016.
- Which outer fields and mutable hop state receive which security coverage?
  Owner: Agent 4; SG-004 after EXP-002.
- Is any visible traffic treatment worth its metadata cost? Owner: Agent 3 +
  Agent 4; EXP-007.
- What is the deterministic post-admission no-effect, partial-fanout, and
  cache-saturation policy? Owner: Agent 3 with Agent 1/4 review;
  EXP-003/EXP-016.

## Review requirements

- [x] Agent 1 logical field, version, extension, TTL, duplicate, failure, and
  processing review recorded in this revision.
- [ ] Agent 1 exact-byte/encoding review after EXP-002.
- [ ] Agent 3 target, hop, duplicate-bound, fanout, and no-route review.
- [x] Agent 4 initial metadata, admission-layer, field-coverage, mutable-hop,
  downgrade, claim-authentication, replay-boundary, and cache-poisoning review.
- [ ] Agent 4 construction/profile selection and SG-004 closure after evidence.
- [ ] EXP-002 cross-language corpus/fuzz results and EXP-014 size evidence.
- [ ] Canonical negative corpus reviewed.

## Acceptance blockers

- routing target kinds, propagation, and numeric bounds are unresolved;
- identity/session construction, outer/control origin integrity, replay
  construction, and mutable-field protection are unresolved;
- EXP-002 has not selected an encoding or proved extension preservation;
- an initial metadata inventory exists, but EXP-007 measurements, approved
  privacy budget, and mitigations are absent;
- EXP-016 adversarial duplicate/cache-poisoning evidence does not exist;
- the initial threat model exists but SG-001/004 remain open;
- EXP-017/018/019 security evidence does not exist.

## Decision record

- 2026-09-01: Agent 1 revision proposed a logical envelope, exact pre-v1
  profiles, hop-limit TTL, first-seen duplicate handling, critical extensions,
  ordered security/routing boundaries, and local failure categories. RFC
  remains Draft pending Routing, Security, and encoding evidence.
- 2026-09-02: Agent 4 required complete negotiation binding, distinct route-
  claim admission, per-field security scope, malicious-peer duplicate quotas,
  explicit mutable-hop limits, and a relay metadata budget. No security
  construction or new field was selected; RFC remains Draft.

## References

- [`RFC-0001`](RFC-0001-samband-network-model.md)
- [`RFC-0002`](RFC-0002-node-identity.md)
- [`RFC-0005`](RFC-0005-mesh-routing.md)
- [`RFC-0006`](RFC-0006-encrypted-channel-payload.md)
- [`shared-contracts.md`](../architecture/shared-contracts.md)
- [`review-gates.md`](../security/review-gates.md)
- [`relay-security.md`](../security/relay-security.md)
- [`node-identity.md`](../security/node-identity.md)
- [`experiment-backlog.md`](../research/experiment-backlog.md)
