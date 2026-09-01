# Samband Agent Guide

Samband is an Apache-2.0 open protocol and reference implementation for
realtime Push-To-Talk communication over opportunistic peer-to-peer mesh
networks.

> Press. Talk. Relay. Connect.

This file contains only stable invariants, mandatory workflows, repository
pointers, and validation commands. Detailed architecture belongs in `docs/` and
protocol semantics belong in accepted RFCs and `protocol/spec`.

## Required reading

Before making changes, read in this order:

1. this file and [`README.md`](README.md);
2. the [`architecture index`](docs/architecture/README.md), especially the
   network model, dependency graph, and shared-contract registry;
3. accepted RFCs relevant to the work in [`docs/rfc/`](docs/rfc/README.md);
4. accepted ADRs relevant to the work in [`docs/adr/`](docs/adr/README.md);
5. the role prompt in [`docs/agents/PROMPTS.md`](docs/agents/PROMPTS.md).

Draft RFCs are non-normative. There are no Accepted protocol RFCs or stable wire
format at the architecture-bootstrap stage.

## Stable project invariants

- The Samband Protocol specification is authoritative. Reference applications
  implement it; they do not define it.
- The shared transport network is distinct from private radio channels.
- A node may be an endpoint, relay, future gateway, or a combination according
  to dynamic capabilities. Do not infer behavior only from device type.
- A relay does not need private-channel membership or channel plaintext.
- Transports carry Samband frames but do not redefine protocol, routing,
  channel, or PTT semantics.
- Network partitions, reconnection, and changing relay willingness are normal.
- Audio is ephemeral. Never persist raw audio, encoded frames, conversations,
  transcripts, or voice history. Missed voice is not replayed.
- Do not claim end-to-end encryption until identity, membership, key management,
  protected payloads, and replay behavior are implemented and reviewed.
- Never invent cryptographic algorithms.
- Samband is not a Web application, SaaS backend, centralized messaging service,
  generic IP proxy, blockchain, or store-and-forward voice system.
- Prefer minimal, bounded, observable, partition-tolerant state. Malformed,
  duplicated, replayed, or looping traffic must not cause unbounded work.
- Platform limitations are advertised as capabilities; they do not silently
  change the protocol.

Canonical terminology is in
[`docs/architecture/glossary.md`](docs/architecture/glossary.md). The full model
is in [`docs/architecture/network-model.md`](docs/architecture/network-model.md).

## Decision authority and mandatory review

Use an RFC for material peer-visible or interoperability semantics. Use an ADR
for implementation architecture that does not alter protocol behavior. Use a
research experiment when evidence is needed before either decision.

Do not independently redefine any entry in
[`docs/architecture/shared-contracts.md`](docs/architecture/shared-contracts.md),
including packet envelope, identity, channel membership, capabilities, routing,
protected payload, PTT, audio, versioning, or canonical vectors.

Required gates:

- Agent 1 or equivalent Protocol review for wire formats, processing semantics,
  versioning, and interoperability contracts;
- Agent 3 or equivalent Routing review for routing, relay, lifetime, metrics,
  loop, partition, and convergence behavior;
- Agent 4 or equivalent Security review for identity, authentication,
  authorization, cryptography, replay, metadata privacy, abuse, and security
  claims.

Security-sensitive RFCs cannot be accepted while their relevant gate in
[`docs/security/review-gates.md`](docs/security/review-gates.md) is open.
Protocol v1 cannot freeze until the threat model and external review gates are
complete.

Follow the full
[`protocol-development workflow`](docs/architecture/protocol-development-workflow.md)
and governance in [`GOVERNANCE.md`](GOVERNANCE.md). Accepted records are
superseded by new records; do not rewrite decision history.

## Canonical repository map

```text
protocol/       implementation-independent specification, schemas, vectors
core/           portable core candidates
simulator/      deterministic virtual mesh
apps/           native reference applications
bindings/       narrow language bindings
docs/
  architecture/ boundaries, contracts, risks, milestones
  rfc/          protocol decision records
  adr/          implementation architecture records
  security/     threat model and security reviews
  research/     experiments and evidence
  agents/       role prompts and handoffs
tools/          public cross-platform contributor tools
```

The detailed tree and ownership are authoritative in
[`docs/architecture/repository-layout.md`](docs/architecture/repository-layout.md).
Changing top-level component or authority boundaries requires an ADR and may
also require an RFC.

## Dependency rules

- `protocol/` depends on no reference implementation.
- Protocol codecs do not depend on routing algorithms, transports, UI,
  persistence, or platform APIs.
- Routing consumes only protocol-approved relay metadata, dynamic capabilities,
  abstract time/randomness, and abstract link metrics. It never consumes channel
  plaintext or secrets.
- Security components do not select routes or physical transports.
- Portable core code depends on transport interfaces, never concrete Android,
  Apple, Wi-Fi, Bluetooth, Internet, or simulator types.
- Transport adapters implement one-hop connectivity and report capabilities;
  they do not define Samband semantics.
- Applications compose policy, UI, audio devices, core, and adapters; they do
  not reimplement shared protocol behavior.
- Simulator and physical nodes consume the same core contracts and canonical
  vectors.
- Bindings expose narrow reviewed APIs and do not become a second protocol
  implementation.
- Cycles across these boundaries are prohibited.

See [`docs/architecture/dependency-graph.md`](docs/architecture/dependency-graph.md).

## Implementation sequencing

The simulator is the first implementation environment. Do not begin production
audio, Android/iOS mesh, routing implementation, networking, or cryptography
until their shared contracts and review gates authorize the work.

The Rust shared core and native Kotlin/Swift reference apps remain Proposed in
ADR-0004 and ADR-0005. Do not create broad production scaffolding before their
required experiments.

Execution waves and role ownership are in
[`docs/agents/PROMPTS.md`](docs/agents/PROMPTS.md). Wave order is a dependency
graph, not permission to start every agent. Measurable gates are in
[`ROADMAP.md`](ROADMAP.md) and
[`docs/architecture/milestone-acceptance.md`](docs/architecture/milestone-acceptance.md).

## Security, privacy, and repository hygiene

- Never commit credentials, tokens, private keys, channel secrets, personal
  data, private captures, or environment-specific user paths.
- Use synthetic public identities, keys, payloads, and audio-like fixtures.
- Never log plaintext audio or channel secrets; minimize stable identity logs.
- Treat transport/link security, node authentication, channel authorization,
  payload protection, replay protection, and metadata privacy as distinct.
- Evaluate every dependency for purpose, maintenance, license, portability,
  provenance, and security. Preserve required attribution in `NOTICE`.
- Keep shared tooling compatible with Windows, macOS, and Linux and independent
  from private infrastructure.
- All Markdown must be UTF-8 without BOM. Avoid corrupted text and local absolute
  paths.

Vulnerabilities follow [`SECURITY.md`](SECURITY.md), never a public issue with
exploit details.

## Git workflow

Before modifying a Git repository:

- inspect working-tree status, current branch/upstream, divergence, and any
  merge/rebase/cherry-pick/revert/bisect operation;
- verify the remote when available;
- fast-forward only a clean tracked branch;
- if local changes, unpublished commits, divergence, conflicts, or an operation
  are present, do not pull, merge, rebase, stash, reset, switch branches, or
  resolve automatically; report the state and request direction;
- preserve unrelated user changes;
- use Conventional Commit prefixes;
- do not commit or push without explicit authorization.

## Validation commands

From the repository root:

```shell
python tools/validate_repository.py
git diff --check
```

Run component-specific builds, tests, vector runners, fuzzers, and platform
checks documented by the affected component. Report static, simulated, physical,
interoperability, and security-review evidence separately.

## Definition of done

A change is complete only when:

- its governing RFC/ADR/shared contract permits the behavior;
- relevant builds and tests pass;
- public behavior and compatibility impact are documented;
- malformed input and bounded-resource behavior are covered;
- security, privacy, routing, and interoperability impact are assessed;
- no unrelated refactor, secret, environment-specific data, proprietary
  dependency, or persisted audio was introduced;
- internal links and repository validation pass;
- assumptions, limitations, blockers, and next step are explicit.

Agent completions use
[`docs/agents/HANDOFF-TEMPLATE.md`](docs/agents/HANDOFF-TEMPLATE.md).

## Guiding test

Ask whether a decision helps achieve this outcome without platform coupling:

```text
Alice (channel member) -> Bob (relay only) -> Carol (channel member)
```

No Internet. No direct Alice-Carol link. Bob is not a channel member, forwards
valid Samband traffic, and cannot recover the protected channel payload. Carol
eventually hears Alice in realtime only after the audio milestone is reached.
