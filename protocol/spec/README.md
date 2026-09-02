# Protocol Specification

Status: no Accepted normative specification. Agent 1's review synthesis,
annotated with Agent 4's initial security requirements, is
[`v0x-experimental.md`](v0x-experimental.md).

The v0.x document is a Draft experimental proposal derived from the current RFC
set. It makes the layering, logical envelope, processing, message, capability,
PTT/audio boundary, and vector contracts reviewable without selecting routing,
cryptography, or wire encoding. Candidate security designs remain separate in
[`../../docs/security/`](../../docs/security/README.md). The synthesis is not
normative or a compatibility/security claim.

The strictly smaller
[`v0x-simulation-profile.md`](v0x-simulation-profile.md) is an explicitly
authorized experimental contract for deterministic Wave 1 simulation and a
narrow core prototype. It selects no production wire, security, routing, PTT,
or audio profile, and passing it is simulated-runtime evidence only.

Future specification work must cover, at minimum:

- versioning and negotiation;
- identity, discovery, authentication, and capabilities;
- relay envelope and processing order;
- routing and relay behavior;
- channel membership and protected payloads;
- PTT and realtime audio framing;
- errors, unknown fields/types, malformed input, replay, duplicate behavior,
  lifetime, and resource bounds.

No Draft RFC text becomes normative merely by being synthesized here.
Specification changes cite their governing RFC and vector coverage. After
acceptance, cohesive normative text will replace or clearly supersede the Draft
experimental synthesis rather than silently promoting it.
