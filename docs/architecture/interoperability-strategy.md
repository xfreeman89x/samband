# Interoperability and Test-Vector Strategy

## Objective

An independent developer should be able to implement a Samband Node from public
specification and test material without observing private reference-app behavior.
Interoperability is therefore a release artifact, not an informal demo.

## Sources of truth

1. Accepted normative text in `protocol/spec`.
2. Versioned canonical vectors in `protocol/test-vectors`.
3. Compatibility profiles in `protocol/compatibility`.
4. Reference implementation tests that consume the same artifacts.

When these disagree, the conflict must be resolved explicitly. Reference code
does not outrank accepted specification text.

## Vector layers

### Semantic vectors

Describe input state, event sequence, expected state transition, observable
output, and failure reason independently from programming language. These cover
routing, duplicate behavior, TTL, PTT, negotiation, and partitions.

### Wire vectors

Provide exact bytes plus decoded meaning after an encoding is accepted. They
cover valid packets, boundary values, canonicalization where required, unknown
extensions, truncation, invalid lengths, and unsupported versions.

### Security vectors

After a governing RFC selects an Agent 4-reviewed standard profile, provide
public non-secret fixtures for identity, authentication, protected records,
replay, membership, and key epochs. Profile-specific vector schemas must pin
the standard/suite/revision, roles, transcript and associated-context bytes,
synthetic inputs/fixed randomness, exact outputs/post-state, provenance, and
resource bounds as required by
[`FORMAT.md`](../../protocol/test-vectors/FORMAT.md). No real user key, channel
secret, identity, captured payload, or human audio is permitted. Known-answer
vectors are interoperability evidence, not proof of side-channel resistance,
metadata privacy, secure storage, compromise recovery, or whole-system security.

### Scenario vectors

Define deterministic topology, seed, timing, link conditions, node capabilities,
events, and expected metrics for simulator and physical conformance harnesses.

## Required vector metadata

The exact machine-readable format remains an Agent 1/Agent 9 decision. Agent
1's current Draft JSON carrier/schema is
[`../../protocol/test-vectors/FORMAT.md`](../../protocol/test-vectors/FORMAT.md).
It makes the proposal reviewable but does not resolve the Agent 9 gate or create
a released canonical vector set.

Every vector must eventually identify:

- stable vector ID and schema version;
- exact envelope-format/protocol-profile pair and governing RFC/spec section;
- exact security profile/construction/suite for a security vector;
- purpose and positive or negative classification;
- deterministic inputs and layered expected outputs or error categories;
- resource bounds relevant to the case;
- provenance/generator version when generated;
- compatibility notes and replacement history.

## Negative testing

Conformance is not only successful decoding. Vectors must cover malformed
lengths, unsupported versions/types, exhausted lifetime, duplicates, replay,
invalid authentication, inconsistent state transitions, excessive nesting or
allocation requests, stale audio, and invalid capability changes as applicable.
Failure categories should be stable enough to test semantics without requiring
identical implementation-specific error strings.

## Immutability and versioning

Vectors published for a release are immutable. An error creates a corrected
vector with a new ID and an explicit supersession record. Implementations pin a
vector-set version in CI. Generated vectors must have a reproducible generator
and checked-in expected output.

## Independent proof

Before Protocol v1.0, at least two independently developed implementations must:

- pass all mandatory vectors for the same profile;
- exchange messages without undocumented configuration or shared internal code;
- agree on rejection behavior for mandatory negative cases;
- demonstrate the foreign-relay scenario;
- publish the tested revisions and known deviations.

Different language bindings over the same core do not by themselves count as
independent protocol implementations.

## Portability

Vector formats and runners must be usable on Windows, macOS, and Linux. Core
fixtures should require no mobile SDK. Platform-specific scenarios supplement,
but never replace, implementation-independent vectors.
