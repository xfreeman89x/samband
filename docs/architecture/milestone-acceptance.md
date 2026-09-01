# Milestone Acceptance Evidence

[`ROADMAP.md`](../../ROADMAP.md) defines product outcomes. This document defines
the evidence package maintainers should inspect before declaring a gate complete.

## Required evidence for every milestone

- tested revision and toolchain versions;
- commands sufficient to reproduce the result on supported host platforms;
- automated test results and clearly separated manual/physical observations;
- governing RFCs, ADRs, and shared-contract versions;
- protocol, public API, security, routing, and interoperability impact;
- malformed-input and resource-bound evidence relevant to the milestone;
- known limitations and failed/unsupported cases;
- no secrets, private captures, environment-specific credentials, or persisted
  audio in artifacts.

## Gate matrix

| Gate | Minimum objective evidence | Review required |
| --- | --- | --- |
| M0 foundation | repository validator, link check, clean diff review, 8 Draft RFCs, ADR index, risk and experiment registers | Architect |
| M1 protocol architecture | cohesive v0.x spec, review records, vector schemas, threat model, unresolved item register | Protocol, Security, Routing where applicable |
| M2 simulator | seeded scenario reports, bounded-state assertions, failure tests, routing metrics | Core, Routing, Simulator, Protocol |
| M3 native direct transport | device/OS matrix, no-Internet proof, lifecycle traces, adapter boundary tests | Android initially; Protocol/Core integration |
| M4 community relay | physical topology proof, membership isolation, opaque payload evidence, policy/resource behavior | Routing, Security, Android, Simulator |
| M5 realtime PTT | latency/loss measurements, non-persistence audit, arbitration tests, protected-payload review | Audio, Security, Protocol, Platform |
| M6 cross-platform | shared vector results and Android-iOS exchange with documented deviations | iOS, Android, Ecosystem, Protocol |
| M7 v1 | two independent implementations, complete security gate, stable compatibility suite, release artifacts | Maintainers plus all affected domains |

## Evidence labels

Reports must distinguish:

- **static** — format, compile, lint, or source inspection;
- **simulated runtime** — deterministic model execution;
- **physical runtime** — observed on named device/OS/transport classes;
- **interoperability** — independently built implementations exchanged or
  rejected traffic as specified;
- **security review** — explicit reviewer assessment, not merely passing tests.

One evidence level does not imply another.

## Acceptance record

A milestone acceptance pull request should link the evidence, list reviewers,
record residual risks, and update the roadmap. A demo without reproducible
artifacts is progress but not milestone acceptance.

