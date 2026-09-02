---
rfc: "0005"
title: Mesh Routing
status: Draft
authors:
  - Samband contributors
created: 2026-09-01
updated: 2026-09-02
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

This Draft RFC proposes the algorithm-independent protocol contract that every
experimental Samband routing profile must satisfy. It constrains routing inputs,
targets, dispositions, control messages, relay capability, lifetime, duplicate
interaction, partitions, resource bounds, and observability without selecting
distance-vector, link-state, on-demand, controlled dissemination, or a hybrid.

## Status and authority

Draft and non-normative. Agent 3 leads candidate evaluation and proposes a
routing profile; selection and acceptance still require the Protocol, Security,
and maintainer reviews defined by project governance. Agent 1 owns the peer-
visible message, envelope, version, and processing contract. Agent 4 owns
admission, route-control authentication, poisoning, metadata, identity binding,
and abuse review.

This revision combines Agent 1's routing-facing boundary, Agent 4's initial
security requirements, and Agent 3's Wave 0 assumptions, candidate metadata,
and experiment plan. It is not a routing algorithm, an experimental profile,
an authorization to implement one, or evidence that numeric bounds pass.

## Motivation

Samband must operate across appearance/disappearance, alternate paths,
partitions, merge, unstable links, and dynamic relay willingness. An envelope
cannot be coherent until routing states exactly what metadata it consumes and
what local-delivery/forwarding decisions it returns. Conversely, Agent 1 must
not choose target kinds or control messages merely to complete a schema.

## Goals

- deliver through willing relays without channel membership or plaintext;
- define one protocol boundary shared by routing candidates;
- make target, local-delivery, forwarding, lifetime, duplicate, and failure
  behavior testable;
- converge within bounded state/work after topology and capability changes;
- keep raw device/resource state local unless evidence justifies disclosure;
- support partitions without central authority or past-media replay;
- expose safe reason categories and deterministic simulator events.

## Non-goals

- select a concrete routing family, metric formula, tie-breaker, or target kind;
- route generic IP traffic;
- expose plaintext channels as routing domains;
- guarantee delivery or retransmission of stale realtime media;
- select identity, signatures, authentication, trust, or anti-poisoning
  mechanisms;
- claim global topology knowledge or consensus.

## Wave 0 operating assumptions

The following assumptions constrain candidate evaluation without selecting a
profile:

- the current mesh is a time-varying directed multigraph, not a stable or
  necessarily symmetric LAN;
- a node can have several transport attachments and several peer links on one
  attachment; receipt from a peer does not prove usable reverse reachability;
- mobility is relevant through contact duration, link degradation, node
  appearance/disappearance, and neighbor churn rather than a device-speed
  label;
- partitions and merge are routine, and no global clock, location service,
  route authority, or continuously reachable coordinator exists;
- traffic is sparse control plus bursty, deadline-bound endpoint traffic, but
  recipient count and locality are not yet known;
- relay willingness changes with policy and resources; a current capability is
  neither permanent availability nor a delivery promise;
- admitted peers can lie, rush, replay, selectively forward, blackhole, form
  Sybils, or collude through a wormhole;
- all routing state, control, fanout, queues, retries, verification, timer
  wakeups, and work per event are finite.

EXP-004 must establish the initial node, density, directed-link, contact,
churn, loss, latency, path, traffic, recipient, and relay-resource envelope.
Values in simulator fixtures are not Protocol v0.x limits. The detailed
sensitivity matrix is in
[`routing-candidate-evaluation.md`](../research/routing-candidate-evaluation.md).

## Routing profile boundary

Every exact Protocol v0.x routing profile must publish all rows below. A
profile that leaves a row implementation-defined is not interoperable.

| Contract area | Required profile definition |
| --- | --- |
| operating envelope | supported node/path/density/directed-link/contact/churn/loss/traffic/recipient assumptions and numeric state/traffic bounds |
| target kinds | syntax/equality, scope/stability, local-delivery predicate, propagation, fanout, no-route behavior, delivery termination, privacy, and security binding |
| control family | exact creation, propagation, replacement, withdrawal or expiry messages/events applicable to the chosen algorithm |
| attachment/session/link model | distinct local attachment, admitted peer session, directional peer-link state, unicast/shared-medium action, and asymmetric-link behavior |
| neighbor/reachability state | admission, origin/incarnation, generation/revision, freshness, expiry, replacement, restart/rollback, and maximum retained state |
| relay capability | snapshot input, withdrawal/expiry, local policy, dampening, and effect on eligibility |
| metrics | local observations versus advertised values, quantization, composition, tie-break, invalid values, and trust limit |
| packet dispositions | independent local-delivery/forwarding predicates and deterministic drop reasons |
| lifetime/duplicates | hop-limit maximum/default, first-seen interaction, cache bounds, loop behavior, and fanout decrement |
| queues/retries | per-class bounds, no-route discovery, enqueue failure, backpressure, replacement, and media deadline/non-retention |
| partitions/merge | local operation, stale-state expiry, reconvergence goal, and prohibited replay |
| observability | bounded semantic events/reasons needed for conformance without protected payloads or secrets |

EXP-003 and EXP-004 must supply evidence for the initial values. The first
profile should be the simplest candidate that satisfies the measured Samband
operating envelope.

## Inputs routing may consume

Routing can consume only:

- an RFC-0004 outer packet that passed the profile's structural and required
  session/outer-security admission stages;
- distinct ingress attachment, admitted immediate-peer session, and directional
  peer-link lifecycle events;
- RFC-0001 capability snapshots, including explicit expiry/withdrawal;
- abstract monotonic time and seeded randomness where the profile requires it;
- local directional send/receive measurements, shared-medium/unicast action
  capability, and local relay/resource policy;
- profile-approved routing-control bodies.

In this RFC, a **directional peer link** is current local one-hop
reachability/action state bound to one admitted immediate-peer session and one
transport attachment. It is not a peer identity, a transferable session
verdict, or proof of a reverse link.

Routing cannot consume channel plaintext, membership, channel labels, PTT
authenticated principals, action subjects, stream IDs, codecs, keys, secrets,
mobile platform types, or concrete
transport API objects. Failure to open/understand an opaque endpoint payload is
not a relay-routing input.

Peer-session authentication proves the admitted exchange and assurance defined
by its security profile; it does not prove that later send capacity, loss,
latency, or reachability is symmetric. A remote assertion cannot create a local
adjacency or reverse link. Any profile that requires a reply or reverse route
must discover or validate that directed path independently rather than merely
reverse the ingress path.

Locally observed link measurements, immediate-peer assertions, and transit-
derived/origin assertions remain distinct provenance classes. Remote input
cannot overwrite or masquerade as a local observation. Every metric is range-
checked before mutation with bounded arithmetic and explicit invalid-value
behavior. Any authenticated issuer/provenance context passed to routing is
opaque, bounded, and no more stable than its reviewed scope.

Raw battery, charging, thermal, data-plan, OS lifecycle, and transport details
remain local policy inputs. A profile may expose only the coarsest derived
capability or metric demonstrated necessary by EXP-003/EXP-007. A capability
claim is willingness/current availability, not identity, authorization, route
truth, or a delivery promise.

The minimum shared resource signal is a session-scoped relay-willingness
capability with generation, bounded validity, and withdrawal. Local battery-
aware behavior can withdraw immediately or add a local resource penalty before
advertising/choosing a route through self. An optional coarse, quantized,
short-lived relay cost class is permitted for experiment only if a boolean
willingness signal fails a measured requirement; it never proves the claimed
resource state. Re-enablement can be damped or hysteretic to avoid route
flapping, but a safety-driven local withdrawal cannot be delayed merely to
reduce control chatter.

## Routing output contract

After common RFC-0004 validation, routing returns two independent decisions:

```text
eligibleForLocalDelivery
eligibleForForwarding -> bounded set of local egress actions
```

Both can be true. A combined endpoint/relay can forward an opaque payload even
when it cannot open, authorize, or consume it locally. Local delivery does not
automatically terminate dissemination; each target kind states that rule.

Next hops, directional peer links, and transport attachments are local results,
not outer fields. The routing contract needs to represent either an admitted
peer-session/link plus its attachment or one profile-defined shared-medium
emission. One physical or logical attachment can serve several neighbors, so a
realistic candidate must distinguish the exact ingress peer link from the
attachment that carried it.

Wave 0 reconciliation makes this a peer-link-aware Draft protocol boundary,
not an attachment-wide prohibition and not a routing-algorithm selection. For
each forwarding action:

- a peer-specific unicast action MUST NOT send the copy immediately back to the
  exact ingress directional peer link;
- an exact candidate profile MAY select a different admitted peer link on the
  same attachment when the transport service can address that peer separately;
- eligibility of another link or session to the same logical peer remains an
  exact profile decision; and
- an exact candidate profile MAY select a shared-medium emission on the ingress
  attachment, but it cannot assume that the ingress peer is excluded from the
  listener set.

Every profile that permits same-attachment or shared-medium forwarding must
define the action representation, listener and reception model, fanout and
work accounting, duplicate effects, resource reservation, and loop controls.
It must distinguish one physical emission from its zero or more resulting
receptions rather than silently charging or suppressing either. Every
forwarding action preserves all RFC-0004 immutable envelope semantics and
applies only the required hop-limit decrement. Further loop prevention belongs
to the selected profile.

A result must be bounded by the profile's maximum fanout and queues. `NO_ROUTE`,
`POLICY_REJECTED`, `LIFETIME_EXHAUSTED`, `DUPLICATE`, `STALE`, and
`RESOURCE_LIMIT` are local dispositions, not automatic network errors.

## Routing target requirements

The common envelope reserves a routing directive but chooses no target kind.
Agent 3 must compare destination-oriented, dissemination-oriented, and mixed
profiles through EXP-003.

Every selected target kind must state:

- whether the origin, target, or both require correlation across sessions;
- how a node determines local eligibility without opening channel payloads;
- whether the target is exact, anycast-like, bounded dissemination, or another
  reviewed semantic;
- whether local delivery also permits forwarding;
- maximum fanout and propagation scope;
- behavior when no route/current recipient is known;
- lifetime and retry interaction;
- security binding and residual forgery/poisoning behavior;
- metadata/linkability cost.

It must also state the exposure audience, correlation scope, rotation/expiry
event, cross-session equality rule, and minimum stability routing actually
needs. Equal-looking identifiers in different sessions/profiles are not linked
without an Agent 4-approved authenticated binding. Authentication, opacity, and
encrypted endpoint content imply neither anonymity nor unlinkability.

A human channel label, channel credential, or plaintext channel identifier is
not admitted as a target merely for convenience. Origin routing context is not
a source route or automatically a stable node identity.

A destination-oriented candidate requires an opaque recipient routing context
with an exact ownership/admission and local-delivery predicate. It must be
stable long enough for the candidate's advertisement/discovery/use window but
must define bounded rotation, overlap, expiry, takeover, and stale-partition
behavior. It is distinct from a discovery handle, raw credential, channel
principal, and action subject.

If one logical endpoint operation is encoded into separate packets for several
recipient targets, every target uses a distinct forwarding/protected-record
instance and packet identity under the current Draft. Reusing one
`(originRoutingContext, packetIdentity)` while changing the immutable target
would create a packet-ID conflict because target is outside the duplicate key.
A bounded dissemination target can instead represent one forwarding instance,
but its observer audience, fanout, duplicate cost, and local-delivery rule must
be measured.

Sharing one `originRoutingContext` across per-recipient copies exposes common-
origin fanout; per-recipient contexts complicate duplicate scoping and abuse-
quota continuity. EXP-007/EXP-016 must measure timing/length correlation,
visible recipient-set cardinality, and linkage even when packet identities and
protected records differ.

## Routing-control message boundary

`MESH_CONTROL` is the routing-visible outer family. The logical names
`ROUTE_ADVERTISEMENT` and `ROUTE_WITHDRAWAL` remain catalog candidates, not a
requirement that every algorithm use distance-vector-like messages.

The selected profile must define the exact reachability-control events it needs,
which can include advertisement, withdrawal, discovery, reply, probe, summary,
or expiration. Each type must define scope, idempotence, generation/revision,
replacement, expiry, rate/fanout, unknown-field behavior, and security/admission
requirements.

For every control assertion, the profile must state whether authority comes
from the immediate admitted peer, a separately authenticated control origin, a
locally derived transition, or an explicit combination. An authenticated
advertiser can replace or withdraw only its own route-view claim slot, including
its own claim about a third-party target. It cannot thereby replace another
issuer's claim, withdraw the target globally, or prove ownership of the target.
Issuer, advertised target/scope, revision/generation, validity, metrics,
capability assertions, unknown optional content, and criticality are bound
under the selected claim-security context and pass security freshness/replay
admission before state mutation.

The profile distinguishes forwarding an unchanged control instance from
originating a derived control update after a state transition. A forwarded
instance preserves packet identity and follows RFC-0004 hop rules. A derived
update has a new packet identity and explicit route/control revision semantics;
it cannot re-identify endpoint data or reset that data's hop limit.

An unknown routing-control type or unsupported routing profile fails closed and
is not forwarded. A route-control heartbeat cannot silently refresh unrelated
capability or reachability state.

A direct session-scoped capability snapshot is bound to that session's exact
pair, generation, validity, and complete canonical content. It is not an
authenticated remote route. Any propagated consequence is a distinct routing-
control assertion with its own identity, authority, freshness, and admission;
it cannot restart or extend the direct snapshot's original validity.

When claim admission maintains security replay/freshness state, the exact
profile pins its key/window, provisional check, authoritative commit, atomic
relationship to duplicate and routing/capability state, and consumption for
every later semantic/resource/no-effect outcome. Unauthenticated claims never
advance it, and accepted observable effects cannot be followed by replay-state
rollback. The policy remains an EXP-018 decision rather than a hidden routing
implementation choice.

## Route freshness and restart

Peer-session liveness, capability validity, routing-control freshness, route
usability, packet hop limit, duplicate retention, security replay, PTT lease,
and media freshness are independent domains. No profile can reuse one value or
expiry event as another without an explicit reviewed rule.

Every propagated route/topology claim must identify its claim issuer and
claimed subject/scope separately, such as a destination target or bounded
topology fact, and define:

- the first accepted incarnation/revision and its finite representation;
- comparison, exhaustion, restart, rollback, and new-incarnation behavior;
- same-revision/changed-content conflict and identical-retry behavior;
- receipt-relative validity and expiry without sender wall-clock trust;
- bounded high-water/tombstone retention and deterministic saturation;
- authority for replacement and withdrawal after partition/merge.

An identical claim retry does not extend validity. Losing revision state at
restart cannot silently reset a persistent issuer's counter; a selected profile
must bind claims to a fresh scoped incarnation/session or use reviewed rollback-
safe state. Authentication identifies authorship of conflicting partition
claims but does not choose a globally current branch.

Receipt-relative validity limits local retention after first admission but
does not prove the claim's age. A malicious relay can delay a never-before-seen
claim and cause a receiver to start its full window later. Forwarding an
unchanged claim cannot increase its remaining validity, and an identical
revision cannot reset first-acceptance expiry. If bounded high-water or
tombstone state is evicted, a receiver cannot claim that it will recognize and
reject the same issuer/incarnation forever after discarding every recognition
record. Each exact profile must instead choose and bound one explicit policy:

- retain issuer/incarnation admission or quarantine state for a declared
  finite horizon, with deterministic saturation and eviction behavior;
- require a fresh authenticated incarnation or, for an immediately owned
  session-scoped claim, a fresh admitted session under a rule an old claim
  cannot satisfy; or
- admit the possibility of stale resurrection after eviction and measure its
  window, influence, and recovery as residual risk.

A new session can reset only a claim explicitly owned by and scoped to that
immediate peer session. A multi-hop claim requires a newly authenticated
incarnation of its original claim issuer; reconnecting an ingress peer cannot
reset third-party freshness state. No profile may claim permanent stale
rejection after all state capable of recognizing the old incarnation has been
evicted.

If a candidate uses destination-owned sequence/freshness separately from an
advertiser's own claim revision, it defines who may originate, advance, copy,
reset, and exhaust that value. Authentication of an advertiser does not let it
mint a higher target-owned freshness value.

The immediate-peer session verdict never transfers to a different ingress or
session. A separately origin-authenticated multi-hop claim may remain current
only under its own exact scope and freshness and must pass claim admission on
every ingress.

## Hop limit, duplicates, and loops

RFC-0004 proposes a common hop-limit TTL and first-seen duplicate policy:

- origin values are `1..profileMaximum`;
- local delivery is possible at 1; forwarding requires greater than 1;
- every forwarded copy carries exactly one less;
- packet identity is preserved and excludes mutable hop limit;
- later copies of an admitted duplicate key do not create delivery/forwarding
  effects or refresh retention.

Agent 3 must evaluate the delivery tradeoff of first-seen suppression when a
later copy has a greater hop limit or better path. The profile defines an exact
`duplicateRetention`, a `minimumDuplicateCapacity` conformance floor, and the
saturation/no-effect rules. Each implementation declares a finite
`configuredDuplicateCapacity` at or above the floor, and vectors parameterize
that declared capacity. The profile must define duplicate insertion for
`LIFETIME_EXHAUSTED`, `POLICY_REJECTED`, `NO_ROUTE`, `RESOURCE_LIMIT`, partial
fanout/enqueue failure, and transport retry. The lookup/reservation/insertion/
action sequence is atomic per duplicate key. Resource safety always bounds
state/work; packet duplicate suppression is not cryptographic replay
protection.

This is also an adversarial race. An admitted relay can rush a low-hop or
otherwise non-viable copy so it commits first and suppresses a later viable
copy. In particular, committing duplicate state for a non-local
`hopLimit == 1`, `NO_ROUTE`, or resource-failed occurrence can turn first-seen
ordering into a targeted denial of service. EXP-016 must compare the exact no-
effect insertion alternatives and their resource costs; this RFC does not
select one.

A finite duplicate-retention window plus hop count does not establish a
temporal network lifetime. A malicious relay can retain a packet and emit it
after duplicate eviction. Endpoint security replay can reject a repeated inner
effect, but transit parsing, authentication, bandwidth, and battery work still
need per-scope quotas unless a separate privacy-reviewed freshness mechanism is
selected.

An expanding-search reactive retry needs either a stable logical discovery ID
plus a strictly advancing integrity-bound attempt revision and search bound, or
a new route-request attempt ID linked to that logical discovery. It also uses a
new outer packet identity. Only the authorized request origin can widen the
bound; an intermediate relay cannot. Packet- and request-level duplicate/replay
state must admit a valid wider attempt without accepting an old or unauthorized
one.

All outer and applicable routing-claim security admissions precede
authoritative duplicate lookup/insertion. An unauthenticated negative cache is
separate and cannot suppress admitted traffic. Global and appropriate per-
attachment, session, scoped-origin, and target limits bound unique-ID floods;
origin rotation cannot silently reset every abuse quota.

Hop limit and duplicates provide safety bounds but do not prove loop-free route
state or convergence. The selected algorithm must address count-to-infinity,
oscillation, persistent loops, stale state, and control storms independently.

## Control and realtime traffic

Routing can apply a coarse protocol-approved traffic treatment. It cannot use
that value as authorization, identity, or proof of content.

Bounded control retransmission/replacement is allowed only when the selected
message semantics define it. Fresh realtime media is best effort: it is not
queued across a partition/reconnection and is not retransmitted after its
profile freshness limit. Routing cannot repair a partition by storing endpoint
media. Queue residence and media staleness remain separate from hop limit.

The selected profile must prevent control starvation by media and bound both
classes under load. Whether a visible traffic distinction is necessary remains
subject to EXP-007 and Agent 4 metadata review.

## Partitions, merge, and relay withdrawal

Each connected component continues with only current local state and peers.
When a node's local relay policy withdraws willingness, it immediately stops
accepting new transit work; already queued work follows the explicit bounded
queue policy. A direct neighbor applies withdrawal or expiry of that relay's
admitted capability snapshot to its local eligibility view. Any remote
reachability consequence propagates or expires only through the selected
routing profile's bounded control semantics; no network-wide instantaneous
withdrawal is assumed.

On merge, the routing profile reconverges through normal bounded control
semantics. It does not replay old endpoint media, reconstruct missed
conversations, or assume a globally ordered history. Alternate-path selection,
replacement, and convergence targets require EXP-003 evidence.

An old peer-session verdict and its direct capability state never transfer to a
new session. An independently authenticated multi-hop control claim can remain
valid only under its own explicit scope and freshness and must be re-admitted on
the new ingress. Expiry, generation/revision, semantic staleness, packet
duplicate, and cryptographic replay are distinct. A delayed authenticated
assertion cannot resurrect withdrawn/superseded state unless the exact
profile's conflict rule permits it. Authentication proves authorship of
conflicting partition claims; it cannot choose the winning branch, create
global order, or provide immediate revocation.

## Failure and resource bounds

Profiles set finite global and appropriate per-attachment, session,
asserted-origin, target, and control-class maxima for parsing/authentication
attempts, neighbors, targets/routes/reachability entries, control origins,
revisions/history, capabilities, duplicate keys, pending verification work,
queues, retries, fanout, packet/control rate, and work per event. Invalid or
over-limit control input cannot evict unrelated admitted state without a
profile-defined deterministic policy or cause recursive error traffic.

At saturation, a node can sacrifice availability but not exceed its state,
memory, CPU, bandwidth, battery, or queue bounds. Deterministic vectors assert
high-water marks and emitted-packet limits, not implementation-specific memory
layouts.

## Privacy and security considerations

Agent 4's initial requirements for peer versus control-origin admission,
routing-control authenticity/integrity, target privacy, negotiation downgrade,
metric provenance, Sybil/resource abuse, poisoning, blackhole/selective
forwarding, wormhole, capability spoofing, and observable failure behavior are
in [`relay-security.md`](../security/relay-security.md). Construction and
evidence review remain open.

Cryptographic authentication cannot make a claimed route or metric truthful and
cannot force a relay to forward. This RFC selects no credential, signature,
trust model, route proof, or stable identifier. Security-sensitive packets do
not update authoritative route/capability/duplicate state before the profile's
required admission verdict.

Only an admitted local transport/session event can create a one-hop adjacency;
a remote assertion cannot manufacture one. Authenticated colluding peers can
still tunnel traffic and create a wormhole. Hop limit counts Samband forwarding
events, not physical distance. No location, distance-bounding, trusted-hardware,
or path-proof assumption exists.

EXP-007 must budget origin, target, control type, packet identity, hop limit,
traffic treatment, capability, length, and timing metadata. An opaque endpoint
payload is not an anonymity or traffic-analysis claim.

Security admission and routing state must keep the immediate-peer principal,
outer origin routing context, route-claim issuer, advertised target, locally
eligible delivery subject, channel principal/action subject, and local-only
abuse-quota scope distinct. Equal bytes do not imply an identity or authority
binding across those contexts.

Quota continuity across identifier rotation exists only through an
authenticated, Security-reviewed local binding. Unverified encounters and new
Sybils rely on attachment, session, and global limits. Timing, target equality,
radio identifiers, or profile fingerprints cannot establish continuity.

Remote metric values are range-limited, provenance-labelled, and given only
profile-defined influence. Locally measured, immediate-peer self-asserted,
transit-aggregated, and separately origin-authenticated values cannot
masquerade as one another. Stable-identifier tie-breakers create tracking and
Sybil-grinding risk; rotating identifiers can instead create oscillation. The
selected tie-break inputs require explicit Security review.

## Alternatives to evaluate

| Alternative | Minimum candidate-specific peer metadata | Benefits | Costs/risks and discriminating evidence |
| --- | --- | --- | --- |
| classic controlled flooding | propagation scope plus common packet ID/origin/hop/target fields | no route acquisition or route advertisements; robust baseline for tiny dynamic components | observer audience, transmissions, and duplicate pressure; sweep density, burst loss, and recipients |
| reduced flooding or gossip | suppression parameters fixed by profile; for relay sets, bounded neighbor/two-hop or selector state, willingness, revision, and validity | can retain dissemination behavior with fewer transmissions | probabilistic delivery tails or extra topology state and selector manipulation; compare saved work with deadline misses |
| proactive loop-avoiding distance vector | opaque target, semantic claim-issuer context/incarnation/revision, bounded aggregate metric, validity, withdrawal/unreachable indication, and any separately authorized destination freshness | compact next-hop state and immediate forwarding after convergence | stale good news, sequence/metric poisoning, chatter, target correlation, and count-to-infinity; sweep churn and idle cost |
| proactive link state | scoped topology origin/incarnation/revision, validity, bounded directed adjacency/metric tuples, withdrawal, and optional relay-selector state | richer alternate-path calculation and immediate routes after synchronization | largest topology/state disclosure and churn/recomputation storms; test whether delivery gain pays the overhead/privacy cost |
| reactive/on-demand | logical discovery and attempt/revision IDs, scoped origin/target, integrity-bound search bound, any separately authorized destination freshness, bounded metric, reply correlation/authority, validity, and route error | little idle route state when communicating pairs are sparse | cold-route latency, target exposure, request/reverse-state floods, forged fast replies, and asymmetric return paths |
| hybrid | bounded union of selected components plus exact mode/zone boundary and transition semantics | can serve distinct measured regimes | combines metadata, state, downgrade surface, and failures; evaluate only after a simpler family misses an explicit threshold |

No algorithm or target model is selected.

Security must supply the semantic claim-issuer context. A wire-visible issuer
identifier is required only where a claim crosses or outlives the immediate
session; the profile avoids duplicating session identity, control origin, and
`originRoutingContext` merely for convenience.

## Future distribution and gateway compatibility

A future multicast/distribution-tree target is not a plaintext channel ID and
cannot make foreign relays channel members. It requires a separate RFC covering
an opaque distribution context; admitted routing claims with separate issuer
and branch/subscription subject; join/prune or branch freshness and replay;
bounded branch fanout; loop-free repair; partition split and merge; target
collision/takeover; malicious branch blackholes; and metadata leakage from
group correlation, joins, roots, and stable branches. A non-member foreign
relay may maintain a ciphertext-forwarding branch without becoming an endpoint
subscriber, locally eligible recipient, or channel member. Per-recipient
copies, bounded dissemination, source trees, and shared trees remain
alternatives. Missed media is never retained for a tree repair.

A future Internet gateway remains an explicit dynamic transport/relay
capability. It is not a central authority, channel endpoint, decryption point,
or generic IP proxy. A future RFC must preserve exact-profile processing,
packet identity, immutable target/context, endpoint protection, and forwarding
lifetime across the bridge; count the gateway forwarding event; keep Internet
endpoint addresses transport-local by default; require a named field,
audience, scope/rotation, integrity rule, and EXP-007 justification for any
outer/multi-hop address exposure; require opt-in data policy; bind gateway
capability/reachability advertisements to issuer, freshness, expiry,
withdrawal, and sinkhole-influence limits; and bound gateway loops,
connections, queues, fanout, and amplification. An Internet shortcut can be a
deliberate topology wormhole, so gateway identity or low latency cannot
establish physical proximity.

## Simulator evaluation plan

Candidate families are instantiated as exact preregistered experimental
profiles with pinned messages, parameters, timers, metrics, bounds, and
tie-breaks. EXP-004 fixes the operating envelope and hard thresholds before the
result-bearing comparison. Candidates receive the same finite tuning budget on
development traces, freeze parameters, and run on paired held-out immutable
exogenous traces with separate named random streams.

The profiles compare delivery before deadline; acquisition, convergence,
alternate recovery, withdrawal propagation, and merge quiescence; path stretch/
stability; control and forwarding packets, bytes, wakeups, and peak bursts;
duplicate/loop/TTL behavior; bounded state and work high-water marks; relay-
load/resource proxies; adversarial degradation; and relay-visible metadata.
Target model is a separate factorial dimension, not silently coupled to a
routing family. The experimental unicast/shared-medium service and provisional
byte/work accounting are pinned and reported.

Scenarios include chains, rings, diamonds, sparse grids, dense graphs,
multi-attachment nodes, directed/asymmetric links, mobility/contact traces,
bridge partitions and merge, target rotation, recipient fanout, no-route
recovery, relay withdrawal/flapping, lossy versus reliable alternate paths,
first-seen low-hop races, every configured `N+1` saturation, stale/dishonest
claims, blackhole/selective forwarding, Sybil rotation, colluding wormholes,
and malformed control. EXP-018 applies adversarial cases to every candidate
without treating authentication as proof of truth, distance, or forwarding.

The complete candidate-distinguishing scenarios, sensitivity points, metrics,
and decision procedure are in
[`routing-candidate-evaluation.md`](../research/routing-candidate-evaluation.md).
EXP-004 supplies the supported node, density, directed-link, contact, churn,
loss, latency, path, traffic, recipient, and resource-timescale assumptions.
Simulator evidence cannot establish physical energy, radio, lifecycle, or
security properties.

## Test-vector and interoperability plan

Semantic vectors must define ordered inputs and expected dispositions without
map iteration order or wall-clock sleeps. Required cases include direct
delivery at hop 1, forward 2-to-1, combined local/forward, the current Draft
peer-link-aware rule that peer-unicast never bounces to the exact ingress
directional link, a different peer on the same attachment, profile-defined
handling of another link/session to the same logical peer, and a shared-medium
emission whose listener, fanout, work, duplicate, reservation, and loop effects
are explicit. They also include bounded fanout, no-route, duplicate paths,
capability withdrawal,
partition/merge without media replay, stale revisions, invalid metrics,
unsupported routing profile/type, and every state/cache/queue limit.

The specification and vector format must represent explicit ingress/egress
directional peer-link and shared-medium action vocabulary before these cases
are executable. RFC-0005 defines the reconciled logical requirement but cannot
independently change the vector carrier or select a transport service model.

Scenario vectors follow the draft format in
[`../../protocol/test-vectors/FORMAT.md`](../../protocol/test-vectors/FORMAT.md).
Routing/security vectors cannot be promoted from Draft until the profile and
review hooks are selected.

## Migration and rollout

Each v0.x compatibility pair pins one exact routing profile with its own
message catalog, target kinds, bounds, and vector coverage. Ordinary relays do
not reinterpret packets under another protocol profile or transcode them to a
different envelope format. Same-format hop-limit reserialization is permitted.
Changing peer-visible propagation, metrics, disposition, lifetime, duplicate,
or control semantics creates a new protocol-profile identifier and
pair/vector-set pin.

## Open questions

- Which network sizes, densities, directed-link fractions, contact durations,
  churn, loss, path lengths, traffic locality, recipient counts, and relay-
  resource timescales define the initial operating envelope? Owner: Architect +
  Agent 3; EXP-004.
- Is the first target destination-oriented, bounded dissemination, or mixed?
  Owner: Agent 3; EXP-003.
- What scoped recipient-target and origin contexts survive the required routing
  lifetime without becoming stable public identities, and is a distinct origin
  context mandatory for every candidate? Owner: Agent 3 + Agent 4;
  EXP-005/EXP-007/EXP-016.
- Which control messages and route state does the simplest passing candidate
  need? Owner: Agent 3; EXP-003.
- Which metrics are local, safe to expose, stable, and composable? Owner: Agent
  3 + Agent 4; EXP-003/EXP-007.
- Can battery-aware behavior remain entirely local plus boolean willingness, or
  is a coarse derived cost class necessary? Owner: Agent 3 + Agent 4;
  EXP-003/EXP-007/EXP-012.
- Which directed-link, peer-unicast, and shared-medium action semantics are
  required by candidate transports? Owner: Agent 3 + Platforms; EXP-003/EXP-004.
- What numeric hop, duplicate, neighbor/route, queue, fanout, and retry bounds
  pass the operating envelope? Owner: Agent 3; EXP-003/EXP-004.
- How do profile identity, routing origin/target, and discovery privacy coexist?
  Owner: Agent 3 + Agent 4; EXP-005.
- What exact first-seen/no-route/cache/partial-fanout policy is acceptable?
  Owner: Agent 3 with Agent 1/4 review; EXP-003 and EXP-016.
- Which restart/incarnation and claim-freshness rules avoid rollback and stale
  resurrection without unbounded tombstones? Owner: Agent 3 + Agent 4;
  EXP-003/EXP-018.
- Do future one-to-many needs justify per-recipient copies, bounded
  dissemination, or a separate distribution-tree RFC, and what gateway
  extension boundary remains compatible? Owner: Agent 3 + Agent 1 + Agent 4;
  later RFC after EXP-003/EXP-007.

## Review requirements

- [x] Agent 3 Wave 0 operating-assumption, candidate-family, minimum-metadata,
  protocol/security requirement, and simulator-plan review recorded.
- [ ] Agent 3 routing-profile proposal and numeric bounds after EXP-003/EXP-004
  evidence.
- [x] Agent 1's 2026-09-01 routing-facing envelope, processing, message,
  version, and vector-boundary review recorded.
- [x] Wave 0 integration reconciliation of the directional peer-link/shared-
  medium action model recorded without selecting a routing algorithm.
- [ ] Agent 1 realization review of the reconciled action model in the Draft
  specification, vector format, and first exact experimental profile.
- [x] Agent 4 initial poisoning, identity/admission, metric provenance,
  malicious-relay, metadata, Sybil, partition, and DoS requirements recorded.
- [ ] Agent 4 review of the selected routing profile and SG-005 closure.
- [ ] RFC-0001 capability and RFC-0004 envelope contracts reconciled with the
  selected experimental profile after evidence.
- [ ] EXP-003/EXP-004/EXP-007/EXP-015/EXP-016/EXP-018 results published.

## Acceptance blockers

- target operating envelope and numeric resource budgets are undefined;
- no routing algorithm, target model, or routing-control catalog is selected;
- no-route, duplicate saturation, fanout, retry, and queue semantics remain
  unresolved;
- identity/admission construction, poisoning limits, metric policy, and
  metadata mitigation remain unresolved after the initial requirements review;
- deterministic candidate comparison has not run.

## Decision record

- 2026-09-01: Agent 1 revision defined the algorithm-independent routing
  profile boundary, independent local/forward dispositions, target contract,
  control-family ownership, and routing interaction with hop/duplicate rules.
  RFC remains Draft for Agent 3 and Agent 4 work.
- 2026-09-02: Agent 4 added algorithm-independent claim authority/freshness,
  metric provenance, per-scope resource, partition-staleness, wormhole/Sybil,
  identifier-privacy, and duplicate-admission requirements. No routing or
  cryptographic construction was selected; RFC remains Draft.
- 2026-09-02: Agent 3 recorded Wave 0 directed-topology assumptions,
  candidate-specific minimum metadata, recipient/distribution/gateway
  constraints, route-freshness and resource requirements, and a discriminating
  simulator plan. No routing algorithm, target kind, metric, numeric bound, or
  security construction was selected, and no simulator experiment was run.
- 2026-09-02: Wave 0 integration reconciled forwarding exclusion at the exact
  ingress directional peer-link rather than the whole attachment, while
  requiring explicit same-attachment/shared-medium listener, accounting,
  duplicate, resource, and loop semantics. RFC remains Draft and no routing
  algorithm or transport service model was selected.

## References

- [`simulator-first.md`](../architecture/simulator-first.md)
- [`shared-contracts.md`](../architecture/shared-contracts.md)
- [`RFC-0001`](RFC-0001-samband-network-model.md)
- [`RFC-0002`](RFC-0002-node-identity.md)
- [`RFC-0003`](RFC-0003-channel-identity-and-membership.md)
- [`RFC-0004`](RFC-0004-relay-envelope.md)
- [`RFC-0006`](RFC-0006-encrypted-channel-payload.md)
- [`RFC-0007`](RFC-0007-ptt-arbitration.md)
- [`RFC-0008`](RFC-0008-audio-transport.md)
- [`relay-security.md`](../security/relay-security.md)
- [`threat-model.md`](../security/threat-model.md)
- [`experiment-backlog.md`](../research/experiment-backlog.md)
- [`routing-candidate-evaluation.md`](../research/routing-candidate-evaluation.md)
