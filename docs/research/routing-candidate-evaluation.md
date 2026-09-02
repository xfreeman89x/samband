# Routing Requirements and Candidate Evaluation Plan

## Status and authority

Wave 0 design and research plan for Agent 3 Routing. This document refines
[`EXP-003`](experiment-backlog.md) and [`EXP-004`](experiment-backlog.md) and
identifies dependencies on EXP-005, EXP-007, EXP-012, EXP-015, EXP-016, and
EXP-018. It records no experimental result, selects no routing algorithm or
target model, sets no Protocol v0.x numeric limit, and authorizes no production
routing implementation.

Peer-visible routing semantics remain owned by Draft
[`RFC-0005`](../rfc/RFC-0005-mesh-routing.md). Routing-security construction
and assurance remain open under
[`SG-005`](../security/review-gates.md), which blocks RFC-0005 acceptance.

## Research question

Which smallest routing profile can deliver fresh Samband traffic through
dynamic, willing, channel-blind relays within a measured operating envelope,
while keeping control traffic, state, resource use, and relay-visible metadata
bounded?

The answer cannot come from a routing family's theoretical reputation. Every
candidate must exercise the same directed topologies, event traces, traffic,
resource limits, and adversarial inputs. A hybrid is justified only if no
simpler candidate passes explicit thresholds.

## Architecture-fixed constraints

These constraints are already part of the Samband architecture and are not
variables in the routing comparison:

- the Samband transport mesh is distinct from private radio channels;
- a foreign relay can forward an eligible opaque endpoint packet without
  channel membership, a membership proof, a channel key, or plaintext;
- node behavior follows current capabilities and policy, not device type;
- transport adapters expose one-hop connectivity and measurements but do not
  define routing semantics;
- partitions, reconnection, relay withdrawal, and merge are normal;
- missed or stale media is not persisted or replayed after reconnection;
- no global clock, location service, central route authority, identity
  registry, or continuously reachable coordinator is assumed;
- all state, parsing, verification, fanout, queues, retries, diagnostics, and
  work per input are finite;
- authentication can establish an issuer and protected context but cannot make
  a route, metric, proximity, resource, or willingness claim truthful.

## Operating assumptions to measure

### Topology and traffic model

The simulator must represent the mesh at time `t` as a directed multigraph.
A node can have several transport attachments and more than one peer link on
an attachment. Receipt from a peer does not prove a usable reverse link, and an
admitted bidirectional peer session does not prove that current data-plane
capacity, loss, or latency is symmetric.

Contact duration relative to routing reaction time is more useful than a
physical-speed label. A candidate that converges in one topology can still be
useless when the usable path disappears before convergence or route discovery
finishes. Exogenous traces use fixed absolute contact times or values normalized
to a candidate-independent traffic deadline. EXP-003 then reports these
candidate-dependent ratios after the run; it never changes a trace to obtain a
desired ratio:

```text
contactDuration / proactiveConvergenceTime
contactDuration / reactiveRouteAcquisitionTime
```

Samband traffic is expected to be sparse control plus bursty, deadline-bound
opaque endpoint traffic. Recipient count, traffic locality, simultaneous
flows, and whether one-to-many delivery is common enough to justify a
distribution mechanism are unresolved inputs, not assumptions.

### Sensitivity points, not protocol limits

The following values deliberately span small plausible communities and stress
conditions. They are independent sweep points, not a required full Cartesian
product and not a claim that Protocol v0.x supports the largest value.

| Dimension | Initial sensitivity points | Decision informed |
| --- | --- | --- |
| admitted nodes in a connected component | 3, 10, 30, 100, 300 | route/control state and scale breakpoints |
| mean current peer degree | 2, 4, 8, 16 | sparse reachability versus dense contention |
| temporal usable path length | 1, 2, 4, 8, 16 forwarding hops | hop budget, convergence, and latency |
| independent and burst loss | 0%, 5%, 20%, 40% | retry, metric, discovery, and dissemination behavior |
| asymmetric directed-link fraction | 0%, 10%, 30% | reverse-path assumptions and directional metrics |
| contact duration / traffic deadline | 0.25, 1, 4, 20 | whether a path persists long enough to carry useful traffic |
| recipients for one logical send | 1, 2, 10, 50 | per-recipient routing versus bounded dissemination |
| relay withdrawal pattern | one leaf, one bridge, 10% synchronized, 50% synchronized, rapid flap | availability, chatter, and safe withdrawal |

EXP-004 must replace or narrow these sensitivity points using documented
platform/contact traces and expected community use. Absolute energy, radio
contention, discovery reach, and OS suspension cannot be inferred from the
simulator and remain physical experiment work.

EXP-004 must also publish the topology generators or immutable traces, in/out/
symmetric degree distributions, clustering and edge connectivity, component
sizes, inter-contact time, neighbor turnover, latency/jitter/bandwidth/MTU/
queue assumptions, independent and burst-loss parameters and receiver
correlation, routable-target population, target rotation/overlap, relay-budget
heterogeneity, and exact traffic manifests. A traffic manifest includes target
population, active-target fraction, pair selection, packet sizes, burst rate
and length, concurrent flows, idle intervals, class deadlines, run horizon,
and cold-start versus warmed phases.

### Controlled comparison method

EXP-003 compares exact experimental candidate profiles, not family labels. Each
candidate ID pins a source/revision or complete pseudocode contract, message
catalog, metric, timers, retry and duplicate behavior, tie-break, limits, and
all parameters. Probabilistic gossip and deterministic relay-set reduction are
separate candidates; link-state accounting includes its control dissemination.

Before the decision run:

1. EXP-004 fixes the operating envelope and hard thresholds independently of
   the result-bearing runs. Pilot results may size the experiment but cannot set
   thresholds.
2. Every candidate receives the same finite tuning budget on development
   traces. Parameters are then frozen and evaluated once on held-out traces.
3. Topology, contacts, per-action link effects, traffic, resources, and attacks
   are precomputed immutable exogenous traces. Named random streams separate
   topology, link effects, traffic, adversary, and candidate-local jitter.
4. The scenario schema version, profile ID, parameters, trace identifiers, and
   every seed are recorded. The exogenous trace is identical across candidates;
   rerunning one candidate/profile/scenario/seed must reproduce its own ordered
   semantic output.
5. Recipient-target and bounded-dissemination workloads form a factorial
   family-by-target-model comparison for every compatible candidate. Results
   with different logical-delivery semantics are never ranked as if equivalent.

The experimental link service defines unicast and shared-medium serialization,
bandwidth, queues, acknowledgements/retries, receiver-specific and correlated
loss, and how one broadcast action is charged against several receptions. If
contention is not modeled, delivery results are labelled ideal-capacity and
airtime is only a proxy. Before EXP-002 selects an encoding, byte comparisons
use one pinned provisional accounting encoding or separate logical-field,
payload, and security-overhead octets; implementation object size is excluded.
Abstract parse, verification, recomputation, and timer work uses published
candidate-independent weights.

## Required routing model

### Directed links and neighbor churn

Routing must receive separate local concepts for:

- the ingress transport attachment;
- the admitted immediate-peer session;
- the directional peer link used by one ingress or egress action;
- current local send and receive evidence, age, and bounded quality samples;
- shared-medium broadcast capability versus peer-specific unicast capability.

In this plan, a **directional peer link** is current local one-hop
reachability/action state bound to one admitted immediate-peer session and one
transport attachment. It is not a peer identity, a transferable session
verdict, or proof of a reverse link.

Wave 0 integration reconciles forwarding exclusion at this directional-link
boundary. Peer-specific unicast never sends a copy immediately back to the
exact ingress directional peer link. An exact candidate may use a different
peer on the same attachment, or an explicit shared-medium emission that the
ingress peer can also hear, only when it defines listener/reception behavior,
fanout and work accounting, resource reservation, duplicate effects, and loop
control. Eligibility of another link/session to the same logical peer remains
profile-defined. This model selects neither a transport service nor a routing
algorithm.

A peer can be heard without being usable as a next hop. A route request's
arrival path cannot be reversed unless the required reverse links are
independently usable. Link loss, session close, and metric degradation are
different events and must have explicit route effects.

Mobility is represented through deterministic link/contact traces: links
appear, degrade, become one-way, recover, or disappear; nodes enter or leave a
component; and the same peers can reconnect through new sessions or
attachments. No algorithm may carry old session authority into the reconnect.

### Relay willingness and resource withdrawal

The minimum shared resource signal is current relay willingness in a
session-scoped capability snapshot with generation, bounded validity, and
withdrawal. Raw battery percentage, charging state, thermal state, mobile-data
plan, queue depth, OS lifecycle, device model, and transport inventory remain
local.

An exact profile may test a coarse, quantized, short-lived relay cost class only
if EXP-003 and EXP-007 show that a boolean willingness signal is insufficient.
Such a class is the relay's own untrusted policy statement, not proof of its
resources. Local battery-aware behavior can instead:

1. refuse new transit work immediately when policy requires withdrawal;
2. add a local resource penalty when choosing or advertising a route through
   self;
3. delay or damp re-enablement to prevent oscillation, without delaying an
   immediate safety-driven withdrawal.

Any remote consequence of a direct capability snapshot is a distinct routing
claim. It must not reset, extend, or launder the underlying snapshot's
receipt-relative validity.

### Freshness domains

The selected profile must keep these domains separate:

| Domain | What becomes stale | Required basis |
| --- | --- | --- |
| peer-session liveness | one admitted neighbor context | transport/session event and bounded local timer |
| capability validity | direct peer's current willingness/features | session-bound generation and receipt-relative validity |
| route-control freshness | one issuer's claim about a target or topology fact | issuer/incarnation, revision, validity, and exact conflict rule |
| route usability | local selected next hop/path | current directed-link, capability, and route state |
| forwarding lifetime | one packet's remaining reach | RFC-0004 hop limit |
| forwarding duplicate retention | one forwarding instance | packet duplicate key and finite local cache window |
| security freshness/replay | one authenticated control or protected record | security-profile replay domain and atomic commit |
| media freshness | whether an endpoint packet can still be useful | endpoint traffic deadline, grant, stream, and sequence semantics |

No sender wall clock is trusted. A propagated route claim needs an exact first
revision, non-wrapping revision or incarnation rule, same-revision conflict
rule, identical-retry behavior, expiry, restart/rollback behavior, and bounded
high-water or tombstone state. An identical retry does not refresh validity.
A withdrawal is owned by the advertiser's own claim slot or caused by a local
expiry/link event; it does not grant authority to erase another issuer's claim
or the target's identity.

Receipt-relative validity limits retention after first admission but does not
prove claim age. A malicious relay can delay a never-before-seen claim and make
a receiver start its full local window later. Forwarding an unchanged claim
cannot increase its remaining validity, and repeated presentation of an
identical revision cannot reset first-acceptance expiry. If bounded high-water
or tombstone state is evicted, the receiver cannot recognize the same
issuer/incarnation forever without some other retained recognition state. Each
exact candidate must therefore either retain bounded issuer/incarnation
admission or quarantine state with deterministic saturation/eviction, require
a fresh authenticated incarnation or eligible fresh session under a rule an
old claim cannot satisfy, or explicitly admit and measure stale resurrection
after eviction. A new session can reset only a claim explicitly owned by and
scoped to that immediate peer session. A multi-hop claim requires a newly
authenticated incarnation of its original claim issuer; reconnecting an
ingress peer cannot reset third-party freshness state. No result may claim
permanent stale rejection after all recognition state has been discarded.

The one-hop session verdict never transfers across a relay. An independently
origin-authenticated control claim can outlive one ingress session only within
its own explicit scope and validity, and it must be re-admitted on every new
ingress.

### Bounded state and work

Every candidate declares finite limits and deterministic saturation behavior
for at least:

- attachments, peer sessions, directional links, and neighbors;
- routing targets, claim issuers, origin/incarnation contexts, and revisions;
- route candidates and alternate next hops per target;
- topology edges or two-hop neighbors where the family uses them;
- pending discoveries, replies, errors, probes, and retransmissions;
- relay capability snapshots and dampening timers;
- packet duplicate and routing-claim replay/freshness state;
- queues, local residence/deadline state, fanout actions, and shared-medium
  emissions;
- parsing, authentication, route recomputation, and emitted control work per
  event and per bounded interval.

An over-limit attacker cannot evict unrelated admitted state through an
unspecified policy. Pseudonym or credential rotation cannot silently reset all
local abuse quotas. Any quota handle stable enough to bridge permitted rotation
is local-only security state: it is not a wire routing identifier or a logged
tracking value.

### Lifetime, duplicates, and route loops

The Draft RFC-0004 hop limit remains mandatory as a data-plane safety bound
even for a routing algorithm intended to be loop-free. Routing-control search
scope, route validity, duplicate retention, queue residence, media deadline,
PTT lease, and security replay windows are different quantities.

First-seen duplicate suppression has a candidate-dependent availability and
security cost. An admitted malicious relay can race a low-hop or otherwise
non-viable copy so that it arrives before a later copy with more remaining
reach. If a non-local `hopLimit == 1`, `NO_ROUTE`, or resource-failed occurrence
commits duplicate state, it may suppress the viable copy. EXP-016 must treat
this as deliberate suppression, not only path-order variance.

A finite duplicate window plus hop count does not create a temporal network
lifetime. A malicious relay can retain a packet and retransmit it after cache
eviction. Endpoint security replay may prevent a repeated inner effect, but
transit CPU, bandwidth, and battery work still require quotas unless a separate
privacy-reviewed freshness mechanism is selected.

Data-plane lifetime and duplicate suppression limit damage but do not make
route state loop-free. Each candidate must define and test its own loop
condition: feasible distances or destination freshness for distance vector,
topology revision and transient-loop behavior for link state, request/reply
freshness or explicit path checks for reactive routing, and at-most-one
committed local/forwarding effect per duplicate key within retention for
dissemination, subject to the declared no-effect and partial-fanout policy.

## Candidate routing families

| Family | Conditions that could favor it | Primary costs and failure modes | What EXP-003 must distinguish |
| --- | --- | --- | --- |
| classic controlled flooding | very small, sparse, rapidly changing components; no route-acquisition delay | transmissions and duplicate work grow sharply with density and recipient traffic | smallest size/density where deadline delivery no longer justifies overhead |
| reduced flooding or gossip | dissemination is useful but classic flooding is too costly | probabilistic delivery tails or extra two-hop/relay-set state; rushing and selector manipulation | delivery tail under burst loss versus saved transmissions and added state |
| loop-avoiding distance vector | repeated recipient-specific traffic and moderate target set | periodic/triggered chatter, stale good news, sequence poisoning, target correlation, metric lies | convergence and path stability across churn versus idle/control cost |
| proactive link state | paths should be immediately available and topology is stable enough | network-scale topology state, churn recomputation/control storms, widest topology disclosure | whether richer alternatives improve deadline delivery enough to pay state/privacy cost |
| reactive/on-demand | many possible targets but few active recipient pairs | cold-route latency, request floods, reverse-state pressure, partition retry storms, forged fast replies | route-acquisition deadline and idle savings under actual demand locality |
| hybrid | measured conditions have distinct regimes that no simple family passes | union of metadata, state, transitions, downgrade surface, and failure modes | only after a simpler candidate misses a named hard threshold |

Representative standards establish credible mechanisms, not Samband field or
algorithm choices: Babel is a loop-avoiding distance-vector reference, OLSRv2
is a proactive link-state/MPR reference, AODV and DSR are reactive references,
and SMF compares classic and reduced flooding with duplicate detection.

DSR-style source routing is useful as an analytical reactive comparator but is
not compatible with the current RFC-0004 rule that the generic relay envelope
does not carry a full path. Testing it as a Samband candidate would first
require an explicit RFC change and would expose every path hop to relays.

## Minimum relay metadata

### Common boundary

The current Draft envelope proposes the following common routing-visible
information for a forwardable packet:

- exact envelope-format/protocol-profile pair;
- coarse outer class/type;
- packet identity and origin routing context for the duplicate domain;
- routing-directive kind, scope, and opaque target where the target kind uses
  one;
- remaining hop limit;
- bounded payload length, extensions, and opaque payload;
- possibly a coarse traffic treatment, still contingent on EXP-003/EXP-007.

The requirement to carry a distinct origin routing context is itself still a
Draft decision. EXP-007 and EXP-016 must compare its correlation cost and its
benefit for duplicate scoping, conflict detection, and abuse quotas, especially
for dissemination candidates.

Ingress attachment, immediate-peer session/link, egress next hops, local link
samples, raw resource state, route table, queue state, and local abuse buckets
are local inputs and are not generic envelope fields.

### Candidate-specific additions

| Family | Minimum peer-visible routing/control metadata beyond common packet fields | Minimum retained state |
| --- | --- | --- |
| classic flood | propagation scope and profile-fixed forwarding/suppression behavior; target may be exact recipient or bounded dissemination | recent packet duplicate keys plus current neighbor/capability eligibility |
| gossip | classic-flood fields; probability, jitter, and suppression constants are profile parameters, not attacker-selected packet hints | duplicate keys plus bounded suppression/timer state |
| reduced relay set | link-local neighbor status, bounded two-hop or selector information, relay willingness, revision, and validity | neighbor/two-hop or selector sets, duplicate keys, and relay-election state |
| distance vector | opaque destination target, semantic claim-issuer context, issuer incarnation and route revision, advertised bounded metric, validity, withdrawal/unreachable indication, and any separately authorized destination freshness | capped per-target/per-neighbor candidates, selected successor, feasible/freshness state, and expiry |
| link state | scoped topology origin, origin incarnation and revision, validity, bounded directed adjacency tuples and metrics, withdrawal, and optional relay-selector state | capped topology database, flooding state, shortest-path result, and duplicate/revision state |
| reactive/on-demand | logical discovery and attempt/revision IDs distinct from packet ID, scoped origin and target, integrity-bound search hop bound, any separately authorized destination freshness, accumulated bounded metric, reply correlation/authority, validity, and route error | reverse request state, pending searches, route cache, precursor/error state, and timers |
| hybrid | union of the chosen components plus exact zone/fallback boundary, transition state, and downgrade-safe mode semantics | bounded union of both families' state plus transition state |

Algorithm-local data such as a feasible distance, shortest-path predecessor,
reverse route, or selected next hop stays local unless another node must receive
it to reproduce peer-visible semantics.

The security boundary always supplies a semantic claim-issuer context. A
wire-visible issuer identifier is required only when a claim crosses or
outlives the immediate admitted session; it must not redundantly expose the
session identity, control origin, and `originRoutingContext`. If a distance-
vector or reactive candidate uses destination-owned sequence/freshness in
addition to the advertiser's claim revision, its profile defines who may
originate, advance, copy, reset, and exhaust it. Authenticating an advertiser
does not authorize it to mint a higher target-owned freshness value.

## Recipient-specific and distribution routing

### Opaque recipient target

A destination-oriented profile needs a routing target that is stable long
enough to advertise, discover, and use, but no longer or wider than necessary.
Its profile must define syntax, equality, collisions, audience, correlation
scope, creation, rotation, expiry, overlap, ownership/admission, target takeover,
and the exact local-delivery predicate. It is not a discovery handle, raw node
credential, human label, channel credential, membership proof, or plaintext
channel identifier.

Target ownership and transit reachability are separate claims. A neighbor can
authenticate its own route-view advertisement about a target without proving
that it owns the target or that the complete route exists.

If an endpoint creates separate copies for several recipient targets, each
target needs a distinct forwarding/protected-record instance and packet
identity under the current Draft. Reusing one `(originRoutingContext,
packetIdentity)` while changing the immutable target creates a packet-identity
conflict; the duplicate key does not include target. A future distribution
target can instead identify one dissemination instance, subject to its own
privacy and fanout rules.

Sharing one `originRoutingContext` across the separate recipient copies exposes
common-origin fanout; using per-recipient origin contexts complicates duplicate
scoping and quota continuity. RTE-016 and EXP-007 therefore measure timing/
length correlation, visible recipient-set cardinality, and linkage even when
packet identities and protected records differ.

### Bounded dissemination

A dissemination target can avoid route acquisition and may better fit small
dynamic groups, but exposes each packet to more relays and increases duplicate,
airtime, and denial-of-service costs. Local delivery remains an endpoint
predicate independent from channel readability. The forwarding scope, fanout,
duplicate policy, shared-medium behavior, and deadline must be exact.

### Future multicast or distribution trees

A future tree cannot simply be a relay-visible private-channel membership tree.
It would require a new RFC and at least:

- an opaque distribution context with scope, rotation, collision, and takeover
  rules distinct from the channel identifier;
- bounded admitted routing claims for soft-state join/prune or branch
  advertisements, with distinct issuer and branch/subscription subject plus
  revision, expiry, replay, and authority semantics;
- branch fanout, loop-free repair, split-tree behavior during partitions, and
  deterministic rebuild or reconciliation after merge;
- an explicit decision about whether non-member relays may maintain or
  advertise ciphertext-forwarding branches without becoming endpoint
  subscribers, locally eligible recipients, or channel members;
- protection against a malicious branch relay blackholing a large subtree;
- a metadata budget for group correlation, joins, stable branches, roots, and
  speaker cadence;
- no retention or replay of media missed during a split.

Per-recipient copies, bounded dissemination, source-specific trees, and shared
trees remain future alternatives. No tree state or message is added in Wave 0.

### Future Internet gateways

A future gateway is an explicit dynamic relay/transport capability, not a
route authority, channel authority, generic IP proxy, or decryption endpoint.
A future RFC must require a gateway to:

- forward only admitted Samband frames under local opt-in and data/billing
  policy;
- preserve the exact profile, packet identity, target, immutable context, and
  endpoint protection instead of transcoding or re-originating traffic;
- count the gateway forwarding event under explicit hop semantics and never
  reset lifetime through re-encapsulation;
- keep Internet endpoint addresses transport-local by default; any outer or
  multi-hop exposure requires a named field, audience, scope/rotation,
  integrity rule, and EXP-007 justification;
- bound connections, fanout, queues, retries, and amplification;
- prevent loops between multiple gateway/transport attachments;
- expose and threat-model IP-level correlation and its natural sinkhole role;
- bind gateway capability and reachability advertisements to an issuer,
  freshness, expiry, withdrawal, and sinkhole-influence limit.

An Internet tunnel is an intentional topology shortcut and can look like a
wormhole. Neither low latency nor gateway authentication proves physical
proximity.

## Protocol requirements

Protocol and future exact routing profiles must expose or define:

1. distinct transport attachment, admitted peer session, and directional
   peer-link contexts for ingress and egress;
2. peer-unicast versus shared-medium broadcast actions and their fanout/work
   accounting;
3. at least an experimental comparison between an opaque recipient target and
   bounded dissemination, with complete target contracts;
4. semantic control issuer, advertised target/subject, provenance class,
   revision or operation identity, validity, and replacement/withdrawal
   authority, with a wire issuer only when the claim crosses/outlives a session;
5. receipt-relative freshness, origin restart/incarnation, revision
   exhaustion, rollback, identical retry, delayed first presentation,
   tombstone eviction, conflict, and expiry behavior;
6. bounded metric range, provenance, composition, saturation, invalid values,
   deterministic tie-breaks, and permitted remote influence;
7. data hop limit plus candidate-specific loop prevention, without treating
   hop count as route or media freshness;
8. duplicate insertion and atomic reservation/action behavior for every
   no-effect, partial-fanout, retry, and saturation result;
9. separate outer packet identity, route-control operation/revision,
   capability generation, security replay, PTT, and media identity domains;
10. bounded `NO_ROUTE` discovery/retry behavior and class-specific queues;
    fresh media may wait only within its deadline and never across a partition;
11. immediate local relay withdrawal, bounded propagation/expiry, and optional
    hysteretic re-enable behavior;
12. deterministic state and work bounds at every scope needed to resist one
    peer, one asserted origin/target, or many rotating Sybils;
13. destination-owned freshness authority where used, distinct from an
    advertiser's own claim revision;
14. safe aggregate observability for route acquisition, convergence, drops,
    state, and resource work without channel/plaintext or stable identity logs.

An expanding-ring reactive retry needs either a stable logical discovery ID
plus a strictly advancing integrity-bound attempt revision and search bound, or
a new route-request attempt ID linked to the logical discovery. It also uses a
new outer packet identity. Only the authorized request origin can widen the
bound; an intermediate relay cannot. Both packet-level and request-level
duplicate/replay state must admit a valid wider attempt without accepting an
old or unauthorized one.

## Security and privacy requirements

The security boundary must provide logically distinct verdicts for:

- peer-session admission under one exact pair and immediate-peer assurance;
- outer-envelope admission and exact immutable/mutable field coverage;
- routing/capability-claim issuer authority, target/subject, provenance,
  freshness, and replay;
- binding between a scoped target and a locally eligible recipient where the
  target kind claims such ownership;
- metric provenance: locally measured, immediate-peer self-asserted,
  transit-aggregated, or separately origin-authenticated;
- provisional freshness checking and an atomic commit with route mutation,
  duplicate insertion, and resource reservation where required.

The following contexts never become equal merely because their bytes match:

```text
immediate peer principal
outer origin routing context
route-claim issuer
advertised routing target
locally eligible delivery subject
channel authenticated principal and action subject
local-only abuse-quota scope
```

Every candidate must be tested against authenticated false reachability,
attractive metrics, false or third-party withdrawals, revision jumps, replayed
state, target takeover, blackholes, selective forwarding, Sybil rotation,
rushing, duplicate-cache poisoning, and colluding wormholes. Authentication
limits who asserted a claim; it does not prove the claim or force forwarding.

Distance vector exposes target reachability and stable freshness context. Link
state exposes the largest topology/contact graph. Reactive discovery exposes
who is seeking which target and approximately how far the search expands.
Flooding exposes less explicit topology but enlarges the observer set for every
packet. A hybrid inherits the union and can additionally reveal its mode.

Remote metrics are range-limited and can have only profile-defined influence.
Raw resource values remain private. Stable-identifier tie-breaks enable
tracking and Sybil grinding; rotating-identifier tie-breaks can create route
oscillation. Tie-break inputs therefore require Agent 4 review.

Safe diagnostics use aggregate counts or ephemeral local handles. They do not
retain channel identifiers, protected payloads, audio, full route pseudonyms,
peer credentials, or a persistent topology/contact history.

Abuse-quota continuity across an identifier rotation is available only through
an authenticated, reviewed local binding. Unverified encounters and new Sybils
fall back to attachment, session, and global quotas. Timing, target equality,
radio identifiers, or profile fingerprints never establish continuity.

## Simulator scenario suite

When an experimental profile is authorized, every candidate uses identical
immutable exogenous inputs and the same recorded seed set. Host runtime
measurements remain separate from virtual-time correctness.

| ID | Class | Topology and event | Candidate distinction and required observation |
| --- | --- | --- | --- |
| RTE-001 | common comparative | direct, two-hop, and three-hop chains; middle nodes have zero channel memberships | basic local/forward independence, hop decrement, deadline delivery, and foreign relay |
| RTE-002 | common comparative | ring and diamond with equal and unequal paths | alternate-path use, deterministic tie-break, transient loops, duplicate order, and path stability |
| RTE-003 | common comparative | directed links, one-way degradation, reply on a different path, several attachments | reverse-path assumptions, directional metric correctness, and same-adapter relay feasibility |
| RTE-004 | common comparative | immutable mobility/contact traces with fixed absolute durations or candidate-independent deadline ratios | proactive convergence versus reactive acquisition versus immediate dissemination; reaction ratios are outputs |
| RTE-005 | common comparative | two clusters joined by one bridge; bridge disappears, partition persists, then merges | local component operation, stale-state expiry, recovery, merge quiescence, and no media replay |
| RTE-006 | safety/conformance | origin restarts and old/new route claims meet after merge | incarnation/revision rollback, conflict, expiry, tombstone eviction, delayed first presentation, and stale-state resurrection |
| RTE-007 | common comparative | one short lossy path and one longer reliable path; metric oscillates near a tie | metric composition, hysteresis, path stretch, flapping, and deadline delivery |
| RTE-008 | common comparative | cold logical send; target is initially unknown or unreachable, later appears, with a partitioned retry opportunity | each candidate's declared no-route behavior, first-deliverable-path delay, amplification, pending-state bounds, and media deadline behavior |
| RTE-009 | family safety | distance-vector triangle loses its destination edge | count-to-infinity/feasibility, stale good news, withdrawal, blackhole interval, and alternate recovery |
| RTE-010 | family safety | link-state grid with burst churn and oversized/rapid adjacency revisions | topology-control burst, recomputation/state high-water, partial maps, and bounded rejection |
| RTE-011 | common comparative | sparse grid through dense graph under independent and burst loss | classic flood, gossip, and reduced-relay delivery tails versus transmissions and duplicate work |
| RTE-012 | safety/conformance | low-hop non-viable copy races a delayed higher-hop viable copy | first-seen suppression rate for every no-effect insertion policy, including malicious rushing |
| RTE-013 | safety/conformance | each configured state/work limit at `N` and `N+1`, plus a common byte/work device budget | deterministic saturation without unbounded memory/work or unrelated-state eviction |
| RTE-014 | security | a fixed attacker capability/placement/duration/identity/work budget mapped to each applicable attack: forged metric/reachability/selector, false withdrawal, rushing, Sybils, blackhole, selective forwarding, or wormhole | family-specific applicability, claim authority, route attraction, suppression, poison persistence, amplification, and recovery; absence of one feature earns no score |
| RTE-015 | common comparative | relay withdraws at a leaf and bridge; random and highest-betweenness 10%/50% groups withdraw; nodes rapidly re-enable | immediate local refusal, propagation delay, connectivity, load shift, and hysteresis chatter |
| RTE-016 | common comparative | one logical send to 1, 2, 10, and 50 eligible recipients, constrained by endpoint count, using each compatible target model | delivery skew, packet-ID separation, origin/fanout linkage, target exposure, state, bytes, fanout, and per-relay burden |
| RTE-017 | security/privacy | routing origin/target rotates at declared lifetimes during discovery, traffic, disconnect, and reconnect | cross-session binding, route invalidation, recovery latency, quota continuity, and linkability |
| RTE-018 | future-only, unscored | synthetic tree and two-gateway extension pressure | metadata/state growth, branch/subscriber authority, gateway advertisement/address disclosure, loops, hop reset attempts, and profile-translation rejection; no feature implementation |
| RTE-019 | common comparative | cold component startup followed by a long stable idle interval and then a sparse burst | first-use readiness, idle control cost, timer work, and retained state |
| RTE-020 | common comparative | topology/control change coincides with concurrent control and deadline media bursts on finite queues | link-service contention, starvation resistance, stale-media drop, and control recovery |
| RTE-021 | family safety | reactive discovery widens through authorized and unauthorized retry attempts | operation/attempt identity, bound authority, request-level duplicate/replay behavior, amplification, and pending-state limits |

Adversarial variants include same packet identity with a changed target,
payload, immutable extension, and hop limit; replay after duplicate retention;
repeated authenticated duplicates that force pre-lookup verification; identical
revision with different content; delayed first presentation; same-incarnation
tombstone eviction; a lower advertisement after a newer withdrawal;
destination-freshness jump/reset; unauthorized reactive-bound widening;
implicit-session versus explicit-wire issuer; forged selector/two-hop state;
validity-refresh attempts at each relay; gateway-address disclosure; tree
branch/subscriber authority confusion; and admitted verification-work floods.

Only common comparative scenarios contribute to cross-family delivery and cost
comparisons. Family safety, security, and conformance probes are hard gates,
not bonus scores; future-only probes cannot affect Protocol v0 selection.

## Metrics to measure

The EXP-003 preregistration fixes seed count, stopping rule, confidence-interval
method, and the minimum sample count for every reported quantile. Across paired
exogenous traces, report uncertainty on candidate differences plus
distributions and preregistered tail quantiles; never report only a mean that
hides delivery tails.

| Category | Metrics |
| --- | --- |
| useful delivery | fraction delivered before the class deadline; first usable path; first-packet and steady-state latency; jitter; recipient delivery spread; stale drops |
| convergence | acquisition, failure detection, alternate recovery, withdrawal propagation, stale-route duration, merge quiescence, and blackhole duration |
| path quality | temporal-oracle path stretch, hop count, expected transmissions, selected-path lifetime, next-hop changes, and route oscillations |
| control cost | packets, bytes, timer wakeups, verification operations, and peak burst per node-second and topology event |
| forwarding cost | transmissions and bytes per successful recipient, broadcast/unicast actions, fanout, duplicates, loop forwards, and TTL exhaustion |
| bounded resources | high-water entries by state class, pending work, queue occupancy/age, retries, recomputations, authentication work, and emitted actions per input |
| relay burden | maximum and distribution of forwarded bytes/actions, airtime/CPU/wakeup proxies, and load shifted after withdrawal |
| adversarial degradation | attacker-byte to victim-work amplification, false-state acceptance, route-diversion fraction, suppression rate, honest-state eviction, poison lifetime, and recovery after attack stops |
| privacy surface | observer audience, visible topology edges, target/origin correlation window, route-control fingerprint uniqueness, and pseudonym-linkage success under EXP-005/007 observers |
| determinism | identical ordered semantic trace and outcomes for the same simulator/profile/scenario/seed |

Metric definitions are part of the preregistration:

- useful delivery is per eligible recipient and permits at most one local
  effect despite duplicate copies;
- `firstDeliverablePath` is the earliest causal sequence of transmissions that
  can finish while every traversed link exists and before the traffic deadline;
  the temporal oracle cannot wait across a forbidden media partition;
- route-table convergence is reported only for candidates that maintain such
  state, while `firstDeliverablePath` is common to all families;
- merge quiescence specifies an observation window and excludes only the exact
  permitted periodic baseline;
- route diversion, false-state acceptance, suppression, poison lifetime, work
  amplification, and recovery each have a formula and denominator;
- privacy trials fix observer positions, collusion set, retained fields, prior
  knowledge, retention, and linkage algorithm.

Simulation energy proxies are transmissions, receives, bytes, crypto work,
timer wakeups, and active relay duration. They do not establish battery drain;
EXP-012 must measure that on physical platforms.

## Decision procedure

Every candidate first passes hard safety and architecture gates:

- no route behavior depends on channel plaintext or membership;
- all loops, floods, state, queues, retries, and work remain within declared
  bounds under honest and malicious input;
- expiry, withdrawal, partition, merge, and saturation are deterministic;
- fresh media is never stored or replayed across a partition;
- directed links and relay withdrawal do not create an unstated reverse-path or
  always-on assumption;
- rerunning the same candidate/profile/scenario/seed produces the same ordered
  semantic output trace;
- the candidate declares every relay-visible field and security verdict it
  needs.

Passing candidates are then compared as a Pareto set across deadline delivery,
acquisition/recovery latency, overhead, state, relay burden, adversarial
degradation, and metadata exposure. Thresholds are set only after EXP-004
narrows the target operating envelope and before result-bearing EXP-003 runs.
Dominance accounts for uncertainty and does not collapse privacy, deadline
delivery, and resource safety into one post-hoc weighted score. Simplicity is a
published vector of peer-visible fields, control types, state classes, timers/
transitions, conformance cases, and resource high-water marks. A hybrid is
evaluated only for two preregistered material regimes, after every simpler
candidate misses at least one explicit threshold, and it must pass held-out
validation under the same tuning rule.

## Decisions that must remain open

- Protocol v0.x node, density, path, churn, loss, contact, traffic, recipient,
  and numeric resource envelope;
- exact preregistered candidate IDs, parameters, transport-service model,
  accounting model, thresholds, seed count, and statistical method;
- final routing family or hybrid composition;
- opaque recipient, bounded dissemination, or mixed target model;
- routing-origin and target construction, ownership, stability, rotation, and
  whether a distinct origin context is mandatory;
- exact directed-link admission and whether any profile excludes one-way links;
- control message catalog, propagation, revision/incarnation, expiry, and
  restart/rollback rules;
- metric algebra, provenance, quantization, remote influence, tie-break, and
  hysteresis;
- whether any battery-derived or traffic-treatment value is wire-visible;
- hop-limit default/maximum and mutable-field protection;
- duplicate retention/capacity and every no-effect/partial-fanout insertion
  rule, including higher-hop-later behavior;
- no-route queue, discovery, retry, and fresh-media deadline policy;
- outer/control authentication construction and malicious-relay assurance;
- PTT propagation/coordinator assumptions and acquisition budget;
- future multicast/distribution-tree and Internet-gateway semantics.

## Coordination requirements

| Owner | Required follow-up from this analysis |
| --- | --- |
| Protocol | preserve separate attachment/session/link and identity domains; review target/control/freshness/duplicate semantics; realize the Wave 0 peer-link-aware ingress/egress model in the Draft specification and vector format; define same-attachment/shared-medium listener and fanout accounting |
| Security | define claim/target admission, outer mutable-field coverage, replay/freshness commits, privacy budgets, and local quota continuity without route-tracking identifiers |
| Architect | narrow EXP-004's operating envelope and decide milestone thresholds from evidence |
| Simulator | implement only an accepted or explicitly experimental profile; reuse the scenarios and expose bounded semantic metrics |
| Platforms | provide directional link/contact, lifecycle, and physical resource traces without leaking platform types into routing |
| PTT and Audio | consume measured routing latency, loss, reordering, and freshness; do not assume reliable multicast, a stable coordinator, or route-level grant authority |

## Primary references considered

- [RFC 2501: MANET performance and evaluation considerations](https://www.rfc-editor.org/rfc/rfc2501.html)
- [RFC 8966: Babel routing protocol](https://www.rfc-editor.org/rfc/rfc8966.html)
- [RFC 7181: OLSRv2](https://www.rfc-editor.org/rfc/rfc7181.html)
- [RFC 6130: MANET neighborhood discovery](https://www.rfc-editor.org/rfc/rfc6130.html)
- [RFC 3561: AODV](https://www.rfc-editor.org/rfc/rfc3561.html)
- [RFC 4728: Dynamic Source Routing](https://www.rfc-editor.org/rfc/rfc4728.html)
- [RFC 6621: Simplified Multicast Forwarding](https://www.rfc-editor.org/rfc/rfc6621.html)
- [RFC 6551: routing metrics for low-power and lossy networks](https://www.rfc-editor.org/rfc/rfc6551.html)
- [RFC 8116: security threats to OLSRv2](https://www.rfc-editor.org/rfc/rfc8116.html)
