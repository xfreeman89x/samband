# Protocol Development Workflow

## Goal

Every observable Samband behavior should be traceable from an explicit question
through evidence and review to specification text, canonical vectors, and
implementations. No reference application may silently become the specification.

## Workflow

```text
question or interoperability gap
             |
             v
issue, research note, or experiment plan
             |
             v
          Draft RFC
             |
             v
Discussion + required domain reviews
             |
             v
evidence, threat analysis, and vector design
             |
             v
Accepted RFC (or Rejected/Superseded)
             |
             v
normative protocol specification + canonical vectors
             |
             v
independent implementations + conformance evidence
```

## Step 1 — Classify the change

Use an RFC if a peer, independent implementation, protected channel, route,
wire message, version, or user-observable network behavior could change. Use an
ADR for internal architecture that preserves protocol semantics. Use an
experiment when evidence is insufficient to select an alternative.

When uncertain, start with an issue or Draft RFC; do not encode the assumption
in production code.

## Step 2 — Draft

Copy [`../rfc/RFC-TEMPLATE.md`](../rfc/RFC-TEMPLATE.md), request the next number,
and fill every required section. Drafts must:

- separate inherited project invariants from proposed semantics;
- name alternatives and the evidence needed to compare them;
- identify compatibility, metadata, resource, and failure implications;
- mark wire-format items for Agent 1 review;
- mark security-sensitive items for Agent 4 review;
- mark routing-sensitive items for Agent 3 review;
- state which shared contracts would change.

Draft is non-normative and may change freely through reviewed pull requests.

## Step 3 — Discussion

A maintainer moves a sufficiently complete Draft to Discussion. The discussion
must be public when possible, time-bounded by the maintainer, and open long
enough for required domain reviewers and affected implementers to respond. The
RFC records substantive objections and their disposition rather than erasing
them from history.

Security disclosures that would enable exploitation use the private reporting
process while the public RFC states only safe design context.

## Step 4 — Evidence and vectors

Claims that depend on platform, routing, energy, latency, scale, metadata, or
cryptographic feasibility require an experiment or analysis with reproducible
inputs and measured outcomes. Wire-visible proposals include vector design
before acceptance, not after implementation has ossified behavior.

Required evidence is proportional to risk. A v0 experimental semantic may be
accepted with explicit limitations; a v1 contract requires independent
interoperability evidence and completed security gates.

## Step 5 — Acceptance

An RFC can become Accepted only when:

- the problem, scope, semantics, processing order, failures, resource bounds,
  version impact, privacy impact, and alternatives are resolved for its scope;
- every shared-contract change is identified;
- required Protocol, Security, and Routing reviews are recorded;
- the test-vector and conformance plan is actionable;
- significant objections and maintainer rationale are recorded;
- no listed acceptance blocker remains.

The accepting change records the date and reviewers in the RFC. Acceptance is a
governance act; merging a Draft does not accept it.

## Step 6 — Specification integration

After acceptance, Agent 1 integrates normative semantics into
[`../../protocol/spec/`](../../protocol/spec/README.md) and creates or updates
schemas and canonical vectors. The RFC preserves rationale; the specification
becomes the cohesive implementation contract.

If integration reveals ambiguity, pause implementation and reopen design work.
Do not let one implementation choose the answer silently.

## Step 7 — Implementation and conformance

Implementations consume the specification and the same canonical vectors.
Decoder and state-machine work includes malformed-input, unknown-version,
duplicate, replay, and resource-bound tests. A discrepancy is classified as an
implementation bug, vector error, or specification ambiguity and resolved at
the authoritative layer.

## Amendments and supersession

Accepted RFC semantics are changed by a new RFC that explicitly amends or
supersedes the old record. Editorial fixes that do not alter behavior may be
merged with maintainer review. Released vectors are immutable; corrections use
new identifiers and record the affected releases.

## ADR workflow

ADRs follow a parallel but implementation-only path: Proposed, review,
Accepted/Rejected, then Superseded or Deprecated when needed. An ADR cannot
bypass an RFC. Experiments can be prerequisites to ADR acceptance.

