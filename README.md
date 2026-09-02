# Samband

> Press. Talk. Relay. Connect.

Samband is an open protocol and reference implementation for realtime
Push-To-Talk communication over opportunistic peer-to-peer mesh networks. It
is intended to let compatible nodes communicate directly, relay opaque traffic
for one another, and continue operating through partitions without requiring
central infrastructure.

Samband is licensed under the [Apache License 2.0](LICENSE).

## Project status

Samband has completed its first architecture integration review. There is no
working network, wire-compatible protocol, production application, or reviewed
cryptographic design yet. The initial RFCs remain Draft and must not be treated
as an interoperability or security promise. A narrowly scoped
[`wave1-sim-v0.1`](protocol/spec/v0x-simulation-profile.md) contract authorizes
deterministic non-production simulation only.

The first implementation milestone is a deterministic simulator, not a mobile
application and not production audio.

## The invariant that shapes Samband

The shared transport network and private radio channels are different layers:

```text
Alice, member of channel 7                Carol, member of channel 7
              \                            /
               Relay X ---- Relay Y ------
              no channel 7 membership
```

The design target is for relay nodes to forward opaque, protected channel
payloads without needing channel membership or plaintext access. A node can be
an endpoint, a relay, a future gateway, or several of these at once according
to advertised capabilities.

See the [network model](docs/architecture/network-model.md) and
[glossary](docs/architecture/glossary.md) for the canonical terminology.

## What Samband is not

The initial project is not a Web application, SaaS product, centralized
messaging backend, generic IP proxy, blockchain, or store-and-forward voice
service. Audio is ephemeral: missed voice is not replayed or persisted.

## Repository map

- [`protocol/`](protocol/README.md) contains the implementation-independent
  specification, schemas, compatibility material, and canonical test vectors.
- [`core/`](core/README.md) is reserved for portable protocol/core logic.
- [`simulator/`](simulator/README.md) is the first implementation environment.
- [`apps/`](apps/README.md) contains native reference applications.
- [`bindings/`](bindings/README.md) contains deliberately narrow language
  bindings when justified.
- [`docs/architecture/`](docs/architecture/README.md) defines components,
  boundaries, risks, milestones, and shared contracts.
- [`docs/rfc/`](docs/rfc/README.md) governs protocol semantics.
- [`docs/adr/`](docs/adr/README.md) records implementation architecture.
- [`docs/security/`](docs/security/README.md) contains the initial threat model,
  candidate security architecture, and still-open review gates.
- [`docs/research/`](docs/research/README.md) tracks questions that require
  experiments rather than assumptions.

The complete canonical layout is documented in
[`docs/architecture/repository-layout.md`](docs/architecture/repository-layout.md).

## Decision authority

The protocol specification is authoritative over reference implementations.
Material protocol changes require an accepted RFC. Implementation architecture
changes require an ADR. Security-, routing-, and wire-format-sensitive work
must receive the reviews listed in the
[shared-contract registry](docs/architecture/shared-contracts.md).

Draft RFCs are research and design proposals. Only accepted RFCs can be used as
normative implementation contracts.

## Getting started

The bootstrap currently has no build dependencies. Python 3.11 or newer is
recommended for the repository validator:

```shell
python tools/validate_repository.py
```

Before contributing, read:

1. [`CONTRIBUTING.md`](CONTRIBUTING.md);
2. [`AGENTS.md`](AGENTS.md) if using an automated agent;
3. the [architecture index](docs/architecture/README.md);
4. accepted RFCs and ADRs relevant to the change.

There are currently no accepted protocol RFCs and therefore no stable Samband
wire format.

## Roadmap

Development proceeds through measurable gates: architecture, reviewed protocol
drafts, deterministic simulation, native offline relay, encrypted synthetic
payloads, realtime PTT, cross-platform interoperability, and finally a v1.0
compatibility contract. See [`ROADMAP.md`](ROADMAP.md).

## Security

Do not deploy Samband for safety-critical or confidential communication yet.
The project does not claim end-to-end encryption until the identity, membership,
key management, and encrypted-envelope design has passed security review. See
[`SECURITY.md`](SECURITY.md).

## Contributing and governance

Contributions are welcome under Apache-2.0. The project uses public RFC and ADR
records so independent implementers can understand why semantics changed.
Review [`CONTRIBUTING.md`](CONTRIBUTING.md), [`GOVERNANCE.md`](GOVERNANCE.md),
and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) before participating.
