# Samband Protocol v0.x Experimental Specification

## Status

Draft experimental synthesis for Protocol, Routing, and Security review. This
document is not an Accepted Samband specification, wire-compatibility promise,
security claim, or implementation authorization.

The governing RFCs remain Draft. Capitalized requirement words below express
their proposed semantics only. They become normative only after the RFC workflow
accepts the applicable profile and integrates it into a released specification.

`draft/v0.x` is a human-readable vector/profile label used by this working
document. It is not an assigned wire value or released Protocol v0.1 profile.

## Scope and readiness

| Area | v0.x status |
| --- | --- |
| layering and two-level message taxonomy | Agent 1 proposal; Agent 4 initial boundary review recorded; gates open |
| logical outer envelope and processing order | Agent 1 proposal plus Agent 4 security requirements; encoding, Routing, and security-profile review open |
| hop-limit TTL and first-seen duplicates | experimental proposal; numeric/routing/security decisions open |
| capabilities | full-snapshot proposal; bounds, registry, Routing/Security review open |
| routing | interface requirements only; no target kind or algorithm selected |
| identity/session admission | candidate assurance/session options documented; no credential or construction selected |
| channel/future-protected payload | MLS-led experiment plan and required interface documented; no construction selected |
| PTT | abstract state/control contract plus authorization requirements; authority/arbitration profile unavailable |
| audio | control/media boundary only; codec/security/routing evidence unavailable |
| test-vector carrier | draft JSON format; security-vector extension and Agent 9 review open |
| wire encoding | deliberately unselected pending EXP-002/EXP-014 |

No real CHANNEL, PTT, or AUDIO action can be accepted under `draft/v0.x` until
a reviewed security profile supplies the required admission, open/replay, and
authorization dispositions. Simulator vectors MAY inject explicitly synthetic,
non-cryptographic dispositions to test protocol ordering; those fixtures MUST
NOT be described as authentication, membership proof, encryption, or replay
protection.

## Architectural invariant

```text
shared Samband transport mesh != private channel
```

A willing non-member relay can process an eligible outer Samband packet without
channel membership or access to the endpoint payload. A node can independently
act as endpoint, relay, both, or neither according to current capabilities and
policy.

## Layering

```text
one-hop transport frame
└── Samband outer protocol
    ├── link-local peer/session control
    ├── routing-profile mesh control
    └── forwardable opaque endpoint container
        └── Agent 4-reviewed channel-security boundary
            ├── CHANNEL control
            ├── PTT control
            ├── AUDIO_CONTROL
            └── AUDIO_MEDIA
```

Transport discovery/connectivity and frame/backpressure limits sit below the
Samband outer protocol. A transport adjacency is untrusted. A peer becomes a
current neighbor only under the admission semantics of the exact selected
profile; Agent 4 still owns that admission evidence.

## Identity domains

The protocol keeps these contexts distinct:

- discovery handle;
- discovery/session exchange identity;
- admitted peer-session context;
- origin routing context;
- forwarding packet identity;
- routing target;
- channel context, authenticated principal, action subject, and security context
  returned or evaluated by the security boundary;
- channel operation identity;
- PTT request and grant identities;
- media stream identity and media sequence;
- local human-facing labels.

Equality in one domain does not establish equality in another. Packet identity
is only a forwarding duplicate-correlation token scoped by the selected
compatibility pair and origin routing context. It proves neither origin nor
authenticity and is not security replay protection.

## Version and exact-profile model

Samband v0.x separates:

1. **envelope format** — selects bounded outer parsing;
2. **protocol profile** — pins exact processing, catalog, routing, limits, and
   extension semantics;
3. **negotiated capabilities** — enable only profile-defined optional behavior.

The exact compatibility selection is the ordered pair `(envelope format,
protocol profile)`. The axes are independent: neither identifier contains or
implies the other. Vector sets and future conformance claims pin both.

Pre-session `DISCOVERY_ADVERTISEMENT` is the only packet without a selected
protocol profile. It uses a supported envelope format's bounded bootstrap
grammar and advertises exact `(envelope format, protocol profile)` pairs.
The initiator selects exactly one intersection from the most recent offer using
local policy and binds it to one link-local session-exchange identity in
`SESSION_INIT`. The responder either echoes that exact pair and exchange
identity in `SESSION_ACCEPT` or rejects; it never substitutes another pair. A
session becomes authoritative only after both roles confirm the same pair and
the selected profile's Agent 4 admission succeeds. Pre-v1 identifiers are
opaque: no implementation infers compatibility, preference, or downgrade safety
from numeric ordering. No intersection means no admitted session. EXP-002 must
define simultaneous initiation, retry, stale-offer, collision, and bootstrap
grammar behavior without parser guessing.

An ordinary relay MUST NOT transcode to another envelope format or reinterpret
a packet under another protocol profile. Reserializing the same envelope format
to apply permitted mutable forwarding fields such as hop limit is not
translation. An unsupported envelope format or protocol profile is dropped
without inner parsing or forwarding. The selected security profile must bind
the complete offered exact-pair set, both selected members, participant roles,
session-exchange identity, credential identities, freshness inputs, and every
accepted or rejection-relevant negotiation transcript element to the same
admitted peer session. Partial transcript binding, role ambiguity, or an
unauthenticated fallback is not a compatible mode. The concrete credential and
session construction remain unselected pending SG-002 and EXP-017.

Every later `LINK_CONTROL`, `MESH_CONTROL`, and `OPAQUE_ENDPOINT` packet must
carry the exact pair admitted for its ingress session before duplicate lookup,
state mutation, local dispatch, or forwarding. Every ordinary egress session
must be admitted under the same pair. Mismatch is a local rejection with no
network response; its stable layered outcome remains a selected-profile Agent
1/4 failure-oracle decision.

A change to envelope bytes/parsing creates a new envelope-format identifier; a
change to any outer field rule, processing order, message behavior, hop/
duplicate rule, criticality, target semantic, numeric limit, or state-machine
outcome creates a new protocol-profile identifier. Either change creates a new
exact pair/vector-set pin. This document does not define Protocol v1 major/minor
compatibility.

## Routing-visible message catalog

| Outer class | Scope | Types/status |
| --- | --- | --- |
| `LINK_CONTROL` | current one-hop adjacency/session; never relayed | `DISCOVERY_ADVERTISEMENT`, `SESSION_INIT`, `SESSION_ACCEPT`, `SESSION_REJECT`, `CAPABILITY_SNAPSHOT`, `HEARTBEAT` are proposed logical types |
| `MESH_CONTROL` | selected routing-profile scope | exact catalog awaits Agent 3; `ROUTE_ADVERTISEMENT` and `ROUTE_WITHDRAWAL` are candidates only |
| `OPAQUE_ENDPOINT` | selected routing target through zero or more relays | one generic relay-visible container; inner subtype is hidden by default |

Neighbor state is locally derived and is not automatically a wire message.
Duplicate suppression and TTL are processing behavior, not RELAY messages.

Unknown `LINK_CONTROL` or `MESH_CONTROL` types are not forwarded. An unknown
inner endpoint type does not affect foreign relay eligibility because the relay
does not inspect it.

## Endpoint-only catalog

| Inner family | Proposed logical types | Availability dependency |
| --- | --- | --- |
| `CHANNEL` | `SESSION_INIT`, `MEMBERSHIP_PROOF`, `SESSION_ACCEPT`, `SESSION_REJECT`, `MEMBERSHIP_UPDATE`, `SESSION_CLOSE` | RFC-0003/0006 plus Agent 4 |
| `PTT` | `REQUEST`, `GRANT`, `BUSY`, `RELEASE` | RFC-0007 plus Agent 3/4 and EXP-008 |
| `AUDIO_CONTROL` | `STREAM_START`, `STREAM_END` | RFC-0008 plus Agent 3/4/8 and EXP-013 |
| `AUDIO_MEDIA` | `FRAME` | RFC-0008 plus a future Agent 4-reviewed protection profile, codec, routing, and physical evidence |

Channel, authenticated principal, action subject, request, grant, stream,
codec, sender/epoch, and inner type are not relay-envelope fields by default.
EXP-007 and Agent 4 must approve any exception.

The proposed visible traffic-treatment registry is limited to
`BOUNDED_CONTROL` and `FRESH_MEDIA`. The first permits only message-specific
bounded control retry/replacement; the second prioritizes freshness and forbids
partition retention. Relays consume it only as an untrusted bounded scheduling
hint. Neither value grants authorization, proves an inner subtype, guarantees
priority/delivery, or makes content current. A future Agent 4-reviewed endpoint
protection profile must bind the value to the opaque payload, and an endpoint
rejects a mismatch with the selected inner semantics as `STATE_CONFLICT`. The
registry itself remains pending EXP-007 and Routing/Security review.

Plaintext or encoded audio MUST NOT occur in any discovery, mesh, channel, PTT,
stream-start, or stream-end control body. Encoded audio occurs only as
future-protected media content of `AUDIO_MEDIA.FRAME` after the relevant Agent 4
and audio gates exist.

## Logical outer envelope

The selected encoding must represent these semantics without ambiguous lengths,
duplicate fields, or criticality:

| Item | Proposed requirement |
| --- | --- |
| envelope format | exact supported parser generation |
| protocol profile | exact pre-v1 semantic profile |
| outer class/type | only routing-visible taxonomy above |
| packet identity | mandatory immutable token for forwardable packets |
| origin routing context | mandatory for forwardable packets; opaque duplicate/routing scope, not a node credential or source route |
| routing directive | profile-defined scope and optional opaque target; never generic next-hop/path fields |
| hop limit | bounded unsigned forwarding-distance limit |
| traffic treatment | at most a coarse, reviewed control/realtime hint; not authorization or guarantee |
| payload length | exact checked bound for the following payload |
| extensions | bounded critical/optional set |
| payload | outer control body or opaque endpoint container |

Exact field order, widths, byte order, numeric assignments, encoding,
canonicalization, extension container, frame/payload maxima, and outer-security
representation are deliberately absent pending EXP-002, EXP-014, Agent 3, and
Agent 4.

Every exact security profile must classify each outer element as link-local,
forwarding-immutable, hop-mutable, or transport-local and state which
authenticated scope covers it. Every immutable element that can affect delivery, duplicate state,
scheduling, interpretation, or authorization must be bound in complete
canonical form, including extension identifier, criticality, length, and value.
The mutable hop limit requires a separately reviewed update/admission contract;
until one exists, the draft makes no malicious-relay lifetime-enforcement
claim. EXP-002 and EXP-018 must test these classifications rather than infer
them from field placement.

A forwardable packet missing either `origin routing context` or `packet
identity` is `MALFORMED`.

Every selected routing target kind must define equality, stability/scope,
local-delivery predicate, propagation/fanout, no-route behavior, whether local
delivery ends forwarding, privacy exposure, and required security binding. A
channel credential or human label is not a routing target by convenience.

## Unknown and extension handling

- Unknown envelope format/profile: `UNSUPPORTED_ENVELOPE` or
  `UNSUPPORTED_PROFILE`; do not parse inner content or forward.
- Unknown outer class, forwarding scope, target kind, or traffic treatment:
  `UNSUPPORTED_OUTER_SEMANTICS`; do not forward.
- Unknown critical extension: `UNSUPPORTED_CRITICAL_EXTENSION`; do not
  forward.
- Unknown optional outer extension: ignore semantically and preserve unchanged
  across forwarding.
- Unknown optional field in a known outer message: ignore locally and preserve
  when forwarding.
- Unknown critical field in a known outer message: `(outer,
  UNSUPPORTED_CRITICAL_EXTENSION)`; reject that message.
- Unknown outer control type: `(outer, UNSUPPORTED_MESSAGE)`; reject and do not
  forward.
- Unknown inner family/profile inside an endpoint payload: relay remains
  eligible; after successful future security processing the local endpoint
  rejects as `(endpoint, UNSUPPORTED_MESSAGE)`. An unknown type inside a known
  family uses that family's `channel`, `ptt`, or `audio` layer.
- Unknown optional semantic field/extension in a known CHANNEL, PTT,
  AUDIO_CONTROL, or AUDIO_MEDIA message: ignore for local behavior only after
  successful channel-open and security-replay admission.
- Unknown critical semantic field/extension in a known inner message: reject
  before action authorization or state mutation as
  `(<channel|ptt|audio>, UNSUPPORTED_CRITICAL_EXTENSION)` according to its
  family. Security-profile, protection-format, algorithm, credential,
  authentication, and replay fields remain Agent 4-owned and fail at the
  `channel-security` boundary; they never downgrade to optional semantics.
- An optional inner semantic element cannot affect channel/principal/subject/
  security context, identity, authority, authorization predicates, replay/freshness,
  state-machine preconditions, or any emitted action. Any element that can must
  be critical or Agent 4-owned. "Ignored" never means outside future integrity
  coverage: Agent 4 must bind its presence and criticality so injection,
  stripping, or critical-to-optional rewriting cannot change behavior, without
  this Draft selecting how.
- Duplicate singular fields, impossible/truncated/overflowing lengths, illegal
  criticality, or ambiguous representations: `MALFORMED`.

EXP-002 must show that the chosen encoding can safely skip and preserve optional
extensions. Unknown security-critical extensions or algorithms never downgrade
to optional behavior.

## Hop-limit TTL

`draft/v0.x` proposes hop count, not wall-clock lifetime:

1. origin emits `hopLimit` in `1..profileMaximum`;
2. a locally eligible receiver MAY deliver at `1`;
3. forwarding requires a value greater than `1`;
4. every forwarded copy carries exactly the received value minus one;
5. all fanout copies receive the same decremented value;
6. local delivery does not decrement;
7. relays never increase/reset the value or re-identify the same forwarding
   instance to bypass it;
8. a non-local packet at `1` is `LIFETIME_EXHAUSTED`;
9. a forwarded copy changes only hop limit and transport framing; all other
   outer semantics and bytes are preserved under the selected encoding.

Hop limit is not capability validity, queue age, PTT validity, media freshness,
media time, or replay protection. Agent 3 supplies numeric values and reviews
the semantics through EXP-003/EXP-004. Agent 4 decides mutable-field protection;
this draft makes no adversarial enforcement claim.

## Packet duplicate behavior

Every forwardable packet carries all scoped key components. The duplicate key
is:

```text
(envelope format, protocol profile, origin routing context, packet identity)
```

The origin assigns one packet identity and every transport retransmission,
multipath copy, and relay preserves it. Inner operation/request/grant/stream/
sequence identities remain separate.

The experimental first-seen policy is:

- only an occurrence that passed required profile/session/outer admission can
  create authoritative duplicate state;
- an admitted occurrence becomes the first committed result only under the
  exact profile's no-effect/partial-action rules;
- only later matches against committed state produce neither effect and do not
  refresh retention;
- a later higher-hop copy is still a duplicate;
- detected conflicting authenticated immutable content is locally
  `PACKET_ID_CONFLICT` and is not accepted;
- every exact profile defines `minimumDuplicateCapacity` and exact
  `duplicateRetention`; an implementation declares a finite
  `configuredDuplicateCapacity` at or above that floor;
- saturation vectors use the declared configured capacity; larger conforming
  capacities may improve availability but cannot change first-seen/retention
  semantics or retain more than their declared bound.

Packet ID generation, collision/linkability, scope rollover, origin binding,
post-admission no-effect insertion, partial fanout, overload, and numeric cache
values remain joint Agent 1/3/4 decisions. Security replay operates
independently even when a replayed operation has a new outer packet identity.

## Capability snapshots

Capabilities are full replacement snapshots scoped to one admitted peer
session. A snapshot has a bounded unsigned non-wrapping generation, bounded
receipt-relative validity duration, and a bounded unique entry set. When no
high-water mark exists, the first valid snapshot establishes it with any value
permitted by the exact profile.

Each capability entry carries explicit criticality; absence is malformed, not
an implicit `false`. Any independently extensible parameter similarly has the
criticality semantics assigned by the exact profile. Encoding remains EXP-002.

- Higher generation atomically replaces prior state.
- While the current snapshot remains unexpired, same generation plus identical
  complete profile-canonical content is idempotent and does not refresh
  receipt-relative expiry. Equality includes unknown optional identifiers/
  parameters and criticality, even when ignored for local behavior; EXP-002
  selects the exact canonical rule.
- Lower generation is stale.
- While current state is unexpired, same generation plus different content is
  `STATE_CONFLICT` and not applied.
- Validity expiry withdraws all entries but retains the session generation
  high-water mark; expired canonical content need not be retained. After
  expiry, every generation less than or equal to the high-water mark is
  `STALE`, including same-generation formerly identical or changed content.
  Only a higher generation can establish new state. Session closure clears the
  high-water mark; generation exhaustion requires a new admitted session and
  never wraps.
- A higher snapshot that omits a capability withdraws it early.
- Unknown non-critical capabilities do not enable behavior.
- Unknown optional parameters are ignored; unknown critical parameters reject
  the atomic snapshot as `(capability, UNSUPPORTED_CRITICAL_EXTENSION)`. An
  unknown capability marked critical has the same result.
- Heartbeat does not silently extend snapshot validity.

Relay willingness defaults unavailable and is never inferred from platform or
device type. Capabilities can enable only optional behavior already registered
by the exact session profile; they cannot renegotiate or replace it. Raw
battery, thermal, data-plan, OS, and transport state remain local. The initial
identifiers, parameter types, bounds, validity, authenticity, privacy, and
dissemination await EXP-015 and Agent 3/4.

Before it creates authoritative state, the complete profile-canonical snapshot
must be integrity-bound to the admitted peer session and exact compatibility
pair, including generation, validity, all known and unknown content, and all
criticality. Immediate-peer authentication authorizes only that peer's own
session-scoped claim; a forwarded third-party capability or routing claim needs
a distinct issuer/delegation/admission contract from RFC-0005. No transitive
authority is inferred from transport adjacency.

## Outer processing order

1. **Transport admission:** enforce frame, ingress, buffering, and backpressure
   bounds.
2. **Bounded prefix parse:** select the envelope parser and validate declared
   lengths without unbounded payload allocation.
3. **Format/profile validation:** reject unsupported and impossible forms.
4. **Structural validation:** validate fields, class/type, extension
   criticality, target, traffic treatment, payload length, and hop range with no
   authoritative state mutation.
5. **Required security admissions:** obtain logically distinct exact-profile
   verdicts for the peer session, outer-envelope integrity/admission, and any
   routing/capability claim authority. A profile can combine their mechanics
   but cannot make immediate-peer authentication imply third-party claim
   authority. All required admissions precede authoritative duplicate state.
   Pre-admission anti-abuse counters can be bounded and non-authoritative only.
6. **Duplicate lookup:** query bounded authoritative state.
7. **Independent routing dispositions:** compute local eligibility and
   forwarding eligibility independently; both can be true.
8. **Resource reservation:** reserve bounded duplicate/local/forward work.
9. **Duplicate insertion:** commit before observable delivery/forward side
   effects.
10. **Local and/or forwarding action:** locally pass opaque endpoint bytes to
    the security boundary and/or emit preserved copies with decremented hop
    limit. A routing-profile-derived control update is a new semantic packet
    with a new packet identity; it cannot reset endpoint-data lifetime.
11. **Bounded observability:** record safe local categories/metrics only.

Stages 6 through 10 are atomic for one duplicate key. Each exact routing
profile defines duplicate-state admission for every post-admission no-effect
result (`LIFETIME_EXHAUSTED`, `POLICY_REJECTED`, `NO_ROUTE`, `RESOURCE_LIMIT`,
partial fanout, and enqueue failure) and defines which reservations form the
committed first-seen result. EXP-016 must exercise those choices and concurrent
arrivals.

Any stateful claim-freshness/replay verdict at stage 5 is provisional. The
exact profile pins its replay key/window, authoritative commit point, atomic
relationship to duplicate and route/capability state, and consumption for each
later no-effect/resource/partial-action outcome. Unauthenticated input never
advances that state, and an observable accepted effect cannot be rolled back.
The Draft deliberately defers the claim-consumption policy to EXP-018 and
profile-specific vectors.

No invalid transit packet automatically produces a network error. Any future
error message requires explicit authentication, amplification/rate bounds,
non-recursion, and Agent 4 failure-oracle review.

## Endpoint processing order

For local `OPAQUE_ENDPOINT` delivery only:

1. parse only the bounded security-profile header and select no more than the
   profile maximum candidate channel/epoch/key contexts;
2. run the profile-defined protected-record authentication/open and security-
   replay workflow in private provisional storage. Authentication/open and
   replay are logically distinct verdicts, but this specification does not
   prescribe separate calls or their construction-internal order;
3. replay state advances only for an authenticated record and is atomically
   checked/committed under concurrent receipt. If either verdict rejects,
   discard provisional results without plaintext exposure, action
   authorization, or inner state mutation;
4. only after both accept, release the authenticated principal, channel/
   security context, and permitted plaintext to the bounded inner parser;
5. validate profile/family/type/extensions and lengths, then reject unknown
   critical semantic elements locally, with no peer response, before
   authorization or state mutation;
6. obtain action authorization for the complete decoded action, explicitly
   separating authenticated principal from action subject and binding the
   permission verdict to the exact channel epoch, referenced grant/stream
   identifiers, and state revision; this verdict does not assert semantic
   state preconditions;
7. validate CHANNEL, PTT, or AUDIO state-machine preconditions, reserve bounded
   state, and atomically apply the authorized action;
8. expose only the permitted application event and safe diagnostics.

The proposed v0.x replay policy is consume-on-authenticated-record: once the
authenticated record commits replay state, a later decode, critical-extension,
authorization, or state-precondition failure does not roll it back. A semantic
retry uses a fresh protected record while retaining its operation identity.
This remains a Draft Agent 1/4 decision requiring canonical vectors and
EXP-019 crash/rollback evidence.

Relays never execute these steps.

## PTT control contract

The abstract PTT states are `IDLE`, `REQUESTING`, `TRANSMIT_GRANTED`,
`RECEIVING`, `RELEASING`, and `RECOVERING`.

Only an accepted `GRANT` in the validated
channel/principal/subject/arbitration context can
enter `TRANSMIT_GRANTED`. Request, silence, timeout, media, or UI optimism does
not grant the floor. Request/grant/release identities survive inner retries;
outer packet IDs do not. Duplicate operations are idempotent and do not extend
grant validity. A release cannot affect a newer/different grant. Audio cannot
create, extend, or transfer ownership.

Disconnected partitions cannot be promised one global speaker. The selected
EXP-008 model must define partition-local grant behavior, user presentation,
merge recovery, authority, term/lease, tie-break, fairness, retry, and bounds.
No missed audio is replayed after merge.

## Audio boundary

`STREAM_START` binds one stream identity and negotiated media profile to an
accepted current PTT grant. `FRAME` is separate opaque media data intended for
protection by a future Agent 4-reviewed profile, with a stream-relative sequence
and media-time context. `STREAM_END` closes only that stream and does not
replace PTT `RELEASE`.

Media sequence/time is not wall-clock time, hop limit, packet identity, replay
state, or a nonce unless a later reviewed security profile explicitly defines
the relation. Invalid/wrong-grant/wrong-stream, duplicate, replayed, or stale
frames drop within bounded state. No media is retained across partition,
reconnection, or suspension. Codec/profile, frame duration, sequence width,
stale threshold, jitter, FEC/redundancy, and latency remain EXP-013 decisions.

## Routing contract

The selected routing profile consumes only admitted outer packets, admitted
one-hop session/link events, capability snapshots, abstract monotonic time/
randomness, local abstract link metrics/policy, and reviewed `MESH_CONTROL`
bodies. It returns independent local and bounded forwarding dispositions.

The profile must define operating envelope, target kinds, routing-control
catalog, state freshness/replacement, metrics, tie-break, queues/retries,
fanout, no-route, capability withdrawal, loop/convergence, partition/merge,
numeric resource limits, and observability. No algorithm or target is selected
in `draft/v0.x`.

For one ingress processing event, no forwarding copy of that instance is
emitted on the event's ingress transport attachment. Whether another attachment
to the same peer/session is eligible remains profile-defined.

Relay withdrawal has three distinct effects: local policy withdrawal
immediately stops accepting new transit work; a direct neighbor applies an
admitted snapshot withdrawal/expiry to its local eligibility view; remote
reachability consequences propagate or expire only under the selected routing
profile. No network-wide instantaneous withdrawal is implied.

## Security dependencies

The draft requires six logically distinct future security dispositions:

1. peer-session admission and authenticated negotiation binding;
2. outer-envelope admission/integrity for routing and duplicate state;
3. routing/capability-claim issuer authority and replay/freshness admission;
4. local protected-record authentication/open;
5. security replay admission and atomic state commit;
6. channel/PTT/audio action authorization with principal/subject separation.

A reviewed standard construction may combine mechanics behind these logical
dispositions, but the protocol cannot infer one authority or success from
another. Candidate constructions, trust assumptions, relay visibility,
partition behavior, compromise consequences, and revocation limits are
documented in the security architecture; none is a selected Samband profile.

Every selected profile maps rejection at each disposition to an exact layered
outcome, state-consumption rule, peer-response rule, and redacted diagnostic.
`SECURITY_REJECTED` denotes failed authentication, integrity, required context,
or replay admission, or a profile-pinned generic coalescing necessary to avoid
an oracle. `POLICY_REJECTED` denotes an otherwise admitted/authenticated claim
or action refused solely by explicit authorization or local policy. If a
profile coalesces these, it must do so consistently and expose no alternate
distinguishing signal.

Agent 4 owns credentials, signatures, authentication, channel credentials,
encryption/protected-payload construction, keys/nonces/tags, epochs, associated
data, replay windows, compromise/revocation claims, downgrade protection,
metadata privacy, PTT authority/abuse, media binding, and failure oracles.

This specification selects none of them. "Opaque" means not parsed at the relay
boundary; it is not a security or privacy guarantee.

## Stable layered outcome vocabulary

Semantic vectors report one or more `(layer, result)` outcomes rather than one
ambiguous acceptance flag or implementation error string. Outer success says
only what the relay-visible envelope did; it never asserts that endpoint
security or an inner action succeeded:

- `OUTER_DISPATCHED_LOCAL`;
- `OUTER_FORWARDED`;
- `OUTER_DISPATCHED_LOCAL_AND_FORWARDED`;
- `STATE_APPLIED`;
- `INNER_ACTION_APPLIED`;
- `IDEMPOTENT_NO_CHANGE`;
- `FRAME_TOO_LARGE`;
- `MALFORMED`;
- `UNSUPPORTED_ENVELOPE`;
- `UNSUPPORTED_PROFILE`;
- `UNSUPPORTED_OUTER_SEMANTICS`;
- `UNSUPPORTED_CRITICAL_EXTENSION`;
- `UNSUPPORTED_MESSAGE`;
- `SECURITY_REJECTED`;
- `LIFETIME_EXHAUSTED`;
- `DUPLICATE`;
- `PACKET_ID_CONFLICT`;
- `STALE`;
- `POLICY_REJECTED`;
- `NO_ROUTE`;
- `RESOURCE_LIMIT`;
- `STATE_CONFLICT`.

The layer is one of `outer`, `session`, `capability`, `routing`,
`channel-security`, `endpoint`, `channel`, `ptt`, `audio`, `wire`, `security`, or
`scenario`. Each result is a local conformance observation at that layer and
does not require a peer-visible response or identical diagnostic text. A case
can therefore report outer forwarding together with a local inner
`UNSUPPORTED_MESSAGE` without contradiction.

`OUTER_*` success results and `UNSUPPORTED_OUTER_SEMANTICS` are valid only at
the `outer` layer. `STATE_APPLIED` is valid only at `session`, `capability`, or
`routing`. `INNER_ACTION_APPLIED` is valid only at `channel`, `ptt`, or `audio`.

## Canonical vectors

The draft machine-readable carrier is defined in
[`../test-vectors/FORMAT.md`](../test-vectors/FORMAT.md) and
[`../test-vectors/vector-set.schema.json`](../test-vectors/vector-set.schema.json).

Semantic/negative processing vectors can be written now. Exact wire bytes wait
for EXP-002. Routing scenarios wait for an Agent 3 experimental profile.
The security-vector requirements are now defined, but real cryptographic
fixtures wait for construction/profile selection and public-standard
provenance. Released vector sets are immutable; draft sets remain review
material and make no compatibility or security claim.

## Deliberately deferred decisions

- wire encoding, field widths/order/codes, canonicalization, and frame maxima;
- concrete profile identifiers and numeric limits;
- packet ID/origin/target constructions and security binding;
- routing target, algorithm, metrics, control catalog, convergence, and queues;
- identity credentials, authentication/signatures, channel membership, payload
  protection, replay, epochs, and metadata mitigations;
- PTT authority/arbitration/lease/fairness/partition algorithm;
- codec, media profile, frame/timestamp parameters, jitter/FEC, and latency;
- Protocol v1 compatibility and stability.

## Governing drafts and evidence

- [`RFC-0001`](../../docs/rfc/RFC-0001-samband-network-model.md)
- [`RFC-0002`](../../docs/rfc/RFC-0002-node-identity.md)
- [`RFC-0003`](../../docs/rfc/RFC-0003-channel-identity-and-membership.md)
- [`RFC-0004`](../../docs/rfc/RFC-0004-relay-envelope.md)
- [`RFC-0005`](../../docs/rfc/RFC-0005-mesh-routing.md)
- [`RFC-0006`](../../docs/rfc/RFC-0006-encrypted-channel-payload.md)
- [`RFC-0007`](../../docs/rfc/RFC-0007-ptt-arbitration.md)
- [`RFC-0008`](../../docs/rfc/RFC-0008-audio-transport.md)
- [`shared-contract registry`](../../docs/architecture/shared-contracts.md)
- [`threat model`](../../docs/security/threat-model.md)
- [`node identity security`](../../docs/security/node-identity.md)
- [`channel security`](../../docs/security/channel-security.md)
- [`relay security`](../../docs/security/relay-security.md)
- [`discovery privacy`](../../docs/security/discovery-privacy.md)
- [`security gates`](../../docs/security/review-gates.md)
- [`experiment backlog`](../../docs/research/experiment-backlog.md)
