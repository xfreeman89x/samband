# Samband Canonical Test-Vector Format

## Status

Draft format version `samband-vector-set/0.1-draft`. Agent 1 defines the
protocol-facing content, and Agent 4 defines the security-boundary and future
security-fixture requirements. Agent 9 Ecosystem review is still required
before the format or any vector set is released as canonical.

This JSON carrier is independent from the future Samband wire encoding. Choosing
JSON for public fixtures does not select JSON, JSON Schema, or text encoding for
Samband packets.

The machine-readable schema is
[`vector-set.schema.json`](vector-set.schema.json). The current illustrative
semantic set is [`draft-v0x-core.json`](draft-v0x-core.json). Its `draft` status
means cases can change during RFC review and are not compatibility promises.
The current schema accepts `draft` sets only. A later versioned schema is
required before a set can be marked `released` or `superseded`.

## File rules

- Files are UTF-8 without BOM and end with one newline.
- JSON object member order has no semantic meaning.
- Duplicate JSON member names are invalid.
- Protocol integers are JSON integers only when their selected range is safely
  interoperable across target parsers; larger future values use an explicitly
  typed decimal string defined by the governing profile.
- Exact binary fixtures use lowercase hexadecimal with no separators plus an
  explicit byte length. Exact wire fixtures do not exist until EXP-002 selects
  an encoding.
- Real credentials, private keys, channel secrets, captured traffic, personal
  data, and raw/encoded human audio are prohibited.
- Synthetic security inputs use named dispositions, never invented signatures,
  tags, nonces, keys, or ciphertext.

## Vector-set object

Every file contains one vector set with:

| Member | Meaning |
| --- | --- |
| `formatVersion` | exact vector carrier/schema version |
| `vectorSetId` | stable set identifier |
| `status` | `draft` in this schema; later schemas may add released lifecycle states |
| `envelopeFormat` | exact semantic-envelope label pinned by this set |
| `protocolProfile` | exact protocol profile or the non-wire `draft/v0.x` label |
| `governingReferences` | RFC/spec sections that define the set |
| `supersedes` | prior vector-set IDs replaced as a whole; empty for the first set |
| `vectors` | non-empty ordered cases; order aids review but cases do not depend on prior cases |

The illustrative set pins both independent version axes: `envelopeFormat` is
`draft/semantic-envelope` and `protocolProfile` is `draft/v0.x`. Neither is a
wire assignment. The present schema requires `status: "draft"`. Future released
vector sets are immutable: a correction will create a new set/case ID and use
the set-level or case-level `supersedes` list as appropriate; it will not
rewrite a released file. Draft sets are mutable review artifacts and cannot
support a conformance claim.

## Common case object

Every case contains:

| Member | Requirement |
| --- | --- |
| `id` | stable ASCII identifier unique across Samband vector sets |
| `layer` | primary semantic area named in the Layers section |
| `classification` | positive or negative |
| `purpose` | concise behavior under test |
| `governingReferences` | exact documents/sections for traceability |
| `requiredFeatures` | draft harness features needed; empty when none |
| `initialState` | complete relevant semantic state before the case |
| `input` | packet/message/state input independent from implementation types |
| `orderedEvents` | deterministic virtual-time events, including synthetic verdicts |
| `expected` | layered outcomes, final observable state, emissions, and safe observations |
| `wire` | conditional exact-byte object, required only when `layer` is `wire` |
| `resourceBounds` | maximum state growth, emitted packets, and payload materialization |
| `provenance` | hand-authored/generated source and revision |
| `supersedes` | prior case IDs replaced by this case |

Required common fields not relevant to a case are represented by empty
arrays/objects instead of being given hidden defaults. Conditional fields such
as `wire` are omitted when their condition does not apply. This carrier defines
event action names; the governing profile defines semantic names used inside
`initialState`, `input`, event `data`, expected state, and emissions.

The JSON Schema validates the carrier and the action-specific synthetic event
payloads. A profile-aware semantic runner MUST additionally validate pair-pin
equality, complete fixture/profile objects, profile numeric bounds, event order
and dependencies, ingress/egress constraints, structured duplicate-key
equality, exact logical emission equality, resource high-water assertions, and
layer-specific state shapes. Passing JSON Schema alone is not a vector pass.

## Layers

- `outer`: envelope validation, profile, extension, hop, packet identity,
  duplicate, local/forward processing.
- `session`: adjacency/session negotiation and selected-profile behavior.
- `capability`: snapshot generation, replacement, expiry, withdrawal, unknown
  behavior, and bounds.
- `routing`: target/control/disposition behavior after Agent 3 selects an
  experimental profile.
- `channel-security`: the interface between channel processing and a future
  Agent 4-reviewed security profile.
- `endpoint`: an inner family/profile cannot be selected after successful
  channel-security processing.
- `channel`: endpoint state behavior with synthetic security results until
  Agent 4 review.
- `ptt`: request/grant/busy/release state behavior.
- `audio`: stream-control/media state and freshness behavior; never human audio.
- `wire`: exact bytes and decoded meaning after EXP-002.
- `security`: reviewed standard public fixtures after Agent 4.
- `scenario`: deterministic topology, seed, link events, and expected metrics.

## Draft semantic outer fixture profile

Every Draft outer-semantic case declares this complete fixture context in
`initialState.fixtureProfile` and repeats the selected envelope/profile labels
in its packet input:

| Member | Draft fixture value |
| --- | --- |
| `envelopeFormat` | `draft/semantic-envelope` |
| `protocolProfile` | `draft/v0.x` |
| `maximumFrameBytes` | `128` fixture-declared bytes |
| `maximumOpaquePayloadBytes` | `64` fixture-declared bytes |
| `maximumOuterExtensions` | `4` |
| `maximumOuterExtensionValueBytes` | `32` fixture-declared bytes |
| `maximumRoutingDirectiveBytes` | `64` fixture-declared bytes |
| `profileMaximumHopLimit` | `8` |
| `minimumDuplicateCapacity` | `4` |
| `configuredDuplicateCapacity` | `8` |
| `duplicateRetentionTicks` | `100` |
| `duplicateScopeSource` | `synthetic.origin-routing-context-v1` |
| `originRoutingContextRequired` | `true` |
| `routingDirectiveRequiredForOpaqueEndpoint` | `true` |
| `maximumForwardingFanout` | `2` |
| `maximumEgressWorkUnits` | `2` |
| `availableIngressPacketReservations` | `1` |
| `availableIngressByteReservations` | `128` |
| `availableLocalDispatchPacketReservations` | `1` |
| `availableLocalDispatchByteReservations` | `128` |
| `availableForwardingQueuePacketReservations` | `2` |
| `availableForwardingQueueByteReservations` | `256` |
| `reservationScope` | `synthetic.shared-across-traffic-treatments` |
| `egressActionModel` | `synthetic.directional-peer-link-and-shared-medium-v1` |
| `sharedMediumListenerAccounting` | `synthetic.explicit-directional-peer-link-list-v1` |
| `routingTargetKind.identifier` | `synthetic.test-opaque-target` |
| `routingTargetKind.testOnly` | `true` |

Each such case also names the distinct
`initialState.ingressAttachment`, `initialState.ingressPeerSession`, and
`initialState.ingressDirectionalPeerLink`. If its input reaches routing,
`routingDirective.targetKind` is
`synthetic.test-opaque-target`, `routingDirective.testOnly` is `true`, and the
opaque target is fixture data. A peer-unicast action never targets the exact
ingress directional peer link. The fixture permits a different admitted peer
link on the same attachment and a shared-medium action whose explicit listener
set may include the ingress peer. Every `OPAQUE_ENDPOINT` fixture input carries
that structurally valid routing directive even when a later extension or
duplicate stage rejects the packet. Field presence never depends on a later
processing disposition.
All fixture strings used in byte-bounded members are printable ASCII, and each
case supplies its declared frame, payload, extension-value, and routing-
directive lengths. These are semantic fixture counters, not a Samband wire
encoding or measured serialization.

Reservation members are currently available units at case start, distinct from
configured maxima. Packet reservations count whole logical emitted packets;
byte reservations count the fixture-declared whole frame once per egress
action. They are one synthetic pool shared across traffic treatments. Every
egress action declares positive `fanoutUnits` and `workUnits`. Peer unicast has
one explicit peer session/directional link and one fanout unit. A shared-medium
action declares the complete fixture listener set as admitted peer-session/
directional-peer-link pairs; its fanout units equal that set's size, while its
work units account for the single medium emission. Receiver-side processing is
charged when each resulting receipt enters the common ingress pipeline. The sum
of fanout units cannot exceed
`maximumForwardingFanout`, and the sum of work units cannot exceed
`maximumEgressWorkUnits`. `duplicateAccounting` pins duplicate lookup per
resulting receiver occurrence: one for peer unicast and one for each declared
shared-medium listener. `loopAccounting` pins the common hop-limit/duplicate
checks while leaving any additional candidate-specific loop control explicit in
that candidate profile.
Local dispatch similarly consumes one packet and its declared frame bytes.
Every illustrative success fits wholly; no partial-fanout or enqueue-failure
policy is selected. These limits close stage-1/stage-8 fixtures without
selecting an Agent 3 target model, route, metric, queue, or fanout policy.

Outer duplicate keys use one object with exactly these four members:
`envelopeFormat`, `protocolProfile`, `profileDuplicateScope`, and
`packetIdentity`. The same object shape is used for retained entries, lookup
observations, and additions. It is a semantic tuple, not a delimiter-joined
string or a selected wire encoding; hop limit is never part of the key. This
fixture sets `duplicateScopeSource` to
`synthetic.origin-routing-context-v1`, requires an input
`originRoutingContext`, and maps that value unchanged to
`profileDuplicateScope`. Another exact profile may derive duplicate scope from
different reviewed inputs and need no distinct wire origin field.

Each expected outer emission is an exact object of the form
`{ "action": { ... }, "packet": { ... } }`. `action` repeats the complete
profile-defined peer-unicast or shared-medium egress action. `packet` repeats
every logical input field, including one synthetic opaque-payload reference,
with only the profile-permitted hop-limit change. Emission arrays follow the
exact order of the synthetic routing disposition's `egressActions`. Exact here
means logical object equality, not wire-byte equality; EXP-002 must later prove
byte preservation for immutable fields and unknown optional extensions.

These labels and numbers exist only to make semantic fixtures closed and
deterministic. They are not assigned wire values, do not define a real routing
target, and select no topology, metric, convergence behavior, forwarding
algorithm, or other Agent 3 routing model. They MUST NOT be advertised as a
released profile or implemented as production routing semantics.

Capability-semantic cases that use the relay-willingness fixture identifier
declare `synthetic.test-relay-forwarding` in
`initialState.fixtureCapabilityRegistry` with `testOnly: true`. That identifier
is registered only for these fixtures. It is not a Samband capability registry
assignment and selects no Agent 3 behavior. Each case also declares this
`initialState.fixtureCapabilityProfile`:

| Member | Draft fixture value |
| --- | --- |
| `maximumSnapshotEntries` | `4` |
| `maximumParametersPerEntry` | `4` |
| `maximumValidityTicks` | `200` |
| `maximumGeneration` | `255` |
| `canonicalEquality` | `synthetic.logical-snapshot-v1` |

The fixture equality compares `generation`, `validFor`, entry identifiers,
explicit `critical` values, and all parameter values as logical JSON content;
object member order is irrelevant and the bounded entry set is compared by
identifier. Omitting `critical` is invalid; it is not another spelling of
`false`. It
excludes receipt time, computed expiry, and local session state. This closes the
semantic cases only; it selects no wire canonicalization, digest, signature, or
cryptographic primitive.

## Event model

`orderedEvents` uses non-negative integer virtual ticks. A tick is an abstract
ordering unit with no implied wall-clock duration. A runner first installs the
complete `initialState`, without deriving any hidden state. It then executes
events in ascending `at` order; equal-time events execute in their array order.
Files must already store events in that execution order.

At the start of a tick, before its events execute, the runner expires every
entry for which `expiresAtVirtualTime <= at`. An admitted value received at tick
`T` with `validFor: N` has candidate expiry `T + N` and is live only while the
current virtual time is less than that expiry. A governing profile may reject a
particular `validFor` range, but it cannot change this vector-time arithmetic.

Every case has exactly one `injectInput` event. That event submits the case's
top-level `input` at its `at` tick and has empty `data`. Earlier same-tick events
install synthetic dispositions used while processing that input; later events
observe or stimulate state after receipt. Wall-clock sleeps, host timestamps,
map iteration order, and unseeded randomness cannot affect expected results.

### Draft feature and event vocabulary

The `0.1-draft` carrier accepts only these event actions. The eight synthetic
actions are test-harness decisions, not protocol messages and not evidence of
authentication, authorization, confidentiality, or integrity:

| Required feature | Event action | Meaning |
| --- | --- | --- |
| none | `injectInput` | submit the top-level `input`; `data` is empty |
| `synthetic-session-admission` | `syntheticSessionAdmission` | supply an admitted/rejected peer-session disposition |
| `synthetic-outer-admission` | `syntheticOuterAdmission` | supply the future outer security/admission hook result |
| `synthetic-claim-admission` | `syntheticClaimAdmission` | supply routing/capability claim-authority and security-freshness admission independently from immediate-peer/outer admission |
| `synthetic-routing-disposition` | `syntheticRoutingDisposition` | supply local-delivery eligibility and selected bounded egress actions |
| `synthetic-channel-open` | `syntheticChannelOpen` | supply the future protected-container validation/open result and provisional fixture channel/authenticated-principal/security contexts; it does not expose inner plaintext by itself |
| `synthetic-security-replay` | `syntheticSecurityReplay` | supply the future security-replay result separately from channel open; never media/application freshness |
| `synthetic-inner-decode` | `syntheticInnerDecode` | expose fixture-only decoded inner semantics after open and replay admission |
| `synthetic-action-authorization` | `syntheticActionAuthorization` | supply the future endpoint action-authorization result |

Event `data` objects have no unspecified members. Their Draft contracts are:

- `injectInput`: exactly `{}`;
- session admission, outer admission, claim admission, security replay, and
  action authorization: `disposition` is `ACCEPTED` or `REJECTED`, with
  `securityClaim: false`; synthetic claim acceptance says only that the fixture
  may continue to semantic generation/revision checks and does not make a
  route, metric, or capability truthful;
- routing disposition: bounded unique `egressActions`, independent boolean
  `eligibleForLocalDelivery` and `eligibleForForwarding`, and
  `securityClaim: false`; forwarding `true` requires at least one action and
  `false` requires none. Each action names its attachment and explicit
  fanout/work/duplicate/loop accounting; peer unicast names its one admitted
  listener peer session and directional peer link, while shared-medium names a
  bounded listener set of those pairs;
- channel open: `disposition`, `plaintextExposed: false`, and
  `securityClaim: false`; `ACCEPTED` additionally returns bounded provisional
  `channelContext`, `authenticatedPrincipalContext`, and `securityContext`,
  while `REJECTED` returns none of them; the principal is not an implicit
  action subject;
- inner decode: bounded `innerFamily` and `innerType`, `disposition` in
  `ACCEPTED`, `MALFORMED`, `UNSUPPORTED_MESSAGE`, or
  `UNSUPPORTED_CRITICAL_EXTENSION`, and `securityClaim: false`.

Each synthetic action's `data` includes `securityClaim: false`. A vector using
one of those actions lists its paired feature in `requiredFeatures`, and every
listed synthetic feature has at least one matching event. The schema enforces
both directions; `injectInput` is the only unpaired action. Unknown actions or
mismatched feature/action pairs are invalid under this draft format.

A capability or future `MESH_CONTROL` case that could mutate authoritative
claim-derived state supplies `syntheticClaimAdmission` independently from
peer-session and outer admission. A rejected claim cannot create or refresh
generation, revision, route, capability, duplicate, or claim-replay state.

Channel/authenticated-principal/security contexts and any opened bytes remain
provisional after
`syntheticChannelOpen`; a harness MUST NOT install or expose them until
`syntheticSecurityReplay` is also `ACCEPTED`. Only then is fixture inner decode
eligible. A rejected replay disposition ends processing before
`syntheticInnerDecode` or `syntheticActionAuthorization`, exposes no plaintext,
mutates no inner state, and emits no endpoint action.

Security-gated semantic cases can include events such as:

```json
{
  "at": 0,
  "action": "syntheticOuterAdmission",
  "data": {
    "disposition": "ACCEPTED",
    "securityClaim": false
  }
}
```

Such an event tests processing boundaries only. A released real-security vector
must instead cite the accepted security profile and public standard fixtures.

## Stable outcomes

`expected.outcomes` is a non-empty array of unique `{ "layer", "result" }`
objects. It records each independently observable processing boundary. An outer success
means only that the envelope was dispatched locally, forwarded, or both; it
never means an inner message or security decision was accepted. A combined
endpoint/relay case can therefore report outer forwarding and a separate local
channel rejection.

Success or no-change results are:

- `OUTER_DISPATCHED_LOCAL`;
- `OUTER_FORWARDED`;
- `OUTER_DISPATCHED_LOCAL_AND_FORWARDED`;
- `STATE_APPLIED`;
- `INNER_ACTION_APPLIED`;
- `IDEMPOTENT_NO_CHANGE`.

Stable failure or rejection results are:

- `FRAME_TOO_LARGE`;
- `MALFORMED`;
- `UNSUPPORTED_ENVELOPE`;
- `UNSUPPORTED_PROFILE`;
- `UNSUPPORTED_CRITICAL_EXTENSION`;
- `UNSUPPORTED_MESSAGE`;
- `UNSUPPORTED_OUTER_SEMANTICS`;
- `SECURITY_REJECTED`;
- `LIFETIME_EXHAUSTED`;
- `DUPLICATE`;
- `PACKET_ID_CONFLICT`;
- `STALE`;
- `POLICY_REJECTED`;
- `NO_ROUTE`;
- `RESOURCE_LIMIT`;
- `STATE_CONFLICT`.

A synthetic event's `REJECTED` disposition is not itself an interoperable
outcome. Each case's `expected.outcomes` pins the applicable layer and result.
`SECURITY_REJECTED` denotes failed required authentication, integrity, context,
or replay admission, or an exact-profile generic coalescing required to avoid
an oracle. `POLICY_REJECTED` denotes an otherwise admitted/authenticated claim
or action refused solely by explicit authorization or local policy. A future
profile that deliberately coalesces those results must pin the choice and must
not expose the hidden distinction through responses, timing requirements, or
diagnostics.

Outcome layers are `outer`, `session`, `capability`, `routing`,
`channel-security`, `endpoint`, `channel`, `ptt`, `audio`, `wire`, `security`, and
`scenario`. Results are conformance categories, not required log strings or
peer-visible errors. `expected.observations` contains only safe semantic facts;
it cannot require secrets, endpoint plaintext, encoded audio, or unnecessary
stable identifiers in diagnostics.

`STATE_APPLIED` is limited to successful `session`, `capability`, or `routing`
state transitions. `INNER_ACTION_APPLIED` is limited to successful `channel`,
`ptt`, or `audio` actions. The schema also limits every `OUTER_*` success and
`UNSUPPORTED_OUTER_SEMANTICS` to the `outer` layer.

`UNSUPPORTED_OUTER_SEMANTICS` is the stable outer-layer result for a
structurally valid but unknown outer class, scope, target form, or traffic
treatment. An unknown message type within a known `LINK_CONTROL` or
`MESH_CONTROL` class is instead outer-layer `UNSUPPORTED_MESSAGE`. An unknown
inner message is also `UNSUPPORTED_MESSAGE`, but at the applicable endpoint
layer, and does not by itself prevent an independently eligible opaque relay
path. An entirely unknown inner family/profile uses
`(endpoint, UNSUPPORTED_MESSAGE)`; an unknown type inside a known family uses
that family's `channel`, `ptt`, or `audio` layer.

An unknown critical outer field or extension is outer-layer
`UNSUPPORTED_CRITICAL_EXTENSION`. An unknown critical capability identifier or
critical capability parameter rejects its atomic snapshot as capability-layer
`UNSUPPORTED_CRITICAL_EXTENSION`. Optional unknown behavior is governed
separately and cannot be inferred from this critical result.

## Resource assertions

Each case states conservative maxima for:

- authoritative state entries added;
- packets emitted;
- payload bytes materialized by the tested layer.

`notes` explains other relevant bounds, such as no cache-retention refresh or
no inner-payload parse. Later profile-specific schemas can add measured metrics,
but cannot remove the common resource-safety assertions.

## Wire vectors

After EXP-002, a `wire` case additionally includes:

```json
{
  "wire": {
    "representation": "lowercase-hex",
    "byteLength": 4,
    "bytes": "000102ff"
  }
}
```

The draft schema requires this object whenever `layer` is `wire`, rejects
it on every non-`wire` case, rejects uppercase or odd-length hexadecimal, and a
runner additionally verifies that `byteLength` equals the decoded hexadecimal
length.

The case also provides decoded logical meaning, expected re-encoding where
canonicalization is required, and a stable rejection outcome for negative
bytes. Truncation, overflow, duplicate fields, unknown optional/critical
extensions, unsupported versions, and allocation bounds are mandatory.

## Scenario vectors

Routing/simulator cases include an explicit protocol/routing profile, seed,
topology, node capabilities, virtual clock, ordered link/policy events, injected
packets, expected semantic event log, and metric/state high-water bounds.
Host performance measurements remain separate and cannot alter correctness.
Ingress and egress topology state distinguishes attachment, admitted peer
session, and directional peer link. Shared-medium cases enumerate fixture
listener peer links and assert recipient-fanout, work, duplicate-receipt, and
loop bounds.

## Security vectors

Real security vectors are added only after the governing RFC selects a reviewed
standard construction and exact security profile. The `0.1-draft` carrier
therefore accepts only the explicitly synthetic dispositions above. It does not
have a generic object into which an implementation can hide an ad hoc cipher,
key schedule, nonce rule, or replay algorithm.

A versioned profile-specific security-vector schema must extend this common
carrier and require, at minimum:

- the exact envelope format, protocol profile, security profile, construction,
  suite, and standard/revision references;
- fixture origin, license/provenance, generator revision, and whether the case
  is copied from a published standard vector or is a Samband adaptation;
- participant roles, published synthetic credential/key material, labeled
  fixed randomness where deterministic injection is supported, and complete
  initial session/channel/epoch/membership/replay state;
- exact transcript bytes, protected-record bytes, immutable associated outer
  context, and expected decoded logical values in unambiguous lowercase-hex or
  another representation pinned by that schema;
- exact success output or stable layered rejection, complete post-state,
  emissions, `plaintextExposed`, and bounded candidate-key, allocation, state,
  and work assertions;
- explicit separation among outer duplicate, handshake/control replay,
  protected-record replay, PTT operation validity, and media freshness.

Mandatory negative coverage includes transcript alteration and role swap,
exact-pair downgrade/substitution, credential mismatch, unknown critical
security elements, corrupted authentication data, wrong or ambiguous channel/
epoch/key selection, duplicate and out-of-window records, excessive forward
gaps, principal/subject authorization mismatch, stale membership/removal state,
partitioned epoch forks, crash/restore rollback, truncation, and resource-limit
exhaustion. A negative case exposes no endpoint plaintext and produces no
unauthenticated automatic error.

All keys, credentials, identifiers, plaintext, and randomness in repository
vectors are synthetic and public. Human audio, real identities, production
secrets, private captures, and environment-specific paths are forbidden.
Imported expected values remain attributable to their upstream source;
Samband-specific wrapping or associated-context adaptations are separately
identified and reproducible. Known-answer vectors demonstrate deterministic
interoperability for their pinned inputs; they do not establish side-channel
resistance, randomness quality, secure storage, compromise recovery, metadata
privacy, or overall protocol security. Those require distinct review and
experiment evidence.
