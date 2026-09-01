# Canonical Repository Layout

## Status

Accepted by
[`ADR-0006`](../adr/ADR-0006-canonical-repository-layout.md). Empty implementation
areas contain README skeletons so ownership and boundaries are visible without
pretending code exists.

## Layout

```text
/
|-- protocol/
|   |-- spec/
|   |-- schemas/
|   |-- test-vectors/
|   `-- compatibility/
|-- core/
|   `-- rust/
|-- simulator/
|-- apps/
|   |-- android/
|   `-- ios/
|-- bindings/
|   |-- kotlin/
|   `-- swift/
|-- docs/
|   |-- architecture/
|   |-- adr/
|   |-- rfc/
|   |-- security/
|   |-- research/
|   `-- agents/
|-- tools/
|-- .github/
|-- AGENTS.md
|-- README.md
|-- ROADMAP.md
|-- CONTRIBUTING.md
|-- SECURITY.md
|-- GOVERNANCE.md
|-- CODE_OF_CONDUCT.md
|-- LICENSE
`-- NOTICE
```

## Directory authority

| Path | Purpose | Primary steward |
| --- | --- | --- |
| `protocol/spec` | normative implementation-independent specification | Protocol |
| `protocol/schemas` | machine-readable forms derived from accepted specification | Protocol |
| `protocol/test-vectors` | canonical interoperability fixtures | Protocol / Ecosystem |
| `protocol/compatibility` | version and independent-implementation guidance | Protocol / Ecosystem |
| `core/rust` | candidate portable core after ADR acceptance | Rust Core |
| `simulator` | deterministic virtual network and reliability scenarios | Simulator / Routing |
| `apps/android` | native Android reference implementation | Android |
| `apps/ios` | native iOS reference implementation | iOS |
| `bindings` | narrow language bindings generated or maintained from core APIs | Ecosystem / Core |
| `docs/architecture` | package boundaries, shared contracts, integration | Architect |
| `docs/rfc` | protocol decision records | Architect / Protocol |
| `docs/adr` | implementation architecture records | Architect |
| `docs/security` | threat model and security architecture | Security |
| `docs/research` | experiment plans and evidence | Relevant domain owner |
| `docs/agents` | role prompts and handoff conventions | Architect |
| `tools` | public cross-platform contributor tooling | Ecosystem / Maintainers |

## Change policy

Moving an authoritative area, adding a new top-level product component, or
changing ownership boundaries requires an ADR. If the layout change also
changes protocol authority or public compatibility, it additionally requires
an RFC. Small organizational additions inside an existing area may be reviewed
as ordinary pull requests when they preserve these boundaries.

Generated files must live next to a documented generator policy or in ignored
build/output directories. Secrets, local credentials, captured private traffic,
and generated audio never belong in the repository.

