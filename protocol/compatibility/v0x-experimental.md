# Protocol v0.x Experimental Compatibility Model

## Status

Draft and non-normative. No released Samband compatibility profile, profile ID,
wire encoding, compatible implementation, or stability promise exists.

The string `draft/v0.x` is used only by review documentation and Draft semantic
vectors. It MUST NOT be advertised as a released wire profile.

## Exact pre-v1 compatibility pairs

Every future v0.x compatibility selection is the ordered pair `(envelope
format, protocol profile)`. The envelope format pins byte framing/parser
generation and its limits. The protocol profile independently pins one exact
set of:

- message/type and extension registries;
- processing order and local outcome semantics;
- routing profile, target kinds, hop/duplicate rules, and numeric bounds;
- required and optional capabilities;
- security profile and negotiation binding after Agent 4 review;
- CHANNEL/PTT/AUDIO state semantics included in its scope;
- canonical vector-set version.

Neither identifier contains or implies the other. The vector set and any
conformance claim pin both members explicitly.

Both identifiers are opaque. A greater-looking version is not automatically
newer, preferred, compatible, or safe. Pre-session discovery offers a bounded
set of exact `(envelope format, protocol profile)` pairs using a supported
format's bounded bootstrap grammar. The initiator selects exactly one pair from
the latest offer using local policy and one session-exchange identity. The
responder can only echo that pair and identity or reject; it cannot substitute
a different intersection. The context is authoritative only after both roles
confirm the same pair and the selected profile's Agent 4 admission succeeds.
Simultaneous initiation, retry, stale-offer, and collision behavior are pinned
by the exact bootstrap profile rather than numeric ordering.

No ordinary node or relay transcodes a packet to another envelope format or
reinterprets it under another protocol profile. Same-format reserialization to
apply a permitted mutable forwarding field such as hop limit is not
translation. Peers with no exact pair intersection do not establish an
admitted session. A node attached to neighbors using different selected pairs
keeps those session/route domains separate unless a future gateway RFC
explicitly defines reviewed translation.

Every post-bootstrap packet pair must equal the pair admitted for its ingress
session before duplicate lookup, state mutation, local dispatch, or forwarding.
Every ordinary egress session selected for that packet must have the same pair.
A supported but session-mismatched pair is rejected locally with no network
response; the selected profile pins its safe layered outcome. It is never
silently reinterpreted or bridged between the separated domains.

## Experimental change rule

Pre-v1 pairs can change incompatibly. A byte/framing/parser, field wire
representation, or canonical serialization change creates a new
envelope-format identifier. A peer-visible or state-machine semantic change
creates a new protocol-profile identifier. A change spanning syntax and
semantics changes both members. Any such change creates a new exact-pair and
vector-set pin. Semantic changes include:

- required/optional field presence, criticality, valid range, or
  interpretation, excluding its byte representation;
- unknown-version/type/field behavior;
- packet identity, hop limit, duplicate, or cache semantics;
- routing target, message, metric, disposition, queue, or convergence behavior;
- capability replacement, freshness, withdrawal, or identifier semantics;
- channel, PTT, media, replay, or authorization behavior;
- numeric resource or timing bounds;
- stable local conformance outcomes.

Released profile documents and vector sets are immutable. Corrections use a new
identifier with explicit supersession/provenance.

## Negotiation boundary

The Draft protocol proposes a bounded link-local exact-pair offer and
selection. A real security profile must bind the complete offered exact-pair
set, both selected members (`envelope format` and `protocol profile`),
participant roles, session-exchange identity, credential identities,
freshness inputs, and every accepted or rejection-relevant transcript element
to the same admitted peer session. Partial transcript binding, role ambiguity,
silent fallback, or accepting a security profile different from the one pinned
by the selected protocol profile is incompatible. Authentication, downgrade
prevention, retry/resumption behavior, failure visibility, and replay remain
open SG-002/EXP-017 decisions before any real profile can use the negotiation.

Discovery offers alone are untrusted hints. They cannot create authoritative
neighbor, capability, route, duplicate, membership, PTT, or media state.

## Unknown behavior

- Unknown envelope format: bounded prefix rejection, no payload parse/forward.
- Unknown exact profile: reject, no translation or best-effort fallback.
- Unknown outer class/scope/target/treatment: reject as
  `UNSUPPORTED_OUTER_SEMANTICS`.
- Unknown critical outer extension: reject as
  `UNSUPPORTED_CRITICAL_EXTENSION`.
- Unknown message type within a known `LINK_CONTROL` or `MESH_CONTROL` class:
  reject as outer-layer `UNSUPPORTED_MESSAGE`; do not forward.
- Unknown optional outer extension: ignore semantically and preserve while
  forwarding when the selected encoding proves safe preservation.
- Unknown optional field in a known forwardable outer control message: ignore
  locally and preserve while forwarding; unknown critical fields reject.
- Unknown inner type inside an endpoint payload: relays remain eligible; the
  local endpoint rejects only after successful future security processing.
- Unknown optional semantic field/extension in a known inner family: ignore
  locally only after channel-open and replay admission. Unknown critical
  semantic fields/extensions reject at the `channel`, `ptt`, or `audio` layer
  as `UNSUPPORTED_CRITICAL_EXTENSION` before authorization/state mutation.
  An optional element cannot affect identity, context, authority,
  authorization, replay/freshness, state preconditions, or emitted actions.
  Agent 4 must bind presence and criticality under future integrity coverage.
  Security-profile fields remain Agent 4-owned at `channel-security` and never
  downgrade to optional behavior.
- Unknown non-critical capability: does not enable behavior. An unknown
  capability or parameter marked critical rejects the atomic snapshot as
  `(capability, UNSUPPORTED_CRITICAL_EXTENSION)`.
- Unknown security-critical version/algorithm/extension: fail closed under the
  Agent 4-reviewed security profile.

## Support and conformance claims

A future implementation can claim support for an experimental profile only if
it publishes:

- exact implementation revision;
- exact envelope-format, protocol-profile, and vector-set identifiers;
- pass/fail results for every mandatory positive and negative vector;
- deviations and unsupported optional features;
- toolchain/runner revisions;
- evidence label: static, simulated runtime, physical runtime,
  interoperability, or security review.

Passing Draft `draft/v0.x` vectors is design feedback, not a compatibility or
security claim. Bindings over one core do not count as independent protocol
implementations.

## Protocol v1

Protocol v1 major/minor compatibility, deprecation periods, extension registry,
independent implementation requirements, and security claims remain governed by
future Accepted RFCs and the M7 gate. This Draft deliberately does not freeze
them.

## References

- [`v0.x experimental specification`](../spec/v0x-experimental.md)
- [`canonical vector format`](../test-vectors/FORMAT.md)
- [`RFC-0004`](../../docs/rfc/RFC-0004-relay-envelope.md)
- [`interoperability strategy`](../../docs/architecture/interoperability-strategy.md)
- [`node identity security`](../../docs/security/node-identity.md)
- [`discovery privacy`](../../docs/security/discovery-privacy.md)
- [`security review gates`](../../docs/security/review-gates.md)
