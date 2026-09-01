# Samband Simulator

Status: architecture skeleton; no simulator implementation exists.

The simulator is the first implementation environment after Wave 0 contracts
are ready. It will compose the same portable core and transport boundary as
physical nodes with virtual time, seeded randomness, a deterministic topology
scheduler, configurable link conditions, bounded traces, and canonical scenario
vectors.

Required scenarios and anti-shortcut rules are defined in
[`../docs/architecture/simulator-first.md`](../docs/architecture/simulator-first.md).
Routing semantics remain blocked on RFC-0005 review.
