# Architecture Index

Samband architecture is intentionally layered so a third party can implement
the protocol without copying an official application.

## Start here

1. [`system-overview.md`](system-overview.md) — project scope and architectural
   shape.
2. [`network-model.md`](network-model.md) — the shared mesh/private channel
   separation and node roles.
3. [`glossary.md`](glossary.md) — canonical terminology.
4. [`component-model.md`](component-model.md) — responsibilities and boundaries.
5. [`dependency-graph.md`](dependency-graph.md) — permitted dependency direction.
6. [`shared-contracts.md`](shared-contracts.md) — contracts, owners, review gates,
   and current readiness.

## Development architecture

- [`repository-layout.md`](repository-layout.md) — canonical directories and
  ownership.
- [`protocol-development-workflow.md`](protocol-development-workflow.md) — from
  question to accepted specification and vectors.
- [`simulator-first.md`](simulator-first.md) — why deterministic simulation is
  the first implementation environment.
- [`interoperability-strategy.md`](interoperability-strategy.md) — canonical
  vectors and independent implementation proof.
- [`milestone-acceptance.md`](milestone-acceptance.md) — measurable evidence
  required at each gate.
- [`risk-register.md`](risk-register.md) — active technical and project risks.

## Authority boundaries

These documents can establish implementation boundaries and stable project
invariants. They do not choose packet bytes, identity algorithms, routing
algorithms, group-key schemes, PTT arbitration, or audio framing. Those choices
require the RFC and review gates listed in
[`shared-contracts.md`](shared-contracts.md).
