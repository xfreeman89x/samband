# Canonical Test Vectors

Status: strategy defined; vector manifest and fixtures not yet selected.

All implementations will consume the same versioned vectors. Planned layers
include semantic state transitions, exact wire bytes, reviewed cryptographic
fixtures, negative/malformed inputs, and deterministic network scenarios.

The authoritative strategy is
[`../../docs/architecture/interoperability-strategy.md`](../../docs/architecture/interoperability-strategy.md).
Agent 1 and Agent 9 must define the machine-readable manifest before fixtures
are treated as canonical.

Rules:

- use only synthetic public test identities, keys, payloads, and audio-like data;
- include the governing specification/RFC and expected outcome;
- bound inputs and expected resource behavior;
- never mutate a vector published for a release; supersede it with provenance;
- make generators deterministic and publicly runnable.

