# Portable Core

This directory is reserved for transport-independent Samband implementation
logic. No production core exists.

Candidate responsibilities and forbidden dependencies are defined in
[`../docs/architecture/component-model.md`](../docs/architecture/component-model.md)
and [`../docs/architecture/dependency-graph.md`](../docs/architecture/dependency-graph.md).

Implementation is blocked on accepted or explicitly experimental shared
contracts. A core cannot choose protocol, routing, identity, cryptography, PTT,
or audio semantics by itself.
