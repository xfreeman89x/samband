# Samband ADR Index

Architecture Decision Records describe implementation and repository structure.
They cannot redefine observable protocol semantics or override an accepted RFC.

## Status lifecycle

- **Proposed** — under evaluation; implementation may run a bounded experiment.
- **Accepted** — governs implementation architecture.
- **Rejected** — considered and not adopted.
- **Deprecated** — retained for history but no longer recommended.
- **Superseded** — replaced by a linked later ADR.

Accepted ADRs are not rewritten to hide changed decisions. Create a new ADR and
link the records.

## Initial records

| ADR | Title | Status |
| --- | --- | --- |
| [0001](ADR-0001-protocol-specification-authority.md) | Protocol Specification Authority | Accepted |
| [0002](ADR-0002-simulator-first-development.md) | Simulator-First Development | Accepted |
| [0003](ADR-0003-transport-abstraction.md) | Transport Abstraction Boundary | Accepted |
| [0004](ADR-0004-rust-shared-core.md) | Rust Shared Core | Proposed |
| [0005](ADR-0005-native-mobile-reference-apps.md) | Native Android and iOS Reference Apps | Proposed |
| [0006](ADR-0006-canonical-repository-layout.md) | Canonical Repository Layout | Accepted |

Copy [`ADR-TEMPLATE.md`](ADR-TEMPLATE.md) for new decisions. Use an RFC instead
if peers or independent implementations could observe the choice.

