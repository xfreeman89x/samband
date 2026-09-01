# Samband Documentation

Documentation is organized by authority and purpose:

- [`architecture/`](architecture/README.md) defines stable project boundaries,
  component relationships, risks, and development gates;
- [`rfc/`](rfc/README.md) contains protocol-semantic proposals and decisions;
- [`adr/`](adr/README.md) contains implementation-architecture decisions;
- [`security/`](security/README.md) contains the threat-model and security-review
  surface;
- [`research/`](research/README.md) contains evidence plans for unresolved
  technical assumptions;
- [`agents/`](agents/README.md) contains agent roles and handoff conventions.

The implementation-independent protocol will live in
[`../protocol/spec/`](../protocol/spec/README.md). Accepted specification text
and accepted RFCs outrank implementation behavior.

## Status matters

- An **invariant** is a project constraint stated in the charter or an accepted
  governance/architecture record.
- An **Accepted ADR** governs implementation structure.
- An **Accepted RFC** governs protocol semantics.
- A **Draft RFC** is non-normative design work.
- An **experiment** gathers evidence and does not create a protocol contract.

Always check a document's status before treating it as authority.
