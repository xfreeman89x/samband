# Samband v0.x Experimental Simulation Profile

## Status and authorization

Profile revision: `wave1-sim-v0.1`.

This document authorizes a bounded implementation for deterministic Wave 1
simulation and routing experiments. It is an **EXPERIMENTAL CONTRACT** and is:

```text
NON-PRODUCTION
NON-SECURITY
EXPERIMENTAL ONLY
```

It is not an Accepted Samband Protocol specification, a wire-format or
compatibility promise, a routing selection, production cryptography, or
permission to begin audio or mobile networking. Passing this profile supports
only a simulated-runtime evidence claim naming this exact revision.

This profile is the limited implementation subset authorized by the
[`Wave 0 Integration Review`](../../docs/architecture/wave0-integration-review.md).
The broader [`v0.x synthesis`](v0x-experimental.md) and all RFCs remain Draft.

## Experiment objective

The profile exists to let the portable-core, routing, and simulator agents
measure unresolved choices without letting simulator convenience define the
protocol. It must reproduce direct and multi-hop delivery, foreign relay,
topology change, partition/merge, lifetime, duplicates, capability withdrawal,
resource saturation, and malicious synthetic inputs with finite work.

## Exact simulation compatibility context

Every run pins:

- profile revision `wave1-sim-v0.1`;
- one synthetic envelope-format label and one synthetic protocol-profile label
  as an exact ordered pair;
- simulator, scenario-schema, candidate-routing-profile, and vector-set
  revisions;
- every seed, virtual-time rule, numeric bound, and candidate parameter.

These labels are in-memory fixture values, not assigned wire identifiers. The
profile performs no byte serialization, parser-compatibility, downgrade, or
interoperability claim. EXP-002 remains responsible for real encoding evidence.

## Typed synthetic identity contexts

Implementations use distinct types for discovery handles, session-exchange
identities, admitted peer-session contexts, origin routing contexts, routing
targets, packet identities, channel contexts, channel principals, and action
subjects. Their separation follows
[`identity-domains.md`](../../docs/architecture/identity-domains.md).

For this profile:

- peer-session admission, outer admission, routing-claim admission, routing
  disposition, channel-open, security-replay, inner-decode, and action-
  authorization results are injected synthetic inputs;
- every synthetic action or verdict is a structured fixture containing
  `securityClaim: false`; a bare Boolean or an omitted flag is invalid;
- a generic simulator node label is local topology data and is never accepted
  where a protocol identity domain is required;
- a synthetic origin routing context is required for the profile's duplicate
  key so the current Draft behavior can be exercised, but this does not settle
  whether every future routing profile needs that field.

## Abstract transport and peer-link model

The simulator exposes three distinct ingress concepts:

1. transport attachment;
2. admitted immediate-peer session;
3. directional peer link on that attachment.

Routing returns a bounded ordered set of either:

```text
PeerUnicast(attachment, peerSession, directionalPeerLink)
SharedMedium(attachment, boundedListenerPeerLinks)
```

The following rules reconcile the Wave 0 attachment conflict:

- a peer-unicast forwarding action never targets the exact directional peer
  link from which that forwarding instance arrived;
- an exact routing candidate may use another admitted peer link on the same
  attachment;
- whether another link/session to the same peer is eligible is pinned by the
  candidate profile;
- a shared-medium emission may be heard by the ingress peer because the sender
  cannot assume listener exclusion;
- every shared-medium action records one emission, the bounded ordered listener
  set, one reception attempt per listener, the byte/airtime accounting rule,
  and all duplicate/loop effects;
- attachment, peer-session, and peer-link values are local action context and
  never generic relay-envelope fields.

Every forwarded copy carries the same decremented hop limit. A shared-medium
emission serializes one copy; every admitted listener processes its received
occurrence independently under the same duplicate and synthetic-admission
order.

## Abstract outer packet

The profile permits an in-memory logical packet with:

- exact synthetic compatibility pair;
- coarse outer class/type;
- synthetic origin routing context and packet identity;
- candidate-pinned routing directive and synthetic opaque target when used;
- hop limit;
- optional experimental traffic treatment;
- bounded extension list and declared payload length;
- `OpaqueEndpointPayload` fixture bytes or a reference to them.

`OpaqueEndpointPayload` means only that relays do not parse the bytes. It is not
called a protected or encrypted payload and makes no confidentiality, integrity,
authentication, privacy, or replay-protection claim.

The permitted outer classes are the Draft logical classes `LINK_CONTROL`,
`MESH_CONTROL`, and `OPAQUE_ENDPOINT`. Each exact routing candidate pins the
control catalog and target model it actually uses. Unknown outer semantics and
critical extensions fail closed; optional extensions are preserved by semantic
equality in this profile, not by unselected wire bytes.

## Hop-limit contract

The simulation implements the Draft honest-node hop semantics:

1. the origin value is within `1..profileMaximum`;
2. local delivery can occur at `1`;
3. forwarding requires a value greater than `1`;
4. every forwarding action emits the received value minus one;
5. local delivery does not decrement;
6. relays never increase or reset the value for the same forwarding instance.

The profile maximum is finite and declared by each exact candidate/scenario.
The simulator must also inject malicious reset, over-decrement, re-origination,
and drop behavior for EXP-018. Honest simulation behavior is not evidence that
malicious relays are cryptographically constrained.

## Duplicate contract

For this profile the duplicate key is:

```text
(synthetic envelope format,
 synthetic protocol profile,
 synthetic origin routing context,
 packet identity)
```

Hop limit is not part of the key. Required synthetic session, outer, and claim
admissions precede profile-authoritative lookup or insertion. Lookup, resource
reservation, insertion, and the committed local/forward effects are atomic for
one key. Later committed duplicates produce no effect and do not refresh
retention.

Every run declares finite retention, minimum and configured capacity, and the
exact policy for lifetime-exhausted, no-route, policy, resource, partial-fanout,
and enqueue-failure occurrences. Those no-effect insertion alternatives remain
an EXP-016 dimension; the core exposes them as explicit experimental policies
instead of choosing one silently. Mesh duplicate state never satisfies
security replay, channel operation idempotence, or media freshness.

## Capability lifecycle

The profile implements session-scoped full replacement snapshots:

- finite non-wrapping generation and receipt-relative validity;
- first valid snapshot establishes the high-water mark;
- a higher generation atomically replaces the complete snapshot;
- identical content at the same current generation is idempotent and does not
  refresh expiry;
- changed content at the same current generation conflicts;
- a lower generation is stale;
- expiry withdraws entries but retains the generation high-water mark;
- after expiry, only a higher generation can establish new state;
- a higher snapshot omitting relay willingness withdraws it;
- heartbeat never refreshes or resurrects a snapshot;
- session closure clears the session-scoped state.

Each case pins finite entry, parameter, validity, and state limits. Synthetic
claim admission does not make willingness, availability, resources, or a
propagated routing consequence truthful. EXP-015 compares this lifecycle with
alternatives and supplies numeric evidence.

## Canonical logical processing pipeline

The outer pipeline is:

```text
transport ingress and bounded buffering
    -> bounded logical framing and length validation
    -> exact compatibility and structural validation
    -> synthetic peer-session and outer admission [securityClaim:false]
    -> synthetic routing/capability-claim admission [securityClaim:false]
       where applicable
    -> profile-authoritative duplicate lookup
    -> independent local-delivery and forwarding dispositions
       [securityClaim:false]
    -> bounded resource reservation
    -> duplicate commit
    -> local opaque dispatch and/or peer-link forwarding actions
    -> bounded redacted observations
```

The duplicate lookup through observable action is atomic for one duplicate key.
An input rejected by either synthetic gate cannot mutate the profile's
committed simulated duplicate, capability, or route state. This is an ordering
property of the harness, not a security claim.

Endpoint-pipeline fixtures are optional in Wave 1 and remain synthetic:

```text
bounded synthetic endpoint-context selection
    -> synthetic channel-open/authentication disposition [securityClaim:false]
    -> synthetic security-replay disposition [securityClaim:false]
    -> release fixture context/inner bytes only after both accept
    -> bounded inner decode [securityClaim:false]
    -> synthetic complete-action authorization [securityClaim:false]
    -> semantic precondition and atomic/revision-guarded action
```

No inner fixture bytes or context become externally observable within the
modeled endpoint pipeline before both synthetic open and replay gates accept.
The opaque outer fixture is never thereby called protected, encrypted, or
authenticated. This verifies ordering only; it does not verify cryptography or
real replay protection.

## Routing experiment interface

Each routing candidate is a separately named exact experimental profile behind
one interface. It pins:

- target kind and local-delivery predicate;
- control messages and claim roles;
- directional-link and shared-medium assumptions;
- metrics, provenance, composition, tie-break, and invalid values;
- route/claim freshness, expiry, withdrawal, and restart behavior;
- no-route, queue, retry, fanout, and partial-action behavior;
- candidate-specific loop prevention;
- all state/work bounds and safe observations.

Classic dissemination, reduced dissemination/gossip, distance-vector,
link-state, and reactive candidates receive the same preregistered traces and
tuning rules. No candidate is named Samband's routing algorithm. A hybrid is
tested only if every simpler candidate misses a preregistered hard threshold.

## Required bounds and observations

Every scenario sets finite maxima for frames/payloads, attachments, sessions,
links, targets, claims, capabilities, duplicate state, route state, queues,
fanout, retries, verification work, timer work, and emitted actions. Saturation
at `N` and `N+1` must have deterministic outcomes and must not evict unrelated
admitted state through an unspecified policy.

For a fixed simulator revision, profile, candidate, scenario, trace, and seed,
the ordered semantic log and asserted outcomes are identical. Logs use local
ephemeral handles or aggregates and contain no channel identifiers, secrets,
plaintext, audio, or unnecessary persistent identity.

The stable Draft layered outcome vocabulary may be used for experimental
vectors. Exact error strings and network responses are not part of the profile.

## Explicit exclusions

This profile does not authorize:

- a wire encoder/decoder or a compatibility claim;
- real credentials, authentication, encryption, signatures, nonces, keys,
  replay protection, or secure storage;
- a production routing algorithm or numeric operating envelope;
- real CHANNEL, PTT, AUDIO, codec, capture, playback, or persisted media;
- Android, iOS, physical transport, gateway, or Internet implementation;
- broad Rust crate/FFI scaffolding beyond the bounded ADR-0004 experiment;
- use of synthetic verdicts outside tests/simulation;
- claims of end-to-end encryption, anonymity, unlinkability, forward secrecy,
  post-compromise security, immediate revocation, or production readiness.

## Evidence and exit

Wave 1 evidence is labelled **simulated runtime** and must name this profile
revision. It can inform RFC/ADR changes but cannot accept them automatically.
The profile is revised or superseded if an experiment exposes an ambiguity; an
implementation must not choose the answer silently.

Promotion beyond this profile requires the governing RFC/ADR, exact vector and
compatibility updates, required Protocol/Routing/Security reviews, and closure
of every blocker applicable to the proposed scope.
