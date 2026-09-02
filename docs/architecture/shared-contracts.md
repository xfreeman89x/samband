# Shared Contract Registry

## Purpose

Shared contracts allow protocol, core, routing, security, simulator, platform,
audio, and ecosystem work to proceed without independently redefining Samband.
A contract is implementation-ready only within the scope authorized by its
category, authority, and completed required review.

Status meanings:

- **ESTABLISHED ARCHITECTURAL INVARIANT** — stable architecture constraint or
  accepted implementation boundary. The classification applies only to the
  contract text in the row; it does not accept a Draft RFC or establish a
  security, compatibility, wire-format, or routing-algorithm claim.
- **EXPERIMENTAL CONTRACT** — an exact versioned, bounded, non-production
  profile that may be implemented only to collect the evidence it names. It
  creates no compatibility or security claim and cannot silently escape its
  experimental boundary.
- **DRAFT INTERFACE** — a reviewable non-normative boundary or candidate
  semantic model. Implementations may not rely on it as shared Samband behavior
  unless an exact Experimental Contract includes it.
- **UNRESOLVED** — one or more required semantics remain unselected or blocked;
  implementations must not assume an answer.

No classification closes an SG gate or changes an RFC/ADR lifecycle status.
The final column records exclusions and remaining work that are outside the
classified contract's current scope.

## Registry

| ID | Contract | Current authority | Required review | Status | Current scope and remaining work |
| --- | --- | --- | --- | --- | --- |
| SC-001 | transport network is distinct from private channels | project charter and network model | Architect | ESTABLISHED ARCHITECTURAL INVARIANT | Layering only; it selects no wire representation. |
| SC-002 | generic relay behavior requires neither channel membership, channel credentials, channel keys, nor channel plaintext | project charter and network model | Protocol, Routing, Security for concrete fields | ESTABLISHED ARCHITECTURAL INVARIANT | Foreign-relay requirement only; it is not a claim that current payloads are protected. Concrete relay-visible fields remain under review. |
| SC-003 | platform transports sit behind an abstract one-hop interface | ADR-0003 | Core and platform feasibility for API | ESTABLISHED ARCHITECTURAL INVARIANT | The boundary is established; the exact portable API and platform feasibility remain unresolved. |
| SC-004 | credential, discovery, session, routing, channel-context, channel-principal, action-subject, packet, operation, media, and human-label domains are distinct and have no implicit binding | identity-domains architecture plus RFC-0002 Draft | Agent 1 Protocol, Agent 3 Routing, Agent 4 Security | ESTABLISHED ARCHITECTURAL INVARIANT | Separation only. Representations, bindings, authentication, authority, privacy properties, and routing use remain unresolved; all applicable SG gates stay open. |
| SC-005 | channel identity, authorization, membership change, and proof | RFC-0003 | Agent 1 Protocol, Agent 3 Routing for dissemination metadata, Agent 4 Security | UNRESOLVED | Credential, authority, group construction, proof, epoch, and partition behavior remain security/experiment blocked. |
| SC-006 | relay envelope fields, encoding, validation order, lifetime, and extensibility | RFC-0004 | Agent 1 Protocol, Agent 3 Routing, Agent 4 Security | DRAFT INTERFACE | The logical model is reviewable; exact bytes, field coverage, mutable-hop security, identifiers, and production profile remain unresolved. |
| SC-007 | capabilities and their freshness/advertisement semantics | RFC-0001 plus future specification | Agent 1 Protocol, Agent 3 Routing, Agent 4 Security, platform reviewers | DRAFT INTERFACE | The replacement-snapshot lifecycle is a Draft candidate; authority, provenance, numeric bounds, platform mapping, and production validation remain unresolved. |
| SC-008 | route messages, metric model, convergence, loop behavior, and relay policy | RFC-0005 | Agent 3 Routing, Agent 1 Protocol, Agent 4 Security | UNRESOLVED | Routing families remain experimental; no message set, metric, algorithm, or operating envelope is selected. |
| SC-009 | endpoint record protection, key epochs, authentication, and security replay | RFC-0006 | Agent 4 Security and Agent 1 Protocol | UNRESOLVED | No credential, group/record construction, primitive, nonce/replay rule, or protected-record profile is selected; SG-003 through SG-006 remain open. |
| SC-010 | distributed PTT state, conflict resolution, timeouts, and partitions | RFC-0007 | Agent 1 Protocol, Agent 3 Routing, Agent 4 Security | DRAFT INTERFACE | Reviewable state-machine boundary only; authorization, algorithm, timers, partition behavior, and vectors remain unresolved. |
| SC-011 | audio framing, freshness, loss, codec negotiation, and stream lifecycle | RFC-0008 | Agent 1 Protocol, Agent 3 Routing, Agent 4 Security, later Audio review | DRAFT INTERFACE | Audio ephemerality and non-persistence remain separate project invariants. This framing/stream interface, codec, media security, timing, numeric bounds, and physical evidence remain Draft or unresolved. |
| SC-012 | protocol versioning, negotiation, unknown fields/types, and error model | RFC-0004 plus Draft v0.x specification | Agent 1 Protocol and Agent 4 Security | DRAFT INTERFACE | The exact-pair and layered-disposition model is Draft; wire identifiers, encoding, downgrade/security binding, and compatibility promise remain unresolved. |
| SC-013 | canonical vector manifest, byte representation, negative outcomes, and version pinning | interoperability strategy plus Draft vector format | Agent 1 Protocol, Agent 4 for security-vector extensions, and Agent 9 Ecosystem | DRAFT INTERFACE | Draft carrier only; canonical wire bytes, released compatibility claims, real-security fixtures, runners, and Ecosystem review remain unresolved. |
| SC-014 | safe observability vocabulary and redaction rules | system overview, threat model, and security gates | Security plus relevant component owner | DRAFT INTERFACE | Project-level prohibitions on logging secrets, plaintext, or audio still apply. The shared vocabulary/schema, component review, retention audit, and bounded-cardinality evidence remain unresolved. |
| SC-015 | portable-core language and FFI ownership/error boundary | ADR-0004 | Core, Android, iOS, Security | UNRESOLVED | ADR remains Proposed and EXP-001 evidence is required; no broad production scaffolding is authorized. |
| SC-016 | native application stacks and lifecycle capability mapping | ADR-0005 | Android and iOS platform review | UNRESOLVED | ADR remains Proposed and platform experiments are required; mobile networking remains blocked. |
| SC-017 | versioned Wave 1 simulation-only logical profile: typed synthetic domains, abstract packet/compatibility context, peer-link actions, hop limit, duplicate semantics, capability lifecycle, pipeline, bounded candidate-routing interface, and synthetic dispositions | [`wave1-sim-v0.1`](../../protocol/spec/v0x-simulation-profile.md) and [`Wave 0 Integration Review`](wave0-integration-review.md) | Agent 0 integration; Agent 1 Protocol, Agent 3 Routing, and Agent 4 Security for changes in their domains | EXPERIMENTAL CONTRACT | NON-PRODUCTION, NON-SECURITY, EXPERIMENTAL ONLY. Every synthetic action/verdict carries `securityClaim: false`; `OpaqueEndpointPayload` is unparsed, not protected. No wire, compatibility, routing-winner, cryptography, SG-gate, audio, or mobile claim. |

## Security review evidence

The Wave 0 security documents refine requirements without superseding or
accepting an RFC and without closing an SG gate:

- [`node-identity.md`](../security/node-identity.md) informs SC-004, SC-007, and
  SC-012;
- [`channel-security.md`](../security/channel-security.md) informs SC-005,
  SC-009, SC-010, and SC-011;
- [`relay-security.md`](../security/relay-security.md) informs SC-002, SC-006,
  SC-007, and SC-008;
- [`discovery-privacy.md`](../security/discovery-privacy.md) informs SC-004 and
  the discovery portion of SC-012;
- [`threat-model.md`](../security/threat-model.md) and
  [`review-gates.md`](../security/review-gates.md) define the initial threat and
  gate evidence across all security-sensitive contracts.

This evidence records an initial Agent 4 review only. It selects no credential,
session protocol, group-key construction, cipher suite, nonce rule, signature,
or route-authentication mechanism, and it closes no security gate.

SC-004 establishes only the architectural non-equivalence of identity domains.
It establishes no credential, binding, authentication, authorization,
confidentiality, anonymity, unlinkability, or routing claim. SC-017's synthetic
gates and dispositions always carry `securityClaim: false`; passing them is
evidence about simulated ordering and bounded behavior only.

## Freeze gates

An EXPERIMENTAL CONTRACT may be implemented only inside its exact named
revision, exclusions, and evidence boundary. It does not satisfy the freeze
gates below. Before a contract can be promoted to stable shared Samband
behavior:

1. every governing protocol RFC is Accepted and every governing architecture
   ADR is Accepted;
2. all listed domain reviews are recorded;
3. normative language is incorporated into `protocol/spec`;
4. positive and negative canonical vectors exist where machine behavior can be
   represented;
5. malformed-input and bounded-resource behavior is testable;
6. compatibility and version-negotiation impact is documented;
7. no unresolved security blocker remains for the proposed scope.

## Change coordination

No agent or component may independently redefine a registry contract. A newly
discovered ambiguity is reported against the owning RFC or as a new RFC issue.
Implementations may prototype alternatives behind explicitly experimental,
non-interoperable boundaries, but must not publish them as Samband protocol
behavior.
