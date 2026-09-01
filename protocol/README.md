# Samband Protocol

This directory is the implementation-independent protocol authority.

## Areas

- [`spec/`](spec/README.md) — cohesive normative specification after RFC
  acceptance;
- [`schemas/`](schemas/README.md) — machine-readable artifacts derived from the
  accepted specification;
- [`test-vectors/`](test-vectors/README.md) — canonical positive, negative,
  security, and scenario fixtures;
- [`compatibility/`](compatibility/README.md) — version profiles, negotiation,
  implementation guidance, and conformance claims.

There is currently no accepted protocol RFC, stable wire format, or compatible
implementation. Draft RFCs in [`../docs/rfc/`](../docs/rfc/README.md) are design
inputs, not normative protocol text.

## Authority rule

Reference implementations consume this directory; they do not define it. A
material semantic change begins with the RFC workflow. Schemas and vectors must
be traceable to accepted specification sections.

