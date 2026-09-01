# Shared Contract Registry

## Purpose

Shared contracts allow protocol, core, routing, security, simulator, platform,
audio, and ecosystem work to proceed without independently redefining Samband.
A contract is implementation-ready only when its authority and required review
are complete.

Status meanings:

- **Invariant** — stable project constraint; details may still require RFCs.
- **Accepted architecture** — implementation boundary established by ADR.
- **Draft** — non-normative proposal.
- **Blocked** — implementation must not assume the contract yet.

## Registry

| ID | Contract | Current authority | Required review | Status |
| --- | --- | --- | --- | --- |
| SC-001 | transport network is distinct from private channels | project charter and network model | Architect | Invariant |
| SC-002 | relay does not require channel membership or plaintext | project charter and network model | Protocol, Routing, Security for concrete fields | Invariant |
| SC-003 | platform transports sit behind an abstract one-hop interface | ADR-0003 | Core and platform feasibility for API | Accepted architecture; API blocked |
| SC-004 | node, discovery, session, and human identity separation | RFC-0002 | Agent 1 Protocol, Agent 3 Routing, Agent 4 Security | Draft; blocked |
| SC-005 | channel identity, authorization, membership change, and proof | RFC-0003 | Agent 1 Protocol, Agent 3 Routing for dissemination metadata, Agent 4 Security | Draft; blocked |
| SC-006 | relay envelope fields, encoding, validation order, lifetime, and extensibility | RFC-0004 | Agent 1 Protocol, Agent 3 Routing, Agent 4 Security | Draft; blocked |
| SC-007 | capabilities and their freshness/advertisement semantics | RFC-0001 plus future specification | Agent 1 Protocol, Agent 3 Routing, platform reviewers | Draft; blocked |
| SC-008 | route messages, metric model, convergence, loop behavior, and relay policy | RFC-0005 | Agent 3 Routing, Agent 1 Protocol, Agent 4 Security | Draft; blocked |
| SC-009 | protected channel payload, key epochs, authentication, and replay | RFC-0006 | Agent 4 Security and Agent 1 Protocol | Draft; blocked |
| SC-010 | distributed PTT state, conflict resolution, timeouts, and partitions | RFC-0007 | Agent 1 Protocol, Agent 3 Routing, Agent 4 Security | Draft; blocked |
| SC-011 | audio framing, freshness, loss, codec negotiation, and stream lifecycle | RFC-0008 | Agent 1 Protocol, Agent 3 Routing, Agent 4 Security, later Audio review | Draft; blocked |
| SC-012 | protocol versioning, negotiation, unknown fields/types, and error model | initial RFC set; specification pending | Agent 1 Protocol and Agent 4 Security | Not yet fully drafted; blocked |
| SC-013 | canonical vector manifest, byte representation, negative outcomes, and version pinning | interoperability strategy | Agent 1 Protocol and Agent 9 Ecosystem | Architecture defined; format blocked |
| SC-014 | safe observability vocabulary and redaction rules | system overview and security gates | Security plus relevant component owner | Architecture defined; schema blocked |
| SC-015 | portable-core language and FFI ownership/error boundary | ADR-0004 | Core, Android, iOS, Security | Proposed; experiment required |
| SC-016 | native application stacks and lifecycle capability mapping | ADR-0005 | Android and iOS platform review | Proposed; experiment required |

## Freeze gates

Before a contract can be implemented as shared behavior:

1. its RFC is Accepted or the RFC explicitly defines a versioned experimental
   profile allowed for implementation;
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
