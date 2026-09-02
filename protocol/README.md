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

The current Agent 1 protocol synthesis, now annotated with Agent 4's initial
security requirements, consists of:

- [`spec/v0x-experimental.md`](spec/v0x-experimental.md), a cohesive Draft
  logical specification;
- [`spec/v0x-simulation-profile.md`](spec/v0x-simulation-profile.md), the
  bounded non-production Wave 1 simulation contract;
- [`test-vectors/FORMAT.md`](test-vectors/FORMAT.md), the Draft canonical-vector
  carrier and outcome vocabulary;
- [`compatibility/v0x-experimental.md`](compatibility/v0x-experimental.md), the
  exact pre-v1 profile/negotiation model.

They remain non-normative. Only the subset explicitly named by the simulation
profile is authorized for experimental implementation; every broader contract
remains blocked on the reviews/evidence it lists. The candidate security
architecture is indexed in
[`../docs/security/README.md`](../docs/security/README.md). In particular, no
wire encoding, routing algorithm, identity or cryptographic construction, PTT
arbitration algorithm, or audio profile is selected.

## Authority rule

Reference implementations consume this directory; they do not define it. A
material semantic change begins with the RFC workflow. Schemas and vectors must
be traceable to accepted specification sections.
