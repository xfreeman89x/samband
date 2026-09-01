# Samband Governance

## Purpose

Samband is an open protocol project. Governance exists to protect protocol
interoperability, security, contributor access, and transparent decision making.
Reference applications implement the protocol; they do not define it.

## Roles

### Maintainers

Maintainers merge changes, steward releases, administer project spaces, and
ensure required reviews occur. Maintainers may delegate domain review but may
not bypass an RFC or security gate for convenience.

### Domain reviewers

Domain reviewers provide accountable review for protocol wire format, routing,
security, platform behavior, simulation, audio, and interoperability. The
current agent-role mapping is documented in
[`docs/agents/PROMPTS.md`](docs/agents/PROMPTS.md).

### Contributors

Anyone may propose issues, RFCs, ADRs, experiments, documentation, tests, or
implementation changes under the contribution rules.

## Decision hierarchy

When records conflict, authority descends in this order:

1. the Apache-2.0 license and applicable law;
2. accepted Samband protocol specification and accepted RFCs;
3. accepted ADRs for implementation architecture;
4. repository policies and maintainer guidance;
5. implementation behavior.

An implementation discrepancy is a bug or a specification gap; it does not
silently redefine the protocol.

## RFC decisions

Material protocol semantics require an RFC. The lifecycle is Draft,
Discussion, Accepted, Rejected, or Superseded. Acceptance requires:

- a complete problem statement, alternatives, compatibility impact, security
  impact, test strategy, and unresolved-question disposition;
- at least one maintainer approval;
- Agent 1 or equivalent protocol review for wire-visible semantics;
- Agent 4 or equivalent security review for security-sensitive semantics;
- Agent 3 or equivalent routing review for routing-sensitive semantics;
- a documented objection-resolution period while in Discussion;
- links to follow-up specification and test-vector work.

Consensus is preferred. When consensus cannot be reached, maintainers publish a
reasoned decision that records significant objections. A maintainer with a
material conflict of interest should recuse from the final decision where
practical.

Protocol v1 RFCs require stronger evidence: complete vectors, interoperability
results, and closure of release-blocking security findings.

## ADR decisions

ADRs record implementation architecture and may be Proposed, Accepted,
Rejected, Deprecated, or Superseded. An ADR cannot override an accepted RFC.
If an implementation decision would change observable protocol behavior, it
must move to the RFC process.

## Changes after acceptance

Substantive changes to an accepted RFC require a new RFC that supersedes or
amends it. Accepted ADRs are never rewritten to hide history; use a new ADR and
link both records. Editorial corrections may be merged when they do not change
semantics and are clearly identified.

## Releases and compatibility

Pre-v1 releases may change, but changes must be documented and reflected in
test vectors. No compatibility promise exists before v1.0 unless a release
explicitly defines a narrower supported contract. The v1.0 gate is specified in
[`ROADMAP.md`](ROADMAP.md).

## Community standards

The project follows the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Security
reports follow [`SECURITY.md`](SECURITY.md). Governance changes use a pull
request and, when they alter decision rights or protocol authority, an ADR.

