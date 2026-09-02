# Canonical Test Vectors

Status: Draft carrier/schema and illustrative semantic vectors proposed; no
released canonical vector set exists.

All implementations will consume the same versioned vectors. Planned layers
include semantic state transitions, exact wire bytes, reviewed cryptographic
fixtures, negative/malformed inputs, and deterministic network scenarios.

The authoritative strategy is
[`../../docs/architecture/interoperability-strategy.md`](../../docs/architecture/interoperability-strategy.md).
Agent 1's proposed carrier is documented in [`FORMAT.md`](FORMAT.md), with the
machine-readable [`vector-set.schema.json`](vector-set.schema.json) and
illustrative [`draft-v0x-core.json`](draft-v0x-core.json). Agent 4 has added the
requirements for a later construction-specific security-vector schema; no real
cryptographic vector or profile exists. Agent 9 review is still required.
`draft` sets can change and cannot support conformance or security claims.

Rules:

- use only synthetic public test identities, keys, payloads, and audio-like data;
- pin the exact envelope-format/protocol-profile pair;
- include the governing specification/RFC and layered expected outcomes;
- bound inputs and expected resource behavior;
- never mutate a vector published for a release; supersede it with provenance;
- make generators deterministic and publicly runnable.
